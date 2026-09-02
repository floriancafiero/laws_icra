# Internal proof notebook

These derivations support the ICRA submission and are kept in the repository for verification. ICRA 2027 does not allow a separate supplementary manuscript, so the submitted paper contains self-contained theorem statements and proof sketches; this file is not part of the submission.

## Lemma 1 — General service-time ceiling

Let \(W\ge0\) be waiting time and \(S\ge0\) the human service requirement. Completion time is \(T=W+S\). Therefore

$$
\{T\le D\}\subseteq\{S\le D\}
$$

and

$$
P(T\le D)\le P(S\le D)=F_S(D).
$$

Multiplying by the independent baseline factors \(rha\) yields

$$
C\le rhaF_S(D).
$$

No arrival-process or scheduling assumption is needed for this upper bound.

For \(S\sim\mathrm{Exp}(\mu)\), \(F_S(D)=1-e^{-\mu D}\).

---

## Lemma 2 — Monotonicity in arrival rate

Take two FCFS, work-conserving \(M\)-server queues with identical service requirements for every shared arrival.

Let system \(L\) contain a Poisson arrival stream of rate \(\nu_1\). Construct system \(H\) by adding an independent Poisson stream of rate \(\nu_2-\nu_1>0\), so system \(H\) has total rate \(\nu_2>\nu_1\).

Couple the two queues from the same empty state and assign each shared customer the same service requirement in both systems. The added jobs can never create an earlier service start for a shared customer. By induction over event times, every shared customer's start and completion time in \(H\) is at least as late as in \(L\).

Therefore the response time is stochastically nondecreasing in \(\nu\):

$$
T(\nu_1)\le_{\rm st}T(\nu_2).
$$

Hence

$$
Q_M(\nu_1,D)\ge Q_M(\nu_2,D).
$$

For positive \(D,\mu\) and interior stable rates, the inequality is strict because the extra stream has positive probability of creating additional work that delays an arrival past a time interval of positive measure.

Continuity follows directly from the closed-form Erlang-C expression on \(0\le\nu<M\mu\).

As \(\nu\uparrow M\mu\), Erlang-C waiting probability tends to one while the conditional waiting rate \(M\mu-\nu\downarrow0\). Thus for every finite \(D\),

$$
P(W+S\le D\mid W>0)\to0,
$$

and hence

$$
Q_M(\nu,D)\to0.
$$

At \(\nu=0\) there is no queueing and

$$
Q_M(0,D)=P(S\le D)=1-e^{-\mu D}.
$$

The intermediate value theorem plus strict monotonicity gives the unique \(\nu_M^*\).

---

## Lemma 3 — Monotonicity in staffing

Couple an \(M\)-server and an \((M+1)\)-server FCFS work-conserving queue with identical arrivals and service requirements.

The extra server can be ignored whenever it is not useful. Equivalently, the feasible set of service-start schedules with \(M\) servers is a subset of that with \(M+1\) servers. Under FCFS/work conservation, adding a server cannot delay a customer's service start or completion.

Therefore

$$
T_{M+1}\le_{\rm st}T_M,
$$

so

$$
Q_{M+1}(\nu,D)\ge Q_M(\nu,D).
$$

This establishes monotonic search for \(M_{\min}\).

---

## Proposition — Finite staffing feasibility

Assume fixed finite \(\nu>0\). In the M/M/M system, as \(M\to\infty\), the probability of waiting tends to zero. Therefore

$$
Q_M(\nu,D)\to1-e^{-\mu D}.
$$

If

$$
C_{\min}<rha(1-e^{-\mu D}),
$$

then the convergence implies that some finite \(M\) satisfies the target.

Conversely, if the target exceeds the service-only ceiling, Lemma 1 makes it impossible. At equality and positive finite load, every finite \(M\) has positive probability of waiting and hence

$$
Q_M(\nu,D)<1-e^{-\mu D},
$$

so equality can only be approached asymptotically.

---

## Theorem — Oversight paradox

Write

$$
C(s)=r(s)haQ_M(\nu(s),D)
$$

with

$$
\nu(s)=\Lambda[\pi r(s)+(1-\pi)f(s)].
$$

Differentiation in the stable interior gives

$$
C'(s)
=
ha\left[
r'(s)Q_M
+
r(s)\frac{\partial Q_M}{\partial\nu}\nu'(s)
\right].
$$

Divide by positive \(rQ_Mha\):

