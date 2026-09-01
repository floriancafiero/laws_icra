# Effective Human Control under Capacity Constraints

Research prototype for a formal and simulation-based study of **effective human control (EHC)** in autonomous multi-agent systems.

## Core question

When does a formal opportunity for human intervention translate into a realistic ability to intervene correctly and in time?

The project models an end-to-end supervisory chain:

`autonomous decision -> escalation detector -> human queue -> human decision -> intervention`

A central quantity is

\[
C = r\,h\,a\,Q_M(\nu,D),
\]

where:

- `r`: true-positive rate / sensitivity of escalation;
- `h`: probability of correct human response after timely review;
- `a`: probability that a correct intervention successfully takes effect;
- `Q_M(ν,D)`: probability an alert is fully processed by a pool of `M` operators before deadline `D`;
- `ν = N λ [π r + (1-π) f]`: total warning rate;
- `N`: number of autonomous systems;
- `λ`: decisions per system per unit time;
- `π`: prevalence of oversight-critical situations;
- `f`: false-positive rate of the warning system.

## Current theoretical claims

1. **Absolute feasibility ceiling.** Staffing cannot compensate for missed detections, insufficient decision time, human error, or ineffective intervention.
2. **Human-control capacity.** For fixed operator capacity and deadlines, each operator pool has a maximum sustainable warning rate compatible with a target EHC.
3. **Oversight paradox.** A more sensitive escalation policy can reduce effective control when the extra warning traffic causes enough congestion.
4. **False-positive scaling law.** In rare-event regimes with fixed nonzero false-positive rate, minimum staffing scales linearly with fleet size.
5. **Average-load insufficiency.** Equal average warning rates can yield radically different EHC when warnings are correlated in bursts.

## Repository layout

- `src/simulations.py` — reproducible baseline queueing calculations and Monte Carlo experiments.
- `MODEL.md` — current formal model and propositions.
- `notes/literature_gap.md` — working literature positioning and novelty boundaries.
- `results/figures/` — six current figures.
- `results/tables/` — simulation results workbook and text summary.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/simulations.py
```

The parameter values currently used are **synthetic**. They test qualitative/theoretical behavior; they are not empirical estimates of any particular military or civilian deployment.

## Next step

Calibrate plausible ranges for alert frequency, event prevalence, detector performance, operator processing time, intervention deadlines, and burstiness from recent HRI / multi-robot / autonomous-system experiments, then rerun robustness analyses across those empirically grounded ranges.
