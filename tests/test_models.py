import unittest
from tech_earnings_sync.models import EarningsReport, SyncResult

class TestModels(unittest.TestCase):
    def test_display_name_and_tag(self):
        report = EarningsReport(
            ticker="PLTR",
            quarter="26Q2",
            title="PLTR 26Q2 財報",
            issue_number=326,
            content="sample content"
        )
        self.assertEqual(report.display_name, "PLTR 26Q2 財報")
        self.assertEqual(report.source_tag, "PLTR_26Q2")

    def test_sync_result(self):
        result = SyncResult(
            ticker="NVDA",
            quarter="25Q4",
            status="CREATED",
            target="NotebookLM",
            details="Added successfully"
        )
        self.assertEqual(result.status, "CREATED")
        self.assertEqual(result.ticker, "NVDA")

if __name__ == "__main__":
    unittest.main()
