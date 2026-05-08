# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy>=1.26",
#   "scipy>=1.12",
#   "matplotlib>=3.8",
#   "autograd>=1.6",
# ]
# ///
"""
Panel 0 — Phase 1 closed-form parametric curve.

Linear-Gaussian POMDP with a designed body B(theta_B) entering as a
static action-repertoire matrix. Panel 0 displays:

  I_B(S; A) = 1/2 logdet Sigma_A(theta_B) - 1/2 logdet Sigma_{A|S;B}(theta_B)

as a function of theta_B, alongside its body-derivative

  dI/d(theta_B) = 1/2 tr[Sigma_A^-1 . dSigma_A]
                - 1/2 tr[Sigma_{A|S;B}^-1 . dSigma_{A|S;B}]

computed three independent ways and verified to agree:

  1. analytical    — closed-form trace identity, scipy.linalg.solve
  2. finite-diff   — central difference of I_B(S;A)
  3. autodiff      — autograd reverse-mode on mutual_information

Phase C substitution: the original alpha-plan named jax.jacrev for the
autodiff leg, but JAX-on-Pyodide does not exist as of 2026-05
(pyodide#2198 dormant since June 2022). autograd-HIPS is the
NumPy-compatible reverse-mode ancestor of JAX, pure-Python, and
installable in Pyodide via micropip. The verification triangle
remains intact; only the autodiff library changes.

Formula provenance: carya R2.6 ask (i), substrate-canonical at
collab/sessions/wp-0128-affordance-sabha/carya.org L1209+.

Discipline foreclosures (per r3-synthesis Section 6.1):
  - body parameter is named theta_B; Warren pi-number naming
    deferred to Phase 1.5 (panel-1).
  - figure caption carries SIGN of the derivative; no magnitude
    claims at any single theta_B.
"""

import numpy as np
import autograd.numpy as anp
from autograd import grad
from numpy.typing import NDArray
from numpy.linalg import slogdet
from scipy.linalg import solve


# -------------------------------------------------------------------
# Designed body family B(theta_B)
# -------------------------------------------------------------------

def body_matrix(theta_B: float, dim_a: int = 4, dim_obs: int = 4) -> NDArray:
    """A one-parameter family of action-repertoire matrices.

    The family is constructed so that:
      * theta_B = 0 collapses B to a rank-1 channel (the body can
        only express one action mode);
      * theta_B large saturates B to identity-scaled (the body
        spans the action space);
      * dB/d(theta_B) is a closed-form matrix, returned by
        body_jacobian below.

    Construction: B = U(theta_B) D(theta_B) V^T with V the latent
    basis (taken as identity here for simplicity), D diagonal with
    entries d_k(theta_B) = 1 - exp(-theta_B / k), so the kth mode
    saturates at scale k. This gives a smooth, monotone, rank-
    increasing family, with closed-form derivative.
    """
    if dim_obs != dim_a:
        raise ValueError("panel-0 ships square B; rectangular case is Phase 2.")
    k = np.arange(1, dim_a + 1, dtype=float)  # mode index 1..dim_a
    d = 1.0 - np.exp(-theta_B / k)
    return np.diag(d)


def body_jacobian(theta_B: float, dim_a: int = 4) -> NDArray:
    """dB/d(theta_B), returned as a matrix of the same shape as B.

    With B = diag(1 - exp(-theta_B / k)),
    dB/d(theta_B) = diag( (1/k) exp(-theta_B / k) ).
    """
    k = np.arange(1, dim_a + 1, dtype=float)
    dd = (1.0 / k) * np.exp(-theta_B / k)
    return np.diag(dd)


# -------------------------------------------------------------------
# Generative-model covariances (designed, fixed across theta_B sweep)
# -------------------------------------------------------------------

