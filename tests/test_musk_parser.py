import unittest
from tech_earnings_sync.musk_parser import MuskNewsletterParser

class TestMuskParser(unittest.TestCase):
    def test_clean_and_parse(self):
        subject = "【馬斯克帝國週報】#103 SPCX 送 TPU 上太空 + 特斯拉電池供應鏈再進一步 | 2026/09/25"
        raw_body = """馬斯克集爭議與尖端人類科技於一身...

【合作推薦】aircolor 圓境磁吸支架藍牙音箱：音質不錯
9/21～9/30 期間限定優惠
👉 如果有興趣的朋友歡迎參考連結： https://shop.labebe.tw/h0kin

《Tesla》
1. Tesla 車內 Grok 串接外部帳戶
2. 美國史上最大電動卡車訂單出爐

《SpaceX》
1. Starlink Gen3 規格曝光

現在就免費訂閱《馬斯克帝國週報》
© 2026 548 Market Street PMB 72296
"""
        newsletter = MuskNewsletterParser.parse(subject, raw_body)
        self.assertEqual(newsletter.issue_number, 103)
        self.assertEqual(newsletter.date_str, "2026/09/25")
        self.assertFalse("【合作推薦】" in newsletter.content)
        self.assertFalse("期間限定優惠" in newsletter.content)
        self.assertFalse("免費訂閱" in newsletter.content)
        self.assertIn("Tesla", newsletter.sections)
        self.assertIn("SpaceX", newsletter.sections)
        self.assertIn("Grok", newsletter.sections["Tesla"])

if __name__ == "__main__":
    unittest.main()
