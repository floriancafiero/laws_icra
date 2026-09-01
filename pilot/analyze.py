"""Descriptive pilot analysis.

Usage:
    python pilot/analyze.py pilot/data/*.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def load_logs(paths):
    frames = [pd.read_csv(path) for path in paths]
    if not frames:
        raise ValueError("No log files supplied")
    return pd.concat(frames, ignore_index=True)


def summarize(df):
    responded = df[df["event_status"].isin(["responded", "missed"])]
    critical = responded[responded["is_critical"] == True].copy()
    critical["ehc_success"] = (
        (critical["event_status"] == "responded")
        & (critical["correct"] == True)
        & (critical["timely"] == True)
    )
    by = ["false_positive_burden", "temporal_pattern"]
    return (
        critical.groupby(by, dropna=False)
        .agg(
            critical_events=("event_id", "count"),
            EHC=("ehc_success", "mean"),
            correct_rate=("correct", "mean"),
            timely_rate=("timely", "mean"),
            mean_latency_s=("response_latency_s", "mean"),
            median_latency_s=("response_latency_s", "median"),
            mean_queue_depth=("queue_depth_at_response", "mean"),
        )
        .reset_index()
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="+")
    parser.add_argument("--out", default="pilot/pilot_summary.csv")
    args = parser.parse_args()
    summary = summarize(load_logs(args.logs))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.out, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
