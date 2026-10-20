"""Retrieval for the auditor: documents are split into one chunk per page, indexed with BM25, and the model
only sees the chunks a query retrieves. Every chunk keeps its document and page, so answers can cite both.

BM25 is enough here: the queries are short lists of accounting terms and the corpus is a few hundred pages.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from . import sources

_TOKEN = re.compile(r"[a-z]+|\d[\d,.]*\d|\d")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


@dataclass(frozen=True)
class Chunk:
    doc: str  # document name (file name of the filing)
    page: int  # 1-based page number in the document
    text: str


def ingest(path: Path) -> list[Chunk]:
    """One chunk per page. HTML filings are split at their page breaks; PDFs page by page."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        pages = [p.extract_text() or "" for p in PdfReader(str(path)).pages]
    else:
        pages = sources.pages(path)
    return [Chunk(path.name, i + 1, text) for i, text in enumerate(pages) if text.strip()]


class BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.tf = [Counter(tokenize(c.text)) for c in chunks]
        self.len = [sum(tf.values()) for tf in self.tf]
        self.avg_len = sum(self.len) / max(len(self.len), 1)
        df = Counter(term for tf in self.tf for term in tf)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def score(self, query: str, i: int) -> float:
        tf, dl = self.tf[i], self.len[i]
        s = 0.0
        for term in tokenize(query):
            f = tf.get(term, 0)
            if f:
                s += self.idf[term] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg_len))
        return s

    def search(self, query: str, k: int = 4, doc: str | None = None) -> list[tuple[Chunk, float]]:
        """Top-k chunks for the query, optionally restricted to one document."""
        scored = [(c, self.score(query, i)) for i, c in enumerate(self.chunks) if doc is None or c.doc == doc]
        scored = [x for x in scored if x[1] > 0]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
