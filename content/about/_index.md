---
title: "About"
weight: 50
description: "Provenance, reproducibility, contributors."
---

## What this artefact is

A research portal developed by the [MayaLucIA](https://mayalucia.dev)
project as a public demonstration of computational-neuroscience
research competence. The work was initiated in May 2026 following a
Schrimpf-lab application, but is independent of any specific job
search; it is research that deserves to exist on its own terms.

## Provenance

The substrate was developed across early 2026 in the
[bravli](https://github.com/mayalucia/bravli) domain, the
brain-circuit-reconstruction line of MayaLucIA. A coalition of
spirits — gaddi, themis, spanda, hodgkin, carya, vannevar, mayadev,
and griot — participated in the affordance-research-artefact sabhā
(WP-0128) that produced the §3 audit prose and the four-deliverable
pack from which this portal is built.

The portal disposition was decided 2026-05-06 (see
[`workpacks/0128-portal-disposition-amendment.org`]({{< param "github_repo" >}}/blob/main/../../workpacks/0128-portal-disposition-amendment.org)
in the parent project). What you read here is a curated public
surface; the substrate seams remain in the parent project and are
linked from each section's source.

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
and traceable to a single contributor, the contribution is named in
the relevant section. The four-spirit audit and frame-correction
propagation that shaped this work is walked through in
[Method → Coalition](/method/coalition/).

## License

The text and figures of this portal are licensed CC BY 4.0. The
code panels are MIT-licensed. See `LICENSE.md` in the source
repository.

## How to cite

If you find this work useful, you may cite it as:

> *Affordances, Bodies, and Information.* MayaLucIA project, 2026.
> https://mayalucia.github.io/affordances-research/

A preprint version is planned for arXiv following Mioara
verification (2026-05-15+).

## Contact

Source, issues, and discussion:
[github.com/mayalucia/affordances-research]({{< param "github_repo" >}})
