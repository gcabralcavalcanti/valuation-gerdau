"""Raw statements from CVM open data (DFP, consolidated), read independently of the thesis scripts."""
from __future__ import annotations

import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from . import config

GERDAU_CVM = 3980  # Gerdau S.A. (never Metalúrgica Gerdau, CVM 2879)
URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{y}.zip"


def zip_path(year: int) -> Path:
    target = config.CACHE / "cvm" / f"dfp_cia_aberta_{year}.zip"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL.format(y=year), timeout=120) as r:
            target.write_bytes(r.read())
    return target


def statement(year: int, kind: str) -> pd.DataFrame:
    """kind: DRE, BPA, BPP or DFC_MI. Gerdau, consolidated, current-year column, R$ million."""
    with zipfile.ZipFile(zip_path(year)) as z:
        d = pd.read_csv(z.open(f"dfp_cia_aberta_{kind}_con_{year}.csv"), sep=";", encoding="latin-1")
    d = d[(d["CD_CVM"] == GERDAU_CVM) & (d["ORDEM_EXERC"] == "ÚLTIMO")]
    d = d[d["VERSAO"] == d["VERSAO"].max()]
    scale = d["ESCALA_MOEDA"].map({"MIL": 1e-3, "UNIDADE": 1e-6}).fillna(1e-3)
    return d.assign(value=d["VL_CONTA"] * scale)[["CD_CONTA", "DS_CONTA", "value"]]


def _code(df, code) -> float:
    s = df.loc[df["CD_CONTA"] == code, "value"]
    return float(s.iloc[0]) if len(s) else float("nan")


def _desc(df, prefix, words) -> float:
    m = df["CD_CONTA"].str.startswith(prefix) & df["DS_CONTA"].str.lower().str.contains(words, regex=True)
    return float(df.loc[m, "value"].sum())


def year_lines(year: int) -> dict:
    dre, bpa, bpp, dfc = (statement(year, k) for k in ("DRE", "BPA", "BPP", "DFC_MI"))
    return {
        "Receita líquida": _code(dre, "3.01"),
        "EBIT (com impairment)": _code(dre, "3.05"),
        "Despesas financeiras": _code(dre, "3.06.02"),
        "Lucro antes do IR": _code(dre, "3.07"),
        "IR e CSLL": _code(dre, "3.08"),
        "Depreciação e amortização": _desc(dfc, "6.01.01", "deprecia"),
        "Capex": -_desc(dfc, "6.02", r"^adi[çc][õo]es de (?:imobilizado|outros ativos intang)|^aquisi[çc][ãa]o de (?:imobilizado|intang)"),
        "Contas a receber": _code(bpa, "1.01.03"),
        "Estoques": _code(bpa, "1.01.04"),
        "Fornecedores": _code(bpp, "2.01.02"),
        "Caixa e aplicações": _code(bpa, "1.01.01") + _code(bpa, "1.01.02"),
        "Dívida bruta (sem arrendamentos)": _code(bpp, "2.01.04") + _code(bpp, "2.02.01"),
        "PL de não controladores": _code(bpp, "2.03.09"),
        # Not in the spreadsheet: interest on financial debt, from the cash-flow reconciliation.
        "Juros sobre dívida (DFC)": _desc(dfc, "6.01.01", r"despesa de juros sobre d[íi]vidas"),
        "Equivalência patrimonial": _code(dre, "3.04.06"),
    }
