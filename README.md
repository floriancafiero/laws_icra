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

The paper uses **variable-autonomy multi-robot firefighting/search-and-rescue** as its neutral engineering scenario. This closely matches recent meaningful-human-control and multi-robot alert studies, while keeping large-fleet analyses explicitly labeled as scaling stress tests.

See `SCENARIO.md`.

## Repository layout

- `MODEL.md` — formal model and current propositions.
- `SCENARIO.md` — primary robotics scenario.
- `CERTIFICATION.md` — proposed measurable performance-based EHC certificate.
- `EXPERIMENT.md` — human-subject validation design.
- `PAPER_PLAN.md` — ICRA narrative and figure plan.
- `pilot/` — runnable local pilot experiment, validation checks, and pilot analysis.
- `notes/literature_gap.md` — novelty boundaries.
- `notes/empirical_calibration.md` — empirical anchors and non-identifiable parameters.
- `notes/dimensionless_formulation.md` — scale-free workload/deadline formulation.
- `src/simulations.py` — baseline analytical/Monte Carlo results.
- `src/calibrated_scenarios.py` — empirical-envelope robustness.
- `src/firefighting_scenario.py` — general-service scaling stress test.
- `src/certification.py` — exact binomial lower-bound/sample-size utilities.

## Reproduce theory/simulation results

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/simulations.py
python src/calibrated_scenarios.py
python src/firefighting_scenario.py
python src/certification.py
```

## Run the human pilot prototype

```bash
python pilot/validate.py
python -m unittest tests/test_pilot_logic.py
python pilot/app.py
```

Then open `http://127.0.0.1:5000`.

The pilot is a counterbalanced 2 × 2 within-subject manipulation of nuisance-alert burden and temporal clustering. It logs correctness, timeliness, response latency, and queue depth while keeping genuine critical-event detector sensitivity fixed at 1 in order to isolate human-capacity effects.

See `pilot/README.md` before using the system with participants.

## Empirical status

The original baseline uses **synthetic** parameters to test qualitative/theoretical behavior. Empirical anchors, cross-domain robustness anchors, and scenario parameters are labeled separately; none are presented as estimates of an autonomous-weapons deployment.

Recent HRI evidence is concentrated at small team sizes, and the model recovers the classic fan-out boundary as a special case. Large-fleet analyses ask a scaling question: what warning quality and human capacity are required to preserve EHC as autonomous systems become more numerous?

The main presentation uses dimensionless offered load

\[
A=\Lambda E[S][\pi r+(1-\pi)f]
\]

and normalized deadline

\[
d=D/E[S],
\]

with non-exponential service-time and burst robustness in simulation.

## Current critical path

The next empirical step is a **small researcher/convenience pilot** using `pilot/app.py`. The purpose is to estimate the actual service-time distribution, check for ceiling/floor effects, verify that the false-positive and burst manipulations change queue pressure as intended, and obtain effect-size estimates for the preregistered main human study.
