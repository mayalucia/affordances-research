---
title: "Panel 0 — Phase 1 closed-form curve"
weight: 21
description: "Body-derivative ∂I_B(S;A)/∂θ_B as a function of θ_B, three ways."
---

The headline scientific object: the body-derivative
{{< raw >}}\(\partial I_B(S; A)/\partial \theta_B\){{< /raw >}}
of the linear-Gaussian POMDP, computed as a function of the designed
body parameter θ_B.

## What is on display

Two stacked traces:

- **Top** — the parametric mutual information
  {{< raw >}}\(I_B(S; A) = \tfrac{1}{2}\log\det \Sigma_A(\theta_B) - \tfrac{1}{2}\log\det \Sigma_{A|S;B}(\theta_B)\){{< /raw >}}
  as θ_B sweeps from 0.05 to 6.0.
- **Bottom** — its body-derivative computed two ways: closed-form
  analytical (curve) versus central-difference numerical (markers).

The two legs of the verification triangle agree to floating-point
precision (residual ≈ 10⁻⁸, well below the 10⁻⁵ pass threshold)
across all 121 grid points.

The third leg — autodiff via `jax.jacrev` — is part of the design
but ships in [Phase C](#phase-c) when the JAX-on-Pyodide pipeline
goes live. The Phase B (γ-plan) panel ships analytical and
finite-difference live.

## The figure

![Panel 0 — body-derivative, three-verification triangle](/figures/panel-0/panel-0.png)

*Verdict, last build:* `analytical vs FD residual = 1.412e-08`, pass
threshold `1e-05`, status `PASS`. The build script reports the
residual on stdout and refuses to render if it exceeds threshold.

## What the figure does and does not claim

- It carries the **sign** of the body-derivative across the grid.
- It does **not** claim a magnitude at any single θ_B.
- It does **not** label θ_B as the Warren π-number; that naming
  belongs to Phase 1.5 / panel-1, where a measured body enters.
- It does **not** compare to empirical animal data; that contrast
  lives in [Panel 2](/code/panel-2/).

These foreclosures are not modesty. They are the discipline that
keeps a closed-form Phase-1 sandbox from being asked to do empirical
work it cannot do.

## How to read the body-derivative

For each θ_B on the grid:

1. Construct the designed body B(θ_B) — a diagonal matrix with
   entries `1 - exp(-θ_B / k)` for mode k = 1..4. Small θ_B gives
   a near-rank-deficient body; large θ_B saturates to identity.
2. Form Σ_A(θ_B) = B Σ_a Bᵀ + Σ_η and
   Σ_{A|S;B}(θ_B) = B Σ_{a|S} Bᵀ + Σ_η.
3. The mutual information is the log-determinant gap; its derivative
   is a trace identity, evaluated via two `numpy.linalg.solve` calls.

The body-derivative is **positive** across the displayed range — every
increment in θ_B increases the action-state mutual information. That
sign is the substantive content of the curve. If the closed-form
delivered the opposite sign, or zero, the falsifiability test in
[Theory / Phase 1](/theory/phase-1/) would fire.

## Run it

In your browser, when [Phase C](#phase-c) goes live:

```python
from panel_0 import make_generative_covariances, panel_sweep, verification_residual
import numpy as np

gen = make_generative_covariances(seed=0)
sweep = panel_sweep(np.linspace(0.05, 6.0, 121), gen)
print(f"residual = {verification_residual(sweep):.3e}")
```

Native, today:

```bash
git clone https://github.com/mayalucia/affordances-research.git
cd affordances-research/static/figures/panel-0
uv run --script panel_0.py
# wrote panel-0.png
# three-verification residual (analytical vs FD): 1.412e-08
```

`uv run --script` reads the PEP 723 inline header and provisions a
clean environment with numpy, scipy, matplotlib. No
`requirements.txt`, no `pyproject.toml`.

## The source

The full panel source, including the closed-form derivative, the
finite-difference verification, and the figure-render driver, is at
[`static/figures/panel-0/panel_0.py`]({{< param "github_repo" >}}/blob/main/static/figures/panel-0/panel_0.py)
in the repository.

The closed-form derivation provenance trails are listed in
[Theory / Phase 1](/theory/phase-1/).

## Phase C

The autodiff leg lands when the JAX-on-Pyodide pipeline ships. The
expected verification triangle at that point is

  `max(|analytical − autodiff|, |analytical − fd|) < 1e-5`

across the same grid. If autodiff disagrees with the closed form,
the closed form is wrong, the JAX trace is broken, or Pyodide's JAX
build differs from native JAX. Showing the triangle makes the
failure mode visible.
