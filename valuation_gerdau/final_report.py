"""final-report.pdf at the repository root: value per date and window, cost of capital before × after,
and what each role found.

Built only from the model and the JSON reports of the last run (no API call). Also writes the README chart.
"""

from __future__ import annotations

import json
import textwrap

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False  # "R$" is currency, not math
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

from . import config  # noqa: E402
from .data import Workbook  # noqa: E402
from .model import DCF, Spec, legacy  # noqa: E402

A4 = (8.27, 11.69)
INK, MUTED, ACCENT = "#1f2937", "#6b7280", "#1d4ed8"
WINDOW_COLORS = {3: "#dc2626", 5: "#1d4ed8", 10: "#059669"}


def _load(name: str) -> dict | None:
    p = config.REPORTS / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def tables(wb: Workbook) -> tuple[pd.DataFrame, pd.DataFrame]:
    m = DCF(wb)
    runs = {w: m.run(Spec(window=w)).set_index("date") for w in (3, 5, 10)}
    old = m.run(legacy(window=5)).set_index("date")
    values = pd.DataFrame({"Price": runs[5]["price"], **{f"{w}y": runs[w]["fair_value"] for w in (3, 5, 10)}})
    wacc = pd.DataFrame(
        {
            "WACC v1 (Ibov − CDI premium, book kd)": old["wacc"],
            "WACC now": runs[5]["wacc"],
            "g": runs[5]["g"],
            "Fair value v1": old["fair_value"],
            "Fair value now": runs[5]["fair_value"],
            "ke now": runs[5]["ke"],
            "kd now": runs[5]["Cost of debt"],
        }
    )
    return values, wacc


def chart(values: pd.DataFrame, ax=None):
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(8, 4.2))
    x = pd.to_datetime(values.index)
    ax.plot(x, values["Price"], color=INK, lw=2.4, marker="o", label="GGBR4 price")
    for w in (3, 5, 10):
        ax.plot(
            x,
            values[f"{w}y"],
            color=WINDOW_COLORS[w],
            lw=1.6,
            ls="--",
            marker="o",
            label=f"Fair value, {w}-year estimation window",
        )
    ax.set_ylabel("R$ per share")
    ax.set_title("Gerdau (GGBR4): price vs DCF fair value by estimation window", fontsize=11, color=INK, loc="left")
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8)
    if own:
        fig.tight_layout()
        return fig


def _text_page(pdf, title: str, blocks: list[tuple[str, str]]):
    fig = plt.figure(figsize=A4)
    fig.text(0.07, 0.95, title, fontsize=15, weight="bold", color=INK, va="top")
    y = 0.90
    for head, body in blocks:
        if y < 0.08:
            break
        fig.text(0.07, y, head, fontsize=10.5, weight="bold", color=ACCENT, va="top")
        y -= 0.025
        for line in textwrap.wrap(body, 100):
            if y < 0.06:
                break
            fig.text(0.07, y, line, fontsize=8.6, color=INK, va="top")
            y -= 0.017
        y -= 0.012
    pdf.savefig(fig)
    plt.close(fig)


def _table(ax, df: pd.DataFrame, fmt):
    ax.axis("off")
    cells = [[fmt(c, v) for c, v in r.items()] for _, r in df.iterrows()]
    t = ax.table(
        cellText=cells, colLabels=list(df.columns), rowLabels=list(df.index), loc="upper left", cellLoc="center"
    )
    t.auto_set_font_size(False)
    t.set_fontsize(7.6)
    t.scale(1, 1.35)


