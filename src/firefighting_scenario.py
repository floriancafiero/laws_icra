"""Scaling robustness for the neutral firefighting/search-and-rescue scenario.

The large-volume rows are scaling stress tests. They are not claims about
current deployed firefighting fleets.

Structural capacity runs set h=a=1 so losses arise only from:
detector misses, nuisance alerts, finite human capacity, and deadlines.
"""

import heapq
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260901


def timely_probability_poisson_gamma(
    alert_rate_h,
    mean_service_s=21.2,
    service_cv=1.0,
    operators=1,
    deadline_s=90,
    n_alerts=20000,
    seed=1,
):
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(3600.0 / alert_rate_h, size=n_alerts))

    if service_cv == 0:
        def draw_service():
            return mean_service_s
    else:
        shape = 1.0 / (service_cv**2)
        scale = mean_service_s / shape

        def draw_service():
            return rng.gamma(shape, scale)

    servers = [0.0] * operators
    heapq.heapify(servers)
    successes = 0

    for arrival in arrivals:
        available = heapq.heappop(servers)
        start = max(arrival, available)
        finish = start + draw_service()
        heapq.heappush(servers, finish)
        successes += (finish - arrival) <= deadline_s

    return successes / n_alerts


def scaling_table():
    base_candidate_rate_h = 45
    prevalence = 0.001   # scenario parameter, not empirical estimate
    sensitivity = 0.99   # scenario parameter
    mean_service_s = 21.2  # cross-domain robustness anchor
    service_cv = 1.0
    deadline_s = 90

    rows = []
    for fpr in [0.05, 0.10, 0.20]:
        for scale in [1, 2, 5, 10, 20, 40]:
            candidate_rate_h = base_candidate_rate_h * scale
            alert_rate_h = candidate_rate_h * (
                prevalence * sensitivity + (1 - prevalence) * fpr
            )

            for operators in [1, 2, 4]:
                reps = [
                    timely_probability_poisson_gamma(
                        alert_rate_h=alert_rate_h,
                        mean_service_s=mean_service_s,
                        service_cv=service_cv,
                        operators=operators,
                        deadline_s=deadline_s,
                        seed=SEED + 1000 * int(100 * fpr) + 100 * scale + 10 * operators + rep,
                    )
                    for rep in range(3)
                ]
                q = float(np.mean(reps))
                rho = (
                    alert_rate_h * mean_service_s / 3600.0 / operators
                )

                rows.append(
                    {
                        "prevalence": prevalence,
                        "sensitivity": sensitivity,
                        "FPR": fpr,
                        "scale_vs_45_candidate_events_h": scale,
                        "candidate_event_rate_h": candidate_rate_h,
                        "operators": operators,
                        "alert_rate_h": alert_rate_h,
                        "utilization": rho,
                        "timely_alert_completion_Q": q,
                        "EHC_timing_only": sensitivity * q,
                    }
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = scaling_table()
    df.to_csv(OUT / "firefighting_scaling_stress.csv", index=False)
    print(df.to_string(index=False))
