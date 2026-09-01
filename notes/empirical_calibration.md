# Empirical calibration of the EHC model

Status: working calibration memo, 1 September 2026.

The purpose of this note is **not** to claim that there is one empirically established parameter vector for autonomous weapons or multi-robot supervision. The current literature does not support that. Instead, we identify quantities that have actually been observed in recent HRI/autonomy studies, quantities that can be derived from those observations, and parameters that must remain scenario/sensitivity dimensions.

## 1. Calibration principles

We distinguish three labels:

- **Observed**: directly reported in an empirical study.
- **Derived**: calculated from directly reported quantities.
- **Scenario**: not identified by the literature and therefore varied explicitly.

We also distinguish:

- candidate decision/opportunity rate, \(\Lambda=N\lambda\);
- escalation/alert rate, \(\nu=\Lambda[\pi r+(1-\pi)f]\);
- human service time, \(S\);
- intervention deadline, \(D\).

Many HRI papers report only the aggregate team-level rate \(\Lambda\), not a per-robot \(\lambda\). Empirical analyses should therefore use \(\Lambda\) directly unless the decomposition is actually observed.

## 2. Recent empirical anchors

| Quantity | Empirical anchor | Value | Status | How we use it |
|---|---|---:|---|---|
| Robot team size | Rey-Becerra & Wischniewski, *Ergonomics* 2025/26 review | fixed teams of 2–12 robots in 35 experiments | Observed | current HRI envelope |
| Robot team size | Perkins et al., ICRA 2025 | 4, 6, 8 robots; nobody kept 8 active in the ceiling trials | Observed | fan-out validation |
| Robot self-sufficient time RST | Perkins et al., ICRA 2025 | 23.41 ± 12.10 s (high); 11.30 ± 4.88 s (low) | Observed | fan-out validation |
| Human interaction time IT | Perkins et al., ICRA 2025 | 4.56 ± 3.04 s | Observed | service-time anchor for micro-interactions |
| Military simulation staffing | Andersson et al., IHIET-AI 2025 | 16 UGVs / 5 operators = 3.2 robots/operator | Derived | military simulation reference point, not a normative ratio |
| Team decision opportunities | Al-Hussaini et al., ACM THRI 2024 | 10–15 decision instances in 15–20 min wall-clock | Observed | 30–60 team decisions/hour, derived |
| Retasking deadline | Al-Hussaini et al., ACM THRI 2024 | 90 s preferred decision limit | Observed | deliberative deadline anchor |
| Query interval | Banerjee et al., ICRA 2025 | experimentally varied 1 vs 2 min | Observed design | workload-relevant query-rate anchor |
| Human inspection time | Frontiers in AI 2025 security-inspection study | 21.2 s/image human-only | Observed, cross-domain | medium-complexity human service-time anchor |
| Automated-driving takeover time | Liang et al., *Human Factors* 2026 review | study means 0.69–19.79 s; average mean 2.72 s | Observed synthesis, cross-domain | fast-control time-scale anchor |
| Takeover deadline | Kästle et al., IEEE ToH 2025 | 7 s total takeover window | Observed, cross-domain | fast deadline anchor |

### Sources

- D. Perkins et al., “Fan-Out Revisited: The Impact of the Human Element on Scalability of Human Multi-Robot Teams,” ICRA 2025.
- E. Rey-Becerra & S. Wischniewski, “Mastering a robot workforce…,” *Ergonomics*, 2025 online / 2026 issue, DOI: 10.1080/00140139.2025.2529316.
- S. Al-Hussaini et al., “Assessing the Impact of Alerts on the Human Supervisor’s Decision-Making Performance in Multi-Robot Missions,” *ACM THRI* 14(1), 2024, DOI: 10.1145/3689828.
- C. Andersson, M. Laine & J. Okkonen, defensive UGV simulation, IHIET-AI 2025, DOI: 10.54941/ahfe1005914.
- R. Banerjee et al., “To Ask or Not To Ask…,” ICRA 2025, DOI: 10.1109/ICRA55743.2025.11127795.
- “Application of human-in-the-loop hybrid augmented intelligence approach in security inspection system,” *Frontiers in Artificial Intelligence*, 2025, DOI: 10.3389/frai.2025.1518850.
- K. Liang et al., “Towards Safe and Comfortable Vehicle Control Transitions…,” *Human Factors*, 2026.
- J. L. Kästle et al., “Correlation Between Reaction Time, Multi-Modal Feedback and Take-Over Requests for Level 3 Automated Vehicles,” *IEEE Transactions on Haptics* 18(3), 2025, DOI: 10.1109/TOH.2025.3555842.

## 3. Fan-out as a special case of the queue model

Perkins et al. report

\[
PFO=\frac{RST}{IT}+1.
\]

Using their observed means:

- high RST: \(23.41/4.56+1=6.13\);
- low RST: \(11.30/4.56+1=3.48\).

The queue formulation recovers exactly the same capacity boundary if each robot generates one interaction request per \(RST+IT\) cycle:

