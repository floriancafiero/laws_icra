"""Headless checks for the pilot manipulation."""

from mission import CONDITIONS, generate_experiment, nearest_critical_distance


def validate_participant(participant_id: str = "pilot-001", demo: bool = False) -> dict:
    blocks = generate_experiment(participant_id, demo=demo)
    assert len(blocks) == 4
    assert {b.condition.key for b in blocks} == {c.key for c in CONDITIONS}

    summary = {}
    for block in blocks:
        critical = [e for e in block.events if e.is_critical]
        nuisance = [e for e in block.events if not e.is_critical]
        assert all(e.correct_action != "DISMISS" for e in critical)
        assert all(e.correct_action == "DISMISS" for e in nuisance)
        assert all(0 <= e.scheduled_at_s <= block.duration_s for e in block.events)
        assert len({e.event_id for e in block.events}) == len(block.events)
        summary[block.condition.key] = {
            "critical": len(critical),
            "nuisance": len(nuisance),
            "mean_nearest_critical_distance_s": nearest_critical_distance(block),
        }

    assert summary["low_dispersed"]["nuisance"] == summary["low_bursty"]["nuisance"]
    assert summary["high_dispersed"]["nuisance"] == summary["high_bursty"]["nuisance"]
    assert summary["high_dispersed"]["nuisance"] > summary["low_dispersed"]["nuisance"]
    assert summary["low_bursty"]["mean_nearest_critical_distance_s"] < summary["low_dispersed"]["mean_nearest_critical_distance_s"]
    assert summary["high_bursty"]["mean_nearest_critical_distance_s"] < summary["high_dispersed"]["mean_nearest_critical_distance_s"]
    return summary


if __name__ == "__main__":
    for key, row in validate_participant().items():
        print(key, row)
