"""python -m valuation_gerdau [auditor|analyst|lab|reviewer|all|final] [--demo|--live] [--no-llm] [--max-calls N]
[--workbook PATH]"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import auditor, config, cvm, data, final_report, lab, reports, reviewer, second_analyst
from .llm import LLM, BudgetExceeded, NoRecording


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="valuation_gerdau", description=__doc__)
    p.add_argument("role", choices=["auditor", "analyst", "lab", "reviewer", "all", "final"])
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--demo", action="store_true", help="replay recorded answers only (no API call)")
    mode.add_argument("--live", action="store_true", help="require an API key")
    p.add_argument("--no-llm", action="store_true", help="numbers only, no LLM text")
    p.add_argument("--max-calls", type=int, default=config.MAX_CALLS_PER_RUN)
    p.add_argument("--workbook", help="local copy of the thesis spreadsheet instead of the raw link")
    args = p.parse_args(argv)

    cvm.ALLOW_SNAPSHOT = args.demo
    llm = (
        None
        if args.no_llm or args.role == "final"
        else LLM("demo" if args.demo else "live" if args.live else "auto", args.max_calls)
    )

    def info() -> dict:
        if llm:
            return llm.summary()
        return {"mode": "no-llm", "model": "-", "api_calls": 0, "recorded_answers_used": 0, "estimated_cost_usd": 0.0}

    if args.workbook:
        os.environ["GERDAU_XLSX"] = args.workbook
    try:
        wb = data.load()
    except data.WorkbookUnavailable as err:
        print(err, file=sys.stderr)
        return 2
    if args.role == "final":
        print(final_report.build(wb))
        return 0
    roles = ["auditor", "analyst", "lab", "reviewer"] if args.role == "all" else [args.role]
    try:
        for role in roles:
            if role == "auditor":
                if llm is None:
                    print("auditor needs the LLM (it reads the documents); skipped with --no-llm")
                    continue
                rows = auditor.run(llm, wb)
                golden = json.loads((config.GOLDEN / "release_figures.json").read_text(encoding="utf-8"))
                reports.auditor(rows, auditor.score_against_golden(rows, golden), info())
            elif role == "analyst":
                reports.analyst(second_analyst.run(llm, wb), info())
            elif role == "lab":
                reports.lab(lab.run(llm, wb), info())
            elif role == "reviewer":
                reports.reviewer(reviewer.run(llm, wb), info())
            print(f"{role}: reports/{'second_analyst' if role == 'analyst' else role}.md")
    except (NoRecording, BudgetExceeded) as e:
        print(f"stopped: {e}", file=sys.stderr)
        return 2
    finally:
        print(json.dumps(info(), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
