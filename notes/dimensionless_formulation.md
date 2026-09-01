# Dimensionless formulation

The baseline model becomes substantially cleaner after non-dimensionalization.

Let

[
Lambda=Nlambda
]

be the total rate of candidate decision situations before escalation, and

[
alpha=pi r+(1-pi)f
]

the probability that a candidate situation generates a human alert. The alert rate is

[

u=Lambdaalpha.
]

Let (m=E[S]) be mean human service/decision time. Define the **offered human work**

[
oxed{A=
u m=Lambda m[pi r+(1-pi)f]}
]

measured in Erlangs (operator-time required per unit clock time).

For (M) operators,

[
oxed{ho=rac{A}{M}}
]

is utilization.

Define normalized deadline slack

[
oxed{d=rac{D}{m}}.
]

For the baseline M/M/M model, (Q_M) depends on physical units only through

[
Q_M = widetilde Q(M,A,d).
]

Hence

[
oxed{
C=rha,widetilde Q(M,A,d).
}
]

This is preferable to presenting results in arbitrary hours/minutes because the same theory applies to fast takeover tasks and slower deliberative supervisory decisions.

## General-service extension

For non-exponential service times, introduce

[
c_s=rac{sqrt{operatorname{Var}(S)}}{E[S]},
]

the service-time coefficient of variation. The queue then depends on

[
(M,A,d,c_s,	ext{arrival correlation/burst distribution}).
]

Closed forms are no longer generally available, so the paper should retain M/M/M for analytical propositions and use gamma/lognormal service distributions for robustness simulations.

## Empirical anchors for (d)

These are examples, not universal constants:

- Al-Hussaini et al. use a 90 s preferred decision deadline for multi-robot retasking.
- A 2025 cross-domain human inspection study reports 21.2 s mean inspection time, giving (dapprox 4.25) when paired only as a composite robustness scenario.
- Recent automated-driving takeover studies operate at a shorter scale; a 7 s takeover window divided by a review-average mean takeover time of 2.72 s gives (dapprox2.57).

The paper should therefore sweep (d), rather than claim a single universal human-response time.

## Fan-out is recovered as a special case

Perkins et al. (ICRA 2025) use

[
PFO=rac{RST}{IT}+1.
]

If each robot creates one human request per (RST+IT) cycle, then

[
lambda_{req}=rac{1}{RST+IT},
qquad
m=IT.
]

Queue stability with one operator requires

[
Nlambda_{req}m<1,
]

hence

[
N<rac{RST+IT}{IT}=PFO.
]

So classical fan-out is the zero-deadline-risk / perfect-escalation capacity boundary nested inside the proposed EHC framework.
