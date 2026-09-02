# ICRA evaluation protocol — no human-subject experiment

The submission should be evaluated as a **formal safety/performance framework**, not as an HRI user-study paper.

## Claims to validate

The computational evaluation must answer five questions:

1. Does the framework recover established fan-out capacity in its limiting special case?
2. How much smaller is the deadline-aware EHC feasibility region than ordinary queue stability?
3. Can maximizing escalation recall decrease end-to-end control?
4. Does minimum staffing exhibit the predicted false-positive scaling law?
5. Can equal mean utilization produce radically different EHC under correlated demand, and does the effect survive non-exponential service times?

## Figure 1 — Deadline-aware feasibility frontier

Use dimensionless variables

$$
A=\nu E[S],\qquad d=D/E[S].
$$

For \(M\in\{1,2,4,8\}\), solve the maximum admissible offered load \(A_M^*(d)\) such that

$$
Q_M(A,d)\ge0.95.
$$

Overlay ordinary stability limits \(A<M\).

Message:

> Stability is necessary but can be far from sufficient for deadline-constrained human control.

No arbitrary physical time units are needed.

## Figure 2 — Oversight paradox and detector/capacity co-design

Use equal-variance binormal ROC curves:

$$
f(t)=1-\Phi(t),\qquad
r(t)=1-\Phi(t-d').
$$

Let pre-escalation candidate load in service-time units be

$$
L=\Lambda E[S].
$$

Then

$$
A(t)=L[\pi r(t)+(1-\pi)f(t)].
$$

Plot

$$
C(t)=r(t)Q_M(A(t),d)
$$

against sensitivity \(r\) for several operator capacities \(M\).

Primary setting:

- \(d'=3\);
- \(\pi=10^{-3}\);
- \(L=20\);
- \(d=4\);
- \(M\in\{2,4,8\}\);
- \(h=a=1\).

Supplementary robustness: \(d'\in\{2,3,4\}\).

Message:

> The system-optimal detector operating point depends on supervisory capacity; maximum recall is not generally maximum control.

## Figure 3 — False-positive staffing scaling

Use:

- per-system candidate load \(\ell=\lambda E[S]=0.2\);
- \(\pi=10^{-4}\);
- \(r=0.99\);
- \(d=4\);
- \(C_{\min}=0.95\);
- \(f\in\{0.001,0.005,0.01,0.02\}\).

Plot \(M_{\min}(N)\) over increasing \(N\), plus the first-order stability slope

$$
N\ell f.
$$

The theorem predicts

$$
\frac{M_{\min}}N\to\ell f
$$

in normalized units.

Message:

> Even rare nuisance-alert probabilities become first-order staffing constraints at scale.

## Figure 4 — Same average load, different temporal structure

Hold fixed:

$$
A=1.2,\qquad M=3,\qquad d=4.
$$

Compare arrival processes with identical long-run mean:

- Poisson;
- batch-Poisson, batch 2;
- batch-Poisson, batch 4;
- batch-Poisson, batch 8;
- two-state MMPP/common-shock process.

Use Gamma service with \(CV=1\) for the main plot.

Message:

> Average utilization \(\rho=0.4\) can coexist with very different probabilities of timely control.

## Figure 5 — Robustness outside M/M/M

Repeat the burst comparison with mean service normalized to one and:

- deterministic \(CV=0\);
- Gamma \(CV=0.5\);
- exponential/Gamma \(CV=1\);
- Gamma \(CV=1.5\);
- lognormal \(CV=1\).

Main comparison: Poisson vs batch size 4 or 8.

Message:

> The burst failure is not an artifact of exponential service times.

## Baselines

The paper should compare EHC against simple criteria without caricaturing them.

### B1. Queue stability

$$
\rho<1.
$$

This tests eventual service, not deadline service.

### B2. Classical fan-out

Use Perkins et al.'s reported \(RST,IT\) to recover

$$
PFO=RST/IT+1.
$$

State explicitly that fan-out was not designed as an EHC guarantee.

### B3. Recall-only detector selection

Choose the ROC operating point that maximizes \(r\), subject only to a conventional detector criterion, and compare it to the operating point maximizing \(C\).

### B4. Mean-load burst criterion

Compare systems with the same \(\rho\) but different burst structure.

## Counterexample table

Include a compact table with columns:

| Case | Standard criterion | Standard verdict | EHC | EHC verdict | Why |
|---|---|---|---:|---|---|

Candidate cases:

1. low utilization but deadline too short;
2. fan-out-stable operation close to the stability boundary;
3. recall-maximized detector causing overload;
4. low mean utilization with synchronized batches.

The point is not that the baseline criteria are wrong. They answer weaker/different questions.

## Ablations

Report at least:

- \(f=0\) versus \(f>0\);
- \(D=\infty\) versus finite \(D\);
- independent versus bursty arrivals;
- one versus multiple operators;
- exponential versus non-exponential service.

## Monte Carlo precision

For simulation-only quantities:

- at least 50,000 completed alerts per replicate;
- at least 5 independent seeds for main figures;
- plot 95% Monte Carlo confidence intervals where visually useful;
- save raw figure data as CSV.

## Submission framing

The rescue/firefighting scenario is an **interpretive anchor**, not an empirical claim that all deployments share one parameter vector.

Large-\(N\) experiments are called **scaling stress tests**.

The certification/policy implication belongs in Discussion. The core paper is about robotics supervisory architecture, safety assurance, and performance evaluation.
