# ICRA mock review — Round 2

Date: 2026-09-02

This review is calibrated against the current six-page ICRA PDF and recent ICRA 2025–2026 papers, with particular attention to formal/simulation-only papers and human-in-the-loop querying work.

## Overall assessment

The manuscript is substantially stronger than the previous version. The main remaining risk is no longer lack of a human study. It is **technical differentiation from prior chance-constrained supervisory queueing, especially Bush (2015), and the absence of an actual capacity-aware supervisory policy or scheduler derived from the framework**.

The paper now looks plausible for ICRA, but still borderline rather than safely accept.

Estimated reviewer distribution if submitted in the current form:

- formal/control reviewer: 5/10 — borderline / weak reject
- HRI reviewer: 6/10 — weak accept / borderline
- multi-robot systems reviewer: 5/10 — borderline / weak reject

Likely meta-review: borderline, with novelty and robotics instantiation determining the decision.

---

## Reviewer A — Formal Methods / Queueing / Safety

**Score: 5/10 (Borderline / Weak Reject)**  
**Confidence: 4/5**

### Strengths

- The central feasibility-frontier formulation is considerably cleaner than the previous collection of separate theorems.
- The end-to-end composition
  [
  C=rhaQ_M(Lambda[pi r+(1-pi)f],D)
  ]
  identifies a real systems-design interaction that is absent from detector-only and fan-out-only metrics.
- The non-monotonic referral result (Oversight Paradox) is the most technically interesting contribution.
- Rare-event false-positive scaling and correlated-demand stress tests are clear and reproducible.
- The manuscript is unusually explicit about what queueing/fan-out results are not claimed as novel.

### Major concern 1 — Bush (2015) is extremely close

Bush already develops a finite-source pooled UAV/operator queue, explicitly replaces expected wait by a **chance constraint on exceeding a maximum wait time**, and uses that probability as a system-effectiveness/design metric.

Therefore the following are not convincing novelty claims on their own:

- pooled multi-server supervisory queueing;
- probabilistic deadline/wait guarantees;
- the claim that average waiting/utilization is not enough;
- a design frontier in fleet/operator/interaction-time space.

The actual novelty is narrower and should be stated even more aggressively:

1. critical-event conditioning;
2. explicit detector/base-rate composition ((pi,r,f));
3. false-referral traffic affecting the shared human channel;
4. referral-threshold/human-capacity co-design;
5. correlated common-cause demand.

At present, several pages still read as if the queueing service-level formulation itself is the contribution.

### Major concern 2 — the strongest new result is not yet strong enough mathematically

Equation (17), the Oversight-Paradox condition, is interesting, but it is a local derivative condition. The paper does not establish:

- existence of an interior EHC-optimal referral point under useful conditions;
- uniqueness;
- how the optimum shifts with (M), (D), or fleet load;
- an algorithmic consequence beyond one-dimensional numerical search.

Figure 4 empirically shows the optimum moving from TPR 0.91 to 0.99 with more operators. A formal result about this capacity-dependent optimum would materially strengthen the paper.

### Major concern 3 — no priority/risk-aware service baseline

All analytical results and most simulations assume FCFS. In a real supervisory system, alerts carrying risk/confidence scores would likely be ranked, deadline-scheduled, or otherwise prioritized.

This matters because the central false-positive argument relies on nuisance alerts delaying true critical alerts. A reviewer can reasonably ask whether a risk-aware scheduler largely eliminates the effect.

A strong revision would compare:

- FCFS;
- earliest-deadline-first;
- static priority by detector/risk score;
- possibly a queue-aware referral threshold.

The claim need not be that priority fails. Showing that it mitigates but does not eliminate the feasibility constraint would be more convincing.

### Minor concerns

- Corollary 1 is correct but too elementary to receive much visual emphasis.
- Proposition 2 is essentially a work-conservation bound. Useful, but not mathematically deep.
- The direct comparison with Bush/Powel is currently categorical (Table I) rather than numerical.

### Recommendation

Borderline. I would become Weak Accept if the authors added either:

1. a stronger theorem around the capacity-dependent referral optimum, or
2. a concrete capacity-aware scheduling/referral policy with convincing comparative evaluation.

---

## Reviewer B — HRI / Human–Multi-Robot Interaction

**Score: 6/10 (Weak Accept / Borderline)**  
**Confidence: 4/5**

### Strengths

- The revised title correctly narrows the claim to capacity guarantees.
- The paper now cites the most relevant recent ICRA querying work and clearly distinguishes “which requests should be made” from “whether a shared human channel can serve the resulting requests.”
- The distinction between nominal intervention availability and effective timed intervention is useful.
- The limitations section is appropriately explicit that (h), (a), and (S) are application-specific.
- No new human study is necessary for the structural claims as currently framed.

### Major concern 1 — the “empirically anchored case study” is not actually a calibration of the proposed arrival model

Al-Hussaini et al. have humans making repeated tasking decisions because robots return mission information. Alerts are **decision support inside those decision instances**, not the exogenous referral process modeled in this paper.

Thus converting 10+ decision instances in 15–20 minutes directly into an alert-service arrival rate is only a timing envelope, not a calibration of (
u).

The section should be renamed to something like:

> Literature-anchored supervisory timing envelope

and should state explicitly that the observed decision cadence is used as an all-review/candidate-demand envelope, not as an estimate of the selective-referral arrival rate.

