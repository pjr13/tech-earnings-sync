import unittest
from tech_earnings_sync.models import EarningsReport
from tech_earnings_sync.idempotency import IdempotencyChecker

class TestIdempotency(unittest.TestCase):
    def setUp(self):
        self.existing_sources = [
            "AAPL 財報",
            "AMZN 財報",
            "GOOG 財報",
            "META 財報 (25Q1-26Q2)",
            "MSFT 財報 (25Q1-26Q2)",
            "NVDA 財報 (25Q4-26Q2 最新季度)",
            "PLTR 財報 (25Q1-26Q2)",
            "SPCX 財報",
            "TSLA 財報"
        ]

    def test_existing_quarter_in_range(self):
        report = EarningsReport(
            ticker="PLTR",
            quarter="26Q1",
            title="PLTR 26Q1",
            issue_number=310,
            content=""
        )
        self.assertTrue(IdempotencyChecker.is_quarter_already_present(report, self.existing_sources))

    def test_new_quarter_not_in_range(self):
        report = EarningsReport(
            ticker="PLTR",
            quarter="26Q3",
            title="PLTR 26Q3",
            issue_number=335,
            content=""
        )
        self.assertFalse(IdempotencyChecker.is_quarter_already_present(report, self.existing_sources))

    def test_exact_quarter_match(self):
        report = EarningsReport(
            ticker="NVDA",
            quarter="25Q4",
            title="NVDA 25Q4",
            issue_number=296,
            content=""
        )
        self.assertTrue(IdempotencyChecker.is_quarter_already_present(report, self.existing_sources))

if __name__ == "__main__":
    unittest.main()
