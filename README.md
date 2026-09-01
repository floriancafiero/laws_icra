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

## Primary robotics scenario

The paper now uses **variable-autonomy multi-robot firefighting/search-and-rescue** as its neutral engineering scenario. This closely matches recent meaningful-human-control and multi-robot alert studies, while keeping large-fleet analyses explicitly labeled as scaling stress tests.

See `SCENARIO.md`.

## Repository layout

- `MODEL.md` — formal model and current propositions.
- `SCENARIO.md` — primary robotics scenario.
- `CERTIFICATION.md` — proposed measurable performance-based EHC certificate.
- `EXPERIMENT.md` — human-subject validation design.
- `PAPER_PLAN.md` — ICRA narrative and figure plan.
- `notes/literature_gap.md` — novelty boundaries.
- `notes/empirical_calibration.md` — empirical anchors and non-identifiable parameters.
- `notes/dimensionless_formulation.md` — scale-free workload/deadline formulation.
- `src/simulations.py` — baseline analytical/Monte Carlo results.
- `src/calibrated_scenarios.py` — empirical-envelope robustness.
- `src/firefighting_scenario.py` — general-service scaling stress test.
- `src/certification.py` — exact binomial lower-bound/sample-size utilities.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/simulations.py
python src/calibrated_scenarios.py
python src/firefighting_scenario.py
python src/certification.py
```

The original baseline uses **synthetic** parameters to test qualitative/theoretical behavior. Empirical anchors, cross-domain robustness anchors, and scenario parameters are labeled separately; none are presented as estimates of an autonomous-weapons deployment.

## Current empirical status

Recent HRI evidence is concentrated at small team sizes, and the model recovers the classic fan-out boundary as a special case. The large-fleet analyses ask a scaling question: what warning quality and human capacity would be required to preserve EHC as autonomous systems become more numerous?

The main presentation should now use dimensionless offered load

\[
A=\Lambda E[S][\pi r+(1-\pi)f]
\]

and normalized deadline

\[
d=D/E[S],
\]

with non-exponential service-time and burst robustness in simulation.

## Immediate research priority

The highest-value remaining empirical step is the human-subject experiment in `EXPERIMENT.md`: manipulate false-positive burden and temporal burstiness while holding true critical events approximately fixed, then test whether end-to-end EHC falls as predicted.