The source actually reports approximately 10–15 decision instances per mission, with missions taking about 15–20 wall-clock minutes and robot updates every 1–2 minutes. This gives a broader and more precise interpretation than the current “ten or more” wording.

### Major concern 2 — human performance remains workload-independent

The model fixes (h) and treats service-time distributions independently of queue state. Yet the HRI motivation includes overload, attention, trust, and decision quality.

The paper correctly labels this a limitation, but should avoid language suggesting that the simulations themselves establish “effective human control” in a cognitive sense. They establish the **capacity component** of an EHC guarantee.

### Major concern 3 — priority is behaviorally realistic

Operators rarely service warnings FIFO when urgency cues exist. This is both an HRI and systems issue. Risk-aware alert ordering should be included as a robustness baseline if time permits.

### Recommendation

Weak Accept if the case-study language is corrected and the authors resist expanding the human-performance claims. A priority-scheduling robustness result would make this an easier accept.

---

## Reviewer C — Multi-Robot Systems / Robotics

**Score: 5/10 (Borderline / Weak Reject)**  
**Confidence: 3/5**

### Strengths

- The robotics interpretation is now concrete enough to understand.
- The paper uses recent multi-robot supervisory work rather than a purely hypothetical application.
- The common-cause burst argument is particularly relevant to fleets sharing environment, communications, maps, or failure modes.
- The paper is compact and visually clean.

### Major concern 1 — the evaluation is still a queue simulator, not a robot supervisory controller

Recent simulation-only ICRA papers can succeed without physical robots when the theory is instantiated in a recognizable robotics algorithm/controller and compared against competing methods. Here the queueing framework is analyzed directly.

The manuscript does not yet implement:

- a robot task allocator;
- a referral controller;
- a supervisory scheduler;
- a capacity-aware autonomy policy.

Consequently, the same framework could still be transplanted almost unchanged to cybersecurity, medical alarms, or fraud review.

### Major concern 2 — no robotics-facing design baseline

The paper demonstrates that recall-only selection can be suboptimal, but it does not actually propose and benchmark an EHC-aware decision policy.

A simple capacity-aware policy could substantially improve venue fit:

- choose the referral threshold from the current queue state;
- allocate alerts by urgency/risk;
- size the pool or threshold jointly to meet (C_{min}).

Even a simple algorithm, if derived from the frontier and compared with fixed threshold / always-query / FCFS baselines, would turn the paper from “analysis of a problem” into “analysis plus a robotics design method.”

### Major concern 3 — current-scale robotics validation remains thin

The literature-anchored timing figure is useful, but it is not a mission simulation. Large-(N) experiments remain asymptotic stress tests.

### Recommendation

Borderline. I would lean Weak Accept if a capacity-aware supervisory policy were added and evaluated under the existing search-and-rescue event model.

---

## Meta-review

### What is now convincing

The paper has a coherent thesis:

> referral decisions and finite human capacity must be co-designed if a timed human-intervention guarantee is required.

The following parts now work well:

- title and framing;
- recent ICRA related work;
- feasibility-frontier language;
- detector/capacity non-monotonicity;
- rare-event FPR scaling;
- burst robustness;
- careful limitations;
- six-page presentation.

### What still threatens acceptance

The most dangerous reviewer sentence is now:

> “The paper insightfully composes a detector confusion matrix with an existing chance-constrained supervisory queue, but the formal consequences are mostly straightforward and no new supervisory policy is proposed.”

This is more precise than the earlier “where are the robots?” criticism, and harder to answer with more prose.

### Highest-value revision

**Add one capacity-aware mitigation/control policy.**

Preferred option:

1. Alerts retain a detector/risk score.
2. Compare FCFS with a risk-priority scheduler.
3. Optionally make the referral threshold queue-aware.
4. Evaluate EHC, true critical-event misses, alert load, and deadline misses at identical candidate-event processes.
5. Show that the framework predicts when mitigation is enough and when staffing/detector quality must change.

This directly answers both the queueing-novelty and robotics-instantiation reviewers.

### Second-highest-value revision

Strengthen the Oversight-Paradox result into a statement about the **optimal referral point**, not only its local derivative:

- sufficient conditions for an interior optimum;
- or a theorem/empirical law showing how (s^*) shifts with available human capacity.

### Easy corrections that should happen regardless

1. Rename “Empirically anchored multi-robot case study” to “Literature-anchored supervisory timing envelope.”
2. Clarify that Al-Hussaini decision cadence is not an estimate of selective-referral alert rate.
3. Use the source's more precise description: missions last about 15–20 min and contain about 10–15 decision instances; updates arrive every 1–2 min.
4. In Fig. 4, include all synthetic parameters needed to reproduce the ROC experiment, especially pre-escalation load (L) and (h=a=1).
5. Consider changing Fig. 4 y-axis from “Effective human control” to “End-to-end timely-control probability” for the (h=a=1) simulation.
6. If no priority experiment is added, explicitly state that FCFS is a deliberately conservative baseline and that severity-aware service can improve but not invalidate the service-time ceiling.

## Current acceptance estimate

Subjective estimate after this round:

- current PDF: roughly 40–50% acceptance probability;
- after the easy corrections only: roughly 45–55%;
- with a convincing capacity-aware priority/referral policy: plausibly 55–65%.

These are not conference statistics; they are a decision-oriented assessment based on the current manuscript and the recent ICRA papers used for calibration.
