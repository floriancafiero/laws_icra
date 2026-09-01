# Formal model — working notes

## 1. Event and warning process

There are `N` autonomous systems. Each generates potentially relevant decisions at mean rate `λ`.

A decision is oversight-critical with probability

\[
P(Z=1)=\pi.
\]

The escalation mechanism has

\[
r=P(A=1\mid Z=1), \qquad f=P(A=1\mid Z=0).
\]

Thus the probability that a decision generates a human alert is

\[
\alpha = \pi r + (1-\pi)f,
\]

and the pooled alert rate is

\[
\nu = N\lambda\alpha.
\]

## 2. Human supervisory queue

There are `M` pooled operators. In the baseline model each operator has exponential processing rate `μ`, alerts are FCFS, and alert arrivals are Poisson. This is an M/M/M queue.

Utilization is

\[
\rho = \frac{\nu}{M\mu}.
\]

A stationary queue requires `ρ < 1`.

Let `Q_M(ν,D)` denote the probability that an alert is fully processed before deadline `D`.

## 3. Effective human control

Let

- `h`: probability of a correct human decision conditional on timely review;
- `a`: probability that a correct intervention successfully takes effect.

Define effective human control for an oversight-critical event as

\[
C = P(\text{successful timely human prevention}\mid Z=1).
\]

Under the baseline independence assumptions:

\[
\boxed{C=rhaQ_M(\nu,D).}
\]

A performance-based control requirement is

\[
C \ge C_{\min}.
\]

## 4. Exact M/M/M completion probability

For `ν < Mμ`, define Erlang-C waiting probability

\[
P_W =
\frac{\frac{x^M}{M!}\frac{1}{1-\rho}}
{\sum_{k=0}^{M-1}\frac{x^k}{k!}+\frac{x^M}{M!}\frac{1}{1-\rho}},
\qquad x=\frac{\nu}{\mu}.
\]

Conditional on waiting, `W ~ Exp(Mμ-ν)`. With service time `S ~ Exp(μ)`,

\[
Q_M(D)=(1-P_W)P(S\le D)+P_W P(W+S\le D).
\]

## 5. Current propositions

### Proposition 1 — Absolute feasibility ceiling

Even with infinitely many operators,

\[
\lim_{M\to\infty} Q_M(\nu,D)=1-e^{-\mu D}.
\]

Hence if

\[
C_{\min}>rha(1-e^{-\mu D}),
\]

no staffing level can satisfy the EHC target.

### Proposition 2 — Effective-control capacity

For fixed `M, μ, D`, `Q_M(ν,D)` decreases with `ν`. For any feasible target queue-level probability

\[
q^*=\frac{C_{\min}}{rha},
\]

there is a unique maximum admissible alert rate `ν_M*` solving

\[
Q_M(\nu_M^*,D)=q^*.
\]

Thus

\[
N_{\max}=\left\lfloor\frac{\nu_M^*}{\lambda[\pi r+(1-\pi)f]}\right\rfloor.
\]

### Proposition 3 — Oversight paradox

Let `s` increase escalation aggressiveness, with `r'(s)>0` and normally `f'(s)>0`. Then

\[
C(s)=r(s)haQ_M(\nu(s),D).
\]

Writing

\[
\kappa_M=-\frac{\partial\log Q_M}{\partial\nu}>0,
\]

we have

\[
\frac{dC}{ds}<0
\iff
\frac{r'}{r}
<
\kappa_M N\lambda[\pi r'+(1-\pi)f'].
\]

Thus more aggressive escalation can reduce effective control when marginal congestion exceeds marginal detection benefit.

### Proposition 4 — Rare-event false-positive scaling

If `π_N -> 0` and fixed `f>0`, then

\[
\nu \sim N\lambda f.
\]

Under a feasible fixed EHC target,

\[
\frac{M_{\min}(N)}{N}\to\frac{\lambda f}{\mu}.
\]

Thus preserving EHC at fleet scale requires either linearly increasing staffing or a false-positive rate that decreases with deployment scale.

### Proposition 5 — Average-load insufficiency

Let batches of size `b` arrive at rate `β_b=\bar\nu/b`, so all processes share the same average alert rate `\bar\nu<M\mu`.

For a simultaneous burst of `b` alerts and deadline `D`, even from an empty system,

\[
P(T\le D\mid B=b)\le \min\left(1,\frac{M\mu D}{b}\right).
\]

Therefore at fixed mean utilization,

\[
\lim_{b\to\infty} C=0.
\]

Average operator utilization alone cannot certify effective human control.
