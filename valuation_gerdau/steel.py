"""Steel cycle: US PPI for steel mill products (FRED WPU101), monthly, cached."""
from __future__ import annotations

import io
import urllib.request

import pandas as pd

from . import config

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU101"
LAG_MONTHS = 2  # the PPI comes out about a month later: use only what was public at the date


def series() -> pd.Series:
    path = config.CACHE / "fred_WPU101.csv"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL, timeout=60) as r:
            path.write_bytes(r.read())
    d = pd.read_csv(io.StringIO(path.read_text()), parse_dates=[0], index_col=0)
    return pd.to_numeric(d.iloc[:, 0], errors="coerce").dropna()


def at_date(date, s: pd.Series | None = None) -> dict:
    s = series() if s is None else s
    month = (pd.Timestamp(date) - pd.DateOffset(months=LAG_MONTHS)).to_period("M").to_timestamp()
    s = s[s.index <= month]
    yoy = s.iloc[-1] / s.iloc[-13] - 1
    vs10y = s.iloc[-1] / s.iloc[-121:-1].mean() - 1
    phase = "rising" if yoy > 0.10 else ("falling" if yoy < -0.10 else "flat")
    return {"steel_month": s.index[-1].strftime("%Y-%m"), "steel_ppi": float(s.iloc[-1]),
            "steel_yoy": float(yoy), "steel_vs_10y_avg": float(vs10y), "phase": phase}
