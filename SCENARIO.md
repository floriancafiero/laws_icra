# Primary robotics scenario: variable-autonomy firefighting and search-and-rescue

## Why this scenario

The paper should use a **neutral multi-robot firefighting / disaster-response scenario** as its primary engineering example.

This is grounded in current literature:

1. Verhagen, Neerincx & Tielman (Frontiers in Robotics and AI, 2024) study meaningful human control using an autonomous firefighting/search-and-rescue robot that identifies morally sensitive situations and allocates those decisions to a human operator. Their experts explicitly identify operator overload as a failure of meaningful human control.
2. Al-Hussaini et al. (ACM THRI 2024/25) experimentally study alerts and task suggestions for human supervisors of multi-robot search-and-rescue missions in disaster-stricken environments. Their simulator uses repeated robot-retasking decisions and a 90 s preferred decision deadline.
3. Current HRI evidence mostly involves small teams. Large-fleet results in this project are therefore **scaling stress tests**, not descriptions of typical present deployments.

Key references:

- Verhagen RS, Neerincx MA, Tielman ML. *Meaningful human control and variable autonomy in human-robot teams for firefighting*. Frontiers in Robotics and AI 11 (2024), 1323980. DOI: 10.3389/frobt.2024.1323980.
- Al-Hussaini S et al. *Assessing the Impact of Alerts on the Human Supervisor's Decision-Making Performance in Multi-Robot Missions*. ACM Transactions on Human-Robot Interaction 14(1), Article 7. DOI: 10.1145/3689828.
- Perkins D et al. *Fan-Out Revisited: The Impact of the Human Element on Scalability of Human Multi-Robot Teams*. ICRA 2025.

## Operational story

A team of semi-autonomous ground robots explores a damaged or burning building.

Robots autonomously handle routine navigation, mapping, exploration, local obstacle avoidance, sensing, and status reporting.

Some situations are designated **oversight-critical** and require timely human review. Examples include:

- conflicting victim/responder safety priorities;
- deciding whether to continue into a rapidly worsening hazard region;
- reallocating robots after a route becomes unsafe or a robot fails;
- uncertain high-consequence classifications that alter mission priorities.

The robot does not know perfectly whether a situation is oversight-critical. A risk/sensitivity classifier produces a score; a threshold determines whether the situation is escalated.

## Why bursts arise naturally

Alerts need not be independent. Common-cause changes can affect many robots together:

- smoke or heat propagation;
- structural changes blocking several routes;
- communication restoration revealing several accumulated contingencies;
- shared localization/sensor degradation;
- newly discovered information changing several task priorities simultaneously.

The scenario therefore supports the distinction between **chronic overload** from average alert traffic and **acute overload** from correlated intervention requests.

## Experimental abstraction

The simulator should expose:

- total candidate-event intensity \(\Lambda\);
- critical-event prevalence \(\pi\);
- detector TPR \(r\);
- detector FPR \(f\);
- alert timestamps and burst statistics;
- operator service-time distribution \(S\);
- intervention deadline \(D\);
- human correctness \(h\);
- intervention enactment success \(a\);
- fleet size \(N\) and operator count \(M\).

Primary outcome:

$$
C=P(\text{timely successful human intervention}\mid Z=1).
$$

## Parameter policy

Do **not** claim one realistic parameter vector.

Use three layers:

1. **Empirical envelope:** current HRI scales and observed timing quantities.
2. **Dimensionless robustness:** sweep \(A,d,c_s,M\).
3. **Scaling stress tests:** scale candidate-event volume by explicit multiples while labeling these as future/large-deployment stress tests.

For structural-capacity simulations, setting \(h=a=1\) is deliberately conservative: any observed loss of EHC is then attributable only to detector misses, nuisance alerts, finite human capacity, and deadlines.
