import unittest
from datetime import date
from pathlib import Path
import sys

SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from report_automation.models import AdsDailyRow
from report_automation.summary import summarize_month


class TestSummary(unittest.TestCase):
    def test_summary_aggregation(self):
        rows = [
            AdsDailyRow(
                date=date(2025, 2, 1),
                platform="meta",
                account_id="acc",
                campaign_id="c1",
                adset_id=None,
                ad_id=None,
                spend=100.0,
                impressions=1000,
                clicks=50,
                conversions=5,
                revenue=300.0,
                client_id="client",
                currency="VND",
            ),
            AdsDailyRow(
                date=date(2025, 2, 2),
                platform="meta",
                account_id="acc",
                campaign_id="c2",
                adset_id=None,
                ad_id=None,
                spend=100.0,
                impressions=1000,
                clicks=50,
                conversions=5,
                revenue=300.0,
                client_id="client",
                currency="VND",
            ),
        ]
        summary = summarize_month(rows, date(2025, 2, 1), "client")
        self.assertEqual(len(summary), 1)
        row = summary[0]
        self.assertEqual(row.spend, 200.0)
        self.assertEqual(row.impressions, 2000)
        self.assertEqual(row.clicks, 100)
        self.assertAlmostEqual(row.ctr, 0.05)
        self.assertAlmostEqual(row.cpc, 2.0)
        self.assertAlmostEqual(row.cpa, 20.0)
        self.assertAlmostEqual(row.roas, 3.0)


if __name__ == "__main__":
    unittest.main()
