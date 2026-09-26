from dataclasses import dataclass, field
from typing import List, Optional, Dict

SUPPORTED_TICKERS = {
    "NVDA": "NVIDIA",
    "GOOG": "Alphabet / Google",
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "SPCX": "SpaceX",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "MSFT": "Microsoft",
    "PLTR": "Palantir Technologies",
}

@dataclass
class EarningsReport:
    ticker: str
    quarter: str
    title: str
    issue_number: Optional[int]
    content: str
    revenue_and_profit: Optional[str] = None
    key_metrics: Optional[str] = None
    analyst_call: Optional[str] = None
    miula_insights: Optional[str] = None
    conclusion: Optional[str] = None
    business_thinking: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return f"{self.ticker} {self.quarter} 財報"

    @property
    def source_tag(self) -> str:
        return f"{self.ticker}_{self.quarter}"

@dataclass
class SyncResult:
    ticker: str
    quarter: str
    status: str  # 'CREATED', 'SKIPPED_EXISTING', 'UPDATED', 'FAILED'
    target: str  # 'NotebookLM' or 'GoogleDrive'
    details: str
    evidence_url: Optional[str] = None
