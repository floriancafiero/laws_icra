# Human-subject validation experiment

## Purpose

The theory and simulations predict that false alerts and correlated alert bursts can reduce effective human control. A human-subject experiment would test that mechanism directly.

The experiment does not need physical robots. A ROS/RViz or equivalent simulated multi-robot environment is sufficient.

## Task

Participants supervise a team of autonomous firefighting/search-and-rescue robots exploring a damaged office building. Routine robot behavior is autonomous; participants handle only escalated supervisory decisions.

Each critical event presents:

- a compact robot/environment state;
- an alert explanation;
- a deadline;
- a small action set (approve / override / abort / reassign).

## Main manipulation: 2 × 2 within-subject design

Two factors:

1. **Alert specificity**
   - low false-positive condition;
   - high false-positive condition.

2. **Temporal correlation**
   - dispersed alerts;
   - bursty alerts.

Hold approximately constant:

- number of genuinely critical events;
- detector sensitivity to those critical events;
- total mean candidate-event volume;
- robot task difficulty;
- interface;
- mission duration.

This isolates the two core mechanisms.

## Primary dependent variable

For critical event \(i\),

$$
Y_i=1
$$

iff the participant receives the escalation, completes the decision before the deadline, and chooses the correct supervisory response.

The primary outcome is the event-level probability of effective control.

## Secondary outcomes

- critical-event miss rate;
- response/service-time distribution;
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

Use a current-HRI-scale team, for example 6–8 robots, in the human study. Large-fleet consequences are explored by validated simulation/model scaling.

## Timing

A 90 s maximum decision window is defensible for a deliberative retasking scenario because Al-Hussaini et al. explicitly used that preferred deadline in a recent multi-robot human-subject study.

The service-time distribution should be learned from the pilot, not imposed from the analytical queue model.

## Pilot before power calculation

Run a small pilot to estimate within-participant variance, service times, baseline EHC, manipulation effect sizes, and learning/fatigue effects. Then preregister the main sample size using a power calculation based on the pilot.

## Analysis

Use a mixed-effects logistic model at the critical-event level:

$$
\operatorname{logit}P(Y_{ij}=1)
=
\beta_0+\beta_1FPR_j+\beta_2Burst_j+\beta_3(FPR_j\times Burst_j)+u_i+\text{mission covariates}.
$$

Participant is a random intercept. Mission and order effects should be modeled as appropriate.

For response times, use a time-to-event or mixed-effects model rather than analyzing only the mean.

## Experimental enrichment

True oversight-critical situations may be rare in deployment. The experiment can deliberately enrich their prevalence for statistical power if enrichment is disclosed and deployment-base-rate conclusions come from the model rather than from treating the laboratory prevalence as realistic.

## Ethics and safety

Human-subject approval is required before data collection. The study should remain a fictional rescue scenario and should not involve real-world hazardous operation.