def build(wb: Workbook) -> str:
    values, wacc = tables(wb)
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    config.DOCS.mkdir(exist_ok=True)
    fig = chart(values)
    fig.savefig(config.DOCS / "price_vs_value.png", dpi=160)
    plt.close(fig)

    aud, ana, lab, rev = (_load(n) for n in ("auditor", "second_analyst", "lab", "reviewer"))
    path = config.ROOT / "final-report.pdf"
    with PdfPages(path) as pdf:
        fig = plt.figure(figsize=A4)
        fig.text(
            0.07,
            0.96,
            "Gerdau S.A. (GGBR4): DCF valuation with an AI review layer",
            fontsize=15,
            weight="bold",
            color=INK,
            va="top",
        )
        fig.text(
            0.07,
            0.925,
            "Undergraduate thesis (Economics, UFRJ). Five valuation dates, each using only data public "
            "on that date.\nCost of debt = expected Selic + Baa credit spread.\nCost of equity = rf + beta x mature US "
            "premium + lambda x EMBI+ Brazil.",
            fontsize=8.6,
            color=MUTED,
            va="top",
        )
        chart(values, fig.add_axes([0.09, 0.56, 0.86, 0.3]))
        fig.text(
            0.07, 0.5, "Fair value per share (R$) by estimation window", fontsize=10.5, weight="bold", color=ACCENT
        )
        _table(fig.add_axes([0.2, 0.36, 0.75, 0.13]), values, lambda c, v: f"{v:,.2f}")
        fig.text(
            0.07,
            0.31,
            "Cost of capital, 5-year window: first version × now",
            fontsize=10.5,
            weight="bold",
            color=ACCENT,
        )
        w = wacc.rename(columns={"WACC v1 (Ibov − CDI premium, book kd)": "WACC v1"})
        _table(fig.add_axes([0.2, 0.15, 0.75, 0.15]), w, lambda c, v: f"{v:,.2f}" if "Fair" in c else f"{v:.1%}")
        fig.text(
            0.07,
            0.1,
            "v1: the Ibovespa − CDI premium since 2009 is negative, so the WACC fell below terminal growth "
            "and the\nGordon value became meaningless (negative or exploding). "
            "Now the WACC sits above g at every date.",
            fontsize=8.4,
            color=MUTED,
            va="top",
        )
        pdf.savefig(fig)
        plt.close(fig)

        blocks = []
        if aud:
            rows = aud["rows"]
            ok = sum(r["status"] == "match" for r in rows)
            g = aud["golden"]
            blocks.append(
                (
                    "1. Data auditor",
                    f"{ok} of {len(rows)} spreadsheet figures match Gerdau's 4Q earnings releases "
                    f"(SEC), each with page and quoted line; extraction accuracy against figures checked by hand: "
                    f"{g['correct']}/{g['cases']}.",
                )
            )
        if ana:
            rec = pd.DataFrame(ana["reconciliation"])
            alt = pd.DataFrame(ana["alternatives"])
            chg = alt.dropna(subset=["fair_value_change"]).pivot_table(
                index="variant", columns="date", values="fair_value_change"
            )
            lines = "; ".join(f"{v}: {chg.loc[v].min():+.0%} to {chg.loc[v].max():+.0%}" for v in chg.index)
            blocks.append(
                (
                    "2. Second analyst",
                    f"{(rec['status'] == 'match').sum()} of {len(rec)} spreadsheet lines match "
                    f"raw CVM filings. Changing one choice at a time moves fair value by: {lines}.",
                )
            )
            if ana.get("memo"):
                blocks.append(("   Memo (LLM, Portuguese)", ana["memo"]["summary"]))
        if lab:
            hyp = pd.DataFrame(lab["hypothesis"]).set_index("window")
            h = "; ".join(f"{w}y: " + ", ".join(f"{c} {hyp.loc[w, c]:+.0%}" for c in hyp.columns) for w in hyp.index)
            blocks.append(
                ("3. Econometric lab", f"Mean deviation (value/price − 1) by window and steel-cycle phase: {h}.")
            )
            if lab.get("summary"):
                blocks.append(("   Reading (LLM, Portuguese)", lab["summary"]["what_moves_value_most"]))
        if rev:
            t = pd.DataFrame(rev["tornado"]).head(3)
            top = "; ".join(
                f"{r.assumption}: R$ {r.value_at_low:,.2f} to R$ {r.value_at_high:,.2f}" for r in t.itertuples()
            )
            blocks.append(
                ("4. Assumption reviewer", f"Assumptions that move value the most at the last date (tornado): {top}.")
            )
            if rev.get("questions"):
                for i, q in enumerate(rev["questions"]["questions"][:2], 1):
                    blocks.append(
                        (
                            f"   Board question {i} (LLM, Portuguese)",
                            q["question"] + " Resposta: " + q["suggested_answer"],
                        )
                    )
        blocks.insert(
            0,
            (
                "How to read the LLM text",
                "Every number the model writes is checked against the tables it "
                "received (no invented figures), but a real number can still be paired with the wrong date: "
                "check against the tables in output/*.md. The model never chooses the specification; the author does.",
            ),
        )
        _text_page(pdf, "What each reviewer found", blocks)
    return str(path)
