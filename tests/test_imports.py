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
