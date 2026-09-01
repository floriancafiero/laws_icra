"""Empirically anchored robustness scenarios for the EHC model.

This script deliberately separates:
  * values observed in recent HRI/autonomy studies,
  * values derived from those observations,
  * scenario parameters that are not empirically identified.

Run from the repository root:
    python src/calibrated_scenarios.py
"""

import heapq
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from simulations import q_mm_m

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260901


def fanout_special_case():
    """Recover ICRA-2025 potential fan-out from queue stability."""
    interaction_s = 4.56
    rows = []
    for condition, rst_s in [("high_RST", 23.41), ("low_RST", 11.30)]:
        cycle_s = rst_s + interaction_s
        request_rate_h = 3600.0 / cycle_s
        service_rate_h = 3600.0 / interaction_s
        rows.append(
            {
                "condition": condition,
                "RST_mean_s": rst_s,
                "IT_mean_s": interaction_s,
                "interaction_cycle_s": cycle_s,
                "request_rate_per_robot_h": request_rate_h,
                "operator_service_rate_h": service_rate_h,
                "capacity_ratio": service_rate_h / request_rate_h,
            }
        )
    return pd.DataFrame(rows)


def deliberative_timing_grid():
    """90-s HRI deadline with reported 30-60 team decisions/h.

    Only 21.2 s is an observed mean service-time anchor, and it comes from
    a cross-domain security-inspection task. Other service times are scenarios.
    """
    rows = []
    for rate_h in [30, 45, 60]:
        for service_s in [15, 21.2, 30, 45, 60, 75]:
            mu = 3600.0 / service_s
            rows.append(
                {
                    "team_decision_rate_h": rate_h,
                    "mean_service_s": service_s,
                    "deadline_s": 90,
                    "utilization": rate_h / mu,
                    "timely_completion_prob": q_mm_m(rate_h, mu, 1, 90 / 3600.0),
                    "service_anchor": (
                        "cross-domain observed (security inspection)"
                        if service_s == 21.2
                        else "scenario"
                    ),
                }
            )
    return pd.DataFrame(rows)


def security_detector_anchor():
    """Convert reported confusion counts to our standard TPR/FPR definition."""
    positive = 8627
    negative = 25192
    true_positive = 8288
    false_positive = 4952
    tpr = true_positive / positive
    fpr = false_positive / negative

    # Equal-variance binormal ROC: FPR=sf(t), TPR=sf(t-d').
    threshold = norm.isf(fpr)
    dprime = threshold - norm.isf(tpr)
    return tpr, fpr, dprime


def optimize_binormal_detector(
    candidate_rate_h,
    operators=1,
    service_s=21.2,
    deadline_s=90,
    prevalence=1e-3,
):
    """Composite scaling stress test, not a deployment estimate."""
    _, _, dprime = security_detector_anchor()
    mu = 3600.0 / service_s
    D = deadline_s / 3600.0

    rows = []
    for threshold in np.linspace(-1.5, 5.5, 1401):
        fpr = norm.sf(threshold)
        tpr = norm.sf(threshold - dprime)
        alert_rate = candidate_rate_h * (
            prevalence * tpr + (1 - prevalence) * fpr
        )
        q = q_mm_m(alert_rate, mu, operators, D)
        # Set h=a=1 here to isolate detector/capacity/deadline effects.
        ehc = tpr * q
        rows.append(
            {
                "threshold": threshold,
                "TPR": tpr,
                "FPR": fpr,
                "alert_rate_h": alert_rate,
                "Q": q,
                "EHC_timing_only": ehc,
            }
        )
    df = pd.DataFrame(rows)
    return df.loc[df["EHC_timing_only"].idxmax()]


def detector_scaling_table():
    rows = []
    for scale in [1, 2, 5, 10, 20]:
        for operators in [1, 2, 4]:
            best = optimize_binormal_detector(
                candidate_rate_h=45 * scale, operators=operators
            )
            rows.append(
                {
                    "scale_vs_45_candidate_events_h": scale,
                    "candidate_event_rate_h": 45 * scale,
                    "operators": operators,
                    "TPR": best["TPR"],
                    "FPR": best["FPR"],
                    "alert_rate_h": best["alert_rate_h"],
                    "Q": best["Q"],
                    "EHC_timing_only": best["EHC_timing_only"],
                }
            )
    return pd.DataFrame(rows)


