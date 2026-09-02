"""ICRA submission evaluation suite.

Regenerates the no-human-experiment figures and raw CSV tables.

Usage:
    python src/icra_evaluation.py

Main axes are dimensionless:
    A = alert_rate * mean_service_time
    d = deadline / mean_service_time
"""

from __future__ import annotations

import heapq
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd
from scipy.stats import norm

from simulations import q_mm_m

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "results" / "figures" / "icra"
TAB = ROOT / "results" / "tables" / "icra"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

SEED = 20260902
TARGET = 0.95

# IEEE single-column figures: generate at final physical width so fonts remain legible.
FIGSIZE = (3.45, 2.45)
plt.rcParams.update({
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
})



def figure_architecture():
    """Black-and-white end-to-end system schematic for the ICRA paper."""
    fig, ax = plt.subplots(figsize=(7.1, 1.75))
    ax.set_xlim(-0.015, 1.015)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x, y, w, h, label, *, dashed=False, fontsize=7.5):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.012,rounding_size=0.015",
            facecolor="white",
            edgecolor="black",
            linewidth=0.9,
            linestyle="--" if dashed else "-",
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fontsize)
        return (x, y, w, h)

    def arrow(x1, y1, x2, y2, label=None, yoff=0.035):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=9, linewidth=0.9, color="black"
        ))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + yoff, label,
                    ha="center", va="bottom", fontsize=6.8)

    b1=box(0.01,0.48,0.12,0.28,"Fleet\n$N$ robots")
    b2=box(0.17,0.48,0.16,0.28,"Candidate situations\n$\\Lambda=N\\lambda$;  $P(Z=1)=\\pi$")
    b3=box(0.37,0.48,0.15,0.28,"Referral mechanism\nTPR $r$; FPR $f$")
    b4=box(0.59,0.48,0.13,0.28,"Human pool\n$M$ operators\nwait $W$, service $S$")
    b5=box(0.77,0.48,0.12,0.28,"Timely review\n$W+S\\leq D$\ncorrectness $h$")
    b6=box(0.93,0.48,0.06,0.28,"Act\n$a$\n$C$")

    arrow(0.13,0.62,0.17,0.62)
    arrow(0.33,0.62,0.37,0.62)
    arrow(0.52,0.62,0.59,0.62)
    arrow(0.72,0.62,0.77,0.62)
    arrow(0.89,0.62,0.93,0.62)

    box(0.39,0.08,0.11,0.20,"Missed critical\n$1-r$",dashed=True,fontsize=7)
    box(0.75,0.08,0.16,0.20,"No timely effective control\n$W+S>D$ or incorrect",dashed=True,fontsize=7)
    arrow(0.445,0.48,0.445,0.28)
    arrow(0.83,0.48,0.83,0.28)

    ax.text(0.555,0.82,"$\\nu=\\Lambda[\\pi r+(1-\\pi)f]$",
            ha="center",va="center",fontsize=8)
    fig.tight_layout(pad=0.15)
    fig.savefig(FIG / "fig0_architecture.pdf")
    fig.savefig(FIG / "fig0_architecture.svg")
    plt.close(fig)

def q_dimless(A: float, M: int, d: float) -> float:
    """M/M/M deadline-completion probability with mean service normalized to 1."""
    return q_mm_m(A, 1.0, M, d)


def max_offered_load(M: int, d: float, target: float = TARGET) -> float:
    """Unique A* satisfying Q_M(A*,d)=target, or NaN if service ceiling fails."""
    if 1.0 - math.exp(-d) <= target:
        return math.nan
    lo, hi = 0.0, M * (1.0 - 1e-10)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if q_dimless(mid, M, d) >= target:
            lo = mid
        else:
            hi = mid
    return lo


def minimum_staffing(
    N: int,
    candidate_load_per_system: float,
    pi: float,
    r: float,
    f: float,
    d: float,
    target: float = TARGET,
    max_m: int = 10000,
):
    """Minimum M in normalized units (mean service = 1)."""
    ceiling = r * (1.0 - math.exp(-d))
    if target >= ceiling:
        return None
    A = N * candidate_load_per_system * (pi * r + (1.0 - pi) * f)
    start = max(1, math.floor(A) + 1)
    for M in range(start, max_m + 1):
        if r * q_dimless(A, M, d) >= target:
            return M
    return None


