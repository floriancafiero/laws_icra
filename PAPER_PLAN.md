# ICRA paper plan

## Working title

**When Can Humans Really Intervene? Capacity-Aware Effective Human Control for Multi-Robot Systems**

Alternative:

**Beyond Human-in-the-Loop: Quantifying Effective Human Control under Alert and Capacity Constraints**

## One-sentence thesis

Regulating or designing *when robots must ask a human* is insufficient unless the detector, alert traffic, operator capacity, deadlines, and common-cause bursts jointly permit humans to act successfully in time.

## 8-page narrative

### 1. Introduction

Start with the apparently safe design rule:

> escalate sensitive situations to a human.

Show why it is incomplete. A formal right/opportunity to intervene can coexist with an operational inability to intervene.

Contributions:

1. end-to-end EHC metric;
2. analytical feasibility/capacity results;
3. oversight paradox;
4. rare-event false-positive scaling;
5. proof that mean utilization cannot guarantee EHC under bursty arrivals;
6. empirically anchored rescue-robot simulation and, ideally, human-subject validation;
7. performance-based certification formulation.

### 2. Related work

Four compact strands:

- fan-out and supervisory control;
- alerts / signal detection / selective querying;
- meaningful human control;
- multi-robot disaster response / variable autonomy.

Explicitly state what is **not** novel.

### 3. Model

Define

[
Lambda,pi,r,f,M,S,D,h,a.
]

Use the dimensionless formulation:

[
A=Lambda E[S][pi r+(1-pi)f],
qquad
d=D/E[S].
]

Define

[
C=P(	ext{successful timely intervention}mid Z=1).
]

### 4. Theory

Keep five central results:

1. absolute feasibility ceiling;
2. effective-control capacity;
3. oversight paradox;
4. false-positive scaling law;
5. average-load insufficiency under correlated bursts.

Proof details that do not fit go to supplementary material.

### 5. Empirical grounding and scenario

Use firefighting/search-and-rescue as the primary scenario.

Show:

- current HRI team-size envelope;
- recovery of ICRA-2025 fan-out as a special case;
- 90 s decision deadline from recent multi-robot alert work;
- clearly marked scenario/sensitivity parameters for quantities the literature does not identify.

### 6. Simulation results

Main figures should be rebuilt around dimensionless or empirically anchored axes:

1. **Fan-out validation:** our stability boundary reproduces PFO.
2. **EHC feasibility map:** (A) or candidate-event volume vs (M).
3. **Oversight paradox:** sensitivity vs EHC along ROC curves at several capacities.
4. **False-positive scaling:** operator requirement vs scale/FPR.
5. **Burst result:** same mean load, different temporal correlation.
6. **General-service robustness:** effect persists across service-time CV.

### 7. Human-subject validation / certification

Preferred: include the 2x2 false-positive x burst human study.

If data are not available in time, use this section for:

- model validation against literature-scale simulations;
- measurable certification protocol;
- explicit limitations and preregistered future human validation.

### 8. Discussion and conclusion

Engineering conclusion first; policy implication second.

Avoid claiming military organizations deliberately overload operators unless evidence is later found.

The transferable conclusion is:

> A human-control requirement must constrain the performance of the entire escalation-and-supervision system, not merely mandate a human intervention channel.

## Reviewer-risk checklist

Before submission:

- do not oversell queueing novelty;
- do not use hundreds-of-robots scenarios as "realistic current deployment";
- distinguish candidate-event rate from alert rate;
- report FPR denominator explicitly;
- keep (h,a,pi) as sensitivity parameters unless directly measured;
- include non-exponential service robustness;
- include correlated arrivals;
- give code and seeds;
- explain why the result is a robotics/HRI design contribution rather than only governance theory.
