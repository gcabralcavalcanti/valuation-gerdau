"""Public documents: download (cached) and split into numbered pages of plain text."""
from __future__ import annotations

import html
import re
import urllib.request
from pathlib import Path

from . import config

# Gerdau's 4Q earnings releases (exhibit 99 of the 6-K filed with the SEC), one per fiscal year.
RELEASES = {
    2020: "https://www.sec.gov/Archives/edgar/data/1073404/000110465921029118/tm217830d1_ex99-1.htm",
    2021: "https://www.sec.gov/Archives/edgar/data/1073404/000110465922026170/tm227483d1_ex99-1.htm",
    2022: "https://www.sec.gov/Archives/edgar/data/1073404/000110465923027810/tm238211d1_ex99-4.htm",
    2023: "https://www.sec.gov/Archives/edgar/data/1073404/000110465924025861/tm246853d1_ex99-1.htm",
    2024: "https://www.sec.gov/Archives/edgar/data/1073404/000110465925015761/tm257156d2_ex99-1.htm",
}

DOCS = config.CACHE / "docs"


def fetch(url: str) -> Path:
    """Download once into .cache/docs/<file name>. A file already there (e.g. copied by hand) is reused."""
    target = DOCS / url.rsplit("/", 1)[-1]
    if target.exists() and target.stat().st_size > 0:
        return target
    if not config.SEC_USER_AGENT:
        raise RuntimeError("SEC requires a User-Agent with a contact: set SEC_USER_AGENT='Your Name you@mail' "
                           f"in .env, or save {url} as {target}.")
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": config.SEC_USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        target.write_bytes(r.read())
    return target


_BREAK = re.compile(r"<[^>]*page-break-(?:after|before)\s*:\s*always[^>]*>", re.I)
_FIELD = re.compile(r"<!--\s*Field:\s*Page;\s*Sequence:\s*\d+[^>]*-->", re.I)  # Toppan Merrill filings


def _row_to_line(match: re.Match) -> str:
    """One data-table row -> one line, so a label and its numbers stay together.
    Page-layout wrappers (one cell, or a cell holding a whole page of text) are left as they are."""
    cells = re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", match.group(0))
    text = [html.unescape(re.sub(r"<[^>]+>", " ", c)) for c in cells]
    if len(cells) < 2 or any(len(c) > 300 for c in text):
        return match.group(0)
    return "<div>" + " ".join(re.sub(r"\s+", " ", c).strip() for c in text if c.strip()) + "</div>"


def html_to_text(fragment: str) -> str:
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", fragment)
    t = re.sub(r"(?is)<tr\b(?:(?!<tr\b).)*?</tr>", _row_to_line, t)  # innermost rows only
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = re.sub(r"(?i)<br\s*/?>|</(tr|p|div|h\d|li)>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    lines = (re.sub(r"[ \t\xa0]+", " ", ln).strip(" |") for ln in t.split("\n"))
    return "\n".join(ln for ln in lines if ln.strip())


def pages(path: Path) -> list[str]:
    """Pages in document order; page 1 is the cover, as in the printed release."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    chunks = _BREAK.split(raw)
    if len(chunks) == 1:
        chunks = _FIELD.split(raw)
        if len(chunks) > 1 and not html_to_text(chunks[0]).strip():
            chunks = chunks[1:]
    return [html_to_text(chunk) for chunk in chunks]


def normalise(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("|", " ")).strip().lower()