def simulate_batch_queue(
    avg_rate_h,
    batch_size,
    mean_service_s,
    service_cv,
    operators,
    deadline_s,
    n_alerts=50_000,
    seed=1,
):
    """Batch-Poisson arrival simulation with gamma service times."""
    rng = np.random.default_rng(seed)
    n_batches = math.ceil(n_alerts / batch_size)
    batch_rate_h = avg_rate_h / batch_size
    batch_times = np.cumsum(rng.exponential(1 / batch_rate_h, size=n_batches))

    servers = [0.0] * operators
    heapq.heapify(servers)

    mean_service_h = mean_service_s / 3600.0
    if service_cv == 0:
        def sample_service():
            return mean_service_h
    else:
        shape = 1.0 / (service_cv**2)
        scale = mean_service_h / shape

        def sample_service():
            return rng.gamma(shape, scale)

    deadline_h = deadline_s / 3600.0
    on_time = 0
    total = 0

    for batch_time in batch_times:
        for _ in range(batch_size):
            if total >= n_alerts:
                break
            available = heapq.heappop(servers)
            start = max(batch_time, available)
            finish = start + sample_service()
            heapq.heappush(servers, finish)
            on_time += finish - batch_time <= deadline_h
            total += 1
        if total >= n_alerts:
            break

    return on_time / total


def burst_robustness_table():
    rows = []
    for operators in [1, 2, 3, 4]:
        for batch_size in [1, 2, 4, 8, 12]:
            values = [
                simulate_batch_queue(
                    avg_rate_h=45,
                    batch_size=batch_size,
                    mean_service_s=21.2,
                    service_cv=1.0,
                    operators=operators,
                    deadline_s=90,
                    seed=SEED + 100 * operators + 10 * batch_size + rep,
                )
                for rep in range(5)
            ]
            rows.append(
                {
                    "operators": operators,
                    "batch_size": batch_size,
                    "avg_alert_rate_h": 45,
                    "mean_service_s": 21.2,
                    "deadline_s": 90,
                    "timely_prob_mean": np.mean(values),
                    "timely_prob_sd": np.std(values, ddof=1),
                }
            )
    return pd.DataFrame(rows)


def service_distribution_robustness():
    """Check that burst effect is not an artifact of exponential service."""
    rows = []
    for cv in [0.0, 0.67, 1.0, 1.5]:
        for batch_size in [1, 4, 8]:
            values = [
                simulate_batch_queue(
                    avg_rate_h=45,
                    batch_size=batch_size,
                    mean_service_s=21.2,
                    service_cv=cv,
                    operators=2,
                    deadline_s=90,
                    seed=SEED + int(cv * 1000) + 10 * batch_size + rep,
                )
                for rep in range(5)
            ]
            rows.append(
                {
                    "service_cv": cv,
                    "batch_size": batch_size,
                    "timely_prob": np.mean(values),
                }
            )
    return pd.DataFrame(rows)


def main():
    fanout_special_case().to_csv(OUT / "calibrated_fanout.csv", index=False)
    deliberative_timing_grid().to_csv(
        OUT / "calibrated_deliberative_timing.csv", index=False
    )
    detector_scaling_table().to_csv(
        OUT / "calibrated_detector_scaling.csv", index=False
    )
    burst_robustness_table().to_csv(
        OUT / "calibrated_burst_robustness.csv", index=False
    )
    service_distribution_robustness().to_csv(
        OUT / "calibrated_service_distribution.csv", index=False
    )

    tpr, fpr, dprime = security_detector_anchor()
    print(f"Cross-domain detector anchor: TPR={tpr:.4f}, FPR={fpr:.4f}, d'={dprime:.3f}")
    print(fanout_special_case().to_string(index=False))
    print()
    print(burst_robustness_table().to_string(index=False))


if __name__ == "__main__":
    main()
