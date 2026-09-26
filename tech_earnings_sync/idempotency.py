from typing import List
import re
from .models import EarningsReport

class IdempotencyChecker:
    @staticmethod
    def is_quarter_already_present(report: EarningsReport, existing_source_titles: List[str]) -> bool:
        target_quarter = report.quarter
        target_ticker = report.ticker

        for title in existing_source_titles:
            if target_ticker not in title:
                continue

            if target_quarter in title:
                return True

            range_match = re.search(r"\((\d{2}Q[1-4])-(\d{2}Q[1-4])\)", title)
            if range_match:
                start_q, end_q = range_match.groups()
                if IdempotencyChecker._is_quarter_in_range(target_quarter, start_q, end_q):
                    return True

        return False

    @staticmethod
    def _is_quarter_in_range(q: str, start_q: str, end_q: str) -> bool:
        def q_to_int(quarter_str: str) -> int:
            yr = int(quarter_str[:2])
            q_num = int(quarter_str[-1])
            return yr * 4 + q_num

        return q_to_int(start_q) <= q_to_int(q) <= q_to_int(end_q)
