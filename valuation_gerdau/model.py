"""Independent re-implementation of the thesis DCF (FCFF / WACC), parameterised by a `Spec`.

The default Spec reproduces the thesis notebook (tests/golden/thesis_results.json, model of 21/10/2026: rf = longest
NTN-F − EMBI+ Brazil; cost of debt = NTN-F + Baa credit spread; ke = rf + beta x mature US premium + lambda x Brazil
country premium). Spec(rf="selic") reproduces the model of 19/10 (tests/golden/thesis_results_v2.json: expected Selic
as rf, Selic + Baa spread as cost of debt). LEGACY reproduces the first version of the notebook
(tests/golden/thesis_results_v1.json: Ibovespa − CDI premium and book cost of debt). Every other Spec is an
alternative the lab or the reviewer can test. All values in R$ million.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .data import Workbook

# One-off gains removed from EBIT in the thesis (identified in the 20-F filings), R$ million.
ONE_OFFS = {2020: 1002, 2021: 1391, 2023: 700, 2024: 808 + 101 - 529}
EXPLICIT_YEARS = 5
STATUTORY_TAX = 0.34


@dataclass(frozen=True)
class Spec:
    window: int = 5  # years used to estimate operating assumptions
    beta_window: int | None = None  # years of returns in the beta regression (None = window)
    beta_freq: str = "W"  # "W" weekly or "M" monthly returns
    beta_adjust: str = "raw"  # "raw" or "blume" (0.67·β + 0.33)
    erp: float | str = "us_mature"  # "us_mature" (US stocks − 10y bonds, geometric, since 1928),
    # "brazil_historical" (Ibovespa − CDI since 2009) or a fixed number
    country_risk: bool = True  # add lambda x country premium (EMBI+ Brazil) to the cost of equity
    rf: str = "ntnf"  # "ntnf" (longest fixed-rate government bond − EMBI+ Brazil) or "selic" (expected Selic t+4)
    kd: str = "rating_spread"  # "rating_spread" (government rate + Baa spread) or "book" (financial expense / debt)
    tax: str = "effective"  # "effective" (clipped to 0–34%) or "statutory" (34%)
    overrides: dict = field(default_factory=dict)  # fixed values for named assumptions

    def label(self) -> str:
        erp = self.erp if isinstance(self.erp, str) else f"{self.erp:.0%}"
        crp = " + country" if self.country_risk else ""
        return (
            f"window {self.window}y · beta {self.beta_window or self.window}y {self.beta_freq} {self.beta_adjust}"
            f" · rf {self.rf} · ERP {erp}{crp} · kd {self.kd} · tax {self.tax}"
        )

    def with_overrides(self, **kw) -> Spec:
        return replace(self, overrides={**self.overrides, **kw})


LEGACY = Spec(erp="brazil_historical", country_risk=False, rf="selic", kd="book")  # thesis notebook v1 (16/10/2026)


def legacy(**kw) -> Spec:
    return replace(LEGACY, **kw)


# Plain definitions sent to the LLM with the numbers, so it does not guess what each column means.
DEFINITIONS = (
    "Definições (do código): rf da tese (desde 21/10) = NTN-F de vencimento mais longo na véspera − EMBI+ Brasil (a "
    "taxa do governo já embute o risco-país, que entra no ke por lambda × EMBI). Cost of debt da tese = NTN-F + "
    "spread de crédito Baa − Treasury de 10 anos (risco do país + risco da empresa; custo atual de captação). Até "
    "20/10 o rf era a Selic esperada t+4, e o Cost of debt, Selic + spread. Custo contábil antigo = despesa "
    "financeira total da DRE (inclui variação cambial) / dívida total média. ke = rf + beta × prêmio maduro dos EUA +"
    " lambda × EMBI+ Brasil, lambda = fatia da receita no Brasil. 'Interest on debt (DFC)' = linha 'Despesa de juros "
    "sobre dívidas financeiras' da DFC / dívida bruta média (despesa de juros, não juros pagos). Tax rate = IR e CSLL"
    " / lucro antes do IR, limitado a 0–34%. EBIT margin exclui impairment e ganhos não recorrentes identificados no "
    "20-F. Percentis e faixas p10–p90 vêm do histórico anual da própria Gerdau. As faixas do prêmio maduro (4%–7%), "
    "do prêmio-país (1,5%–4%), do spread de crédito (1%–3%) e de g (± 1 p.p.) são faixas de teste, não dados."
)

ASSUMPTIONS = [
    "Revenue growth",
    "EBIT margin",
    "D&A / revenue",
    "Capex / revenue",
    "Working capital / revenue",
    "Tax rate",
]  # operating assumptions, estimated by window


class DCF:
    def __init__(self, wb: Workbook, one_offs: dict | None = None):
        self.wb = wb
        f = wb.fundamentals.copy()
        one_offs = ONE_OFFS if one_offs is None else one_offs
        f["EBIT adjusted"] = f["EBIT sem impairment"] - pd.Series(one_offs, dtype=float).reindex(f.index).fillna(0)
        f["Working capital"] = f["Contas a receber"] + f["Estoques"] - f["Fornecedores"]
        f["Total debt"] = f["Dívida bruta (sem arrendamentos)"] + f["Arrendamentos (IFRS 16)"]
        self.f = f
        rev = f["Receita líquida"]
        r = pd.DataFrame(index=f.index)
        r["Revenue growth"] = rev.pct_change()
        r["EBIT margin"] = f["EBIT adjusted"] / rev
        r["D&A / revenue"] = f["Depreciação e amortização"] / rev
        r["Capex / revenue"] = f["Capex"] / rev
        r["Working capital / revenue"] = f["Working capital"] / rev
        r["Tax rate"] = (-f["IR e CSLL"] / f["Lucro antes do IR"]).clip(0, STATUTORY_TAX)
        r["Book cost of debt"] = -f["Despesas financeiras"] / f["Total debt"].rolling(2, min_periods=1).mean()
        self.ratios = r
        p = wb.prices
        self._cdi_daily = 1 + p["CDI (% ao dia)"] / 100

    # ------------------------------------------------------------ assumptions
    def assumptions(self, last_year: int, years: int) -> pd.Series:
        a = self.ratios.loc[last_year - years + 1 : last_year].mean()
        rev = self.f["Receita líquida"]
        a["Revenue growth"] = (rev[last_year] / rev[last_year - years]) ** (1 / years) - 1
        return a

    def excess_returns(self, freq: str = "W") -> pd.DataFrame:
        rule = "W-FRI" if freq == "W" else "ME"
        p = self.wb.prices
        last = p.resample(rule).last()
        cdi = self._cdi_daily.resample(rule).prod() - 1
        return pd.DataFrame(
            {
                "GGBR4": last["GGBR4 ajustada (R$)"].pct_change() - cdi,
                "Ibovespa": last["Ibovespa (pontos)"].pct_change() - cdi,
            }
        ).dropna()

    def beta_regression(self, date, years: int, freq: str = "W"):
        ret = self.excess_returns(freq)
        w = ret[(ret.index < date) & (ret.index >= date - pd.DateOffset(years=years))]
        return sm.OLS(w["GGBR4"], sm.add_constant(w["Ibovespa"])).fit()

    def historical_erp(self, date) -> float:
        p = self.wb.prices[self.wb.prices.index < date]
        annual = p.resample("YE").last()
        ibov = annual["Ibovespa (pontos)"].pct_change()
        cdi = (1 + p["CDI (% ao dia)"] / 100).resample("YE").prod() - 1
        return float((ibov - cdi).dropna().mean())

    def us_mature_erp(self, date, start: int = 1927) -> float:
        """Geometric annual real return of US stocks minus 10-year bonds, Dec/start to Dec of the year before date."""
        u, end = self.wb.us_returns, date.year - 1
        n = end - start
        stocks = (u.loc[end].iloc[0] / u.loc[start].iloc[0]) ** (1 / n) - 1
        bonds = (u.loc[end].iloc[1] / u.loc[start].iloc[1]) ** (1 / n) - 1
        return float(stocks - bonds)

    def market_at(self, date) -> pd.Series:
        return self.wb.market.loc[self.wb.market["Data-base"] == date].iloc[0]

    # -------------------------------------------------------------- valuation
    def value(self, row: pd.Series, spec: Spec = Spec()) -> dict:
        d, last = row["Data-base"], int(row["Último exercício publicado"])
        a = self.assumptions(last, spec.window)
        if spec.tax == "statutory":
            a["Tax rate"] = STATUTORY_TAX
        fo = self.wb.focus.loc[self.wb.focus["Data-base"] == d].iloc[0]
        ov = spec.overrides

        reg = self.beta_regression(d, spec.beta_window or spec.window, spec.beta_freq)
        beta = float(reg.params["Ibovespa"])
        if spec.beta_adjust == "blume":
            beta = 0.67 * beta + 0.33
        beta = ov.get("Beta", beta)
        if spec.erp == "us_mature":
            erp = self.us_mature_erp(d)
        elif spec.erp in ("brazil_historical", "historical"):
            erp = self.historical_erp(d)
        else:
            erp = float(spec.erp)
        erp = ov.get("Equity risk premium", erp)
        lam = crp = country_spread = 0.0
        if spec.country_risk or spec.kd == "rating_spread" or spec.rf == "ntnf":
            me = self.market_at(d)
        if spec.rf == "ntnf":
            # The Brazilian government rate already carries the country default spread: take it out of rf so that
            # country risk is not counted twice (it enters ke through lambda x EMBI), and put it back in the cost of
            # debt, which pays both the country spread and the company spread.
            country_spread = me["EMBI+ Brasil, véspera (%)"] / 100
            rf = me["NTN-F mais longa, véspera (% a.a.)"] / 100 - country_spread
        else:
            rf = fo["Selic ano t+4 (%)"] / 100
        rf = ov.get("Risk-free rate", rf)
        if spec.country_risk:
            lam = me["Receita no Brasil, último exercício (%)"] / 100
            crp = me["EMBI+ Brasil, véspera (%)"] / 100
        lam, crp = ov.get("Lambda", lam), ov.get("Country risk premium", crp)
        if spec.kd == "rating_spread":
            spread = ov.get("Credit spread", me["Spread Baa − Treasury 10 anos, mês anterior (%)"] / 100)
            kd = rf + country_spread + spread
        else:
            kd = float(a["Book cost of debt"])
        kd = ov.get("Cost of debt", kd)
        g = (1 + fo["IPCA ano t+4 (%)"] / 100) * (1 + fo["PIB ano t+3 (%)"] / 100) - 1
        g = ov.get("Terminal growth", g)
        for k in ASSUMPTIONS:
            if k in ov:
                a[k] = ov[k]

        ke = rf + beta * erp + lam * crp
        E = row["Valor de mercado (R$ mi)"]
        D = self.f.loc[last, "Total debt"]
        t = a["Tax rate"]
        wacc = E / (D + E) * ke + D / (D + E) * kd * (1 - t)

        revenue, wc_prev, fcff = self.f.loc[last, "Receita líquida"], self.f.loc[last, "Working capital"], []
        for year in range(1, EXPLICIT_YEARS + 1):
            growth = a["Revenue growth"] + (g - a["Revenue growth"]) * year / EXPLICIT_YEARS
            revenue *= 1 + growth
            wc = a["Working capital / revenue"] * revenue
            fcff.append(
                revenue * (a["EBIT margin"] * (1 - t) + a["D&A / revenue"] - a["Capex / revenue"]) - (wc - wc_prev)
            )
            wc_prev = wc
        disc = (1 + wacc) ** -np.arange(1, EXPLICIT_YEARS + 1)
        terminal = fcff[-1] * (1 + g) / (wacc - g)  # meaningless when wacc <= g: flagged below
        firm = float(np.dot(fcff, disc) + terminal * disc[-1])
        equity = (
            firm
            - row["Dívida líquida (R$ mi)"]
            - self.f.loc[last, "Arrendamentos (IFRS 16)"]
            - self.f.loc[last, "PL de não controladores"]
        )
        price = float(row["GGBR4 na data (R$)"])
        fair = equity / row["Ações em circulação (mi)"]
        return {
            "date": d.date().isoformat(),
            "last_fy": last,
            "spec": spec.label(),
            "window": spec.window,
            "price": price,
            "fair_value": fair,
            "deviation": fair / price - 1,
            "beta": beta,
            "beta_se": float(reg.bse["Ibovespa"]),
            "beta_r2": float(reg.rsquared),
            "beta_n": int(reg.nobs),
            "erp": erp,
            "lambda": lam,
            "crp": crp,
            "rf": rf,
            "ke": ke,
            "Cost of debt": kd,
            "Book cost of debt": float(a["Book cost of debt"]),
            "wacc": wacc,
            "g": g,
            "fcff_year1": fcff[0],
            "firm_value": firm,
            "valid": bool(wacc > g),
            **{k: float(a[k]) for k in ASSUMPTIONS},
        }

    def run(self, spec: Spec = Spec()) -> pd.DataFrame:
        return pd.DataFrame([self.value(r, spec) for _, r in self.wb.dates.iterrows()])
