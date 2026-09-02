# Supplementary proof notes

These proofs are written to support the ICRA submission. The main paper should contain concise proof sketches; full details can move to supplementary material.

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

## Theorem — Rare-event false-positive staffing law

Let

$$
\nu_N=N\lambda[\pi_Nr+(1-\pi_N)f].
$$

Because \(\pi_N\to0\) and fixed \(f>0\),

$$
\frac{\nu_N}{N}\to\lambda f.
$$

### Lower bound

Every feasible stationary system requires

$$
M_{\min}(N)\mu>\nu_N.
$$

Therefore

$$
\liminf_{N\to\infty}\frac{M_{\min}(N)}N
\ge
\lim_{N\to\infty}\frac{\nu_N}{N\mu}
=
\frac{\lambda f}{\mu}.
$$

### Upper bound

Fix any utilization level \(\rho_0\in(0,1)\) and choose

$$
\widetilde M_N=
\left\lceil
\frac{\nu_N}{\rho_0\mu}
\right\rceil.
$$

Then the system remains uniformly subcritical. In the many-server limit with fixed utilization \(\rho_0<1\), Erlang-C waiting probability tends to zero. Hence

$$
Q_{\widetilde M_N}(\nu_N,D)
\to
1-e^{-\mu D}.
$$

Since the target is strictly below

$$
rha(1-e^{-\mu D}),
$$

\(\widetilde M_N\) is feasible for all sufficiently large \(N\). Thus

$$
\limsup_{N\to\infty}
\frac{M_{\min}(N)}N
\le
\frac{\lambda f}{\rho_0\mu}.
$$

Because this holds for every \(\rho_0<1\), let \(\rho_0\uparrow1\):

$$
\limsup_{N\to\infty}
\frac{M_{\min}(N)}N
\le
\frac{\lambda f}{\mu}.
$$

The liminf and limsup coincide.

### Fixed-staffing corollary

If \(M\) remains bounded, stability alone requires

$$
N\lambda[\pi_Nr+(1-\pi_N)f_N]=O(1).
$$

Thus

$$
\pi_Nr+(1-\pi_N)f_N=O(1/N).
$$

If additionally \(\pi_N=O(1/N)\), nonnegativity implies \(f_N=O(1/N)\).

---

## Theorem — Average-load insufficiency

At time zero let \(b\) exchangeable jobs arrive to \(M\) initially idle servers. Service times are iid exponential with rate \(\mu\). Give the servers an infinite backlog after the \(b\) tagged jobs if necessary; this can only increase the total number of service completions by time \(D\).

With infinite backlog, each server's completion process is Poisson with rate \(\mu\). Therefore the expected total number of completions by \(D\) is \(M\mu D\).

Let \(K_D\) be the number of tagged batch jobs actually completed by \(D\). Then

$$
E[K_D]\le M\mu D.
$$

Let \(J\) be uniformly sampled from the \(b\) exchangeable batch jobs. Conditional on \(K_D\), exactly \(K_D/b\) of the batch has completed, so

$$
P(T_J\le D)
=
E\left[\frac{K_D}{b}\right]
=
\frac{E[K_D]}b
\le
\frac{M\mu D}{b}.
$$

The probability is trivially at most one, giving

$$
P(T_J\le D)
\le
\min\left(1,\frac{M\mu D}{b}\right).
$$

Now make batch arrival epochs Poisson with rate \(\beta_b=\bar\nu/b\). The long-run mean alert rate is always \(\bar\nu\), hence nominal utilization is always \(\bar\nu/(M\mu)\), independent of \(b\).

Yet the favorable empty-system bound for an alert inside a batch tends to zero as \(b\to\infty\). Residual backlog from previous batches can only worsen completion times. Thus equal average utilization does not imply any positive uniform lower bound on deadline-completion probability.

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