def make_generative_covariances(
    dim_S: int = 4,
    dim_a: int = 4,
    seed: int = 0,
) -> dict[str, NDArray]:
    """Designed Sigma_S, Sigma_a, Sigma_{a|S}, Sigma_eta.

    The latent state S generates the latent action a via
        a = M_aS S + xi,    xi ~ N(0, Sigma_xi),
    so Sigma_a = M_aS Sigma_S M_aS^T + Sigma_xi and
    Sigma_{a|S} = Sigma_xi.

    Observation A = B a + eta, eta ~ N(0, Sigma_eta), independent.

    All four matrices are designed (positive-definite by
    construction); no fitting, no estimation.
    """
    rng = np.random.default_rng(seed)

    def random_psd(dim: int, scale: float) -> NDArray:
        L = rng.standard_normal((dim, dim))
        return scale * (L @ L.T) + np.eye(dim) * 1e-2

    Sigma_S = random_psd(dim_S, scale=1.0)
    M_aS = rng.standard_normal((dim_a, dim_S)) * 0.5
    Sigma_xi = random_psd(dim_a, scale=0.3)  # this is Sigma_{a|S}
    Sigma_a = M_aS @ Sigma_S @ M_aS.T + Sigma_xi
    Sigma_eta = random_psd(dim_a, scale=0.05)

    return {
        "Sigma_S": Sigma_S,
        "Sigma_a": Sigma_a,
        "Sigma_a_given_S": Sigma_xi,
        "Sigma_eta": Sigma_eta,
        "M_aS": M_aS,
    }


# -------------------------------------------------------------------
# Closed-form I_B(S; A) and dI/d(theta_B)
# -------------------------------------------------------------------

def Sigma_A(theta_B: float, gen: dict[str, NDArray]) -> NDArray:
    """Marginal action covariance Sigma_A(theta_B) = B Sigma_a B^T + Sigma_eta."""
    B = body_matrix(theta_B, dim_a=gen["Sigma_a"].shape[0])
    return B @ gen["Sigma_a"] @ B.T + gen["Sigma_eta"]


def Sigma_A_given_S(theta_B: float, gen: dict[str, NDArray]) -> NDArray:
    """Conditional action covariance Sigma_{A|S;B} = B Sigma_{a|S} B^T + Sigma_eta."""
    B = body_matrix(theta_B, dim_a=gen["Sigma_a_given_S"].shape[0])
    return B @ gen["Sigma_a_given_S"] @ B.T + gen["Sigma_eta"]


def mutual_information(theta_B: float, gen: dict[str, NDArray]) -> float:
    """I_B(S; A) at theta_B in closed form (logdet form)."""
    SA = Sigma_A(theta_B, gen)
    SAS = Sigma_A_given_S(theta_B, gen)
    sgn_a, ldet_a = slogdet(SA)
    sgn_b, ldet_b = slogdet(SAS)
    if sgn_a <= 0 or sgn_b <= 0:
        # Should not occur for designed PSD covariances; named-pending
        # if it does (saturation boundary discipline; r3 §6.1).
        raise FloatingPointError(
            f"non-positive logdet at theta_B={theta_B}; outside Phase-1 "
            f"sandbox. r3 §6.1 saturation-boundary discipline applies."
        )
    return 0.5 * (ldet_a - ldet_b)


def dSigma_A_dtheta(theta_B: float, gen: dict[str, NDArray]) -> NDArray:
    """d Sigma_A / d theta_B = (dB) Sigma_a B^T + B Sigma_a (dB)^T."""
    B = body_matrix(theta_B, dim_a=gen["Sigma_a"].shape[0])
    dB = body_jacobian(theta_B, dim_a=gen["Sigma_a"].shape[0])
    return dB @ gen["Sigma_a"] @ B.T + B @ gen["Sigma_a"] @ dB.T


def dSigma_A_given_S_dtheta(theta_B: float, gen: dict[str, NDArray]) -> NDArray:
    """d Sigma_{A|S;B} / d theta_B = (dB) Sigma_{a|S} B^T + B Sigma_{a|S} (dB)^T."""
    B = body_matrix(theta_B, dim_a=gen["Sigma_a_given_S"].shape[0])
    dB = body_jacobian(theta_B, dim_a=gen["Sigma_a_given_S"].shape[0])
    return dB @ gen["Sigma_a_given_S"] @ B.T + B @ gen["Sigma_a_given_S"] @ dB.T


