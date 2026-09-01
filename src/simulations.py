"""Baseline calculations and Monte Carlo experiments for effective human control.

Current values are synthetic. They are intended to test theoretical behavior,
not to estimate a particular real-world system.
"""

import heapq
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "results" / "figures"
TAB = ROOT / "results" / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)
SEED = 20260901


def erlang_c_prob_wait(arrival, mu, m):
    if arrival <= 0:
        return 0.0
    if arrival >= m * mu:
        return 1.0
    x = arrival / mu
    rho = arrival / (m * mu)
    terms = [x**k / math.factorial(k) for k in range(m)]
    tail = (x**m / math.factorial(m)) / (1 - rho)
    return tail / (sum(terms) + tail)


def q_mm_m(arrival, mu, m, deadline):
    """Stationary P(alert completes service before deadline) in an M/M/m queue."""
    if arrival >= m * mu:
        return 0.0
    if arrival <= 0:
        return 1 - math.exp(-mu * deadline)

    p_wait = erlang_c_prob_wait(arrival, mu, m)
    p_no_wait_done = 1 - math.exp(-mu * deadline)
    delta = m * mu - arrival

    if abs(delta - mu) < 1e-10:
        p_wait_done = 1 - math.exp(-mu * deadline) * (1 + mu * deadline)
    else:
        p_wait_done = 1 - (
            mu * math.exp(-delta * deadline)
            - delta * math.exp(-mu * deadline)
        ) / (mu - delta)

    return (1 - p_wait) * p_no_wait_done + p_wait * p_wait_done


def effective_control(N, lam, pi, r, f, M, mu, deadline, h, a):
    alpha = pi * r + (1 - pi) * f
    alert_rate = N * lam * alpha
    return r * h * a * q_mm_m(alert_rate, mu, M, deadline)


def minimum_staffing(N, lam, pi, r, f, mu, deadline, h, a, cmin, max_m=10000):
    ceiling = r * h * a * (1 - math.exp(-mu * deadline))
    if cmin >= ceiling:
        return None
    alert_rate = N * lam * (pi * r + (1 - pi) * f)
    start = max(1, math.floor(alert_rate / mu) + 1)
    for M in range(start, max_m + 1):
        if r * h * a * q_mm_m(alert_rate, mu, M, deadline) >= cmin:
            return M
    return None


def simulate_poisson_queue_q(arrival_rate, mu, M, deadline, n_alerts=60000, seed=1):
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(1 / arrival_rate, size=n_alerts))
    servers = [0.0] * M
    heapq.heapify(servers)
    on_time = 0
    for arrival in arrivals:
        available = heapq.heappop(servers)
        start = max(arrival, available)
        finish = start + rng.exponential(1 / mu)
        heapq.heappush(servers, finish)
        on_time += finish - arrival <= deadline
    return on_time / n_alerts


def simulate_batch_queue(avg_rate, batch_size, mu, M, deadline, n_alerts=50000, seed=1):
    rng = np.random.default_rng(seed)
    n_batches = math.ceil(n_alerts / batch_size)
    batch_rate = avg_rate / batch_size
    batch_times = np.cumsum(rng.exponential(1 / batch_rate, size=n_batches))
    servers = [0.0] * M
    heapq.heapify(servers)
    on_time = total = 0
    for bt in batch_times:
        for _ in range(batch_size):
            if total >= n_alerts:
                break
            available = heapq.heappop(servers)
            start = max(bt, available)
            finish = start + rng.exponential(1 / mu)
            heapq.heappush(servers, finish)
            on_time += finish - bt <= deadline
            total += 1
        if total >= n_alerts:
            break
    return on_time / total


