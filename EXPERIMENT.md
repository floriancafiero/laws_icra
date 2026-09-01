# Human-subject validation experiment

## Purpose

The theory and simulations establish that false alerts and correlated alert bursts can reduce effective human control. A human-subject experiment would make the ICRA paper much stronger by testing the mechanism directly.

The experiment does not need physical robots. A ROS/RViz or equivalent simulated multi-robot environment is sufficient.

## Task

Participants supervise a team of autonomous firefighting/search-and-rescue robots exploring a damaged office building.

Routine robot behavior is autonomous. Participants only handle escalated supervisory decisions.

Each critical event has:

- a compact robot/environment state;
- an alert explanation;
- a deadline;
- a small action set (approve / override / abort / reassign).

The environment should remain non-weaponized and safety/rescue oriented.

## Main manipulation: 2 x 2 within-subject design

Two factors:

1. **Alert specificity**
   - low false-positive condition;
   - high false-positive condition.

2. **Temporal correlation**
   - dispersed alerts;
   - bursty alerts.

Keep the following as constant as technically possible:

- number of genuinely critical events;
- detector sensitivity to those critical events;
- total mean candidate-event volume;
- robot task difficulty;
- visual interface;
- mission duration.

This isolates our two core claims.

## Primary dependent variable

For critical event (i):

[
Y_i=1
]

iff the participant:

1. receives the escalation;
2. completes the decision before deadline;
3. chooses the correct supervisory response.

The primary participant-level outcome is

[
widehat C.
]

## Secondary outcomes

- critical-event miss rate;
- response/service time distribution;
- queue waiting time;
- number of false alerts processed;
- decision accuracy;
- NASA-TLX workload;
- situation-awareness measure;
- trust/calibration measure;
- ignored/dismissed alerts.

## Hypotheses

### H1 — False-positive burden

At fixed true-critical-event count and sensitivity, increasing false-positive traffic decreases critical-event EHC.

### H2 — Burst effect

At fixed mean alert count, temporally clustered alerts decrease critical-event EHC relative to dispersed alerts.

### H3 — Interaction

The adverse effect of false positives is larger in bursty conditions because nuisance alerts occupy supervisory capacity exactly when true alerts compete for attention.

## Mission size

Use a current-HRI-scale team for the human study, for example 6–8 robots, not hundreds.

Large-fleet consequences are then explored by validated simulation/model scaling.

## Timing

A 90 s maximum decision window is defensible for the deliberative retasking scenario because Al-Hussaini et al. explicitly used that preferred deadline in a recent multi-robot human-subject study.

The exact service-time distribution should be learned from the pilot rather than assumed.

## Pilot before power calculation

Run a small pilot to estimate:

- within-participant variance;
- service-time distribution;
- baseline EHC;
- effect sizes for false-positive and burst manipulations;
- learning/fatigue effects.

Then preregister the main sample size using a power analysis based on the pilot. Do not choose the final (N) from generic HRI conventions.

## Analysis

Use a mixed-effects logistic model at the critical-event level:

[
operatorname{logit}P(Y_{ij}=1)
=
eta_0
+eta_1 FPR_j
+eta_2 Burst_j
+eta_3 FPR_j Burst_j
+u_i
+	ext{mission covariates}.
]

Participant is a random intercept; mission/order can be included as fixed or random effects depending on design.

For response time, use an appropriate survival/time-to-event or mixed-effects model rather than analyzing only the mean.

## Experimental enrichment

True oversight-critical situations may be rare in deployments. The experiment can deliberately enrich their prevalence to obtain statistical power, provided:

- enrichment is disclosed;
- background nuisance traffic is independently controlled;
- deployment-base-rate conclusions are produced by the mathematical model, not by pretending the laboratory prevalence is realistic.

## Ethics and safety

Human-subject approval is required before data collection.

The simulated scenario should avoid unnecessary distress and should not involve real-world hazardous operation. The study measures attention allocation and supervisory decision-making in a fictional rescue environment.
