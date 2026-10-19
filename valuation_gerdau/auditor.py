"""Role 1 — Data auditor.

Reads Gerdau's public 4Q earnings releases and checks the spreadsheet figures against them,
citing document, page and the exact line. Retrieval is plain keyword scoring (no embeddings needed
for ~25 pages); the LLM only reads the selected pages and extracts. Code then verifies that the quote
really is on the cited page and that the number is in the quote, and compares with the spreadsheet.
"""
from __future__ import annotations

import re

from . import sources
from .data import Workbook
from .llm import LLM, load_schema

METRICS = {  # metric -> (spreadsheet column, words that locate it in the release)
    "net_revenue": ("Receita líquida", ["net sales"]),
    "gross_debt": ("Dívida bruta (sem arrendamentos)", ["gross debt"]),
    "net_debt": ("Dívida líquida (sem arrendamentos)", ["net debt"]),
    "cash": ("Caixa e aplicações", ["cash, cash equivalents"]),
}
TOLERANCE = 0.01  # 1%: releases round to R$ million and Gerdau's net debt nets out accrued interest

SYSTEM = (
    "You extract figures from a company's earnings release. Use only the pages provided. "
    "All figures are in R$ million unless the text says billion (then convert to million). "
    "For net_revenue use the full-year figure of the fiscal year (12M column or annual text), never the quarter. "
    "For gross_debt, net_debt and cash use the balance on December 31 of the fiscal year. "
    "quote must be copied character for character from one line of the cited page and must contain the number. "
    "If a figure is not on the pages, set found=false, value_rs_million=0, page=0, quote=''."
)


def select_pages(pages: list[str], max_pages: int = 4) -> list[int]:
    """Indices of the pages with most table lines mentioning a metric next to a number."""
    def score(text: str) -> int:
        s = 0
        for line in text.lower().splitlines():
            if any(w in line for _, ws in METRICS.values() for w in ws) and re.search(r"\d{1,3},\d{3}", line):
                s += 3
            elif any(w in line for _, ws in METRICS.values() for w in ws):
                s += 1
        return s
    ranked = sorted(range(len(pages)), key=lambda i: score(pages[i]), reverse=True)
    return sorted(ranked[:max_pages])


def _number_in_quote(value: float, quote: str) -> bool:
    digits = re.sub(r"\D", "", quote)
    candidates = {str(round(value)), f"{value / 1000:.1f}".replace(".", ""), f"{value / 1000:.2f}".replace(".", "")}
    return any(c and c in digits for c in candidates)


def make_check(pages: list[str], shown: list[int]):
    def check(answer: dict) -> list[str]:
        problems, seen = [], [f["metric"] for f in answer["figures"]]
        for m in METRICS:
            if seen.count(m) != 1:
                problems.append(f"{m}: expected exactly one entry, got {seen.count(m)}")
        for f in answer["figures"]:
            if not f["found"]:
                continue
            if f["page"] - 1 not in shown:
                problems.append(f"{f['metric']}: page {f['page']} was not provided")
                continue
            page = sources.normalise(pages[f["page"] - 1])
            quote = sources.normalise(f["quote"])
            if quote not in page:
                problems.append(f"{f['metric']}: quote is not on page {f['page']}")
                continue
            if not _number_in_quote(f["value_rs_million"], f["quote"]):
                # Table rows are sometimes split over two lines (label, then numbers): extend the quote
                # with what follows it on the same page, and accept only if the number is there.
                start = page.index(quote)
                extended = page[start: start + len(quote) + 80]
                if _number_in_quote(f["value_rs_million"], extended):
                    f["quote"] = extended
                else:
                    problems.append(f"{f['metric']}: value {f['value_rs_million']} is not in the quote; "
                                    "quote the line that contains the number")
        return problems
    return check


def audit_year(llm: LLM, wb: Workbook, year: int) -> list[dict]:
    url = sources.RELEASES[year]
    pages = sources.pages(sources.fetch(url))
    shown = select_pages(pages)
    body = "\n\n".join(f"[page {i + 1}]\n{pages[i]}" for i in shown)
    prompt = (f"Fiscal year: {year}. Extract net_revenue, gross_debt, net_debt and cash "
              f"(one entry each).\n\n{body}")
    answer = llm.ask(f"auditor-{year}", SYSTEM, prompt, load_schema("release_figures"),
                     check=make_check(pages, shown))
    rows = []
    for f in sorted(answer["figures"], key=lambda f: list(METRICS).index(f["metric"])):
        column = METRICS[f["metric"]][0]
        sheet = float(wb.fundamentals.loc[year, column])
        doc = f["value_rs_million"] if f["found"] else None
        diff = None if doc is None else sheet / doc - 1
        rows.append({"fiscal_year": year, "metric": f["metric"], "spreadsheet_column": column,
                     "spreadsheet": round(sheet, 1), "document": doc, "diff": diff,
                     "status": "not found" if doc is None else ("match" if abs(diff) <= TOLERANCE else "CHECK"),
                     "source": url, "page": f["page"], "quote": f["quote"], "column_read": f["column"]})
    return rows


def run(llm: LLM, wb: Workbook, years=None) -> list[dict]:
    years = years or [y for y in sources.RELEASES if y in wb.fundamentals.index]
    return [row for y in years for row in audit_year(llm, wb, y)]


def score_against_golden(rows: list[dict], golden: dict) -> dict:
    """Extraction accuracy against the figures the author read by hand."""
    truth = {(c["fiscal_year"], c["metric"]): c["value"] for c in golden["cases"]}
    hits, misses = 0, []
    for r in rows:
        key = (r["fiscal_year"], r["metric"])
        if key not in truth:
            continue
        if r["document"] is not None and abs(r["document"] / truth[key] - 1) <= 0.005:
            hits += 1
        else:
            misses.append({"case": key, "extracted": r["document"], "expected": truth[key]})
    return {"cases": hits + len(misses), "correct": hits, "misses": misses}
