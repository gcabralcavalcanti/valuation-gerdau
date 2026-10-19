"""The independent DCF: economic sanity on synthetic data, and the golden set on the real spreadsheet."""
import json

import pytest

from valuation_gerdau import config, data
from valuation_gerdau.model import DCF, Spec

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


@pytest.mark.skipif(real_workbook_path() is None, reason="real spreadsheet not on disk")
def test_golden_thesis_results():
    """Reproduces every number the author's notebook printed (45 cases)."""
    golden = json.loads((config.GOLDEN / "thesis_results.json").read_text(encoding="utf-8"))
    m = DCF(data.load(real_workbook_path()))
    runs = {}
    for c in golden["cases"]:
        key = (c["window"], c["erp"])
        if key not in runs:
            runs[key] = m.run(Spec(window=c["window"], erp=c["erp"])).set_index("date")
        got = runs[key].loc[c["date"]]
        assert got["fair_value"] == pytest.approx(c["fair_value"], abs=c["tol"]), c
        if "beta" in c:
            assert got["beta"] == pytest.approx(c["beta"], abs=0.005), c
