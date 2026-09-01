"""Utilities for an EHC performance-based certification calculation."""

from pathlib import Path

import pandas as pd
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
OUT.mkdir(parents=True, exist_ok=True)


def clopper_pearson_lower(successes: int, total: int, confidence: float = 0.95) -> float:
    """One-sided exact binomial lower confidence bound."""
    if not (0 <= successes <= total):
        raise ValueError("Require 0 <= successes <= total")
    if total <= 0:
        raise ValueError("total must be positive")
    if successes == 0:
        return 0.0
    alpha = 1.0 - confidence
    return float(beta.ppf(alpha, successes, total - successes + 1))


def minimum_events(c_min: float, confidence: float, failures: int, max_n: int = 100000):
    """Minimum n such that n-failures successes give lower bound >= c_min."""
    for n in range(failures + 1, max_n + 1):
        successes = n - failures
        if clopper_pearson_lower(successes, n, confidence) >= c_min:
            return n
    return None


def sample_size_table():
    rows = []
    for c_min in [0.90, 0.95, 0.99]:
        for confidence in [0.95, 0.99]:
            for failures in [0, 1, 2, 3]:
                n = minimum_events(c_min, confidence, failures)
                rows.append(
                    {
                        "C_min": c_min,
                        "confidence": confidence,
                        "failures_observed": failures,
                        "minimum_critical_events": n,
                        "successes": n - failures,
                        "one_sided_CP_lower_bound": clopper_pearson_lower(
                            n - failures, n, confidence
                        ),
                    }
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = sample_size_table()
    df.to_csv(OUT / "certification_sample_sizes.csv", index=False)
    print(df.to_string(index=False))
