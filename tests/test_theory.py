import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulations import q_mm_m
from icra_evaluation import max_offered_load


class TheorySanityTests(unittest.TestCase):
    def test_mm1_sojourn_closed_form(self):
        arrival = 0.3
        mu = 1.0
        deadline = 4.0
        expected = 1.0 - math.exp(-(mu - arrival) * deadline)
        self.assertAlmostEqual(
            q_mm_m(arrival, mu, 1, deadline), expected, places=12
        )

    def test_completion_decreases_with_arrival_rate(self):
        vals = [q_mm_m(a, 1.0, 2, 4.0) for a in [0.1, 0.5, 1.0, 1.5]]
        self.assertTrue(all(x > y for x, y in zip(vals, vals[1:])))

    def test_completion_increases_with_staffing(self):
        vals = [q_mm_m(0.8, 1.0, m, 4.0) for m in [1, 2, 3, 4]]
        self.assertTrue(all(x <= y for x, y in zip(vals, vals[1:])))

    def test_service_time_ceiling(self):
        ceiling = 1.0 - math.exp(-4.0)
        for m in [1, 2, 4, 8]:
            for a in [0.1, 0.5]:
                self.assertLessEqual(q_mm_m(a, 1.0, m, 4.0), ceiling + 1e-12)

    def test_feasibility_frontier_known_point(self):
        self.assertAlmostEqual(max_offered_load(4, 4.0), 2.9414259939, places=6)

    def test_fanout_recovery_identity(self):
        rst, it = 23.41, 4.56
        pfo = rst / it + 1.0
        per_robot_offered_load = it / (rst + it)
        queue_capacity = 1.0 / per_robot_offered_load
        self.assertAlmostEqual(pfo, queue_capacity, places=12)


if __name__ == "__main__":
    unittest.main()
