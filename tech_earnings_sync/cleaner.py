import re

VOCUS_HEADER_PATTERNS = [
    r"^親愛的\s*.*?，你好.*?(?=#[^#\n]+財報)",
    r"^.*?你加入的\s*科技巨頭解碼\s*剛剛發佈了新內容.*?(?=#[^#\n]+財報)",
    r"^.*?邀請你搶先瀏覽熱騰騰的全新創作！.*?(?=#[^#\n]+財報)",
    r"^.*?到\s*vocus\s*瀏覽此篇內容.*?(?=#[^#\n]+財報)",
]

VOCUS_FOOTER_PATTERNS = [
    r"(\n---\s*)?\n*©\s*\d{4}\s*vocus.*$",
    r"(\n---\s*)?\n*退訂電子報.*$",
    r"(\n---\s*)?\n*如果你不想再收到這類郵件.*$",
    r"(\n---\s*)?\n*追蹤作者.*?贊助作者.*$",
    r"(\n---\s*)?\n*本文為【.*?】系列文章，原則上會由.*$",
]

def clean_vocus_email(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = raw_text.strip()

    # Step 1: Strip prefix boilerplate up to main title
    match = re.search(r"(#[^#\n]+(?:財報|思考紀錄)[^\n]*)", text)
    if match:
        text = text[match.start():]
    else:
        for pat in VOCUS_HEADER_PATTERNS:
            text = re.sub(pat, "", text, flags=re.DOTALL | re.IGNORECASE)

    # Step 2: Strip footer boilerplate
    for pat in VOCUS_FOOTER_PATTERNS:
        text = re.sub(pat, "", text, flags=re.DOTALL | re.IGNORECASE)

    # Step 3: Remove tracking parameters in URLs
    text = re.sub(r'(\?|&)(?:utm_[^&)\s]+|token=[^&)\s]+)', '', text)
    text = re.sub(r'\?&', '?', text)
    text = re.sub(r'\?\)', ')', text)

    # Step 4: Normalize consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
