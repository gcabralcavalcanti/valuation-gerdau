# valuation-gerdau

**An AI review layer for a discounted-cash-flow thesis: four roles that audit the data, rebuild the numbers,
stress-test the method and prepare the defence, each one checked by code.**

![Price vs fair value by estimation window](reports/figures/price_vs_value.png)

My undergraduate thesis (Economics, UFRJ) values Gerdau S.A. (GGBR4) at five dates of the steel cycle, each using
only information public on that date, and asks whether the **window used to estimate the assumptions** creates
systematic gaps between fair value and price. The chart shows the pattern: the 3-year window gives the highest
values at the 2022–2023 peak. The thesis itself (data, notebook, text) is mine and lives in
[`tcc-valuation-gerdau`](https://github.com/gcabralcavalcanti/tcc-valuation-gerdau); this repository reads its
spreadsheet through the raw link (single source of truth, no copy).

The AI never writes the thesis or picks a specification. It checks the work and points at what to defend.

## Try it (no API key)

```bash
pip install -r requirements.txt
python demo.py
```

Runs the four roles in sequence on recorded model answers (no API call, no cost) and writes
[`reports/final-report.pdf`](reports/final-report.pdf).

## The four roles

| Role | Code does | LLM does | Result (19/10/2026) |
|---|---|---|---|
| **1. Data auditor** | splits Gerdau's 4Q earnings releases (SEC) into pages, picks the relevant ones, verifies the answer | extracts revenue, gross debt, net debt and cash as JSON with page and quoted line | **20/20** figures match; extraction **20/20** against figures checked by hand · [report](reports/auditor.md) |
| **2. Second analyst** | rebuilds the inputs from **raw CVM filings**, reconciles line by line, recomputes FCFF and WACC changing one choice at a time | writes the memo from the computed tables | **130/130** lines match · [report](reports/second_analyst.md) |
| **3. Econometric lab** | runs estimation windows (3/5/7/10 years), beta regression designs, premiums and cost-of-capital methods; betas across the 95% interval | summarises what moves value and lists the options with pros and cons | [report](reports/lab.md) |
| **4. Assumption reviewer** | places each assumption in Gerdau's own history and in the steel cycle (data public at each date); tornado of fair value | writes the board's likely questions with the numbers for the answer | [report](reports/reviewer.md) |

## What it changed in the thesis

The first version of the thesis model estimated the equity premium as Ibovespa minus CDI since 2009, which is
negative, and the cost of debt as total financial expense over book debt, which includes FX losses. The WACC
(5–8%) fell below terminal growth and the Gordon value exploded. The review led to the current method, all
numbers computed from market data:

| | First version | Now |
|---|---|---|
| Cost of debt | financial expense / average debt (10.7–15.4%) | expected Selic + Moody's Baa credit spread (8.2–11.2%) |
| Cost of equity | rf + β × (Ibovespa − CDI) | rf + β × mature US premium (Shiller, since 1928) + λ × EMBI+ Brazil, λ = revenue share in Brazil |
| WACC, 5-year window | 5.1–7.8%, below g | 11.6–14.2%, above g at every date |

Both versions are reproduced exactly by the independent model here: 15/15 results of the current notebook and
45/45 of the first one (`golden/`, `tests/test_model.py`).

## Engineering

- **Structured output, checked twice.** JSON constrained by a schema (`schemas/`), validated again locally, plus
  role checks: the quote must be on the cited page and contain the number; names the model picks come from closed
  lists (`enum`); **every number the model writes must exist in the tables it received**. A failed check triggers one
  retry with the reasons; a second failure stops the run. Known limit: a real number paired with the wrong date can
  still pass, so the reports say so.
- **Cost limits.** Cheapest model that handles the task (`claude-haiku-5-5`), effort `low`, thinking off, small
  `max_tokens`, hard cap of calls per run. Every answer is recorded under `recordings/` by a hash of the request, so
  the same call is never paid twice and the demo replays it. All runs while building this: 28 calls, **US$ 0.03**
  (from the logged tokens).
- **Observability.** One JSON line per call in `logs/`: task, request hash, source (api or recording), tokens, failed checks.
- **Secrets.** `ANTHROPIC_API_KEY` from the environment or a git-ignored `.env`; never in code or logs.
- **Tests without network or API.** A fake client exercises schema checks, retries, cache, call cap and demo mode;
  synthetic data tests the model; the golden tests run when the spreadsheet is on disk (`python -m pytest -q`).

## Run with a key

```bash
cp .env.example .env              # ANTHROPIC_API_KEY, SEC_USER_AGENT
python -m valuation_gerdau all    # live if a key exists, demo otherwise
python -m valuation_gerdau final  # rebuilds reports/final-report.pdf
```

## Layout

```
demo.py              one-command demo (no key)
valuation_gerdau/
  data.py            spreadsheet from the thesis repository (raw link, cached)
  model.py           independent FCFF/WACC model; Spec = one specification, LEGACY = first thesis version
  llm.py             API wrapper: schema, checks, retry, recordings, call cap, JSON log
  sources.py         SEC releases -> numbered pages
  cvm.py             raw CVM statements (DFP, consolidated)
  steel.py           steel cycle (FRED steel price index)
  auditor.py · second_analyst.py · lab.py · reviewer.py   the four roles
  reports.py · final_report.py                            Markdown, JSON and the PDF
schemas/  golden/  recordings/  reports/  tests/
```
