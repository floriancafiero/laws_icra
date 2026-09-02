# ICRA submission plan — no human-subject experiment

## Working title

**When Can Humans Really Intervene? Capacity-Aware Safety Guarantees for Supervisory Multi-Robot Systems**

Alternative:

**Effective Human Control under Capacity Constraints: A Probabilistic Framework for Supervisory Multi-Robot Systems**

## Thesis

A human intervention channel is not itself a human-control guarantee. Effective control is an end-to-end system property jointly determined by escalation quality, event base rates, finite supervisory capacity, service time, deadlines, and correlated demand.

## Main contribution statement

Prior work separately characterizes human supervisory capacity, alert reliability, fan-out, selective querying, and meaningful human control. We connect these components through an end-to-end probabilistic guarantee

$$
C=P(\text{successful timely human intervention}\mid Z=1).
$$

This produces four system-level results:

1. **capacity/feasibility:** some targets are impossible regardless of staffing, and every finite operator pool has a unique deadline-aware alert-rate capacity;
2. **oversight paradox:** increasing escalation sensitivity can reduce end-to-end control;
3. **rare-event scaling:** fixed nonzero FPR produces linear first-order staffing requirements as fleet scale grows;
4. **burst failure:** average utilization cannot guarantee deadline-constrained control under correlated intervention demand.

A fifth validation result shows that the classical potential-fan-out boundary is recovered as a special stability case.

## Eight-page narrative

### 1. Introduction — ~1 page

Motivate the common design principle “escalate sensitive decisions to a human.”

State the missing question: can the human channel actually process those escalations correctly and before their deadlines?

Give the EHC definition and four contributions immediately.

### 2. Related work — ~0.8 page

Four strands only:

- supervisory control / fan-out / queueing;
- alert reliability and Signal Detection Theory;
- selective querying / variable autonomy;
- Meaningful Human Control / safety assurance.

Explicitly say what is not novel.

### 3. Model — ~1.1 pages

Use dimensionless variables:

$$
A=\Lambda E[S][\pi r+(1-\pi)f],
\qquad
d=D/E[S].
$$

Define the M/M/M analytical baseline and exact \(Q_M\).

### 4. Theory — ~1.5 pages

Main text contains theorem statements and proof intuition:

1. general service-time feasibility ceiling;
2. unique effective-control capacity;
3. oversight paradox;
4. rare-event false-positive staffing law;
5. average-load insufficiency.

Because ICRA 2027 permits no separate supplementary manuscript, the essential proof arguments must appear inside the 8-page submission. `SUPPLEMENT_PROOFS.md` is an internal author notebook only.

### 5. Evaluation — ~2.2 pages

Five figures:

1. deadline-aware feasibility frontier versus ordinary stability;
2. oversight paradox / detector-capacity co-design;
3. false-positive staffing scaling;
4. same mean load, Poisson vs burst/MMPP;
5. non-exponential service robustness.

Include compact baseline-counterexample table and fan-out recovery.

### 6. Robotics interpretation — ~0.6 page

Use variable-autonomy firefighting/search-and-rescue as a neutral anchor.

Current-HRI-scale values provide interpretation only. Large-\(N\) experiments are explicitly scaling stress tests.

### 7. Discussion / assurance implications — ~0.5 page

Engineering implication first:

> safety assurance should constrain the performance of the complete escalation-and-supervision channel.

Certification language is a consequence, not the contribution.

Mention priority scheduling and empirical human-response calibration as future work.

### 8. Conclusion — ~0.3 page

Return to the distinction between opportunity to intervene and ability to intervene.

## Main-figure policy

Do not exceed five principal result figures.

A system architecture diagram can be compactly integrated into Figure 1 or the model section.

Material that does not fit the 8-page paper stays in the reproducibility repository, but the paper itself must be self-contained. Keep only the strongest ROC robustness, service-distribution robustness, and proof sketches in the paper; the pilot prototype is future work.

## Required baselines

- queue stability \(\rho<1\);
- classical fan-out;
- recall-only escalation threshold;
- mean-load criterion under bursty arrivals.

Never describe these baselines as wrong. Show that they answer weaker or different questions.

## Ablations

Must show that:

- setting \(f=0\) removes false-positive scaling;
- \(D\to\infty\) removes deadline failures in stable systems;
- removing arrival correlation removes the acute-burst failure;
- increasing \(M\) shifts the detector operating optimum;
- burst effect persists across service distributions.

## Reviewer-defense checklist

### “Queueing is old.”

Agree. Queueing is machinery, not novelty. Novelty is the joint end-to-end guarantee and derived system-level consequences.

### “This is policy, not robotics.”

Lead with supervisory architecture, detector operating points, fleet scale, deadline guarantees, and safety assurance. Policy appears only in Discussion.

### “The parameters are arbitrary.”

Main plots are dimensionless; empirical values only interpret axes. Sweep broad parameter ranges and publish raw data.

### “There is no user study.”

Claims are structural system-feasibility claims, not claims about universal human cognition. Treat service distributions parametrically and demonstrate robustness outside M/M/M. Empirical HRI calibration is a future validation layer.

### “Fan-out already solves this.”

Show exact fan-out recovery, then demonstrate deadline, false-alert, and burst cases that fan-out is not designed to certify.

## Submission critical path

1. Freeze theorem statements and proofs.
2. Regenerate all five ICRA figures from one script.
3. Inspect baseline counterexamples and ablations.
4. Draft manuscript around results, not around policy.
5. Run hostile-review pass.
6. Only then polish supplementary material and repository.


## ICRA 2027 hard format constraints

Current official call:

- complete submission: **8 pages maximum including references**;
- IEEE/ICRA double-column format;
- double-anonymous review;
- no separate supplementary manuscript/attachment;
- optional accompanying video only.

Practical page budget target:

| component | target pages |
|---|---:|
| Abstract + Introduction + contributions | 0.9 |
| Related work / positioning | 0.7 |
| Model | 1.0 |
| Theory + proof sketches | 1.4 |
| Evaluation | 2.3 |
| Robotics interpretation + discussion + limitations | 0.7 |
| Conclusion | 0.2 |
| References | 0.8 |
| **Total** | **8.0** |

If theory expands, reduce prose or merge figures before cutting the evaluation.
