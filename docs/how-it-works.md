# How it works

## How I use it

I ran the four reviewers on my thesis live in October 2026, and again after the next change to the model; each run
cost a few cents and changed nothing on its own. Their findings led to the change in the cost of debt and the risk
premium: the second analyst showed that my cost of debt included currency losses, and the method lab showed that the
historical market premium made the value explode. I checked the valuation manuals, chose a new method, compared the
values before and after, and only then changed the thesis model. Next I switched the risk-free rate from the expected
policy rate to the long fixed-rate government bond minus the Brazil risk index, so that country risk is not counted
twice, and reran the reviewers on the new numbers. I plan to rerun them by hand whenever the spreadsheet changes and
before the defence, when the data checker confirms the new figures and the board questions help me prepare.

## The four reviewers

1. **Data.** The thesis spreadsheet is read straight from the thesis repository,
   [`tcc-valuation-gerdau`](https://github.com/gcabralcavalcanti/tcc-valuation-gerdau), so there is one copy only.
2. **Data checker (search, then answer).** Gerdau's results reports are split into pages and indexed for keyword
   search. For each figure the code finds the best pages, and the AI answers using only those pages, citing the page
   and the exact line. The code then confirms that the line is really on that page and contains the number.
3. **Second analyst.** Rebuilds the inputs from the regulator's raw files and redoes the valuation changing one
   choice at a time. The AI writes a short memo from those tables.
4. **Method lab.** Tries other reasonable ways to set the assumptions and shows how much each moves the value. The
   AI lists the options with pros and cons; the choice stays with me.
5. **Board questions.** Compares each assumption with Gerdau's own history and the steel cycle, and the AI drafts the
   questions an examiner would ask, with the numbers for the answer.
6. **Safety checks.** Answers must follow a fixed format, every number the AI writes must exist in the tables it was
   given, and the same question is never paid for twice.

## What was checked

| What was checked | Result | Where to see it |
|---|---|---|
| Every company figure in the thesis spreadsheet that I checked against Gerdau's published results | all match, each with the page it came from | [output/auditor.md](../output/auditor.md) |
| The same spreadsheet against the raw filings with the Brazilian securities regulator (CVM), 2015 to 2024 | all lines match | [output/second_analyst.md](../output/second_analyst.md) |
| My thesis model, rebuilt from scratch here | gives the same values as the thesis | [answer key: the values I had already calculated](../tests/golden/) |
| The discount rate (the return investors require) | fixed: it was below or barely above the long-run growth rate (5.1% to 7.8% against 5.1% to 6.1%), which makes the value explode; now it is 11.7% to 16.9% | [final-report.pdf](../final-report.pdf) |
| API cost of building and testing all of this | about US$ 0.04 | [RUNBOOK.md](../RUNBOOK.md) |

## Recorded answers

`data/recorded/` keeps every AI answer, keyed by the exact question, plus the figures already extracted from the large
CVM files. The demo replays them, so it runs without a key and without downloading those files; a live run only pays
for questions that changed.

## Commands

| Goal | Command |
|---|---|
| Demo, no key | `python demo.py` |
| Demo with a local copy of the spreadsheet | `python demo.py --workbook <file>` |
| One reviewer (live if a key is set) | `python -m valuation_gerdau auditor` (or `analyst`, `lab`, `reviewer`, `all`) |
| Numbers only, no AI text | `python -m valuation_gerdau lab --no-llm` |
| Rebuild the PDF | `python -m valuation_gerdau final` |
| Tests | `python -m pytest -q` |

## Data

All public: financial statements from the CVM, Gerdau's results reports filed with the US SEC, share prices, Brazilian
central bank data, the US Federal Reserve database (steel prices, corporate bond yields), the Brazil sovereign risk
index and long-run US stock and bond returns.

## More limits

- The results reports are web pages, so "page" means the page breaks of the filed document.
- The safe interest rate is the expected Brazilian policy rate; a long government bond is the next thing to test.
