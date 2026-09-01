"""Mission generator for the EHC human-subject pilot.

The pilot isolates two mechanisms:
1) false-positive burden (low/high nuisance alert count)
2) temporal correlation (dispersed/bursty nuisance alerts)

All genuine critical events are escalated in the pilot (TPR=1) so any loss in
effective control is attributable to the human-supervision channel rather than
detector misses. A later study can relax this.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Iterable


ACTIONS = ("ABORT", "REASSIGN", "HOLD", "DISMISS")


@dataclass(frozen=True)
class Condition:
    false_positive_burden: str
    temporal_pattern: str

    @property
    def key(self) -> str:
        return f"{self.false_positive_burden}_{self.temporal_pattern}"


CONDITIONS = (
    Condition("low", "dispersed"),
    Condition("high", "dispersed"),
    Condition("low", "bursty"),
    Condition("high", "bursty"),
)

CONDITION_ORDERS = (
    (0, 1, 3, 2),
    (1, 2, 0, 3),
    (2, 3, 1, 0),
    (3, 0, 2, 1),
)


@dataclass
class AlertEvent:
    event_id: str
    block: int
    scheduled_at_s: float
    robot_id: int
    title: str
    description: str
    is_critical: bool
    correct_action: str
    deadline_s: float
    event_type: str

    def public_dict(self) -> dict:
        data = asdict(self)
        data.pop("is_critical")
        data.pop("correct_action")
        data.pop("event_type")
        return data


@dataclass
class MissionBlock:
    block: int
    condition: Condition
    duration_s: float
    events: list[AlertEvent]

    def to_dict(self, include_ground_truth: bool = True) -> dict:
        return {
            "block": self.block,
            "condition": asdict(self.condition),
            "duration_s": self.duration_s,
            "events": [
                asdict(e) if include_ground_truth else e.public_dict()
                for e in self.events
            ],
        }


def stable_int(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def participant_condition_order(participant_id: str) -> list[Condition]:
    idx = stable_int(participant_id) % len(CONDITION_ORDERS)
    return [CONDITIONS[i] for i in CONDITION_ORDERS[idx]]


CRITICAL_BUILDERS = (
    ("battery_critical", "Battery reserve is below the safe-return threshold.", "ABORT"),
    ("route_blocked", "The assigned route is no longer traversable.", "REASSIGN"),
    ("heat_spike", "Local thermal conditions exceed the safe exposure threshold.", "HOLD"),
    ("victim_priority", "High-confidence victim detection requires immediate resource reallocation.", "REASSIGN"),
    ("communication_loss", "Robot telemetry is stale beyond the supervisory threshold.", "HOLD"),
    ("structural_risk", "Structural risk estimate crossed the stop-and-review threshold.", "HOLD"),
)

NUISANCE_BUILDERS = (
    ("battery_nominal", "Battery fluctuation detected; reserve remains above the safe-return threshold."),
    ("route_uncertain", "Temporary route uncertainty detected; route remains traversable."),
    ("heat_nominal", "Thermal anomaly detected; temperature remains within the safe envelope."),
    ("victim_low_conf", "Possible victim signature detected at low confidence."),
    ("communication_jitter", "Short telemetry delay detected; link remains within the supervisory threshold."),
    ("structure_nominal", "Structural vibration detected below the stop-and-review threshold."),
)


def _critical_event(rng, block, idx, when, deadline_s):
    event_type, description, action = CRITICAL_BUILDERS[idx % len(CRITICAL_BUILDERS)]
    titles = {
        "battery_critical": "Battery safety alert",
        "route_blocked": "Route obstruction",
        "heat_spike": "Thermal hazard",
        "victim_priority": "Victim-priority conflict",
        "communication_loss": "Telemetry loss",
        "structural_risk": "Structural-risk warning",
    }
    return AlertEvent(
        f"B{block}-C{idx+1}", block, when, rng.randint(1, 6),
        titles[event_type], description, True, action, deadline_s, event_type
    )


def _nuisance_event(rng, block, idx, when, deadline_s):
    event_type, description = NUISANCE_BUILDERS[idx % len(NUISANCE_BUILDERS)]
    return AlertEvent(
        f"B{block}-N{idx+1}", block, when, rng.randint(1, 6),
        "Supervisory review requested", description, False, "DISMISS",
        deadline_s, event_type
    )


def _critical_times(rng, duration_s, critical_count):
    margin = min(55.0, max(8.0, duration_s * 0.12))
    start = margin
    end = duration_s - margin
    spacing = (end - start) / max(1, critical_count - 1)
    times = []
    for i in range(critical_count):
        base = start + i * spacing
        jitter = rng.uniform(-0.16 * spacing, 0.16 * spacing)
        times.append(min(end, max(start, base + jitter)))
    return sorted(times)


def _dispersed_nuisance_times(rng, duration_s, nuisance_count, critical_times):
    critical = list(critical_times)
    if nuisance_count == 0:
        return []
    segment = duration_s / nuisance_count
    candidates = []
    for i in range(nuisance_count):
        low = i * segment + 8
        high = min(duration_s - 8, (i + 1) * segment - 8)
        t = min(duration_s - 8, low) if high <= low else rng.uniform(low, high)
        nearest = min(critical, key=lambda c: abs(c - t))
        if abs(nearest - t) < 18:
            t += 24 if t < nearest else -24
            t = min(duration_s - 8, max(8, t))
        candidates.append(t)
    return sorted(candidates)


def _bursty_nuisance_times(rng, duration_s, nuisance_count, critical_times):
    critical = list(critical_times)
    if nuisance_count == 0:
        return []
    times = []
    for i in range(nuisance_count):
        center = critical[i % len(critical)]
        t = center + rng.uniform(-8.0, 8.0)
        times.append(min(duration_s - 3, max(3, t)))
    return sorted(times)


def generate_block(
    participant_id,
    block_number,
    condition,
    *,
    duration_s=480.0,
    critical_count=6,
    low_nuisance_count=6,
    high_nuisance_count=18,
    critical_deadline_s=90.0,
    nuisance_deadline_s=120.0,
):
    seed = stable_int(f"{participant_id}|block={block_number}|scenario=v1")
    rng = random.Random(seed)
    critical_times = _critical_times(rng, duration_s, critical_count)
    nuisance_count = low_nuisance_count if condition.false_positive_burden == "low" else high_nuisance_count
    nuisance_times = (
        _dispersed_nuisance_times(rng, duration_s, nuisance_count, critical_times)
        if condition.temporal_pattern == "dispersed"
        else _bursty_nuisance_times(rng, duration_s, nuisance_count, critical_times)
    )
    events = [
        _critical_event(rng, block_number, i, when, critical_deadline_s)
        for i, when in enumerate(critical_times)
    ]
    events += [
        _nuisance_event(rng, block_number, i, when, nuisance_deadline_s)
        for i, when in enumerate(nuisance_times)
    ]
    events.sort(key=lambda e: (e.scheduled_at_s, e.event_id))
    return MissionBlock(block_number, condition, duration_s, events)


def load_config() -> dict:
    return json.loads(Path(__file__).with_name("config.json").read_text(encoding="utf-8"))


def generate_experiment(participant_id: str, *, demo: bool = False) -> list[MissionBlock]:
    conditions = participant_condition_order(participant_id)
    config = load_config()["demo" if demo else "main"]
    return [
        generate_block(participant_id, i + 1, condition, **config)
        for i, condition in enumerate(conditions)
    ]


def nearest_critical_distance(block: MissionBlock) -> float:
    critical = [e.scheduled_at_s for e in block.events if e.is_critical]
    nuisance = [e.scheduled_at_s for e in block.events if not e.is_critical]
    if not nuisance:
        return math.nan
    distances = [min(abs(t - c) for c in critical) for t in nuisance]
    return sum(distances) / len(distances)
