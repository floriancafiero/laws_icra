# ICRA 2027 manuscript

## Official constraints checked 2 September 2026

The current ICRA 2027 call requires:

- at most **8 pages for the complete paper**, including figures, tables, acknowledgments, bibliography and references;
- ICRA/IEEE double-column format;
- double-anonymous review;
- no separate supplementary manuscript; an accompanying video is the only separate review attachment described by the call.

Use the current template linked from the official ICRA 2027 call / PaperPlaza manuscript-preparation page.

The source here is intentionally anonymized.

## Build workflow

1. Copy the current official ICRA LaTeX class/template files into this directory.
2. Regenerate figures from the repository root with `make figures`.
3. Build `paper/main.tex`.

Generated submission figures are placed in `results/figures/icra/` in both PDF and SVG formats.

## Paper strategy

This is a **formal safety/performance-evaluation paper**, not a human-subject HRI paper.

The manuscript must be self-contained. Do not write “see supplementary proof”: ICRA 2027 does not permit a separate supplementary manuscript.

`SUPPLEMENT_PROOFS.md` is an internal derivation notebook used to compress correct proof sketches into the paper.

## Optional video

The call allows a video up to 180 seconds / 20 MB with the initial submission. Only produce one if the manuscript is already stable and the video can visually explain common-cause burst overload or the feasibility frontier.
