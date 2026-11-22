import unittest

from app.metrics import classify_status


class TestMetrics(unittest.TestCase):

    def test_healthy_status(self):
        metrics = {
            "cpu_percent": 40,
            "memory_percent": 50,
            "disk_percent": 60
        }
        self.assertEqual(classify_status(metrics), "HEALTHY")

    def test_warning_status(self):
        metrics = {
            "cpu_percent": 75,
            "memory_percent": 40,
            "disk_percent": 30
        }
        self.assertEqual(classify_status(metrics), "WARNING")

    def test_critical_status(self):
        metrics = {
            "cpu_percent": 90,
            "memory_percent": 40,
            "disk_percent": 30
        }
        self.assertEqual(classify_status(metrics), "CRITICAL")


if __name__ == "__main__":
    unittest.main()