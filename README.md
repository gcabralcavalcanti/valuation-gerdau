# valuation-gerdau — an AI review layer for a DCF thesis

My undergraduate thesis (Economics, UFRJ) values Gerdau S.A. (GGBR4) by discounted cash flow at five dates
of the steel cycle and asks whether the **window used to estimate the assumptions** creates systematic gaps
between fair value and price. The thesis itself — data, notebook and text — is mine and lives in
[`tcc-valuation-gerdau`](https://github.com/gcabralcavalcanti/tcc-valuation-gerdau).

This repository is the layer around it: four roles that **audit, recompute and stress-test** the work, the way
a second pair of eyes would in a consulting team. The AI never replaces the analysis; it checks it and points
at what to defend.

The data is read from the thesis repository through its raw link (single source of truth, no copy here).

## The four roles

| Role | What it does | Where the LLM is used | Output |
|---|---|---|---|
| **1. Data auditor** | Checks the spreadsheet against Gerdau's public 4Q earnings releases (SEC, exhibit 99), citing document, page and line | Reads the selected pages and extracts the figures as JSON. Code then verifies that the quote is really on the cited page and contains the number (anti-hallucination), and scores the extraction against figures I read by hand (golden set) | [`reports/auditor.md`](reports/auditor.md) |
| **2. Second analyst** | Rebuilds the inputs from **raw CVM filings** with its own code, reconciles line by line, then recomputes FCFF and WACC with choices the raw data allow (interest on debt instead of total financial expense, statutory tax, EBIT without equity income) | Writes the memo; every number comes from the computed tables | [`reports/second_analyst.md`](reports/second_analyst.md) |
| **3. Econometric lab** | Runs alternative specifications: estimation window (3/5/7/10 years), beta regression window, weekly vs monthly returns, Blume adjustment, equity risk premium, betas across the 95% interval | Summarises what moves value and lists the options with pros and cons. **It does not choose**: I do | [`reports/lab.md`](reports/lab.md) |
| **4. Assumption reviewer** | Places each assumption in Gerdau's own history (percentile since 2010) and in the steel cycle at that date (FRED steel PPI, only data public at the date), and builds a tornado of fair value | Writes the questions an examining board is likely to ask, each with the numbers for the answer | [`reports/reviewer.md`](reports/reviewer.md) |

What the first full run found (19/10/2026):
- Auditor: **20 of 20** figures match the releases, each with page and quoted line; extraction accuracy
  against my hand-checked figures **20/20**.
- **130 of 130** spreadsheet lines match the raw CVM filings (2015–2024).
- The independent DCF reproduces **45 of 45** results printed by the thesis notebook (golden set, `tests/test_model.py`).
- Cost of debt measured as interest on financial debt is ~6.7% a year, against 11–15% when it includes FX losses
  (an open point of the thesis); the second analyst shows the effect on value at each date.
- The EBIT margin used at the last date sits at the 87th percentile of Gerdau's history and is the assumption
  that moves value the most (tornado).

Cost of all real runs while building it (about 21 calls, retries included): **US$ 0.017** estimated from the
logged tokens. A full run is 8 calls; after that, the recorded answers make it free.

## Engineering choices

- **Structured output, checked twice:** the API is asked for JSON constrained by a JSON Schema (`schemas/`), and the
  answer is validated again locally plus role-specific checks (quote on page, number in quote, allowed topics).
  A failed check triggers one retry with the reasons; a failed retry stops the run. Names the model
  must pick from (topics, assumptions) are closed lists (`enum`) in the schema, and the prompt carries the exact
  definition of each column, after a first run showed the model guessing what "cost of debt" meant.
- **Cost limits:** cheapest model that handles the task (`claude-haiku-5-5`), low `max_tokens`, effort `low`,
  thinking off, hard cap of calls per run (`VALUATION_MAX_CALLS`, default 40), and every answer recorded in
  `recordings/` keyed by a hash of the request, so the same call is never paid twice.
- **Demo mode:** without an API key the recorded answers replay the run; a request with no recording stops with a clear message.
- **Observability:** one JSON line per call in `logs/` (task, request hash, source api/recording, tokens, check failures)
  and an estimated cost at the end of each run.
- **Secrets:** `ANTHROPIC_API_KEY` from the environment or `.env` (git-ignored). Never in code or logs.
- **Tests without network:** a fake API client exercises schema checks, retry, cache, call cap and demo mode;
  synthetic data tests the model; the golden test runs when the spreadsheet is on disk.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env            # add ANTHROPIC_API_KEY and SEC_USER_AGENT
python -m valuation_gerdau all          # live if a key exists, demo otherwise
python -m valuation_gerdau lab --no-llm # numbers only, no API
python -m pytest -q
```

## Layout

```
valuation_gerdau/
  data.py            spreadsheet from the thesis repo (raw link, cached)
  model.py           independent FCFF/WACC model, parameterised by a Spec
  llm.py             API wrapper: schema, retry, recordings, call cap, JSON log
  sources.py         SEC releases -> numbered pages of text
  cvm.py             raw CVM statements (DFP, consolidated)
  steel.py           steel cycle (FRED WPU101)
  auditor.py · second_analyst.py · lab.py · reviewer.py   the four roles
  reports.py         Markdown + JSON reports
schemas/  golden/  recordings/  reports/  tests/
```
