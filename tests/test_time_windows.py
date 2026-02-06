import unittest
from datetime import date
from pathlib import Path
import sys

SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from report_automation.time_windows import month_window, previous_month_window


class TestTimeWindows(unittest.TestCase):
    def test_month_window(self):
        window = month_window(date(2025, 2, 5))
        self.assertEqual(window.start, date(2025, 2, 1))
        self.assertEqual(window.end, date(2025, 3, 1))

    def test_previous_month_window(self):
        window = previous_month_window(date(2025, 1, 10))
        self.assertEqual(window.start, date(2024, 12, 1))
        self.assertEqual(window.end, date(2025, 1, 1))


if __name__ == "__main__":
    unittest.main()