def body_derivative_analytical(theta_B: float, gen: dict[str, NDArray]) -> float:
    """Closed-form ∂I_B(S;A)/∂theta_B via the log-det-trace identity.

    dlogdet(M)/d(theta) = tr(M^-1 dM/d(theta)).
    Computed as tr(solve(M, dM)) to avoid an explicit inverse.
    """
    SA = Sigma_A(theta_B, gen)
    dSA = dSigma_A_dtheta(theta_B, gen)
    SAS = Sigma_A_given_S(theta_B, gen)
    dSAS = dSigma_A_given_S_dtheta(theta_B, gen)
    term_marginal = np.trace(solve(SA, dSA, assume_a="pos"))
    term_conditional = np.trace(solve(SAS, dSAS, assume_a="pos"))
    return 0.5 * (term_marginal - term_conditional)


def body_derivative_finite_difference(
    theta_B: float,
    gen: dict[str, NDArray],
    eps: float | None = None,
) -> float:
    """Central-difference verification of dI/d(theta_B).

    eps follows the rule of thumb eps = 1e-5 * max(|theta_B|, 1)
    per carya R2.6 ask (ii) (substrate-canonical carya.org L1271+).
    """
    if eps is None:
        eps = 1e-5 * max(abs(theta_B), 1.0)
    return (
        mutual_information(theta_B + eps, gen)
        - mutual_information(theta_B - eps, gen)
    ) / (2.0 * eps)


# -------------------------------------------------------------------
# Autodiff leg — autograd-HIPS reverse-mode (Phase C alpha-plan)
# -------------------------------------------------------------------
#
# These functions parallel the numpy-only routines above but route
# all array ops through autograd.numpy (anp) so reverse-mode tracing
# can build the gradient graph through I_B(S;A) as a function of the
# scalar theta_B. The analytical and FD legs above remain pure
# numpy+scipy, so the three legs are independent verifications.

def _body_matrix_anp(theta_B, dim_a: int = 4):
    """autograd-traced version of body_matrix."""
    k = anp.arange(1, dim_a + 1, dtype=float)
    d = 1.0 - anp.exp(-theta_B / k)
    return anp.diag(d)


def _mutual_information_anp(theta_B, gen: dict[str, NDArray]) -> float:
    """autograd-traced I_B(S;A) at scalar theta_B.

    The generative covariances Sigma_a, Sigma_{a|S}, Sigma_eta are
    designed (theta_B-independent) and pulled in as constants; only
    B(theta_B) is traced.
    """
    dim_a = gen["Sigma_a"].shape[0]
    B = _body_matrix_anp(theta_B, dim_a=dim_a)
    SA = B @ gen["Sigma_a"] @ B.T + gen["Sigma_eta"]
    SAS = B @ gen["Sigma_a_given_S"] @ B.T + gen["Sigma_eta"]
    # autograd defines slogdet on PSD inputs; use it for parity with
    # the closed-form route. Sign is +1 here (designed PSD).
    _, ldet_a = anp.linalg.slogdet(SA)
    _, ldet_b = anp.linalg.slogdet(SAS)
    return 0.5 * (ldet_a - ldet_b)


def body_derivative_autodiff(theta_B: float, gen: dict[str, NDArray]) -> float:
    """Reverse-mode autodiff verification of dI/d(theta_B).

    Implementation: autograd.grad on _mutual_information_anp w.r.t.
    its first (scalar) argument. autograd-HIPS is the pure-Python
    NumPy-compatible reverse-mode ancestor of JAX; substituted for
    jax.jacrev because JAX-on-Pyodide does not exist as of 2026-05
    (pyodide#2198 dormant since June 2022). The verification
    triangle is intact; only the autodiff library has changed.
    """
    g = grad(_mutual_information_anp, argnum=0)
    return float(g(float(theta_B), gen))


# -------------------------------------------------------------------
# Fibred sweep: the panel curve
# -------------------------------------------------------------------

