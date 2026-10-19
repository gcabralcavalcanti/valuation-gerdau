"""Lab, reviewer and steel cycle on synthetic data, with the LLM off."""
import numpy as np
import pandas as pd

from valuation_gerdau import lab, reviewer, steel


def fake_steel():
    idx = pd.date_range("2000-01-01", "2025-12-01", freq="MS")
    return pd.Series(np.linspace(100, 300, len(idx)), index=idx)


def test_steel_phase_uses_only_past_data():
    s = fake_steel()
    s.loc["2024-12-01":] = 10_000  # a jump after the date must not leak in
    info = steel.at_date("2025-02-20", s)
    assert info["steel_month"] == "2024-12" or info["steel_ppi"] < 10_000
    assert steel.at_date("2020-06-15", s)["phase"] in {"rising", "flat", "falling"}


def test_lab_grid_and_beta_ci(synthetic_wb, monkeypatch):
    monkeypatch.setattr(steel, "series", fake_steel)
    out = lab.run(None, synthetic_wb)
    assert set(out["grid"]["dimension"]) == set(lab.specs())
    ci = out["beta_ci"].pivot_table(index="scenario", columns="date", values="fair_value")
    assert (ci.loc["β − 1.96 se"] > ci.loc["β + 1.96 se"]).all()   # lower beta, lower WACC, higher value
    assert out["summary"] is None


def test_reviewer_tornado_sorted_and_history_bounded(synthetic_wb, monkeypatch):
    monkeypatch.setattr(steel, "series", fake_steel)
    out = reviewer.run(None, synthetic_wb)
    swings = out["tornado"]["swing"].tolist()
    assert swings == sorted(swings, reverse=True)
    h = out["history"]
    assert ((h["percentile_of_used"] >= 0) & (h["percentile_of_used"] <= 1)).all()
