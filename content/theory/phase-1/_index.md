---
title: "Phase 1 — Linear-Gaussian POMDP, Schur, log-det"
weight: 11
description: "Closed-form derivative of mutual information with respect to a designed body parameter."
---

The Phase 1 sandbox is fully closed-form. Body B is *designed*, not
measured, not estimated. The headline scientific object is the
parametric family {I_B(S;A)}_B and its derivative ∂I_B/∂θ_B at any
θ_B in the family.

## Setup

A latent state S and a latent action a, both Gaussian, with the
state generating the action via a fixed linear map. The body acts on
the latent action to produce an observable action A.

{{< raw >}}
\[
S \sim \mathcal{N}(\mu_S, \Sigma_S),
\qquad
a \mid S \sim \mathcal{N}(M_{aS} S, \Sigma_{a \mid S}),
\qquad
A = B(\theta_B)\,a + \eta,
\quad \eta \sim \mathcal{N}(0, \Sigma_\eta)
\]
{{< /raw >}}

with η independent of (S, a). All five matrices Σ_S, M_aS, Σ_{a|S},
Σ_η, B(θ_B) are *designed*; θ_B is the one designer parameter we
will sweep.

The two relevant covariances are

{{< raw >}}
\[
\Sigma_A(\theta_B) = B(\theta_B)\,\Sigma_a\,B(\theta_B)^\top + \Sigma_\eta,
\qquad
\Sigma_{A \mid S; B}(\theta_B) = B(\theta_B)\,\Sigma_{a \mid S}\,B(\theta_B)^\top + \Sigma_\eta,
\]
{{< /raw >}}

where Σ_a = M_aS Σ_S M_aSᵀ + Σ_{a|S}.

## The mutual information

Two Gaussians; the conditional-entropy gap closes in log-det form:

{{< raw >}}
\[
I_B(S; A)
= \tfrac{1}{2}\log\det \Sigma_A(\theta_B)
- \tfrac{1}{2}\log\det \Sigma_{A \mid S; B}(\theta_B)
\]
{{< /raw >}}

This is a function of θ_B. Both determinants depend on θ_B only
through B(θ_B); everything else is held fixed across the parametric
sweep.

## The body-derivative

Apply the matrix log-det identity
{{< raw >}}\(\partial_\theta \log \det M = \mathrm{tr}(M^{-1}\,\partial_\theta M)\){{< /raw >}}
to each term:

{{< raw >}}
\[
\frac{\partial I_B(S; A)}{\partial \theta_B}
= \tfrac{1}{2}\,\mathrm{tr}\!\left[\Sigma_A^{-1}(\theta_B)\,\partial_{\theta_B}\Sigma_A(\theta_B)\right]
- \tfrac{1}{2}\,\mathrm{tr}\!\left[\Sigma_{A \mid S; B}^{-1}(\theta_B)\,\partial_{\theta_B}\Sigma_{A \mid S; B}(\theta_B)\right].
\]
{{< /raw >}}

The covariance derivatives unwind by the product rule:

{{< raw >}}
\[
\partial_{\theta_B}\Sigma_A
= (\partial_{\theta_B} B)\,\Sigma_a\,B^\top + B\,\Sigma_a\,(\partial_{\theta_B} B)^\top,
\]
{{< /raw >}}

and analogously for Σ_{A|S;B} with Σ_a → Σ_{a|S}. ∂B/∂θ_B is the
closed-form Jacobian of the body-map, given B(θ_B) as an analytical
formula.

The whole expression is **closed-form**: three layers of
matrix-valued composition, every one of them differentiable in
elementary calculus, no numerical optimisation anywhere.

## What this licenses and what it does not

It licenses:

- A **sign** for ∂I_B/∂θ_B at any θ_B in the parametric family.
- A **falsifiability sandbox**: pick a designed body family, plot
  the curve, check that closed-form, autodiff, and finite-difference
  agree.

It does **not** license:

- Magnitude claims about I_B(S; A) at any specific θ_B value.
- Interpretation of θ_B as a Warren π-number or any other measured
  quantity. That naming belongs to **Phase 1.5**.
- Any comparison to empirical animal data. That contrast belongs to
  **Phase 2** and to **Panel 2** (Position-C contrast).

The Phase 1 sandbox is *theorist-internal*. The figure caption may
carry the sign of the partial derivative; it may not carry magnitude.

## The methods §1.5 type-match lemma

The discipline that connects Phase 1 to a framing-paragraph
prediction is the type-match lemma, introduced in
[the Lemma section](/theory/lemma/):

{{< raw >}}
\[
\mathrm{sgn}\!\bigl(c \cdot \text{(animal prediction)}\bigr)
= \mathrm{sgn}\!\left(\frac{\partial I_B(S; A)}{\partial \theta_B}\right) \quad \text{at } \theta_B^\star.
\]
{{< /raw >}}

The lemma is sign-equality only. The framing paragraph is licensed
to predict the sign of an animal effect at θ_B*; it is not licensed
to predict the magnitude.

This is the fence between framing-register and methods-register
predictions. Phase 1 supplies the right-hand side; Phase 1.5
supplies the coordinate map c and the operating point θ_B*; the
framing paragraph speaks the left-hand side and stays inside the
sign-equality envelope.

## See also

- [Code / Panel 0](/code/panel-0/) — the parametric curve and the
  three-verification triangle (γ leg ships analytical and
  finite-difference; α leg ships autodiff in Phase C).
- [Theory / Lemma](/theory/lemma/) — the methods §1.5 type-match
  lemma in canonical sentence form (named-pending: coordinate fill).
