import argparse
from .parser import EarningsParser

def main():
    parser = argparse.ArgumentParser(description="Tech Earnings Sync CLI")
    subparsers = parser.add_subparsers(dest="command")

    parse_cmd = subparsers.add_parser("parse", help="Parse and clean an earnings report")
    parse_cmd.add_argument("--subject", required=True, help="Email subject")
    parse_cmd.add_argument("--file", required=True, help="Path to raw email body file")

    args = parser.parse_args()

    if args.command == "parse":
        with open(args.file, "r", encoding="utf-8") as f:
            raw_body = f.read()
        report = EarningsParser.parse(args.subject, raw_body)
        print(f"[OK] Parsed Report:")
        print(f"Ticker: {report.ticker}")
        print(f"Quarter: {report.quarter}")
        print(f"Issue: #{report.issue_number}")
        print(f"Title: {report.title}")
        print(f"Cleaned Body Length: {len(report.content)} chars")

if __name__ == "__main__":
    main()
