---
title: "About"
weight: 50
description: "Provenance, reproducibility, contributors."
---

## What this artefact is

A research portal developed by the [MayaLucIA](https://mayalucia.dev)
project as a public demonstration of computational-neuroscience
research. It is independent research, pursued because the work
deserves to exist on its own terms.

## Provenance

The substrate was developed across early 2026 in the
brain-circuit-reconstruction line of MayaLucIA, through a
collaborative review process that produced an audit pass and a
four-deliverable pack from which this portal is built.

The portal disposition was decided 2026-05-06. What you read here
is a curated public surface; the underlying substrate sources are
maintained privately and linked from each section where reproducible.

## Reproducibility

Every claim in [Theory](/theory/) anchors to a substrate seam (file
+ line range) in the source repository. Every code panel in
[Code](/code/) is tangled from `org-babel` source and runs both
in-browser (Pyodide) and locally (`uv run`). External citations in
[Reading](/reading/) are checked against published text, not memory.

To reproduce locally:

```bash
git clone https://github.com/mayalucia/affordances-research.git
cd affordances-research
hugo server
# open http://localhost:1313/
```

To run a single panel natively:

```bash
cd static/figures/panel-0
uv run python panel-0.py
```

## Contributors

The work is built collaboratively. Where an idea is load-bearing
and traceable to a single contribution, that contribution is named
in the relevant section. The collaborative review process that
shaped this work is walked through in
[Method → Coalition](/method/coalition/).

## License

The text and figures of this portal are licensed CC BY 4.0. The
code panels are MIT-licensed. See `LICENSE.md` in the source
repository.

## How to cite

If you find this work useful, you may cite it as:

> *Affordances, Bodies, and Information.* MayaLucIA project, 2026.
> https://mayalucia.github.io/affordances-research/

A preprint version is planned for arXiv following the 2026-05-15
external-review touchpoint.

## Contact

Source, issues, and discussion:
[github.com/mayalucia/affordances-research]({{< param "github_repo" >}})