$$
\frac{C'(s)}{C(s)}
=
\frac{r'(s)}{r(s)}
+
\frac{\partial\log Q_M}{\partial\nu}\nu'(s).
$$

Define

$$
\kappa_M=-\partial_\nu\log Q_M>0.
$$

Then

$$
C'(s)<0
\iff
\frac{r'}r<\kappa_M\nu'
$$

and substitute

$$
\nu'=\Lambda[\pi r'+(1-\pi)f'].
$$

For \(M=1\),

$$
Q_1=1-e^{-[\mu-\nu]D}.
$$

Direct differentiation gives

$$
C'
=
ha\left[
r'(1-e^{-\delta D})
-rD\nu'e^{-\delta D}
\right],
\qquad
\delta=\mu-\nu.
$$

Multiplying by \(e^{\delta D}\) yields

$$
C'<0
\iff
r'(e^{\delta D}-1)<rD\nu'.
$$

---

## Theorem — Constant safety margin at large offered load

Work in normalized units, so service time is \(\mathrm{Exp}(1)\), offered load is \(A\), and staffing is \(M>A\). Fix a deadline \(d>0\) and a target

\[
q^*=\frac{C_{\min}}{rha}\in(0,1-e^{-d}).
\]

Consider any sequence \(A_n\to\infty\), \(M_n>A_n\), with

\[
c_n=M_n-A_n\to c\in(0,\infty).
\]

### Erlang-C waiting probability tends to one

Erlang-C can be written as

\[
p_W^{-1}
=
1+
\left(1-\frac{A_n}{M_n}\right)
\frac{\sum_{k=0}^{M_n-1}A_n^k/k!}{A_n^{M_n}/M_n!}.
\]

Let \(X_n\sim\mathrm{Pois}(A_n)\). Since \(1-A_n/M_n=c_n/M_n\),

\[
p_W^{-1}
=
1+
\frac{c_n}{M_n}
\frac{P(X_n\le M_n-1)}{P(X_n=M_n)}.
\]

Because \(M_n-A_n=O(1)\), the Poisson central limit theorem gives

\[
P(X_n\le M_n-1)\to \frac12,
\]

while the local limit theorem (equivalently Stirling's formula) gives

\[
P(X_n=M_n)\sim \frac1{\sqrt{2\pi A_n}}.
\]

Therefore

\[
\frac{c_n}{M_n}
\frac{P(X_n\le M_n-1)}{P(X_n=M_n)}
=
O(A_n^{-1/2})\to0,
\]

and hence

\[
p_W\to1.
\]

### Limiting deadline-completion probability

Conditional on waiting,

\[
W/m\mid W>0\sim \mathrm{Exp}(M_n-A_n)=\mathrm{Exp}(c_n),
\]

while

\[
S/m\sim\mathrm{Exp}(1).
\]

Therefore

\[
Q_{M_n}(A_n,d)
\to
H_c(d)
=
P(\mathrm{Exp}(c)+\mathrm{Exp}(1)\le d).
\]

For \(c\neq1\),

\[
H_c(d)
=
1-\frac{e^{-cd}-ce^{-d}}{1-c},
\]

and for \(c=1\),

\[
H_1(d)=1-e^{-d}(1+d).
\]

If \(c_2>c_1\), then \(\mathrm{Exp}(c_2)\le_{\rm st}\mathrm{Exp}(c_1)\), so \(H_c(d)\) is strictly increasing in \(c\). Also

\[
\lim_{c\downarrow0}H_c(d)=0,
\qquad
\lim_{c\uparrow\infty}H_c(d)=1-e^{-d}.
\]

Hence there is a unique \(c^*=c^*(d,q^*)\) satisfying

\[
H_{c^*}(d)=q^*.
\]

For every \(\varepsilon>0\), staffing with spare capacity \(c^*-\varepsilon\) is eventually infeasible and staffing with \(c^*+\varepsilon\) is eventually feasible. Thus the minimum integer staffing obeys

\[
M_{\min}(A)=\left\lceil A+c^*+o(1)\right\rceil.
\]

For \(d=4\) and \(q^*=0.95\),

\[
c^*\approx1.4997568.
\]

This is stronger than a first-order offered-load statement: the deadline guarantee requires only a constant spare-capacity margin at large scale.

### Rare-event false-positive corollary

For the fleet,

\[
A_N
=
\frac{\nu_N}{\mu}
=
N\ell[\pi_Nr+(1-\pi_N)f],
\qquad
\ell=\lambda E[S]=\frac{\lambda}{\mu}.
\]

If \(\pi_N\to0\) and \(f>0\) is fixed,

\[
\frac{A_N}{N}\to\ell f.
\]

Since \(M_{\min}(N)=A_N+O(1)\) up to integer rounding,

\[
\frac{M_{\min}(N)}N\to\ell f.
\]

If additionally \(\pi_N=O(1/N)\), then

\[
A_N=N\ell f+O(1),
\]

so the stronger statement holds:

\[
M_{\min}(N)=N\ell f+O(1).
\]

If staffing remains bounded, stability alone requires

\[
\pi_Nr+(1-\pi_N)f_N=O(1/N).
\]

When \(\pi_N=O(1/N)\), this forces \(f_N=O(1/N)\).

---

## Theorem — Distribution-free burst impossibility

Let service times \(S_1,S_2,\ldots\) be iid, strictly positive and nonexplosive. Define the renewal function

\[
U_S(D)
=
\sum_{k\ge1}P(S_1+\cdots+S_k\le D)
=
E[N_S(D)]
<\infty,
\]

where \(N_S(D)\) is the number of completions by time \(D\) from one continuously busy server.

At time zero, let a batch of \(b\) exchangeable jobs arrive to \(M\) initially idle servers. Give every server infinite backlog if necessary. This can only increase the number of service completions by \(D\). Therefore, if \(K_D\) is the number of tagged batch jobs completed by \(D\),

\[
E[K_D]\le M U_S(D).
\]

For a uniformly selected batch job \(J\),

\[
P(T_J\le D)
=
\frac{E[K_D]}b
\le
\min\left(1,\frac{M U_S(D)}b\right).
\]

Now let batches of size \(b\) arrive as a Poisson process of rate

\[
\beta_b=\frac{\bar\nu}{b}.
\]

The mean alert rate is always \(\bar\nu\), so the nominal utilization is always

\[
\rho=\frac{\bar\nu E[S]}{M},
\]

independent of \(b\). Yet the favorable empty-system bound above tends to zero as \(b\to\infty\). Residual backlog from earlier batches can only worsen completion times.

Thus equal average utilization does not imply any positive uniform lower bound on deadline completion, for arbitrary service distributions satisfying \(U_S(D)<\infty\).

For exponential service,

\[
U_S(D)=\mu D,
\]

which recovers the earlier bound

\[
P(T_J\le D)\le \min(1,M\mu D/b).
\]

---

## Proposition — Uncertainty-aware feasibility certificate

Expose the service-rate dependence as \(Q_M(\nu,D;\mu)\). Suppose calibration provides a rectangular uncertainty set

\[
\lambda\in[\lambda^-,\lambda^+],\quad
\pi\in[\pi^-,\pi^+],\quad
r\in[r^-,r^+],\quad
f\in[f^-,f^+],
\]

\[
\mu\in[\mu^-,\mu^+],\quad
D\in[D^-,D^+],\quad
h\ge h^-,\quad
a\ge a^-,
\]

with \(r^-\ge f^+\). The last condition ensures that increasing prevalence increases total referral traffic throughout the uncertainty set.

By the arrival-rate coupling above, \(Q_M\) decreases in \(\nu\). By coupling exponential service requirements, it increases in \(\mu\). It also increases in \(D\). Hence, for each fixed \(r\), the worst case occurs at

\[
\lambda=\lambda^+,\quad
\pi=\pi^+,\quad
f=f^+,\quad
\mu=\mu^-,\quad
D=D^-,\quad
h=h^-,\quad
a=a^-.
\]

Therefore every admissible parameter vector satisfies

\[
C\ge C_{\rm cert},
\]

where

\[
C_{\rm cert}
=
h^-a^-
\min_{r\in[r^-,r^+]}
r\,Q_M\!\left(
N\lambda^+[\pi^+r+(1-\pi^+)f^+],
D^-;\mu^-
\right).
\]

Thus

\[
C_{\rm cert}\ge C_{\min}
\]

is a conservative certificate for the entire uncertainty set. The only remaining optimization is one-dimensional in \(r\), because the Oversight Paradox means the control probability need not be monotone in referral sensitivity.

---

## Corollary — Finite-source conservatism

Suppose each robot has a rate-\(\lambda\) Poisson candidate clock, but candidate arrivals from that robot are suppressed while it has an outstanding referred alert.

Couple this finite-source system with the open model using:

- the same Poisson clocks,
- the same critical/noncritical marks,
- the same referral marks,
- and the same service requirements for every arrival present in both systems.

Every finite-source arrival is then also an arrival in the open system. The open system may contain additional jobs but never fewer. Under FCFS with identical service requirements, these added jobs cannot advance any shared alert's service start or completion.

Hence, sample-path-wise for every shared alert,

\[
T_{\rm finite}\le T_{\rm open},
\]

so

\[
Q_M^{\rm finite}(D)\ge Q_M^{\rm open}(D).
\]

The open-Poisson model is therefore conservative for this common class of finite-source supervisory systems.

---

## Fan-out recovery

Take one operator. Suppose each robot alternates between an autonomous interval \(RST\) and a human interaction interval \(IT\), generating one human request per cycle. The per-robot request rate is

$$
\lambda_{\rm req}=\frac1{RST+IT}
$$

and operator service rate is

$$
\mu=\frac1{IT}.
$$

The queue stability condition is

$$
N\lambda_{\rm req}<\mu.
$$

Rearranging,

$$
N<\frac{RST+IT}{IT}=\frac{RST}{IT}+1=PFO.
$$

This is only a capacity/stability correspondence. The proposed framework does not claim that classical fan-out was intended to provide a deadline guarantee.
