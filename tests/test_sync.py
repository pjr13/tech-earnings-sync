import unittest
from tech_earnings_sync.models import EarningsReport
from tech_earnings_sync.sync import NotebookLMSyncAdapter

class TestSync(unittest.TestCase):
    def setUp(self):
        self.adapter = NotebookLMSyncAdapter("notebooks/85beffc0-35bf-41ef-a38b-a08e2a199c40")
        self.existing_sources = [
            "PLTR 財報 (25Q1-26Q2)",
            "NVDA 財報 (25Q4-26Q2 最新季度)"
        ]

    def test_sync_skips_when_present(self):
        report = EarningsReport(
            ticker="PLTR",
            quarter="26Q2",
            title="PLTR 26Q2",
            issue_number=326,
            content="content"
        )
        result = self.adapter.sync_report(report, self.existing_sources)
        self.assertEqual(result.status, "SKIPPED_EXISTING")

    def test_sync_creates_when_new(self):
        report = EarningsReport(
            ticker="PLTR",
            quarter="26Q3",
            title="PLTR 26Q3",
            issue_number=335,
            content="content"
        )
        result = self.adapter.sync_report(report, self.existing_sources)
        self.assertEqual(result.status, "CREATED")
        self.assertIn("Successfully added", result.details)

if __name__ == "__main__":
    unittest.main()