def simulate_priority_queue(policy, arrival_rate=44, mu=12, M=4, n_tasks=30000,
                            p_critical=0.10, seed=1):
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(1 / arrival_rate, size=n_tasks))
    critical = rng.random(n_tasks) < p_critical
    scores = np.where(critical, rng.beta(5, 2, n_tasks), rng.beta(2, 5, n_tasks))
    urgent = rng.random(n_tasks) < np.where(critical, 0.45, 0.20)
    duration = np.where(urgent, 0.10, 0.50)
    deadlines = arrivals + duration
    service = rng.exponential(1 / mu, size=n_tasks)

    completions, waiting = [], []
    idle, idx = M, 0
    on_time = np.zeros(n_tasks, dtype=bool)

    def choose():
        if policy == "FIFO":
            return 0
        if policy == "Earliest deadline":
            return min(range(len(waiting)), key=lambda j: deadlines[waiting[j]])
        if policy == "Risk first":
            return max(range(len(waiting)), key=lambda j: (scores[waiting[j]], -deadlines[waiting[j]]))
        if policy == "Risk/deadline":
            return max(range(len(waiting)), key=lambda j: (scores[waiting[j]] / duration[waiting[j]], scores[waiting[j]]))
        raise ValueError(policy)

    while idx < n_tasks or completions:
        next_arrival = arrivals[idx] if idx < n_tasks else math.inf
        next_completion = completions[0][0] if completions else math.inf

        if next_arrival <= next_completion:
            current = next_arrival
            task = idx
            idx += 1
            if idle > 0:
                idle -= 1
                heapq.heappush(completions, (current + service[task], task))
            else:
                waiting.append(task)
        else:
            current, task = heapq.heappop(completions)
            on_time[task] = current <= deadlines[task]
            if waiting:
                j = choose()
                nxt = waiting.pop(j)
                heapq.heappush(completions, (current + service[nxt], nxt))
            else:
                idle += 1

    return {
        "overall_timely": on_time.mean(),
        "critical_timely": on_time[critical].mean(),
        "urgent_critical_timely": on_time[critical & urgent].mean(),
        "slow_critical_timely": on_time[critical & ~urgent].mean(),
    }


