# Runbook

## Run

| Goal | Command |
|---|---|
| Demo, no API key, no cost | `python demo.py` |
| Same, with a local copy of the thesis spreadsheet | `python demo.py --workbook "Database Valuation Gerdau.xlsx"` |
| Live run (calls the API; set `ANTHROPIC_API_KEY` and `SEC_USER_AGENT` in `.env`) | `python -m valuation_gerdau all --live` |
| Rebuild `final-report.pdf` from the last run | `python -m valuation_gerdau final` |
| Tests (no network, no API) | `python -m pytest -q` |

Every API call is logged in `output/logs/` with its tokens. A run stops at 40 calls (`VALUATION_MAX_CALLS`). Building
and testing the project cost about US$ 0.03 in total.

## Update after the thesis spreadsheet changes

1. Delete the cached copy: `.cache/Database Valuation Gerdau.xlsx`. The next run downloads the new one.
2. `python -m pytest -q`. If the thesis model changed, the test that compares with the values I had already calculated
   (the answer key in `tests/golden/`) fails: copy the new values printed by the thesis notebook into
   `tests/golden/thesis_results.json` and run the tests again.
3. `python -m valuation_gerdau all --live`. Only questions whose tables changed are sent to the API; the rest come
   from `data/recorded/`.
4. `python -m valuation_gerdau final`, check `final-report.pdf`, commit.

## When a source is down

| Source | Symptom | What to do |
|---|---|---|
| Thesis spreadsheet (raw link on GitHub) | message "could not be downloaded" | check the connection, or run with `--workbook <local file>` |
| CVM open data (`dados.cvm.gov.br`) | the second analyst fails while downloading the yearly zip files | files already in `.cache/cvm/` keep working; the demo uses the figures saved in `data/recorded/cvm_lines.json`; otherwise try again later |
| SEC (Gerdau's results reports) | "Earnings releases unavailable" | set `SEC_USER_AGENT="Your Name you@mail"` in `.env` (the SEC requires it); the demo works without it |
| FRED (steel price index) | download error in the lab or the reviewer | try again later; once downloaded it stays in `.cache/` |
| Anthropic API | error or call cap reached | run with `--demo` to replay the recorded answers |
