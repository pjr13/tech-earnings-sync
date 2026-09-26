import re
from typing import Optional
from .models import EarningsReport, SUPPORTED_TICKERS
from .cleaner import clean_vocus_email

class EarningsParser:
    @staticmethod
    def identify_ticker(text: str) -> Optional[str]:
        for ticker in SUPPORTED_TICKERS.keys():
            pattern = rf"\b{ticker}\b"
            if re.search(pattern, text, re.IGNORECASE):
                return ticker
        return None

    @staticmethod
    def identify_quarter(text: str) -> Optional[str]:
        match = re.search(r"\b(20\d{2}|\d{2})\s*[Qq]([1-4])\b", text)
        if match:
            year, q = match.groups()
            if len(year) == 4:
                year = year[2:]
            return f"{year}Q{q}"
        return None

    @staticmethod
    def extract_issue_number(text: str) -> Optional[int]:
        match = re.search(r"#(\d+)", text)
        if match:
            return int(match.group(1))
        return None

    @classmethod
    def parse(cls, subject: str, raw_body: str) -> EarningsReport:
        cleaned_body = clean_vocus_email(raw_body)
        combined_header = f"{subject}\n{cleaned_body[:300]}"

        ticker = cls.identify_ticker(combined_header)
        if not ticker:
            raise ValueError(f"Could not identify supported tech ticker in: {subject}")

        quarter = cls.identify_quarter(combined_header)
        if not quarter:
            raise ValueError(f"Could not identify quarter in: {subject}")

        issue_num = cls.extract_issue_number(combined_header)

        first_line = cleaned_body.split("\n", 1)[0]
        title = first_line.lstrip("#").strip() if first_line.startswith("#") else subject

        sections = cls._extract_sections(cleaned_body)

        return EarningsReport(
            ticker=ticker,
            quarter=quarter,
            title=title,
            issue_number=issue_num,
            content=cleaned_body,
            revenue_and_profit=sections.get("revenue_and_profit"),
            key_metrics=sections.get("key_metrics"),
            analyst_call=sections.get("analyst_call"),
            miula_insights=sections.get("miula_insights"),
            conclusion=sections.get("conclusion"),
            business_thinking=sections.get("business_thinking"),
            metadata={"subject": subject, "clean_length": str(len(cleaned_body))}
        )

    @classmethod
    def _extract_sections(cls, text: str) -> dict:
        results = {}
        section_patterns = {
            "revenue_and_profit": r"###\s*\*?(?:營收與獲利|營收獲利)\*?\n(.*?)(?=\n###|\Z)",
            "key_metrics": r"###\s*\*?重點數據\*?\n(.*?)(?=\n###|\Z)",
            "analyst_call": r"###\s*\*?分析師電話會議重點\*?\n(.*?)(?=\n###|\Z)",
            "miula_insights": r"###\s*\*?(?:針對於.*?Miula\s*的看法|Miula\s*觀點).*?\n(.*?)(?=\n###|\Z)",
            "conclusion": r"###\s*\*?結論\*?\n(.*?)(?=\n###|\Z)",
            "business_thinking": r"###\s*\*?本期科技巨頭解碼的商業思考\*?\n(.*?)(?=\n###|\Z)",
        }
        for sec_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                results[sec_name] = match.group(1).strip()
        return results