def panel_sweep(
    theta_grid: NDArray,
    gen: dict[str, NDArray],
    include_autodiff: bool = True,
) -> dict[str, NDArray]:
    """Compute (I, dI/dtheta x {analytical, finite-difference, autodiff})
    over a grid of theta_B values.

    Returns four arrays of length len(theta_grid) when include_autodiff
    is True, three otherwise. Pass criterion (carya R2.6 ask (ii)):
    max(|ana - fd|, |ana - autodiff|) < tau, tau = 1e-6 in
    single-precision-defensive units; relaxed to 1e-5 in in-browser
    float64 builds.
    """
    n = theta_grid.shape[0]
    I_vals = np.empty(n)
    dI_ana = np.empty(n)
    dI_fd = np.empty(n)
    dI_ad = np.empty(n) if include_autodiff else None
    for k, t in enumerate(theta_grid):
        I_vals[k] = mutual_information(float(t), gen)
        dI_ana[k] = body_derivative_analytical(float(t), gen)
        dI_fd[k] = body_derivative_finite_difference(float(t), gen)
        if include_autodiff:
            dI_ad[k] = body_derivative_autodiff(float(t), gen)
    out = {
        "theta": theta_grid,
        "I": I_vals,
        "dI_analytical": dI_ana,
        "dI_finite_difference": dI_fd,
    }
    if include_autodiff:
        out["dI_autodiff"] = dI_ad
    return out


def verification_residual(sweep: dict[str, NDArray]) -> dict[str, float]:
    """Pairwise max-residuals across the grid.

    Returns a dict with keys 'ana_vs_fd', 'ana_vs_autodiff' (if
    autodiff present), and 'max' (the worst pairwise residual). The
    'max' value is the headline three-verification figure.
    """
    res = {
        "ana_vs_fd": float(np.max(np.abs(
            sweep["dI_analytical"] - sweep["dI_finite_difference"]
        ))),
    }
    if "dI_autodiff" in sweep:
        res["ana_vs_autodiff"] = float(np.max(np.abs(
            sweep["dI_analytical"] - sweep["dI_autodiff"]
        )))
    res["max"] = max(res.values())
    return res


# -------------------------------------------------------------------
# CLI entry point — local reproduction
# -------------------------------------------------------------------

def main() -> None:
    """Native run via `uv run --script panel_0.py`. Renders panel-0.png."""
    import matplotlib
    matplotlib.use("Agg")  # headless; works in browser-tangled run too.
    import matplotlib.pyplot as plt

    gen = make_generative_covariances(dim_S=4, dim_a=4, seed=0)
    theta_grid = np.linspace(0.05, 6.0, 121)
    sweep = panel_sweep(theta_grid, gen, include_autodiff=True)

    res = verification_residual(sweep)
    pass_threshold = 1e-5
    verdict = "PASS" if res["max"] < pass_threshold else "FAIL"
    print(f"three-verification residuals across {theta_grid.size} grid points:")
    print(f"  analytical vs finite-difference : {res['ana_vs_fd']:.3e}")
    print(f"  analytical vs autodiff (autograd): {res['ana_vs_autodiff']:.3e}")
    print(f"  max pairwise                    : {res['max']:.3e}")
    print(f"pass threshold: {pass_threshold:.0e}    verdict: {verdict}")

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(7.0, 5.6), sharex=True)

    ax_top.plot(sweep["theta"], sweep["I"], color="#1f4068", lw=1.6)
    ax_top.set_ylabel(r"$I_B(S; A)$ (nats)")
    ax_top.grid(True, alpha=0.3)
    ax_top.set_title("Phase 1 closed-form parametric curve")

    ax_bot.plot(
        sweep["theta"], sweep["dI_analytical"],
        color="#1f4068", lw=1.6, label="analytical (closed form)",
    )
    ax_bot.plot(
        sweep["theta"], sweep["dI_finite_difference"],
        color="#c44536", lw=0, marker="x", ms=3.5, mew=0.8,
        label="finite-difference",
    )
    ax_bot.plot(
        sweep["theta"], sweep["dI_autodiff"],
        color="#2a9d8f", lw=0, marker="o", ms=3.0,
        markerfacecolor="none", markeredgecolor="#2a9d8f",
        label="autodiff (autograd-HIPS)",
    )
    ax_bot.axhline(0.0, color="#888", lw=0.6)
    ax_bot.set_xlabel(r"$\theta_B$ (designed body parameter)")
    ax_bot.set_ylabel(r"$\partial I_B(S; A) / \partial \theta_B$")
    ax_bot.grid(True, alpha=0.3)
    ax_bot.legend(loc="upper right", framealpha=0.9)

    fig.suptitle(
        "Panel 0 — body-derivative, three-verification triangle",
        y=0.99,
    )
    fig.tight_layout()
    fig.savefig("panel-0.png", dpi=150, bbox_inches="tight")
    print("wrote panel-0.png")


if __name__ == "__main__":
    main()
