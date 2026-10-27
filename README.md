# valuation-gerdau

**[See it working](https://gcabralcavalcanti.github.io/valuation-gerdau/)** · [Final report, 2 pages (PDF)](final-report.pdf)

Four AI reviewers for my undergraduate thesis, which values the steelmaker Gerdau from the cash it is expected to
generate: one checks the data, one redoes the math, one tests other ways of doing it, and one prepares the questions
the examining board is likely to ask.

![Public data only](https://img.shields.io/badge/data-public%20only-2a78d6)
![Built with AI assistance](https://img.shields.io/badge/built%20with-AI%20assistance-52514e)

![Share price vs estimated value](docs/price_vs_value.png)

## What it shows

- **The thesis question at a glance.** Using only the last 3 years of history, the estimated value jumps highest at
  the 2022–2023 peak of the steel cycle; longer histories give calmer estimates.
- **Every figure traced to its source.** The AI reads Gerdau's published results and quotes the page for each number;
  all of them match the thesis spreadsheet.
- **A method error caught and fixed.** The discount rate was too close to the growth rate, so the value exploded; the
  corrected rate gives sensible values at every date. Full write-up: [final-report.pdf](final-report.pdf).

## Run it

```bash
pip install -r requirements.txt
python demo.py
```

Runs without an API key, replaying recorded answers. Set `ANTHROPIC_API_KEY` to call Claude live.

## More

- [How I use it](docs/how-it-works.md#how-i-use-it): what the reviewers found on my thesis and what I changed.
- [How it works](docs/how-it-works.md): the four reviewers, what was checked, recorded answers, data and commands.
- [Runbook](RUNBOOK.md): run, update with a new thesis spreadsheet, and what to do when a source is down.

## Limits

- The AI's numbers are checked against its tables, but a real number can still be tied to the wrong year.
- The Brazil risk index stopped in July 2024, so the February 2025 date uses its last value.

## How AI was used

I use Claude (Claude Code and the API) for coding, review and documentation. The questions, modelling choices,
validation and conclusions are mine.

## License

MIT. See [LICENSE](LICENSE).
