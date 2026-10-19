"""One-command demo: the four review roles in sequence, without an API key, then final-report.pdf.

    python demo.py                      # spreadsheet from the thesis repository (raw link)
    python demo.py --workbook <file>    # local copy of the spreadsheet

Uses the answers recorded in data/recorded/ (no API call, no cost). Needs internet for the thesis spreadsheet
(raw link) and the steel price index; nothing else is downloaded.
"""

import json
import sys
from pathlib import Path

from valuation_gerdau.__main__ import main

REPORTS = Path(__file__).resolve().parent / "output"


def show(name, line):
    print(f"\n=== {name} ===\n{line}")


def summary():
    aud = json.loads((REPORTS / "auditor.json").read_text(encoding="utf-8"))
    ana = json.loads((REPORTS / "second_analyst.json").read_text(encoding="utf-8"))
    lab = json.loads((REPORTS / "lab.json").read_text(encoding="utf-8"))
    rev = json.loads((REPORTS / "reviewer.json").read_text(encoding="utf-8"))
    ok = sum(r["status"] == "match" for r in aud["rows"])
    show(
        "1. Data auditor",
        f"{ok}/{len(aud['rows'])} figures match the earnings releases, each with page and quote; "
        f"golden set {aud['golden']['correct']}/{aud['golden']['cases']}.",
    )
    rec = ana["reconciliation"]
    show(
        "2. Second analyst",
        f"{sum(r['status'] == 'match' for r in rec)}/{len(rec)} lines match raw CVM filings.\n{ana['memo']['summary']}",
    )
    show("3. Econometric lab", lab["summary"]["what_moves_value_most"])
    q = rev["questions"]["questions"][0]
    show("4. Assumption reviewer", f"Top board question: {q['question']}\nNumbers: {q['numbers_for_the_answer']}")


if __name__ == "__main__":
    extra = sys.argv[1:3] if sys.argv[1:2] == ["--workbook"] else []
    code = main(["all", "--demo", *extra])
    if code:
        sys.exit(code)
    main(["final", *extra])
    summary()
    print("\nFull report: final-report.pdf · details: output/*.md")
