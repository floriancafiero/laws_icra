# Human-subject pilot prototype

This directory contains a runnable local prototype for the proposed 2 × 2 EHC experiment.

## What the pilot tests

Within-subject factors:

1. **False-positive burden:** low vs high nuisance-alert traffic.
2. **Temporal correlation:** dispersed vs bursty alerts.

The pilot deliberately sets critical-event detector sensitivity to 1.0. Every genuine critical event is escalated. This isolates the human-capacity mechanism: if EHC drops, it cannot be blamed on missed detector triggers.

Default block design:

- 4 blocks, one per condition;
- counterbalanced condition order from pseudonymous participant ID;
- 8-minute blocks;
- 6 genuine critical events per block;
- 6 nuisance alerts in low-FP blocks;
- 18 nuisance alerts in high-FP blocks;
- 90 s critical-event deadline;
- 6 autonomous rescue robots.

Bursty blocks keep the alert count fixed but place nuisance alerts close to genuine critical events. Dispersed blocks spread the same nuisance count across the block and avoid critical-event clusters where possible.

These values are **pilot settings**, not deployment estimates. They are stored in `pilot/config.json`; freeze that file before collecting the main study.

## Run

From the repository root:

```bash
pip install -r requirements.txt
python pilot/validate.py
python -m unittest tests/test_pilot_logic.py
python pilot/app.py
```

Open `http://127.0.0.1:5000`.

Use a pseudonymous participant code such as `P001`.

The **accelerated demo** option shortens blocks to 90 s and deadlines to 20–25 s for interface testing. Do not use demo mode as experimental data.

## Decision rules shown to participants

- **ABORT** — battery below safe-return threshold.
- **REASSIGN** — route blocked or high-confidence victim requires reallocation.
- **HOLD** — thermal, structural, or telemetry threshold crossed.
- **DISMISS** — alert does not cross an intervention threshold.

The visible alert descriptions encode whether a rule is crossed. Ground truth is never sent to the browser.

## Data

The local server writes `pilot/data/<participant>_<session>.csv`.

One row is produced for every alert. The log contains condition, critical-vs-nuisance ground truth, event type, scheduled arrival, deadline, action, correctness, timeliness, response latency, and queue depth at response.

`pilot/data/*.csv` is gitignored.

Summarize pilot logs with:

```bash
python pilot/analyze.py pilot/data/*.csv
```

## Before collecting real participants

1. Obtain the relevant human-subject/ethics approval.
2. Run `pilot/validate.py` and the unit tests.
3. Run several researcher-only demo sessions.
4. Pilot with a small convenience sample to estimate service times, baseline EHC, learning effects, and manipulation strength.
5. Inspect whether high-FP and burst conditions actually alter queue depth without producing ceiling/floor effects.
6. Freeze the mission generator and preregister the primary analysis before the main study.

## Design rationale

The pilot asks one narrow causal question:

> At fixed genuine critical-event count and detector sensitivity, do nuisance-alert burden and temporal clustering reduce the probability of a correct, timely human intervention?

If the effect is confirmed, the measured service-time and response distributions can replace the current cross-domain robustness anchors in the main model.
