# ICRA paper plan

## Working title

**When Can Humans Really Intervene? Capacity-Aware Effective Human Control for Multi-Robot Systems**

Alternative:

**Beyond Human-in-the-Loop: Quantifying Effective Human Control under Alert and Capacity Constraints**

## One-sentence thesis

Regulating or designing *when robots must ask a human* is insufficient unless detector quality, alert traffic, operator capacity, deadlines, and common-cause bursts jointly permit humans to act successfully in time.

## 8-page narrative

### 1. Introduction

Start with the apparently safe rule: *escalate sensitive situations to a human*. Show why this is incomplete: a formal opportunity to intervene can coexist with operational inability to intervene.

Contributions:

1. end-to-end EHC metric;
2. analytical feasibility/capacity results;
3. oversight paradox;
4. rare-event false-positive scaling;
5. average-load insufficiency under bursty arrivals;
6. empirically anchored rescue-robot simulation and, ideally, human-subject validation;
7. measurable performance-based certification formulation.

### 2. Related work

Four compact strands:

- fan-out and supervisory control;
- alerts / signal detection / selective querying;
- meaningful human control;
- multi-robot disaster response / variable autonomy.

Explicitly state what is **not** novel.

### 3. Model

Define \(\Lambda,\pi,r,f,M,S,D,h,a\).

Use the dimensionless formulation

$$
A=\Lambda E[S][\pi r+(1-\pi)f],
\qquad
d=\frac{D}{E[S]}.
$$

Define

$$
C=P(\text{successful timely intervention}\mid Z=1).
$$

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

Rebuild main figures around dimensionless or empirically anchored axes:

1. fan-out validation;
2. EHC feasibility map in \(A\) versus \(M\);
3. oversight paradox along ROC curves at several capacities;
4. false-positive scaling;
5. same mean load, different temporal correlation;
6. general-service robustness across service-time CV.

### 7. Human-subject validation / certification

Preferred: include the 2 × 2 false-positive × burst human study.

If data are unavailable in time, use this section for model validation, the measurable certification protocol, and explicit limitations/future human validation.

### 8. Discussion and conclusion

Engineering conclusion first; policy implication second.

Avoid claiming that organizations deliberately overload operators unless independent evidence is later found.

Transferable conclusion:

> A human-control requirement must constrain the performance of the entire escalation-and-supervision system, not merely mandate a human intervention channel.

## Reviewer-risk checklist

- Do not oversell queueing novelty.
- Do not describe large-fleet stress tests as typical present deployments.
- Distinguish candidate-event rate from alert rate.
- Report the FPR denominator explicitly.
- Keep \(h,a,\pi\) as sensitivity parameters unless directly measured.
- Include non-exponential service robustness.
- Include correlated arrivals.
- Release code and seeds.
- Explain why this is a robotics/HRI design and assurance contribution rather than only governance theory.
