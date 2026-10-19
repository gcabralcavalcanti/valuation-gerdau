"""Every module the CLI and the demo load must import with the packages in requirements.txt."""

import importlib

import pytest

MODULES = [
    "valuation_gerdau.__main__",
    "valuation_gerdau.final_report",
    "valuation_gerdau.auditor",
    "valuation_gerdau.second_analyst",
    "valuation_gerdau.lab",
    "valuation_gerdau.reviewer",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)


def test_demo_script_imports():
    importlib.import_module("demo")


def test_missing_spreadsheet_gives_a_clear_message(monkeypatch, tmp_path, capsys):
    from valuation_gerdau import __main__, config

    monkeypatch.delenv("GERDAU_XLSX", raising=False)
    monkeypatch.setattr(config, "CACHE", tmp_path)
    monkeypatch.setattr(config, "DATA_URL", "http://127.0.0.1:9/missing.xlsx")
    assert __main__.main(["lab", "--no-llm"]) == 2
    err = capsys.readouterr().err
    assert "missing.xlsx" in err and "--workbook" in err
    assert __main__.main(["lab", "--no-llm", "--workbook", str(tmp_path / "nope.xlsx")]) == 2
    assert "not found" in capsys.readouterr().err