\[
\lambda_{req}=\frac{1}{RST+IT},\qquad
\mu=\frac{1}{IT}.
\]

Then the stability condition \(N\lambda_{req}<\mu\) gives

\[
N<\frac{RST+IT}{IT}=\frac{RST}{IT}+1=PFO.
\]

This is useful **validation, not novelty**: our model nests the classic fan-out result and then adds detector errors, hard deadlines, multiple operators, and burst correlation.

## 4. Decision-rate and deadline benchmark

Al-Hussaini et al. report roughly 10–15 supervisor decisions during 15–20 minutes of wall-clock interaction. This corresponds to a team-level candidate decision rate of approximately

\[
\Lambda \approx 30\text{–}60\text{ decisions/hour}.
\]

The same experiment explicitly used a 90 s preferred retasking deadline.

The study does **not** report a universal mean service time for each decision. We therefore do not infer one. In robustness tables we vary mean service time, with 21.2 s included as a cross-domain observed human-inspection anchor.

At a midpoint \(\Lambda=45/h\), \(D=90s\), one operator, and a 21.2 s mean exponential service time, the baseline model gives

\[
Q\approx0.956.
\]

At 30/h it gives \(Q\approx0.970\); at 60/h, \(Q\approx0.936\).

These are **composite benchmarks**, not estimates of the Al-Hussaini participants.

## 5. Detector quality: definition correction

Our model needs the standard conditional false-positive rate

\[
f=P(\text{alert}\mid Z=0).
\]

The 2025 security-inspection paper reports a quantity called “false alarm rate” whose denominator is the set of predicted rejects; that is not the \(f\) used in our equations.

Its confusion counts allow us to derive the standard rates for the machine decision that triggers human review in the clear-priority hybrid:

- actual positives: 8,627;
- actual negatives: 25,192;
- true positives: 8,288;
- false positives: 4,952.

Thus

\[
r=8288/8627\approx0.961,
\]

and

\[
f=4952/25192\approx0.197.
\]

This is **cross-domain** and should not be presented as a robot-alert FPR. It is useful as an empirical discriminability anchor. Under an equal-variance binormal ROC model it corresponds to approximately

\[
d'\approx2.61.
\]

We use that \(d'\) only for a robustness/stress-test ROC, not as a robotics parameter estimate.

## 6. Parameters that are *not* identified

### Critical-event prevalence \(\pi\)

No universal value is defensible. It depends on the mission, environment, definition of “oversight-critical,” and temporal unit. Laboratory studies often manipulate event base rates for experimental power.

Plan: vary \(\pi\) over orders of magnitude, e.g.

\[
10^{-4},10^{-3},10^{-2},10^{-1},
\]

plus domain-specific values when a future application supplies them.

### Human correctness \(h\)

There is no universal probability of making the correct intervention after timely review.

Plan: sensitivity analysis, not point calibration.

### Intervention success \(a\)

Likewise, whether a correct human instruction can still physically alter the system is architecture- and deadline-specific.

Plan: sensitivity analysis.

### Burst-size distribution

Recent multi-robot work explicitly discusses simultaneous/conflicting contingencies, but does not provide a reusable empirical distribution of synchronized alerts.

Plan: treat burst size and correlation as stress-test parameters and report results as such.

## 7. What changes in the paper

The earlier synthetic baseline used fleets of hundreds or thousands. That is useful for asymptotic theory but should **not** be described as typical current HRI practice.

The empirical story should instead be:

1. Current HRI evidence is mainly at small team sizes (roughly 2–12 robots).
2. Our queue model reproduces the established fan-out boundary in that regime.
3. Recent alert-assisted multi-robot experiments already operate with explicit deadlines and repeated decision demands.
4. We then ask the scaling question: if such architectures expand to larger fleets, what detector quality, staffing, and burst resilience are needed to preserve a specified end-to-end control guarantee?
5. Large-fleet experiments are therefore explicitly **scaling stress tests**, not empirical descriptions of present deployments.

## 8. Current robustness findings

Using the empirically anchored 45 candidate decisions/hour, 90 s deadline, and 21.2 s medium-complexity service-time anchor:

- independent arrivals: one operator completes about 95.5% in time;
- same mean rate but batches of 4: about 70.4%;
- batches of 8: about 41.6%;
- batches of 12: about 27.2%.

With two operators the same batch-size-8 case rises to about 81.4%; with four operators to about 97.2%.

This retains the main burst result under time scales drawn from recent human-autonomy studies.

A composite detector-scaling stress test using the cross-domain \(d'\approx2.61\), rare-event prevalence \(\pi=10^{-3}\), fixed one-operator staffing, 21.2 s mean service, and 90 s deadline finds that the EHC-maximizing detector threshold becomes increasingly selective as candidate-event volume grows. The optimized timing-only EHC drops from about 0.97 at 45 candidate events/hour to 0.87 at 450/hour and 0.81 at 900/hour. Adding operators largely restores performance.

Again, this is a **mechanism robustness test**, not an estimate of a weapon or robot deployment.
