# Dimensionless formulation

Let

$$
\Lambda=N\lambda
$$

be the total rate of candidate decision situations before escalation, and

$$
\alpha=\pi r+(1-\pi)f
$$

the probability that a candidate situation generates a human alert. The alert rate is

$$
\nu=\Lambda\alpha.
$$

Let \(m=E[S]\) be mean human service/decision time. Define the **offered human work**

$$
\boxed{A=\nu m=\Lambda m[\pi r+(1-\pi)f]}
$$

measured in Erlangs (operator-time required per unit clock time).

For \(M\) operators,

$$
\boxed{\rho=\frac{A}{M}}
$$

is utilization.

Define normalized deadline slack

$$
\boxed{d=\frac{D}{m}}.
$$

For the baseline M/M/M model, \(Q_M\) depends on physical units only through

$$
Q_M=\widetilde Q(M,A,d).
$$

Hence

$$
\boxed{C=rha\,\widetilde Q(M,A,d).}
$$

This scale-free form is preferable to presenting results only in hours/minutes.

## General-service extension

For non-exponential service times, introduce

$$
c_s=\frac{\sqrt{\operatorname{Var}(S)}}{E[S]},
$$

the service-time coefficient of variation. The general queue then depends on

$$
(M,A,d,c_s,\text{arrival correlation/burst distribution}).
$$

Closed forms are no longer generally available, so the paper should retain M/M/M for analytical propositions and use gamma/lognormal service distributions for robustness simulations.

## Empirical anchors for \(d\)

These are examples, not universal constants:

- Al-Hussaini et al. use a 90 s preferred decision deadline for multi-robot retasking.
- A 2025 cross-domain human inspection study reports 21.2 s mean inspection time, giving \(d\approx4.25\) when the two values are paired only as a composite robustness scenario.
- Recent automated-driving work provides a shorter-timescale anchor: a 7 s takeover window and review-average mean takeover time of 2.72 s correspond to \(d\approx2.57\).

The paper should sweep \(d\) rather than claim a universal human-response time.

## Fan-out is recovered as a special case

Perkins et al. (ICRA 2025) use

$$
PFO=\frac{RST}{IT}+1.
$$

If each robot creates one human request per \(RST+IT\) cycle,

$$
\lambda_{\mathrm{req}}=\frac{1}{RST+IT},
\qquad
m=IT.
$$

Queue stability with one operator requires

$$
N\lambda_{\mathrm{req}}m<1,
$$

hence

$$
N<\frac{RST+IT}{IT}=PFO.
$$

Classical fan-out is therefore a special capacity boundary nested inside the proposed EHC framework.
