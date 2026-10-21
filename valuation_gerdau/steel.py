"""Steel cycle: US PPI for steel mill products (FRED WPU101), monthly, cached.

When FRED is down (it can answer with an HTML maintenance page), the saved copy in data/fred_WPU101.csv is used.
"""

from __future__ import annotations

import io
import sys
import urllib.request

import pandas as pd

from . import config

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU101"
SNAPSHOT = config.ROOT / "data" / "fred_WPU101.csv"  # public FRED data, saved so the demo runs without FRED
LAG_MONTHS = 2  # the PPI comes out about a month later: use only what was public at the date


def _is_csv(text: str) -> bool:
    """FRED's CSV starts with a date column header; anything else (an HTML page, an error) is not data."""
    first = text.lstrip().split("\n", 1)[0].lower()
    return first.startswith(("observation_date,", "date,"))


def _download() -> str | None:
    try:
        with urllib.request.urlopen(URL, timeout=60) as r:
            text = r.read().decode("utf-8", errors="replace")
    except OSError:  # no connection, timeout, HTTP error
        return None
    return text if _is_csv(text) else None


def _parse(text: str) -> pd.Series:
    d = pd.read_csv(io.StringIO(text), parse_dates=[0], index_col=0)
    return pd.to_numeric(d.iloc[:, 0], errors="coerce").dropna()


def series() -> pd.Series:
    path = config.CACHE / "fred_WPU101.csv"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if not _is_csv(text):  # missing, or a bad file saved by an older version
        text = _download() or ""
        if text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    if text:
        return _parse(text)
    s = _parse(SNAPSHOT.read_text(encoding="utf-8"))
    print(
        f"FRED unavailable: using the saved copy of the steel price index (up to {s.index[-1]:%Y-%m})", file=sys.stderr
    )
    return s


def at_date(date, s: pd.Series | None = None) -> dict:
    s = series() if s is None else s
    month = (pd.Timestamp(date) - pd.DateOffset(months=LAG_MONTHS)).to_period("M").to_timestamp()
    s = s[s.index <= month]
    yoy = s.iloc[-1] / s.iloc[-13] - 1
    vs10y = s.iloc[-1] / s.iloc[-121:-1].mean() - 1
    phase = "rising" if yoy > 0.10 else ("falling" if yoy < -0.10 else "flat")
    return {
        "steel_month": s.index[-1].strftime("%Y-%m"),
        "steel_ppi": float(s.iloc[-1]),
        "steel_yoy": float(yoy),
        "steel_vs_10y_avg": float(vs10y),
        "phase": phase,
    }
