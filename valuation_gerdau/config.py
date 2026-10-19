"""Paths, model choice and cost limits. Everything that costs money is capped here."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"            # downloaded data and documents (not versioned)
RECORDINGS = ROOT / "recordings"   # recorded LLM answers: response cache + demo mode (versioned)
REPORTS = ROOT / "reports"         # generated reports (versioned, so the repo shows real output)
LOGS = ROOT / "logs"               # one JSON line per LLM call (not versioned)
SCHEMAS = ROOT / "schemas"
GOLDEN = ROOT / "golden"

# Single source of truth for the data: the spreadsheet in the thesis repository (no copy here).
DATA_URL = os.environ.get(
    "GERDAU_DATA_URL",
    "https://raw.githubusercontent.com/gcabralcavalcanti/tcc-valuation-gerdau/main/"
    "4.%20Dados%20Gerdau/Database%20Valuation%20Gerdau.xlsx",
)

# Cheapest model that handles extraction and short structured writing.
MODEL = os.environ.get("VALUATION_MODEL", "claude-haiku-5-5")
PRICE_PER_MTOK = {"claude-haiku-5-5": (0.10, 0.50)}  # USD (input, output), Anthropic price list

# Hard limits per run (the account has a fixed monthly credit and no card on file).
MAX_CALLS_PER_RUN = int(os.environ.get("VALUATION_MAX_CALLS", "40"))
MAX_TOKENS = 700          # per answer; every schema is small
TIMEOUT_S = 45.0
SDK_RETRIES = 2           # network/429/5xx retries done by the SDK
SCHEMA_RETRIES = 1        # one extra call if the answer fails our own checks

# SEC asks automated clients to identify themselves ("Name email"). Set it in .env.
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "")
