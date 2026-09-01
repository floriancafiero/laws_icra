# Proposed performance-based certification of effective human control

## Core principle

A system should not be certified merely because a human operator exists, the system displays warnings, or the operator has an override button.

The certification target is an end-to-end operational property:

$$
C=P(\text{critical situation is successfully handled by a human before its deadline})
$$

within a declared **Operational Design Domain (ODD)** and at a declared maximum deployment scale. A candidate requirement is

$$
C\ge C_{\min}.
$$

## Proposed certificate

The certificate must declare:

1. ODD and mission/task class.
2. Maximum fleet size \(N_{\mathrm{cert}}\).
3. Number and organization of operators \(M\).
4. Escalation model/version and operating threshold.
5. Definition of an oversight-critical situation \(Z=1\).
6. Deadline definition \(D\), including class-specific deadlines where applicable.
7. Measured TPR \(r\) and FPR \(f\), with denominators stated explicitly.
8. Alert-rate and burst statistics.
9. Human service-time distribution, not only its mean.
10. End-to-end EHC estimate and uncertainty.
11. Separate performance under prescribed burst/common-cause stress conditions.

Changing fleet size, alert threshold, operator staffing, or material interface behavior invalidates extrapolation beyond the tested certificate unless a validated model establishes equivalence.

## Test protocol

### Stage 1 — Detector characterization

On a labeled scenario corpus representative of the ODD, estimate

$$
r=P(A=1\mid Z=1)
$$

and

$$
f=P(A=1\mid Z=0).
$$

Also report prevalence \(\pi\), because predictive value and workload depend on base rate. “False alarm rate” is unacceptable unless the denominator is explicitly defined.

### Stage 2 — Supervisory workload characterization

Run the declared system configuration and record alert timestamps, pending-alert counts, operator start/completion times, service-time distribution \(S\), alert classes, and deadlines.

Estimate average offered load

$$
A=\nu E[S]
$$

as well as burst/tail statistics. Average utilization alone is not a sufficient pass criterion.

### Stage 3 — Blinded end-to-end challenge events

Inject or select labeled oversight-critical events while keeping background alert traffic representative.

For every critical event, record a binary success \(Y_i=1\) iff:

1. the event is escalated;
2. the operator reaches and completes review before the deadline;
3. the operator chooses a correct permitted action;
4. the intervention successfully takes effect.

Then

$$
\widehat C=\frac{1}{n}\sum_iY_i.
$$

### Stage 4 — Burst/common-cause stress stratum

Repeat end-to-end testing under a declared burst regime, for example an empirical 99th/99.9th-percentile burst when adequate field data exist, or a standardized design-burst stress test.

Report \(C_{\mathrm{burst}}\) separately; do not average it into easy nominal cases.

## Statistical pass rule

A simple transparent rule is:

> The one-sided \(100(1-\alpha)\%\) Clopper–Pearson lower confidence bound for \(C\) must exceed \(C_{\min}\).

For \(C_{\min}=0.95\) and one-sided 95% confidence:

- 59/59 successful critical events are sufficient;
- with one observed failure, 92/93 successes are required;
- with two failures, 122/124 successes are required;
- with three failures, 150/153 successes are required.

These are illustrative certification sample sizes, not a claim that 59 trials validate every ODD. Coverage across event classes and burst strata still matters.

## Direct and model-assisted certification

A direct empirical certificate uses the observed \(Y_i\) outcomes. It is strongest evidentially but expensive when true critical events are rare.

A model-assisted certificate estimates

$$
r,\ f,\ \pi,\ \Lambda,\ S,\ D,\ h,\ a,
$$

validates the queue/simulation model against held-out trials, then uses the validated model to establish performance across deployment scales and tail-load conditions.

The paper should present direct testing and model-assisted extrapolation as complementary.

## Candidate regulatory language

> Within the declared operational design domain and at the declared maximum fleet-to-operator configuration, the supervisory architecture shall demonstrate a specified lower bound on the probability of timely and successful human intervention conditional on an oversight-critical situation. Demonstration shall include representative operations and prescribed correlated-alert stress conditions. Alert detection performance, false-positive rate, human-service-time distribution, intervention deadlines, and deployment scale shall be reported as part of the evidence.

This regulates **performance**, not merely the existence of a human-in-the-loop architecture.
