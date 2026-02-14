import unittest
from unittest.mock import patch

import sector_tracker


class SectorTrackerTests(unittest.TestCase):
    @patch("sector_tracker.fetch_adjusted_closes")
    def test_compute_5d_performance(self, mock_fetch):
        # 6 candles required; compare last vs 5 trading days ago
        mock_fetch.return_value = [100.0, 101.0, 102.0, 103.0, 104.0, 110.0]
        result = sector_tracker.compute_5d_performance("XLK")
        self.assertEqual(result.ticker, "XLK")
        self.assertAlmostEqual(result.base_close_5d, 100.0)
        self.assertAlmostEqual(result.latest_close, 110.0)
        self.assertAlmostEqual(result.performance_5d_pct, 10.0)


if __name__ == "__main__":
    unittest.main()
