"""Loads the thesis spreadsheet from the thesis repository (raw link), with a local cache.

--workbook <path> (or GERDAU_XLSX=<path>) reads a local file instead: offline, or before the thesis repo is published.
"""

from __future__ import annotations

import os
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from . import config


@dataclass
class Workbook:
    dates: pd.DataFrame  # one row per valuation date
    fundamentals: pd.DataFrame  # annual, index = fiscal year, R$ million
    prices: pd.DataFrame  # daily, index = date
    macro: pd.DataFrame  # annual, index = year
    focus: pd.DataFrame  # Focus survey available at each valuation date
    source: str
    market: pd.DataFrame | None = None  # credit spread, EMBI+ Brazil, revenue in Brazil at each date
    us_returns: pd.DataFrame | None = None  # US real total-return indexes in December (Shiller), index = year


class WorkbookUnavailable(RuntimeError):
    pass


def workbook_path(refresh: bool = False) -> Path:
    local = os.environ.get("GERDAU_XLSX")
    if local:
        if not Path(local).exists():
            raise WorkbookUnavailable(f"Spreadsheet not found: {local}")
        return Path(local)
    target = config.CACHE / "Database Valuation Gerdau.xlsx"
    if refresh or not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(config.DATA_URL, headers={"User-Agent": "valuation-gerdau"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                target.write_bytes(r.read())
        except OSError as err:  # URLError and HTTPError (e.g. 404) are OSErrors
            raise WorkbookUnavailable(
                f"The thesis spreadsheet comes from {config.DATA_URL} and could not be downloaded ({err}). "
                "Check the connection, or run with --workbook <path to Database Valuation Gerdau.xlsx>."
            ) from None
    return target


def load(path: Path | None = None) -> Workbook:
    path = path or workbook_path()
    sheets = pd.read_excel(path, sheet_name=None)
    dates = sheets["Datas-base"].copy()
    dates["Data-base"] = pd.to_datetime(dates["Data-base"])
    return Workbook(
        dates=dates,
        fundamentals=sheets["Fundamentos"].set_index("Ano"),
        prices=sheets["Preços diários"].assign(Data=lambda d: pd.to_datetime(d["Data"])).set_index("Data"),
        macro=sheets["Macro anual"].set_index("Ano"),
        focus=sheets["Expectativas Focus"].assign(**{"Data-base": lambda d: pd.to_datetime(d["Data-base"])}),
        source=str(path),
        market=sheets["Mercado nas datas"].assign(**{"Data-base": lambda d: pd.to_datetime(d["Data-base"])}),
        us_returns=sheets["Retornos EUA (anual)"].set_index("Ano"),
    )
