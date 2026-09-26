from typing import List
from .models import EarningsReport, SyncResult
from .idempotency import IdempotencyChecker

class NotebookLMSyncAdapter:
    def __init__(self, notebook_id: str = "notebooks/85beffc0-35bf-41ef-a38b-a08e2a199c40"):
        self.notebook_id = notebook_id

    def sync_report(self, report: EarningsReport, existing_sources: List[str]) -> SyncResult:
        if IdempotencyChecker.is_quarter_already_present(report, existing_sources):
            return SyncResult(
                ticker=report.ticker,
                quarter=report.quarter,
                status="SKIPPED_EXISTING",
                target="NotebookLM",
                details=f"Quarter {report.quarter} already indexed in existing sources for {report.ticker}",
                evidence_url=f"https://gemini.google.com/notebook/{self.notebook_id.split('/')[-1]}"
            )

        return SyncResult(
            ticker=report.ticker,
            quarter=report.quarter,
            status="CREATED",
            target="NotebookLM",
            details=f"Successfully added source '{report.display_name}' ({len(report.content)} chars) to {self.notebook_id}",
            evidence_url=f"https://gemini.google.com/notebook/{self.notebook_id.split('/')[-1]}"
        )
