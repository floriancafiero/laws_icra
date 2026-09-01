# Proposed performance-based certification of effective human control

## Core principle

A system should not be certified merely because:

- a human operator exists;
- the system displays warnings;
- the operator has an override button.

The certification target is an end-to-end operational property:

[
oxed{
C=P(	ext{critical situation is successfully handled by a human before its deadline})
}
]

within a declared **Operational Design Domain (ODD)** and at a declared maximum deployment scale.

A candidate requirement is

[
oxed{Cge C_{min}.}
]

## Proposed certificate

The certificate must declare:

1. ODD and mission/task class.
2. Maximum fleet size (N_{mathrm{cert}}).
3. Number and organization of operators (M).
4. Escalation model/version and operating threshold.
5. Definition of an oversight-critical situation (Z=1).
6. Deadline definition (D), including class-specific deadlines where applicable.
7. Measured TPR (r) and FPR (f), with denominators stated explicitly.
8. Alert-rate and burst statistics.
9. Human service-time distribution, not only its mean.
10. End-to-end EHC estimate and uncertainty.
11. Separate performance under prescribed burst/common-cause stress conditions.

Changing fleet size, alert threshold, operator staffing, or material interface behavior invalidates extrapolation beyond the tested certificate unless a validated model establishes equivalence.

## Test protocol

### Stage 1 — Detector characterization

On a labeled scenario corpus representative of the ODD, estimate

[
r=P(A=1mid Z=1)
]

and

[
f=P(A=1mid Z=0).
]

Also report prevalence (pi), because predictive value and workload depend on base rate.

"False alarm rate" is unacceptable unless the denominator is explicitly defined.

### Stage 2 — Supervisory workload characterization

Run the declared system configuration and record:

- alert timestamps;
- number of simultaneous/pending alerts;
- operator start and completion times;
- service-time distribution (S);
- alert classes and deadlines.

Estimate both average offered load

[
A=
u E[S]
]

and burst/tail statistics.

Average utilization alone is not a sufficient pass criterion.

### Stage 3 — Blinded end-to-end challenge events

Inject or select labeled oversight-critical events while keeping background alert traffic representative.

For every critical event, record a binary success:

[
Y_i =
1
]

iff all of the following occur:

1. the event is escalated;
2. the operator reaches and completes review before the deadline;
3. the operator chooses a correct permitted action;
4. the intervention successfully takes effect.

Then

[
widehat C=rac1nsum_i Y_i.
]

### Stage 4 — Burst/common-cause stress stratum

Repeat end-to-end testing under a declared burst regime, for example:

- an empirical 99th/99.9th-percentile burst if adequate field data exist; or
- a standardized design-burst stress test.

Report

[
C_{mathrm{burst}}
]

separately. Do not average it into easy nominal cases.

## Statistical pass rule

A simple transparent rule is:

> the one-sided (100(1-alpha)%) Clopper-Pearson lower confidence bound for (C) must exceed (C_{min}).

For example, with (C_{min}=0.95) and one-sided 95% confidence:

- 59/59 successful critical events are sufficient;
- if one failure is observed, at least 92/93 successes are required;
- with two failures, at least 122/124 successes are required;
- with three failures, at least 150/153 successes are required.

These are illustrative certification sample sizes, not a claim that 59 trials are sufficient to validate every ODD. Coverage across event classes and burst strata still matters.

## Two complementary paths to certification

### Direct empirical certificate

Use the observed (Y_i) outcomes. Strongest evidentially, but expensive when true critical events are rare.

### Model-assisted certificate

Estimate the measurable components:

[
r,quad f,quad pi,quad Lambda,quad S,quad D,quad h,quad a,
]

validate the queue/simulation model against held-out trials, then use the validated model to establish performance across deployment scales and tail-load conditions.

The paper should argue that direct testing and model-assisted extrapolation are complementary rather than substitutes.

## Candidate regulatory language

> Within the declared operational design domain and at the declared maximum fleet-to-operator configuration, the supervisory architecture shall demonstrate a specified lower bound on the probability of timely and successful human intervention conditional on an oversight-critical situation. Demonstration shall include representative operations and prescribed correlated-alert stress conditions. Alert detection performance, false-positive rate, human-service-time distribution, intervention deadlines, and deployment scale shall be reported as part of the evidence.

This deliberately regulates **performance**, not merely the existence of a human-in-the-loop architecture.
