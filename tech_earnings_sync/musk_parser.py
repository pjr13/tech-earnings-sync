import re
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class MuskNewsletter:
    issue_number: int
    title: str
    date_str: str
    content: str
    sections: Dict[str, str]

class MuskNewsletterParser:
    AD_PATTERNS = [
        r"【合作推薦】.*?(?=\n《(?:Tesla|SpaceX|xAI|X|Neuralink|The Boring Company)》|\Z)",
        r"9/\d+～9/\d+ 期間限定優惠.*?(?=\n《|\Z)",
        r"👉 如果有興趣的朋友歡迎參考連結：.*?(?=\n《|\Z)",
    ]

    FOOTER_PATTERNS = [
        r"現在就免費訂閱《馬斯克帝國週報》.*$",
        r"© \d{4}.*548 Market Street.*$",
        r"Unsubscribe.*$",
    ]

    SECTION_HEADERS = [
        "Tesla",
        "SpaceX",
        "xAI / SpaceXAI",
        "SpaceXAI",
        "xAI",
        "X",
        "Neuralink",
        "The Boring Company",
        "馬斯克其他事務"
    ]

    @classmethod
    def clean(cls, raw_text: str) -> str:
        text = raw_text.strip()
        # Remove ads
        for pat in cls.AD_PATTERNS:
            text = re.sub(pat, "", text, flags=re.DOTALL)
        # Remove footers
        for pat in cls.FOOTER_PATTERNS:
            text = re.sub(pat, "", text, flags=re.DOTALL | re.MULTILINE)
        # Normalize whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @classmethod
    def parse(cls, subject: str, raw_body: str) -> MuskNewsletter:
        cleaned = cls.clean(raw_body)
        
        # Extract issue number
        match_issue = re.search(r"#(\d+)", subject)
        issue_no = int(match_issue.group(1)) if match_issue else 0

        # Extract date
        match_date = re.search(r"(\d{4}[/-]\d{2}[/-]\d{2})", subject)
        date_str = match_date.group(1) if match_date else ""

        # Extract sections
        sections = {}
        header_regex = r"《(" + "|".join(re.escape(h) for h in cls.SECTION_HEADERS) + r")》"
        splits = re.split(header_regex, cleaned)
        if len(splits) > 1:
            for i in range(1, len(splits), 2):
                sec_name = splits[i].strip()
                sec_content = splits[i+1].strip() if i+1 < len(splits) else ""
                sections[sec_name] = sec_content

        return MuskNewsletter(
            issue_number=issue_no,
            title=subject,
            date_str=date_str,
            content=cleaned,
            sections=sections
        )
