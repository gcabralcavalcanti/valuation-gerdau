"""Role 2 — Second analyst.

Own code rebuilds the inputs from CVM raw filings (not from the spreadsheet), reconciles them line by
line, then recomputes FCFF and WACC with the choices the raw data allow and the thesis did not make
(interest on debt instead of total financial expense, statutory tax, EBIT without equity income).
The LLM writes the memo; every number in it comes from the tables computed here.
"""
from __future__ import annotations

import json

import pandas as pd

from . import cvm
from .data import Workbook
from .llm import LLM, load_schema, unsupported_numbers
from .model import DEFINITIONS, DCF, Spec

TOL = 0.005
BASE = Spec(window=5)  # thesis model since 19/10: Selic + Baa spread for debt, mature premium + country risk


def reconcile(wb: Workbook, years) -> pd.DataFrame:
    rows = []
    for y in years:
        for line, raw in cvm.year_lines(y).items():
            if line not in wb.fundamentals.columns:
                continue
            sheet = float(wb.fundamentals.loc[y, line])
            diff = raw - sheet
            ok = abs(diff) <= TOL * max(abs(raw), 1.0)
            rows.append({"year": y, "line": line, "cvm_raw": round(raw, 1), "spreadsheet": round(sheet, 1),
                         "diff": round(diff, 1), "status": "match" if ok else "DIFFERS"})
    return pd.DataFrame(rows)


def alternative_specs(wb: Workbook, raw: dict[int, dict]) -> dict[str, callable]:
    """Spec builders per valuation row; each changes one choice, using raw CVM lines."""
    f = DCF(wb).f

    def window_years(row, spec):
        last = int(row["Último exercício publicado"])
        return range(last - spec.window + 1, last + 1)

    def kd_interest(row, spec):
        ys = list(window_years(row, spec))
        debt = f["Dívida bruta (sem arrendamentos)"]
        kd = [raw[y]["Juros sobre dívida (DFC)"] / ((debt[y] + debt[y - 1]) / 2) for y in ys]
        return spec.with_overrides(**{"Cost of debt": sum(kd) / len(kd)})

    def ebit_ex_equity(row, spec):
        ys = list(window_years(row, spec))
        m = [(f.loc[y, "EBIT adjusted"] - raw[y]["Equivalência patrimonial"]) / f.loc[y, "Receita líquida"] for y in ys]
        return spec.with_overrides(**{"EBIT margin": sum(m) / len(m)})

    def statutory(row, spec):
        return Spec(**{**spec.__dict__, "tax": "statutory"})

    def all_three(row, spec):
        s = statutory(row, spec)
        s = kd_interest(row, s)
        return ebit_ex_equity(row, s)

    def no_country(row, spec):
        return Spec(**{**spec.__dict__, "country_risk": False})

    return {"Cost of debt = interest on debt (DFC)": kd_interest,
            "No country risk (lambda = 0)": no_country,
            "Statutory tax 34%": statutory,
            "EBIT without equity income": ebit_ex_equity,
            "All three": all_three}


def recompute(wb: Workbook, raw: dict[int, dict]) -> pd.DataFrame:
    m = DCF(wb)
    rows = []
    for _, row in wb.dates.iterrows():
        base = m.value(row, BASE)
        rows.append({"date": base["date"], "variant": "Thesis model (19/10)", **_pick(base)})
        for name, build in alternative_specs(wb, raw).items():
            v = m.value(row, build(row, BASE))
            rows.append({"date": v["date"], "variant": name, **_pick(v),
                         "fair_value_change": v["fair_value"] / base["fair_value"] - 1})
    return pd.DataFrame(rows)


def _pick(v):
    return {k: v[k] for k in ("fair_value", "price", "wacc", "Cost of debt", "Tax rate", "EBIT margin", "fcff_year1")}


SYSTEM = (
    "Você é uma segunda analista revisando o valuation de um TCC de economia (FCFF/WACC da Gerdau). "
    "Escreva em português, frases curtas. Use SOMENTE os números das tabelas recebidas, sem inventar nenhum. "
    "Para cada achado: o que diverge, os números, a causa provável e uma ação sugerida. "
    "No máximo 5 achados, um por tópico. Você aponta; quem decide é o autor do TCC."
)


def memo(llm: LLM, recon: pd.DataFrame, alt: pd.DataFrame) -> dict:
    topics = sorted(alt["variant"].unique().tolist() + ["Reconciliação com a CVM"])
    differs = recon[recon["status"] != "match"]
    summary_alt = (alt[alt["variant"] != "Thesis model (19/10)"]
                   .pivot_table(index="variant", columns="date", values="fair_value_change").round(3))
    base = alt[alt["variant"] == "Thesis model (19/10)"].set_index("date")[["fair_value", "price", "wacc", "Cost of debt", "Tax rate"]].round(3)
    prompt = DEFINITIONS + "\n\n" + (
        f"Reconciliação planilha × CVM: {len(recon) - len(differs)} de {len(recon)} linhas batem "
        f"(tolerância 0,5%). Divergências:\n{differs.to_string(index=False) if len(differs) else 'nenhuma'}\n\n"
        f"Valuation com o modelo do TCC (desde 19/10):\n{base.to_string()}\n\n"
        f"Variação do valor justo por ação quando a segunda analista muda UMA escolha (fração; 0.10 = +10%):\n"
        f"{summary_alt.to_string()}\n\n"
        f"Custo da dívida por variante e data:\n"
        f"{alt.pivot_table(index='variant', columns='date', values='Cost of debt').round(3).to_string()}\n\n"
        f"Tópicos permitidos: {json.dumps(topics, ensure_ascii=False)}"
    )

    def check(a):
        bad = [f["topic"] for f in a["findings"] if f["topic"] not in topics]
        return [f"unknown topic: {t}" for t in bad] + unsupported_numbers(a, prompt)

    return llm.ask("second-analyst", SYSTEM, prompt, load_schema("analyst_memo"), check=check, max_tokens=1500)


def run(llm: LLM | None, wb: Workbook, years=range(2015, 2025)) -> dict:
    raw = {y: cvm.year_lines(y) for y in years}
    recon = reconcile(wb, years)
    alt = recompute(wb, raw)
    return {"reconciliation": recon, "alternatives": alt,
            "memo": memo(llm, recon, alt) if llm else None}
