import unittest
from tech_earnings_sync.parser import EarningsParser

class TestParser(unittest.TestCase):
    def test_parse_pltr_report(self):
        subject = "Miula 發佈了〈PLTR 26Q2 財報 - 超強財報下 | #326 科技巨頭解碼〉"
        raw_body = """親愛的 Ralphy，你好 到 vocus 瀏覽此篇內容

# PLTR 26Q2 財報 - 超強財報下，Palantir 未來還是有硬仗要打 | #326 科技巨頭解碼

### 營收與獲利
在 2026 年第二季，Palantir 營收來到 19.35 億美元。

### 重點數據
本季 Palantir 商業客戶全體營收來到 9.45 億美元。

### 分析師電話會議重點
管理層表示正在加速推進 AIP。

### 針對於 Palantir 2026 第二季財報，Miula 的看法如下 –
1. 商業客戶增長迅猛。

### 結論
長線來看競爭優勢明顯。

### 本期科技巨頭解碼的商業思考
Positive Story:
- 主權 AI 需求強勁。
"""
        report = EarningsParser.parse(subject, raw_body)
        self.assertEqual(report.ticker, "PLTR")
        self.assertEqual(report.quarter, "26Q2")
        self.assertEqual(report.issue_number, 326)
        self.assertIsNotNone(report.revenue_and_profit)
        self.assertIn("19.35 億美元", report.revenue_and_profit)
        self.assertIsNotNone(report.key_metrics)
        self.assertIn("9.45 億美元", report.key_metrics)
        self.assertIsNotNone(report.analyst_call)
        self.assertIsNotNone(report.miula_insights)
        self.assertIsNotNone(report.conclusion)
        self.assertIsNotNone(report.business_thinking)

    def test_unsupported_ticker_raises(self):
        subject = "Miula 發佈了〈XYZ 25Q1 財報〉"
        body = "# XYZ 25Q1 財報"
        with self.assertRaises(ValueError):
            EarningsParser.parse(subject, body)

if __name__ == "__main__":
    unittest.main()
