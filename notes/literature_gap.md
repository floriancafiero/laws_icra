# Literature positioning — working memo

## What is already established

We must not claim novelty for any of these in isolation:

- human supervisory overload;
- fan-out / number of robots per operator;
- queueing models of human operators;
- multi-server operator pools;
- false alarms and cry-wolf effects;
- Signal Detection Theory for oversight;
- selective human querying / adaptive autonomy;
- the concept of Meaningful Human Control;
- risk-aware alert thresholds.

## Closest recent strands identified so far

1. **Meaningful Human Control / operationalization** — recent work argues that human control must be effective rather than nominal, but usually stops short of a joint detector-quality + staffing + deadline guarantee.
2. **Multi-robot fan-out and supervisory control** — mature literature, including recent ICRA work; capacity itself is not novel.
3. **Alert reliability / human factors** — false positives and low predictive value are known to degrade operator performance.
4. **Selective HITL robotics** — current HRI work already optimizes when robots should ask humans, including intervention cost/workload.
5. **Recent adaptive oversight systems** — at least one 2026 paper already combines risk-triggered human activation, workload, and intervention latency.
6. **LAWS operator literature** — recent reviews still identify major gaps in realistic field-operator decision processes and workload.

## Candidate novelty claim

Existing research separately studies detector/alert quality, human workload, multi-robot supervisory capacity, adaptive querying, and meaningful human control. The proposed contribution is to integrate these into an **end-to-end probabilistic control guarantee**:

\[
P(\text{critical situation detected, processed, correctly resolved and successfully acted upon before deadline})\ge C_{\min}.
\]

This yields system-level consequences not captured by the components separately:

- a detector can become *too sensitive* to maximize end-to-end human control;
- in rare-event regimes, false positives can dominate human-supervision scaling;
- fixed average workload does not guarantee control under correlated bursts;
- staffing, detector specificity, fleet size, deadlines, and prioritization are joint design/certification variables.

## Regulatory motivation

A rule saying that sensitive situations must be referred to a human is incomplete unless it also constrains whether the human-supervisory system can realistically act on those referrals.

Memorable formulation:

> Regulating when machines must call humans is not enough; we must regulate whether humans can realistically answer.
