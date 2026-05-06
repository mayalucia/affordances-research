# affordances-research

A research portal — closed-form information-theoretic accounts of
affordance theory, with live executable JAX panels.

**Live**: https://mayalucia.github.io/affordances-research/

## What this is

The publishable surface of the WP-0128 affordance research artefact
from the [MayaLucIA](https://mayalucia.dev) project. A demonstration
of computational-neuroscience research competence — closed-form
derivations, runnable code, methodological reflection, and a
discipline that ships with the work.

## Status

Portal v1.0 in development for a Mioara Vasile touchpoint on
2026-05-15.

## Develop

```bash
git clone https://github.com/mayalucia/affordances-research.git
cd affordances-research
hugo server
# open http://localhost:1313/
```

Hugo extended ≥ 0.150 required. Tested on macOS + Linux.

## Run a code panel natively

```bash
cd static/figures/panel-0
uv run python panel-0.py
```

`uv` from https://github.com/astral-sh/uv. PEP 723 inline metadata
declares the panel's dependencies; no separate `requirements.txt`.

## Structure

```
content/
├── _index.md         landing page
├── theory/           closed-form derivations
├── code/             executable panels
├── method/           discipline that ships with the work
├── reading/          annotated bibliography
└── about/            provenance + reproducibility
static/
├── pyodide/          Pyodide runtime + pinned JAX wheel
└── figures/          tangled panel sources + rendered figures
layouts/
├── shortcodes/       Hugo shortcodes (code-execute, etc.)
└── _default/         theme overrides
```

## Deploy

GitHub Actions builds and deploys on push to `main`. See
`.github/workflows/deploy.yml`.

## License

Text and figures: CC BY 4.0. Code: MIT. See `LICENSE.md`.

## Origin

Commissioned under WP-0128 (sabhā 2026-05-01) and given portal
disposition under WP-0128-portal-disposition-amendment 2026-05-06.
Both work-packs live in the [mayalucia parent project](https://github.com/mayalucia/mayalucia).
