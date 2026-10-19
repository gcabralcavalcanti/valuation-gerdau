"""The independent DCF: economic sanity on synthetic data, and the golden set on the real spreadsheet."""

import json

import pytest

from valuation_gerdau import config, data
from valuation_gerdau.model import DCF, Spec, legacy

from .conftest import real_workbook_path


def test_value_moves_in_the_right_direction(synthetic_wb):
    m = DCF(synthetic_wb)
    row = synthetic_wb.dates.iloc[-1]
    base = m.value(row, Spec(erp=0.05))
    assert base["valid"]
    assert m.value(row, Spec(erp=0.05).with_overrides(**{"EBIT margin": 0.20}))["fair_value"] > base["fair_value"]
    assert m.value(row, Spec(erp=0.07))["fair_value"] < base["fair_value"]
    assert m.value(row, Spec(erp=0.05).with_overrides(**{"Capex / revenue": 0.10}))["fair_value"] < base["fair_value"]


def test_beta_regression_recovers_the_true_beta(synthetic_wb):
    reg = DCF(synthetic_wb).beta_regression(synthetic_wb.dates.iloc[-1]["Data-base"], 5)
    assert reg.params["Ibovespa"] == pytest.approx(1.2, abs=0.15)


def test_assumptions_use_only_the_window(synthetic_wb):
    a = DCF(synthetic_wb).assumptions(2024, 5)
    assert a["Revenue growth"] == pytest.approx(0.05, abs=1e-9)
    assert a["EBIT margin"] == pytest.approx(0.12, abs=1e-9)


def test_mature_premium_and_country_risk(synthetic_wb):
    m = DCF(synthetic_wb)
    row = synthetic_wb.dates.iloc[-1]
    v = m.value(row)
    assert v["erp"] == pytest.approx(0.065 - 0.02, abs=1e-9)  # geometric mean of stocks − geometric mean of bonds
    assert v["ke"] == pytest.approx(v["rf"] + v["beta"] * v["erp"] + 0.44 * 0.023, abs=1e-9)
    assert v["Cost of debt"] == pytest.approx(v["rf"] + 0.015, abs=1e-9)  # expected Selic + credit spread
    assert m.value(row, Spec(country_risk=False))["fair_value"] > v["fair_value"]


@pytest.mark.skipif(real_workbook_path() is None, reason="real spreadsheet not on disk")
def test_golden_thesis_results():
    """Reproduces the 15 results the current thesis notebook printed (3 windows x 5 dates)."""
    golden = json.loads((config.GOLDEN / "thesis_results.json").read_text(encoding="utf-8"))
    m = DCF(data.load(real_workbook_path()))
    runs = {w: m.run(Spec(window=w)).set_index("date") for w in (3, 5, 10)}
    for c in golden["cases"]:
        got = runs[c["window"]].loc[c["date"]]
        assert got["fair_value"] == pytest.approx(c["fair_value"], abs=c["tol"]), c
        assert got["beta"] == pytest.approx(c["beta"], abs=0.005), c


@pytest.mark.skipif(real_workbook_path() is None, reason="real spreadsheet not on disk")
def test_golden_thesis_results_v1():
    """LEGACY reproduces every number the first notebook printed (45 cases)."""
    golden = json.loads((config.GOLDEN / "thesis_results_v1.json").read_text(encoding="utf-8"))
    m = DCF(data.load(real_workbook_path()))
    runs = {}
    for c in golden["cases"]:
        key = (c["window"], c["erp"])
        if key not in runs:
            erp = "brazil_historical" if c["erp"] == "historical" else c["erp"]
            runs[key] = m.run(legacy(window=c["window"], erp=erp)).set_index("date")
        got = runs[key].loc[c["date"]]
        assert got["fair_value"] == pytest.approx(c["fair_value"], abs=c["tol"]), c
        if "beta" in c:
            assert got["beta"] == pytest.approx(c["beta"], abs=0.005), c
