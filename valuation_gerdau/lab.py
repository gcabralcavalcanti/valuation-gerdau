"""Role 3: Econometric lab.

Runs alternative specifications of the thesis question (estimation window of the assumptions,
beta regression design, equity risk premium) and shows the effect on fair value and on the
price deviation at each valuation date. It does not pick a winner: the author decides.
"""

from __future__ import annotations

import pandas as pd

from . import steel
from .data import Workbook
from .llm import LLM, load_schema, unsupported_numbers
from .model import DCF, Spec, legacy


def specs() -> dict[str, list[Spec]]:
    return {
        "Estimation window (assumptions and beta)": [Spec(window=w) for w in (3, 5, 7, 10)],
        "Beta: regression window": [Spec(window=5, beta_window=b) for b in (2, 3, 5, 10)],
        "Beta: return frequency and adjustment": [
            Spec(window=5),
            Spec(window=5, beta_freq="M"),
            Spec(window=5, beta_adjust="blume"),
        ],
        "Equity risk premium": [Spec(window=5, erp=e) for e in ("us_mature", 0.04, 0.05, 0.06, 0.07)],
        "Cost of capital method": [
            Spec(window=5),
            Spec(window=5, country_risk=False),
            Spec(window=5, kd="book"),
            legacy(window=5, erp=0.05),
            legacy(window=5),
        ],
    }


def cycle_phase(wb: Workbook, steel_series=None) -> pd.Series:
    """Phase of the steel cycle at each date: 12-month change of the steel price index known at the date."""
    s = steel.series() if steel_series is None else steel_series
    return pd.Series(
        {r["Data-base"].date().isoformat(): steel.at_date(r["Data-base"], s)["phase"] for _, r in wb.dates.iterrows()},
        name="cycle",
    )


def run_grid(wb: Workbook) -> pd.DataFrame:
    m = DCF(wb)
    rows = []
    for dim, ss in specs().items():
        for s in ss:
            for r in m.run(s).to_dict("records"):
                rows.append({"dimension": dim, **r})
    out = pd.DataFrame(rows)
    out["cycle"] = out["date"].map(cycle_phase(wb))
    return out


def beta_ci_scenarios(wb: Workbook, spec: Spec = Spec(window=5)) -> pd.DataFrame:
    """The scenario the advisor's manual suggests: betas across the regression's 95% interval."""
    m = DCF(wb)
    rows = []
    for _, row in wb.dates.iterrows():
        base = m.value(row, spec)
        for label, b in (
            ("β − 1.96 se", base["beta"] - 1.96 * base["beta_se"]),
            ("β", base["beta"]),
            ("β + 1.96 se", base["beta"] + 1.96 * base["beta_se"]),
        ):
            v = m.value(row, spec.with_overrides(Beta=b))
            rows.append(
                {
                    "date": v["date"],
                    "scenario": label,
                    "beta": b,
                    "fair_value": v["fair_value"],
                    "deviation": v["deviation"],
                }
            )
    return pd.DataFrame(rows)


def hypothesis_table(grid: pd.DataFrame) -> pd.DataFrame:
    """Mean price deviation by cycle phase for each window: the thesis question in one table."""
    g = grid[grid["dimension"] == "Estimation window (assumptions and beta)"]
    return g.pivot_table(index="window", columns="cycle", values="deviation", aggfunc="mean")


SYSTEM = (
    "Você é uma assistente de pesquisa num TCC de economia (valuation FCFF da Gerdau em 5 datas). "
    "Recebe tabelas de especificações alternativas já calculadas. Em português e frases curtas: diga que "
    "dimensão mais move o valor, onde o resultado da pergunta do TCC muda de sinal ou de tamanho, e as "
    "opções do autor com prós e contras (no máximo 5 achados e 4 opções). Use só números das tabelas; "
    "um intervalo cita os dois extremos da MESMA data, e diga a data. NÃO escolha a especificação: o autor decide."
)


def summary(llm: LLM, grid: pd.DataFrame, ci: pd.DataFrame) -> dict:
    spread = grid.groupby(["dimension", "date"])["fair_value"].agg(lambda s: s.max() - s.min()).unstack().round(1)
    by_spec = grid.pivot_table(index=["dimension", "spec"], columns="date", values="fair_value").round(1)
    prompt = (
        f"Valor justo por ação (R$) por especificação e data:\n{by_spec.to_string()}\n\n"
        f"Amplitude do valor justo dentro de cada dimensão (máx − mín, R$):\n{spread.to_string()}\n\n"
        f"Desvio médio (valor/preço − 1) por janela e fase do ciclo:\n{hypothesis_table(grid).round(3).to_string()}\n\n"
        f"Cenários de beta no intervalo de 95%:\n"
        f"{ci.pivot_table(index='scenario', columns='date', values='fair_value').round(1).to_string()}\n\n"
        f"Dimensões: {list(specs())}"
    )
    dims = list(specs()) + ["Beta confidence interval", "Thesis question"]

    def check(a):
        return [
            f"unknown dimension: {f['dimension']}" for f in a["findings"] if f["dimension"] not in dims
        ] + unsupported_numbers(a, prompt)

    schema = load_schema("lab_summary")
    schema["properties"]["findings"]["items"]["properties"]["dimension"]["enum"] = dims  # closed list
    return llm.ask("lab", SYSTEM, prompt, schema, check=check, max_tokens=2500)


def run(llm: LLM | None, wb: Workbook) -> dict:
    grid = run_grid(wb)
    ci = beta_ci_scenarios(wb)
    return {
        "grid": grid,
        "beta_ci": ci,
        "hypothesis": hypothesis_table(grid),
        "summary": summary(llm, grid, ci) if llm else None,
    }
