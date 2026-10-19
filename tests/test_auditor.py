"""Auditor plumbing: page split, page selection and the anti-hallucination checks."""
from valuation_gerdau import auditor, sources

HTML = (
    "<div>Cover</div><div style='page-break-after:always'></div>"
    "<table><tr><td>Net Sales</td><td>16,822</td><td>67,026</td></tr></table>"
    "<div style='page-break-after: always'></div>"
    "<table><tr><td>Gross Debt</td><td>13,637</td></tr><tr><td>Net Debt</td><td>5,360</td></tr>"
    "<tr><td>Cash, cash equivalents and short-term investments</td><td>8,277</td></tr></table>"
)


def test_pages_split_and_rows_stay_on_one_line(tmp_path):
    p = tmp_path / "doc.htm"
    p.write_text(HTML, encoding="utf-8")
    pages = sources.pages(p)
    assert len(pages) == 3
    assert "Net Sales 16,822 67,026" in pages[1]
    assert {1, 2} <= set(auditor.select_pages(pages))


def _answer(**over):
    base = {"net_revenue": (67026, 2, "Net Sales 16,822 67,026"), "gross_debt": (13637, 3, "Gross Debt 13,637"),
            "net_debt": (5360, 3, "Net Debt 5,360"),
            "cash": (8277, 3, "Cash, cash equivalents and short-term investments 8,277")}
    base.update(over)
    return {"figures": [{"metric": k, "found": True, "value_rs_million": v, "page": pg, "quote": q, "column": "12M"}
                        for k, (v, pg, q) in base.items()]}


def test_check_accepts_a_correct_answer(tmp_path):
    p = tmp_path / "doc.htm"
    p.write_text(HTML, encoding="utf-8")
    pages = sources.pages(p)
    assert auditor.make_check(pages, [1, 2])(_answer()) == []


def test_check_rejects_invented_quote_wrong_page_and_wrong_number(tmp_path):
    p = tmp_path / "doc.htm"
    p.write_text(HTML, encoding="utf-8")
    check = auditor.make_check(sources.pages(p), [1, 2])
    assert any("not on page" in e for e in check(_answer(net_debt=(5360, 3, "Net Debt 5,999"))))
    assert any("was not provided" in e for e in check(_answer(cash=(8277, 1, "Cover"))))
    assert any("not in the quote" in e for e in check(_answer(gross_debt=(9999, 3, "Gross Debt 13,637"))))


def test_billions_in_text_are_accepted():
    assert auditor._number_in_quote(82400, "In 2022, net sales came to R$ 82.4 billion")


def test_golden_scoring():
    rows = [{"fiscal_year": 2024, "metric": "cash", "document": 8277.0},
            {"fiscal_year": 2024, "metric": "net_debt", "document": 9999.0}]
    golden = {"cases": [{"fiscal_year": 2024, "metric": "cash", "value": 8277},
                        {"fiscal_year": 2024, "metric": "net_debt", "value": 5360}]}
    s = auditor.score_against_golden(rows, golden)
    assert s["correct"] == 1 and s["cases"] == 2


def test_label_line_without_number_is_extended_on_the_page(tmp_path):
    html = ("<div>x</div><div style='page-break-after:always'></div>"
            "<p>Cash, cash equivalents and short-term</p><p>investments 5,434 8,590</p>")
    p = tmp_path / "doc.htm"
    p.write_text(html, encoding="utf-8")
    pages = sources.pages(p)
    answer = _answer(cash=(5434, 2, "Cash, cash equivalents and short-term"))
    for f in answer["figures"]:
        if f["metric"] != "cash":
            f["found"] = False
    assert auditor.make_check(pages, [1])(answer) == []
    assert "5,434" in [f for f in answer["figures"] if f["metric"] == "cash"][0]["quote"]