def main():
    P = dict(lam=30, pi=.001, r=.99, f=.005, mu=12, D=.5, h=.98, a=.99, Cmin=.95)

    rows = []
    for M in [4, 6, 8]:
        for N in np.arange(10, 601, 5):
            rows.append({"N": N, "M": M, "EHC": effective_control(N, P["lam"], P["pi"], P["r"], P["f"], M, P["mu"], P["D"], P["h"], P["a"])})
    df1 = pd.DataFrame(rows)
    plt.figure(figsize=(7.5, 5))
    for M in [4, 6, 8]:
        d = df1[df1.M == M]
        plt.plot(d.N, d.EHC, label=f"{M} operators")
    plt.axhline(P["Cmin"], linestyle="--", label="95% target")
    plt.xlabel("Number of autonomous systems"); plt.ylabel("Effective human control probability")
    plt.ylim(0, 1); plt.title("Effective control declines as fleet size approaches human capacity"); plt.legend(); plt.tight_layout()
    plt.savefig(FIG / "figure1_ehc_vs_fleet_size.png", dpi=180); plt.close()

    frontier = []
    for M in range(1, 21):
        feasible = 0
        for N in range(1, 2001):
            if effective_control(N, P["lam"], P["pi"], P["r"], P["f"], M, P["mu"], P["D"], P["h"], P["a"]) >= P["Cmin"]:
                feasible = N
            elif N > feasible + 100:
                break
        frontier.append({"M": M, "N_max": feasible})
    df2 = pd.DataFrame(frontier)
    plt.figure(figsize=(7.5, 5)); plt.plot(df2.M, df2.N_max, marker="o")
    plt.xlabel("Number of human operators"); plt.ylabel("Maximum fleet size at EHC ≥ 95%")
    plt.title("Human-control feasibility frontier"); plt.tight_layout(); plt.savefig(FIG / "figure2_feasibility_frontier.png", dpi=180); plt.close()

    roc = []
    for t in np.linspace(1.5, 4.5, 241):
        f = norm.sf(t); r = norm.sf(t - 4.0)
        rate = 500 * P["lam"] * (P["pi"] * r + (1 - P["pi"]) * f)
        ehc = r * P["h"] * P["a"] * q_mm_m(rate, P["mu"], 10, P["D"])
        roc.append({"threshold": t, "r": r, "f": f, "alert_rate": rate, "EHC": ehc})
    df3 = pd.DataFrame(roc); best = df3.loc[df3.EHC.idxmax()]
    plt.figure(figsize=(7.5, 5)); plt.plot(df3.r, df3.EHC); plt.scatter([best.r], [best.EHC], s=55, label="Best system-level threshold")
    plt.xlabel("Detector sensitivity (true-positive rate)"); plt.ylabel("Effective human control probability"); plt.ylim(0, 1)
    plt.title("Oversight paradox: more sensitive escalation can reduce control"); plt.legend(); plt.tight_layout(); plt.savefig(FIG / "figure3_oversight_paradox.png", dpi=180); plt.close()

    rows = []
    for f in np.linspace(.0001, .02, 80):
        rows.append({"f": f, "M_min": minimum_staffing(1000, P["lam"], P["pi"], P["r"], f, P["mu"], P["D"], P["h"], P["a"], P["Cmin"])})
    df4 = pd.DataFrame(rows)
    plt.figure(figsize=(7.5, 5)); plt.plot(100 * df4.f, df4.M_min)
    plt.xlabel("False-positive rate (%)"); plt.ylabel("Minimum operators for EHC ≥ 95%")
    plt.title("Small false-positive rates become expensive at fleet scale"); plt.tight_layout(); plt.savefig(FIG / "figure4_false_positive_staffing.png", dpi=180); plt.close()

    burst = []
    for b in [1, 2, 5, 10, 20, 50, 100]:
        vals = [simulate_batch_queue(10, b, 12, 5, 1/6, 50000, SEED + 1000*b + rep) for rep in range(5)]
        burst.append({"batch_size": b, "timely_mean": np.mean(vals), "timely_sd": np.std(vals, ddof=1)})
    df5 = pd.DataFrame(burst)
    plt.figure(figsize=(7.5, 5)); plt.errorbar(df5.batch_size, df5.timely_mean, yerr=2 * df5.timely_sd / math.sqrt(5), marker="o", capsize=3)
    plt.xlabel("Alerts arriving in each synchronized burst"); plt.ylabel("Probability alert is processed within 10 minutes"); plt.ylim(0, 1)
    plt.title("Same 10 alerts/hour on average, radically different control"); plt.tight_layout(); plt.savefig(FIG / "figure5_burstiness_same_average_load.png", dpi=180); plt.close()

    policies = ["FIFO", "Earliest deadline", "Risk first", "Risk/deadline"]
    prows = []
    for pol in policies:
        vals = [simulate_priority_queue(pol, seed=SEED + 10000 * policies.index(pol) + rep) for rep in range(6)]
        prows.append({
            "policy": pol,
            "critical_timely_mean": np.mean([v["critical_timely"] for v in vals]),
            "critical_timely_sd": np.std([v["critical_timely"] for v in vals], ddof=1),
            "urgent_critical_mean": np.mean([v["urgent_critical_timely"] for v in vals]),
            "overall_timely_mean": np.mean([v["overall_timely"] for v in vals]),
        })
    df6 = pd.DataFrame(prows)
    plt.figure(figsize=(8, 5)); plt.bar(np.arange(len(df6)), df6.critical_timely_mean)
    plt.xticks(np.arange(len(df6)), df6.policy, rotation=15, ha="right"); plt.ylabel("Critical alerts completed before deadline"); plt.ylim(0, 1)
    plt.title("Capacity-aware prioritization can recover effective control"); plt.tight_layout(); plt.savefig(FIG / "figure6_scheduling_policies.png", dpi=180); plt.close()

    with pd.ExcelWriter(TAB / "part6_simulation_results.xlsx") as writer:
        df1.to_excel(writer, sheet_name="ehc_vs_fleet", index=False)
        df2.to_excel(writer, sheet_name="feasibility_frontier", index=False)
        df3.to_excel(writer, sheet_name="oversight_paradox", index=False)
        df4.to_excel(writer, sheet_name="false_positive_staffing", index=False)
        df5.to_excel(writer, sheet_name="burstiness", index=False)
        df6.to_excel(writer, sheet_name="scheduling", index=False)

    print("Simulation outputs written under results/.")


if __name__ == "__main__":
    main()
