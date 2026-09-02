# Effective Human Control under Capacity Constraints

Research repository for an ICRA 2027 submission on **capacity-aware effective human control (EHC)** in supervisory multi-robot systems.

## Core claim

A human intervention channel is not itself a human-control guarantee. The end-to-end quantity is

$$
C=P(\text{successful timely human intervention}\mid Z=1)
=
rhaQ_M(\nu,D),
$$

with

$$
\nu=N\lambda[\pi r+(1-\pi)f].
$$

The submission connects detector quality, base rates, finite human capacity, deadlines, and correlated demand.

## Submission mode

The ICRA paper is now intentionally a **formal safety/performance evaluation paper without a human-subject experiment**.

The four main theoretical contributions are:

1. deadline/service-time feasibility and unique effective-control capacity;
2. the **Oversight Paradox**: more escalation sensitivity can reduce end-to-end control;
3. a rare-event false-positive staffing law;
4. a proof that mean utilization cannot guarantee control under synchronized demand.

Classical fan-out is recovered as a special stability case.

## Main files

- `MODEL.md` — frozen formal model and theorem statements.
- `SUPPLEMENT_PROOFS.md` — full proof notes.
- `ICRA_EVALUATION.md` — exact no-user-study evaluation protocol.
- `PAPER_PLAN.md` — eight-page ICRA narrative and reviewer-defense plan.
- `SCENARIO.md` — neutral firefighting/search-and-rescue interpretation.
- `notes/empirical_calibration.md` — HRI/autonomy empirical anchors.
- `src/icra_evaluation.py` — regenerates all five submission evaluation figures and raw tables.
- `src/simulations.py` — analytical M/M/M utilities and earlier simulation code.
- `RESULTS_PREVIEW.md` — current numerical sanity-check results.
- `pilot/` — optional future human-validation prototype; **not on the ICRA critical path**.

## Run the submission evaluation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make figures
```

Equivalent:

```bash
python src/icra_evaluation.py
```

Outputs are written to:

- `results/figures/icra/`
- `results/tables/icra/`

Run mathematical sanity checks with:

```bash
python -m unittest tests/test_theory.py
```

## Dimensionless evaluation

The main evaluation uses

$$
A=\nu E[S]
$$

as offered human workload and

$$
d=\frac{D}{E[S]}
$$

as normalized deadline.

This avoids pretending that one physical response-time scale is universal. Physical HRI values are used to interpret the axes, not to define the theory.

## Robotics anchor

The neutral scenario is variable-autonomy multi-robot firefighting/search-and-rescue. Current HRI team sizes and timings ground interpretation; large fleets are explicitly labeled **scaling stress tests**.

## Current critical path

1. regenerate and inspect the five ICRA figures;
2. run all required ablations/baseline comparisons;
3. draft the eight-page manuscript around the formal results;
4. run a hostile-review pass;
5. polish supplementary proofs and reproducibility materials.

Human-subject validation is future work, not required for the current submission.