def figure_feasibility():
    ds = np.linspace(3.01, 8.0, 220)
    rows = []
    for M in [1, 2, 4, 8]:
        for d in ds:
            a_star = max_offered_load(M, d)
            rows.append({"M": M, "d": d, "A_star": a_star, "rho_star": a_star / M})
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fig1_feasibility_frontier.csv", index=False)

    plt.figure(figsize=FIGSIZE)
    for M in [1, 2, 4, 8]:
        sub = df[df["M"] == M]
        plt.plot(sub["d"], sub["rho_star"], label=f"M={M}")
    plt.axhline(1.0, linestyle=":", linewidth=0.8, label="stability")
    plt.xlabel(r"Normalized deadline $d=D/E[S]$")
    plt.ylabel(r"Max. feasible utilization $\rho^*$")
    plt.ylim(0, 1.03)
    plt.legend(ncol=2)
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig1_feasibility_frontier.pdf")
    plt.savefig(FIG / "fig1_feasibility_frontier.svg")
    plt.close()
    return df


def binormal_roc(threshold, dprime):
    f = norm.sf(threshold)
    r = norm.sf(threshold - dprime)
    return r, f


def figure_oversight_paradox():
    pi = 1e-3
    candidate_load = 20.0
    dprime = 3.0
    d = 4.0
    thresholds = np.linspace(-1.0, 6.0, 1401)
    rows = []

    for M in [2, 4, 8]:
        for threshold in thresholds:
            r, f = binormal_roc(threshold, dprime)
            A = candidate_load * (pi * r + (1 - pi) * f)
            C = r * q_dimless(A, M, d)
            rows.append(
                {
                    "M": M,
                    "threshold": threshold,
                    "TPR": r,
                    "FPR": f,
                    "A": A,
                    "EHC": C,
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fig2_oversight_paradox.csv", index=False)

    plt.figure(figsize=FIGSIZE)
    for M in [2, 4, 8]:
        sub = df[df["M"] == M].sort_values("TPR")
        plt.plot(sub["TPR"], sub["EHC"], label=f"M={M}")
        best = sub.loc[sub["EHC"].idxmax()]
        plt.scatter([best["TPR"]], [best["EHC"]], s=28)
    plt.xlabel("Escalation sensitivity / TPR")
    plt.ylabel("Effective human control")
    plt.xlim(0.75, 1.005)
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig2_oversight_paradox.pdf")
    plt.savefig(FIG / "fig2_oversight_paradox.svg")
    plt.close()

    robustness = []
    for dp in [2.0, 3.0, 4.0]:
        for M in [2, 4, 8]:
            best_row = None
            for threshold in thresholds:
                r, f = binormal_roc(threshold, dp)
                A = candidate_load * (pi * r + (1 - pi) * f)
                C = r * q_dimless(A, M, d)
                row = (C, threshold, r, f, A)
                if best_row is None or row[0] > best_row[0]:
                    best_row = row
            robustness.append(
                {
                    "dprime": dp,
                    "M": M,
                    "max_EHC": best_row[0],
                    "threshold": best_row[1],
                    "TPR": best_row[2],
                    "FPR": best_row[3],
                    "A": best_row[4],
                }
            )
    pd.DataFrame(robustness).to_csv(
        TAB / "oversight_optima_robustness.csv", index=False
    )
    return df


def figure_false_positive_scaling():
    ell = 0.2
    pi = 1e-4
    r = 0.99
    d = 4.0
    Ns = np.unique(np.round(np.geomspace(50, 10000, 80)).astype(int))
    rows = []

    for f in [0.001, 0.005, 0.01, 0.02]:
        for N in Ns:
            M = minimum_staffing(N, ell, pi, r, f, d)
            asymptotic = N * ell * f
            rows.append(
                {
                    "N": N,
                    "FPR": f,
                    "M_min": M,
                    "first_order_N_ell_f": asymptotic,
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fig3_false_positive_scaling.csv", index=False)

    plt.figure(figsize=(3.45, 2.55))
    for f in [0.001, 0.005, 0.01, 0.02]:
        sub = df[df["FPR"] == f]
        line, = plt.plot(sub["N"], sub["M_min"], label=f"FPR={100*f:.1f}%")
        plt.plot(
            sub["N"],
            sub["first_order_N_ell_f"],
            linestyle=":",
            linewidth=0.9,
            color=line.get_color(),
        )
    plt.xscale("log")
    plt.xlabel(r"Fleet scale $N$")
    plt.ylabel(r"Minimum operators for $C\geq0.95$")
    plt.legend()
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig3_false_positive_scaling.pdf")
    plt.savefig(FIG / "fig3_false_positive_scaling.svg")
    plt.close()
    return df


def generate_arrivals(process, mean_rate, n, rng):
    if process == "poisson":
        return np.cumsum(rng.exponential(1.0 / mean_rate, size=n))

    if process.startswith("batch"):
        batch = int(process.replace("batch", ""))
        n_batches = math.ceil(n / batch)
        batch_times = np.cumsum(
            rng.exponential(batch / mean_rate, size=n_batches)
        )
        return np.repeat(batch_times, batch)[:n]

    if process == "mmpp":
        # Symmetric two-state MMPP: equal stationary probabilities and
        # low/high rates chosen to preserve the requested long-run mean.
        contrast = 9.0
        low = 2.0 * mean_rate / (1.0 + contrast)
        high = contrast * low
        switch_rate = 0.12
        state = int(rng.random() < 0.5)
        t = 0.0
        out = []
        while len(out) < n:
            rate = high if state else low
            dt_arrival = rng.exponential(1.0 / rate)
            dt_switch = rng.exponential(1.0 / switch_rate)
            if dt_arrival < dt_switch:
                t += dt_arrival
                out.append(t)
            else:
                t += dt_switch
                state = 1 - state
        return np.asarray(out)

    raise ValueError(process)


def sample_service(dist, n, rng, cv=1.0):
    if dist == "deterministic":
        return np.ones(n)
    if dist == "gamma":
        shape = 1.0 / (cv * cv)
        return rng.gamma(shape, 1.0 / shape, size=n)
    if dist == "exponential":
        return rng.exponential(1.0, size=n)
    if dist == "lognormal":
        sigma2 = math.log(1.0 + cv * cv)
        return rng.lognormal(-0.5 * sigma2, math.sqrt(sigma2), size=n)
    raise ValueError(dist)


def simulate_queue(
    process,
    service_dist,
    A,
    M,
    d,
    *,
    service_cv=1.0,
    n=50000,
    warmup=5000,
    seed=1,
):
    """Stationary-like FCFS simulation after discarding a warm-up period."""
    rng = np.random.default_rng(seed)
    total = n + warmup
    arrivals = generate_arrivals(process, A, total, rng)
    services = sample_service(service_dist, total, rng, service_cv)
    servers = [0.0] * M
    heapq.heapify(servers)
    successes = 0

    for idx, (arrival, service) in enumerate(zip(arrivals, services)):
        available = heapq.heappop(servers)
        start = max(arrival, available)
        finish = start + service
        heapq.heappush(servers, finish)
        if idx >= warmup:
            successes += finish - arrival <= d

    return successes / n


def burst_process_results(A=1.2, M=3, d=4.0, reps=5):
    processes = ["poisson", "batch2", "batch4", "batch8", "mmpp"]
    rows = []
    for process in processes:
        vals = [
            simulate_queue(
                process, "gamma", A, M, d,
                service_cv=1.0, seed=SEED + 1000 * i + 13 * j
            )
            for j, i in enumerate(range(reps))
        ]
        rows.append(
            {
                "process": process,
                "A": A,
                "M": M,
                "rho": A / M,
                "d": d,
                "Q_mean": np.mean(vals),
                "Q_sd": np.std(vals, ddof=1),
            }
        )
    return pd.DataFrame(rows)


def figure_burst_same_mean():
    df = burst_process_results()
    df.to_csv(TAB / "fig4_same_mean_burst.csv", index=False)

    x = np.arange(len(df))
    ci = 1.96 * df["Q_sd"] / math.sqrt(5)
    plt.figure(figsize=FIGSIZE)
    plt.bar(x, df["Q_mean"], yerr=ci, capsize=2)
    plt.axhline(TARGET, linestyle="--", linewidth=0.8, label="95% target")
    plt.xticks(x, ["Pois.", "B2", "B4", "B8", "MMPP"])
    plt.ylabel("Deadline completion probability")
    plt.ylim(0, 1)
    plt.legend(loc="lower left")
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig4_same_mean_burst.pdf")
    plt.savefig(FIG / "fig4_same_mean_burst.svg")
    plt.close()
    return df


def figure_general_service_robustness():
    A, M, d = 1.2, 3, 4.0
    specs = [
        ("deterministic", 0.0, "Deterministic"),
        ("gamma", 0.5, "Gamma CV=0.5"),
        ("exponential", 1.0, "Exponential"),
        ("gamma", 1.5, "Gamma CV=1.5"),
        ("lognormal", 1.0, "Lognormal CV=1"),
    ]
    rows = []

    for dist, cv, label in specs:
        for process in ["poisson", "batch4", "batch8"]:
            vals = [
                simulate_queue(
                    process, dist, A, M, d,
                    service_cv=cv, seed=SEED + 2000 * j + len(label)
                )
                for j in range(5)
            ]
            rows.append(
                {
                    "service": label,
                    "process": process,
                    "Q_mean": np.mean(vals),
                    "Q_sd": np.std(vals, ddof=1),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fig5_service_robustness.csv", index=False)

    pivot = df.pivot(index="service", columns="process", values="Q_mean")
    x = np.arange(len(pivot))
    width = 0.24
    plt.figure(figsize=(3.45, 2.7))
    for offset, process in zip([-width, 0, width], ["poisson", "batch4", "batch8"]):
        plt.bar(x + offset, pivot[process], width, label=process)
    plt.xticks(x, pivot.index, rotation=18, ha="right")
    plt.ylabel("P(alert completed before deadline)")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig5_service_robustness.pdf")
    plt.savefig(FIG / "fig5_service_robustness.svg")
    plt.close()
    return df


def counterexample_table():
    rows = []

    A, M, d, r = 1.0, 4, 2.0, 0.99
    C = r * q_dimless(A, M, d)
    rows.append(
        {
            "case": "Low utilization, short deadline",
            "baseline": "rho < 1 and TPR >= 0.95",
            "baseline_verdict": "PASS",
            "rho": A / M,
            "EHC": C,
            "EHC_verdict": "PASS" if C >= TARGET else "FAIL",
            "reason": "Finite service time/deadline ceiling",
        }
    )

    rst, it, N = 23.41, 4.56, 6
    pfo = rst / it + 1.0
    A = N / pfo
    C = q_dimless(A, 1, 4.0)
    rows.append(
        {
            "case": "Near fan-out capacity",
            "baseline": f"N < PFO ({N} < {pfo:.2f})",
            "baseline_verdict": "PASS",
            "rho": A,
            "EHC": C,
            "EHC_verdict": "PASS" if C >= TARGET else "FAIL",
            "reason": "Stability does not imply deadline service",
        }
    )

    dp, L, M, d, pi, target_r = 4.0, 60.0, 4, 4.0, 1e-3, 0.99
    threshold = dp + norm.isf(target_r)
    r, f = binormal_roc(threshold, dp)
    A = L * (pi * r + (1 - pi) * f)
    C = r * q_dimless(A, M, d)
    rows.append(
        {
            "case": "High-recall escalation",
            "baseline": f"TPR={r:.2f}",
            "baseline_verdict": "PASS",
            "rho": A / M,
            "EHC": C,
            "EHC_verdict": "PASS" if C >= TARGET else "FAIL",
            "reason": "Detector-only recall ignores congestion cost",
        }
    )

    vals = [
        simulate_queue(
            "batch8", "gamma", 1.2, 3, 4.0,
            service_cv=1.0, seed=SEED + j
        )
        for j in range(5)
    ]
    C = float(np.mean(vals))
    rows.append(
        {
            "case": "Synchronized alerts",
            "baseline": "rho = 0.40",
            "baseline_verdict": "PASS",
            "rho": 0.40,
            "EHC": C,
            "EHC_verdict": "PASS" if C >= TARGET else "FAIL",
            "reason": "Mean load hides burst/tail risk",
        }
    )

    df = pd.DataFrame(rows)
    df.to_csv(TAB / "counterexample_baselines.csv", index=False)
    return df


def fanout_validation():
    it = 4.56
    rows = []
    for condition, rst in [("high_RST", 23.41), ("low_RST", 11.30)]:
        pfo = rst / it + 1.0
        request_load_per_robot = it / (rst + it)
        queue_capacity = 1.0 / request_load_per_robot
        rows.append(
            {
                "condition": condition,
                "RST_s": rst,
                "IT_s": it,
                "PFO_reported_formula": pfo,
                "queue_stability_capacity": queue_capacity,
                "absolute_difference": abs(pfo - queue_capacity),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fanout_recovery.csv", index=False)
    return df



def exact_simulation_validation():
    """Validate the discrete-event engine against the exact M/M/M result."""
    rows = []
    for A, M, d in [(0.5, 1, 4.0), (1.0, 2, 4.0), (2.5, 4, 4.0), (5.0, 8, 4.0)]:
        vals = [
            simulate_queue(
                "poisson", "exponential", A, M, d,
                n=50000, seed=SEED + 7000 * j + M
            )
            for j in range(5)
        ]
        exact = q_dimless(A, M, d)
        mean = float(np.mean(vals))
        rows.append(
            {
                "A": A,
                "M": M,
                "d": d,
                "exact_Q": exact,
                "MC_Q_mean": mean,
                "MC_Q_sd": float(np.std(vals, ddof=1)),
                "absolute_error": abs(mean - exact),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(TAB / "simulation_exact_validation.csv", index=False)
    return df


def ablation_summary():
    """Compact mechanism checks supporting the main claims."""
    rows = []

    # Deadline ablation at fixed stable utilization.
    A, M = 0.9, 1
    rows.append({
        "ablation": "finite deadline",
        "setting": "A=0.9, M=1, d=4",
        "metric": q_dimless(A, M, 4.0),
    })
    rows.append({
        "ablation": "deadline removed",
        "setting": "A=0.9, M=1, d=infinity",
        "metric": 1.0,
    })

    # False-positive burden at fixed rare-event deployment scale.
    for fpr in [0.0, 0.001, 0.01]:
        rows.append({
            "ablation": "false-positive burden",
            "setting": f"N=10000, FPR={fpr}",
            "metric": minimum_staffing(
                10000, 0.2, 1e-4, 0.99, fpr, 4.0
            ),
        })

    # Arrival correlation at exactly the same mean offered load.
    for process in ["poisson", "batch4", "batch8"]:
        vals = [
            simulate_queue(
                process, "exponential", 1.2, 3, 4.0,
                n=50000, seed=SEED + 9000 * j + len(process)
            )
            for j in range(5)
        ]
        rows.append({
            "ablation": "arrival correlation",
            "setting": f"{process}, A=1.2, M=3, d=4",
            "metric": float(np.mean(vals)),
        })

    # Capacity changes the optimal detector operating point.
    thresholds = np.linspace(-1.0, 6.0, 1401)
    for M in [2, 4, 8]:
        best = (-1.0, None)
        for threshold in thresholds:
            r, fpr = binormal_roc(threshold, 3.0)
            A = 20.0 * (1e-3 * r + (1 - 1e-3) * fpr)
            C = r * q_dimless(A, M, 4.0)
            if C > best[0]:
                best = (C, r)
        rows.append({
            "ablation": "supervisory capacity",
            "setting": f"M={M}, optimal TPR",
            "metric": best[1],
        })

    df = pd.DataFrame(rows)
    df.to_csv(TAB / "ablation_summary.csv", index=False)
    return df

def figure_robotics_case_study():
    """Timing envelope anchored to Al-Hussaini et al.'s mission cadence/deadline."""
    deadline_s = 90.0
    service_s = np.linspace(8.0, 60.0, 220)
    rates = [30, 40, 60]
    rows = []

    plt.figure(figsize=FIGSIZE)
    for rate_h in rates:
        qvals = []
        for mean_s in service_s:
            mu_h = 3600.0 / mean_s
            q = q_mm_m(rate_h, mu_h, 1, deadline_s / 3600.0)
            qvals.append(q)
            rows.append({
                "decision_rate_h": rate_h,
                "mean_service_s": mean_s,
                "deadline_s": deadline_s,
                "Q": q,
                "empirical_status": (
                    "lower-envelope from 10 decisions / 15-20 min"
                    if rate_h in [30, 40]
                    else "denser stress case"
                ),
            })
        label = f"{rate_h}/h" + ("" if rate_h < 60 else " stress")
        plt.plot(service_s, qvals, label=label)

    plt.axhline(TARGET, linestyle="--", linewidth=0.8, label="95% target")
    plt.xlabel("Mean human review time (s)")
    plt.ylabel("Deadline completion probability")
    plt.ylim(0, 1.01)
    plt.legend()
    plt.tight_layout(pad=0.3)
    plt.savefig(FIG / "fig6_robotics_case_study.pdf")
    plt.savefig(FIG / "fig6_robotics_case_study.svg")
    plt.close()

    df = pd.DataFrame(rows)
    df.to_csv(TAB / "fig6_robotics_case_study.csv", index=False)
    return df


def main():
    figure_architecture()
    figure_feasibility()
    figure_oversight_paradox()
    figure_false_positive_scaling()
    figure_burst_same_mean()
    figure_general_service_robustness()
    figure_robotics_case_study()
    counterexample_table()
    fanout_validation()
    exact_simulation_validation()
    ablation_summary()

    print("ICRA evaluation regenerated.")
    print("Figures:", FIG)
    print("Tables:", TAB)
    print()
    print(counterexample_table().to_string(index=False))


if __name__ == "__main__":
    main()
