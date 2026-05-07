---
title: "Code"
weight: 20
description: "Live, executable JAX panels. Three-verification triangle, in your browser."
---

The closed-form results in [Theory](/theory/) come with executable
panels that you can run from this page.

## Execution register

Code runs **in your browser** via Pyodide — a port of CPython
compiled to WebAssembly. JAX is preloaded as a pinned wheel; numpy
and scipy come in the base distribution.

**First load is slow** — about ten to thirty seconds on broadband.
The Pyodide runtime (~10 MB) and the JAX wheel (~50 MB) load once
per browser session, then cache. After that, code blocks execute
locally; nothing is sent to a server.

If you would rather run the code natively, every panel is also
tangled to a `.py` file in the [GitHub repository]({{< param "github_repo" >}}).
Reproducing locally:

```bash
git clone https://github.com/mayalucia/affordances-research.git
cd affordances-research/static/figures/panel-0
uv run python panel-0.py
```

## Three-verification triangle

Each panel computes its result three ways:

1. **Analytical** — closed-form expression, evaluated directly
2. **Autodiff** — `jax.jacrev` on the closed form
3. **Finite-difference** — numerical gradient, stencil width small

The discipline is to show all three agreeing. Disagreement is a bug;
either the closed form is wrong, the autodiff trace is broken, or
the finite-difference stencil is poorly chosen. Showing the triangle
makes the failure mode visible.

## Panels

- **panel-0** — Phase 1 closed-form curve. The body-derivative as a
  function of body parameter, three ways. *Live.*
- **panel-1** — Phase 1.5 Warren-grounded. Gates on primate hand
  data ingestion. *Post-May-15.*
- **panel-2** — Position-C contrast. Sign-change vs invariance under
  property-environment swap. *Live.*

## Honesty about what runs where

If the JAX-on-Pyodide load fails on your browser (rare, but it
happens — adblockers, restricted networks, very old browsers), the
panels degrade to numpy + scipy only. The autodiff leg becomes
"shown-but-not-run-here"; the analytical and finite-difference legs
still run live. The local reproduction (`uv run`) gives you the JAX
leg without any browser.

This is part of the discipline: name where execution lives, name the
fallback, do not pretend the in-browser path is universal.
