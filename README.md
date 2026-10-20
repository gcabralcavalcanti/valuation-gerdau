# valuation-gerdau

Four AI reviewers that check my undergraduate thesis, which values the steelmaker Gerdau from the cash it is
expected to generate: one checks the data, one redoes the math, one tests other ways of doing it, and one prepares
the questions the examining board is likely to ask.

![Public data only](https://img.shields.io/badge/data-public%20only-2a78d6)
![Built with AI assistance](https://img.shields.io/badge/built%20with-AI%20assistance-52514e)

## Results

![Share price vs estimated value](docs/price_vs_value.png)

The chart compares Gerdau's share price with the value the thesis estimates at five dates, using 3, 5 or 10 years
of history to set the assumptions. With only 3 years of history the estimate jumps highest at the 2022–2023 peak of
the steel cycle, which is exactly what the thesis studies.

| What was checked | Result | Where to see it |
|---|---|---|
| Every company figure in the thesis spreadsheet that I checked against Gerdau's published results | all match, each with the page it came from | [output/auditor.md](output/auditor.md) |
| The same spreadsheet against the raw filings with the Brazilian securities regulator (CVM), 2015–2024 | all lines match | [output/second_analyst.md](output/second_analyst.md) |
| My thesis model, rebuilt from scratch here | gives the same values as the thesis | [answer key: the values I had already calculated](tests/golden/) |
| The discount rate (the return investors require) | fixed: it was below the long-run growth rate, which breaks the formula; now it is 11.6% to 14.2% | [final-report.pdf](final-report.pdf) |
| API cost of building and testing all of this | about US$ 0.03 | [RUNBOOK.md](RUNBOOK.md) |

Full write-up: [final-report.pdf](final-report.pdf).

## Run it

```bash
pip install -r requirements.txt
python demo.py
```

Runs without an API key, replaying recorded answers. Set `ANTHROPIC_API_KEY` to call Claude live.
The demo runs the four reviewers one after the other, prints what each one found and rebuilds `final-report.pdf`.
How to update it, and what to do when a source is down: [RUNBOOK.md](RUNBOOK.md).

## How it works

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

## Data

All public: financial statements from the CVM, Gerdau's results reports filed with the US SEC, share prices,
Brazilian central bank data, the US Federal Reserve database (steel prices, corporate bond yields), the Brazil
sovereign risk index and long-run US stock and bond returns. `data/recorded/` keeps the AI answers and the figures
already extracted from the large CVM files, so the demo does not need to download them.

## Limits

- The number check catches made-up figures, not a real figure attached to the wrong year; the reports warn about it.
- The Brazil risk index stopped being published in July 2024, so the February 2025 date uses its last value.
- The safe interest rate is the expected Brazilian policy rate; a long government bond is the next thing to test.
- The results reports are web pages, so "page" means the page breaks of the filed document.

## How AI was used

I use Claude (Claude Code and the API) for coding, review and documentation. The questions, modelling choices,
validation and conclusions are mine. Here the API is also part of the tool: it reads documents and drafts text, and
code checks every answer.

## License

MIT. See [LICENSE](LICENSE).
