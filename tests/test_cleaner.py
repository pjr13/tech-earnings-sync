import unittest
from tech_earnings_sync.cleaner import clean_vocus_email

class TestCleaner(unittest.TestCase):
    def test_clean_header_and_footer(self):
        raw = """親愛的 Ralphy，你好 你加入的 科技巨頭解碼 剛剛發佈了新內容！
到 vocus 瀏覽此篇內容

# PLTR 26Q2 財報 - 超強財報下，Palantir 未來還是有硬仗要打 | #326 科技巨頭解碼

### 營收與獲利
營收成長 93%。

---
© 2026 vocus
退訂電子報
追蹤作者贊助作者
"""
        cleaned = clean_vocus_email(raw)
        self.assertTrue(cleaned.startswith("# PLTR 26Q2 財報"))
        self.assertTrue("營收成長 93%。" in cleaned)
        self.assertFalse("親愛的 Ralphy" in cleaned)
        self.assertFalse("退訂電子報" in cleaned)
        self.assertFalse("© 2026 vocus" in cleaned)

    def test_clean_tracking_urls(self):
        raw = """# NVDA 25Q4 財報
[點擊此處](https://example.com/article?utm_source=email&utm_campaign=digest&id=123)
"""
        cleaned = clean_vocus_email(raw)
        self.assertFalse("utm_source" in cleaned)
        self.assertTrue("id=123" in cleaned)

if __name__ == "__main__":
    unittest.main()
