import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pilot"))

from mission import CONDITIONS, generate_experiment, nearest_critical_distance


class MissionTests(unittest.TestCase):
    def test_four_conditions_once(self):
        blocks = generate_experiment("P001")
        self.assertEqual(len(blocks), 4)
        self.assertEqual({b.condition.key for b in blocks}, {c.key for c in CONDITIONS})

    def test_false_positive_manipulation(self):
        blocks = {b.condition.key: b for b in generate_experiment("P001")}
        nuisance = lambda key: sum(not e.is_critical for e in blocks[key].events)
        self.assertEqual(nuisance("low_dispersed"), nuisance("low_bursty"))
        self.assertEqual(nuisance("high_dispersed"), nuisance("high_bursty"))
        self.assertGreater(nuisance("high_dispersed"), nuisance("low_dispersed"))

    def test_burst_manipulation(self):
        for pid in ["P001", "P002", "P003", "P004", "P101"]:
            blocks = {b.condition.key: b for b in generate_experiment(pid)}
            self.assertLess(nearest_critical_distance(blocks["low_bursty"]), nearest_critical_distance(blocks["low_dispersed"]))
            self.assertLess(nearest_critical_distance(blocks["high_bursty"]), nearest_critical_distance(blocks["high_dispersed"]))

    def test_demo_mode(self):
        blocks = generate_experiment("P001", demo=True)
        self.assertTrue(all(b.duration_s == 90 for b in blocks))


if __name__ == "__main__":
    unittest.main()
