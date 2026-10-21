"""Shared fixtures. Nothing here touches the network or the API."""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from valuation_gerdau import config, model
from valuation_gerdau.data import Workbook


def real_workbook_path():
    """The real spreadsheet, only if it is already on disk (GERDAU_XLSX or the local cache)."""
    p = os.environ.get("GERDAU_XLSX") or config.CACHE / "Database Valuation Gerdau.xlsx"
    return Path(p) if Path(p).exists() else None


@pytest.fixture
def synthetic_wb(monkeypatch) -> Workbook:
    """A small made-up company with the same sheet layout as the thesis spreadsheet."""
    monkeypatch.setattr(model, "ONE_OFFS", {})  # Gerdau's one-off gains do not apply to it
    rng = np.random.default_rng(0)
    years = list(range(2009, 2025))
    rev = 1000 * np.cumprod([1.0] + [1.05] * (len(years) - 1))
    f = pd.DataFrame(
        {
            "Receita líquida": rev,
            "EBIT sem impairment": 0.12 * rev,
            "Depreciação e amortização": 0.05 * rev,
            "Capex": 0.06 * rev,
            "Contas a receber": 0.10 * rev,
            "Estoques": 0.15 * rev,
            "Fornecedores": 0.08 * rev,
            "IR e CSLL": -0.025 * rev,
            "Lucro antes do IR": 0.10 * rev,
            "Despesas financeiras": -0.02 * rev,
            "Dívida bruta (sem arrendamentos)": 0.3 * rev,
            "Arrendamentos (IFRS 16)": 0.0 * rev,
            "PL de não controladores": 0.01 * rev,
        },
        index=pd.Index(years, name="Ano"),
    )
    days = pd.bdate_range("2009-01-02", "2025-03-31")
    mkt = rng.normal(0.0004, 0.012, len(days))
    stock = 1.2 * mkt + rng.normal(0, 0.01, len(days))
    prices = pd.DataFrame(
        {
            "GGBR4 ajustada (R$)": 10 * np.exp(np.cumsum(stock)),
            "Ibovespa (pontos)": 50000 * np.exp(np.cumsum(mkt)),
            "CDI (% ao dia)": 0.04,
        },
        index=days,
    )
    dates = pd.DataFrame(
        {
            "Data-base": pd.to_datetime(["2023-03-01", "2025-02-20"]),
            "Último exercício publicado": [2022, 2024],
            "GGBR4 na data (R$)": [20.0, 25.0],
            "Ações em circulação (mi)": [10.0, 10.0],
            "Valor de mercado (R$ mi)": [200.0, 250.0],
            "Dívida líquida (R$ mi)": [300.0, 320.0],
        }
    )
    focus = pd.DataFrame(
        {
            "Data-base": dates["Data-base"],
            "Selic ano t+4 (%)": [9.0, 10.0],
            "IPCA ano t+4 (%)": [3.5, 3.5],
            "PIB ano t+3 (%)": [2.0, 2.0],
        }
    )
    market = pd.DataFrame(
        {
            "Data-base": dates["Data-base"],
            "NTN-F mais longa, véspera (% a.a.)": [12.0, 13.0],
            "Spread Baa − Treasury 10 anos, mês anterior (%)": [2.0, 1.5],
            "EMBI+ Brasil, véspera (%)": [2.5, 2.3],
            "Receita no Brasil, último exercício (%)": [45.0, 44.0],
        }
    )
    years_us = range(1900, 2025)
    us = pd.DataFrame(
        {"stocks": [1.065 ** (y - 1900) for y in years_us], "bonds": [1.02 ** (y - 1900) for y in years_us]},
        index=pd.Index(years_us, name="Ano"),
    )
    return Workbook(
        dates=dates,
        fundamentals=f,
        prices=prices,
        macro=pd.DataFrame(),
        focus=focus,
        source="synthetic",
        market=market,
        us_returns=us,
    )
