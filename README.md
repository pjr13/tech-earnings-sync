# Tech Earnings Sync (科技巨頭財報分析整合)

[![CI Pipeline](https://github.com/ralph-pm/tech-earnings-sync/actions/workflows/ci.yml/badge.svg)](https://github.com/ralph-pm/tech-earnings-sync/actions)

自動化監聽、清洗並同步「科技巨頭解碼」發布之科技巨頭財報分析至 NotebookLM 知識庫與 Google Drive。

## 支援標的 (9 大巨頭)
- **NVDA** (NVIDIA)
- **GOOG** (Alphabet / Google)
- **AAPL** (Apple)
- **TSLA** (Tesla)
- **SPCX** (SpaceX)
- **AMZN** (Amazon)
- **META** (Meta Platforms)
- **MSFT** (Microsoft)
- **PLTR** (Palantir Technologies)

## 功能模組
1. `cleaner.py`: 去除電子報前導歡迎語、贊助、追蹤參數與退訂頁尾雜訊。
2. `parser.py`: 提取 Ticker、Quarter、期數，並結構化切分核心章節（營收與獲利、重點數據、電話會議、Miula 看法、商業思考）。
3. `idempotency.py`: 智慧防重機制（支援單季與季度區間如 `25Q1-26Q2` 檢查）。
4. `sync.py`: NotebookLM 與 Drive 整合介面。

## 測試執行
```bash
make test
# 或
python3 -m unittest discover -s tests -p "test_*.py" -v
```
