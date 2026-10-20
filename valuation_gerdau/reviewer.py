"""Role 4: Assumption reviewer.

For each assumption at each date: the value used, where it sits in Gerdau's own history and the steel
cycle at that date. A tornado measures how much each assumption moves fair value when it goes to the
10th and 90th percentile of Gerdau's history. The LLM then writes the questions an examining board is
likely to ask, each with the numbers for the answer. No comparison with other theses (author's decision).
"""

from __future__ import annotations

import pandas as pd

from . import steel
from .data import Workbook
from .llm import LLM, load_schema, unsupported_numbers
from .model import ASSUMPTIONS, DCF, DEFINITIONS, Spec

BASE = Spec(window=5)
HISTORY_FROM = 2010
# Ranges that do not come from Gerdau's statements: stated as test ranges, not as data.
TEST_RANGES = {
    "Equity risk premium": (0.04, 0.07),
    "Country risk premium": (0.015, 0.04),
    "Credit spread": (0.01, 0.03),
    "Terminal growth": (-0.01, +0.01),
}  # g: ± 1 p.p. around the base


def history_table(wb: Workbook) -> pd.DataFrame:
    m = DCF(wb)
    rows = []
    for _, row in wb.dates.iterrows():
        last = int(row["Último exercício publicado"])
        used = m.value(row, BASE)
        hist = m.ratios.loc[HISTORY_FROM:last]
        for a in ASSUMPTIONS:
            h = hist[a].dropna()
            rows.append(
                {
                    "date": used["date"],
                    "assumption": a,
                    "used": used[a],
                    "hist_min": h.min(),
                    "hist_p10": h.quantile(0.1),
                    "hist_median": h.median(),
                    "hist_p90": h.quantile(0.9),
                    "hist_max": h.max(),
                    "percentile_of_used": float((h < used[a]).mean()),
                    "years": f"{h.index.min()}–{last}",
                }
            )
    return pd.DataFrame(rows)


def tornado(wb: Workbook, date_index: int = -1) -> pd.DataFrame:
    m = DCF(wb)
    row = wb.dates.iloc[date_index]
    base = m.value(row, BASE)
    hist = history_table(wb)
    hist = hist[hist["date"] == base["date"]].set_index("assumption")
    cases = {a: (hist.loc[a, "hist_p10"], hist.loc[a, "hist_p90"], "Gerdau p10–p90") for a in ASSUMPTIONS}
    se = base["beta_se"]
    cases["Beta"] = (base["beta"] - 1.96 * se, base["beta"] + 1.96 * se, "95% interval of the regression")
    for k, label in (
        ("Equity risk premium", "test range 4%–7%"),
        ("Country risk premium", "test range 1.5%–4%"),
        ("Credit spread", "test range 1%–3%"),
    ):
        cases[k] = (*TEST_RANGES[k], label)
    d = TEST_RANGES["Terminal growth"][1]
    cases["Terminal growth"] = (base["g"] - d, base["g"] + d, "test range ± 1 p.p.")
    rows = []
    for a, (low, high, src) in cases.items():
        v_low = m.value(row, BASE.with_overrides(**{a: low}))["fair_value"]
        v_high = m.value(row, BASE.with_overrides(**{a: high}))["fair_value"]
        rows.append(
            {
                "assumption": a,
                "low": low,
                "high": high,
                "range_source": src,
                "value_at_low": v_low,
                "value_at_high": v_high,
                "swing": abs(v_high - v_low),
                "base_value": base["fair_value"],
                "price": base["price"],
                "date": base["date"],
            }
        )
    return pd.DataFrame(rows).sort_values("swing", ascending=False).reset_index(drop=True)


def cycle_table(wb: Workbook, steel_series=None) -> pd.DataFrame:
    s = steel.series() if steel_series is None else steel_series
    return pd.DataFrame(
        [
            {"date": r["Data-base"].date().isoformat(), **steel.at_date(r["Data-base"], s)}
            for _, r in wb.dates.iterrows()
        ]
    )


SYSTEM = (
    "Você prepara um aluno de economia para a banca do TCC (valuation FCFF da Gerdau em 5 datas, "
    "custo da dívida = Selic esperada + spread Baa; ke com prêmio maduro dos EUA + lambda × EMBI). "
    "Gere de 6 a 8 perguntas que a banca "
    "provavelmente fará sobre as PREMISSAS, das mais perigosas para as menos. Para cada uma: a pergunta como "
    "a banca falaria, por que ela é perigosa, os números que respondem (copiados das tabelas) e uma resposta "
    "curta sugerida. Português; cada campo com no máximo 2 frases. Só use números das tabelas. "
    "Não compare com outros TCCs."
)


def questions(llm: LLM, hist: pd.DataFrame, torn: pd.DataFrame, cyc: pd.DataFrame) -> dict:
    h = hist.pivot_table(index="assumption", columns="date", values="used").round(3)
    pct = hist.pivot_table(index="assumption", columns="date", values="percentile_of_used").round(2)
    last = (
        hist[hist["date"] == hist["date"].max()]
        .set_index("assumption")[["hist_min", "hist_p10", "hist_median", "hist_p90", "hist_max", "years"]]
        .round(3)
    )
    t = torn[["assumption", "low", "high", "range_source", "value_at_low", "value_at_high", "swing"]].round(3)
    prompt = (
        DEFINITIONS
        + "\n\n"
        + (
            f"Premissas usadas (janela de 5 anos) por data:\n{h.to_string()}\n\n"
            f"Percentil de cada premissa no histórico da própria Gerdau até a data "
            f"(0 = mínimo, 1 = máximo):\n{pct.to_string()}\n\n"
            f"Histórico da Gerdau até o último exercício:\n{last.to_string()}\n\n"
            f"Tornado na última data ({torn['date'].iloc[0]}; valor base R$ {torn['base_value'].iloc[0]:.2f}, "
            f"preço R$ {torn['price'].iloc[0]:.2f}):\n{t.to_string(index=False)}\n\n"
            f"Ciclo do aço em cada data (PPI de produtos de usina siderúrgica, EUA):\n"
            f"{cyc[['date', 'steel_month', 'steel_yoy', 'steel_vs_10y_avg', 'phase']].round(3).to_string(index=False)}"
        )
    )
    allowed = set(ASSUMPTIONS) | {
        "Beta",
        "Equity risk premium",
        "Country risk premium",
        "Credit spread",
        "Cost of debt",
        "Terminal growth",
        "Janela de estimação",
    }

    def check(a):
        p = [f"unknown assumption: {q['assumption']}" for q in a["questions"] if q["assumption"] not in allowed]
        p += [
            f"question without numbers: {q['question'][:40]}"
            for q in a["questions"]
            if not any(ch.isdigit() for ch in q["numbers_for_the_answer"])
        ]
        p += unsupported_numbers(a, prompt)
        if not 6 <= len(a["questions"]) <= 8:
            p.append(f"expected 6 to 8 questions, got {len(a['questions'])}")
        return p

    schema = load_schema("board_questions")
    schema["properties"]["questions"]["items"]["properties"]["assumption"]["enum"] = sorted(allowed)  # closed list
    return llm.ask("reviewer", SYSTEM, prompt, schema, check=check, max_tokens=2500)


def run(llm: LLM | None, wb: Workbook) -> dict:
    hist = history_table(wb)
    torn = tornado(wb)
    cyc = cycle_table(wb)
    return {
        "history": hist,
        "tornado": torn,
        "cycle": cyc,
        "questions": questions(llm, hist, torn, cyc) if llm else None,
    }
