"""Shared loading for the concept ledger (glossary.yaml).

The ledger is this book's canon. Both the glossary generator and the term
linter read it through here so they can never disagree about what it says.
"""

# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "glossary.yaml"
CHAPTERS = ROOT / "chapters"


@dataclass
class Concept:
    term: str
    definition: str
    defined_in: int
    aka: list[str] = field(default_factory=list)
    analogy: str = ""
    depends_on: list[str] = field(default_factory=list)
    scan: bool | None = None

    @property
    def names(self) -> list[str]:
        """Every string that refers to this concept."""
        return [self.term, *self.aka]

    @property
    def scannable_names(self) -> list[str]:
        """The names distinctive enough to hunt for in prose.

        Scanning is deliberately conservative. Ordinary English words —
        "test", "plan", "state", "image", "fake" — appear constantly in prose
        that is not about the concept at all, and flagging them would make the
        gate noisy enough that people would learn to ignore it, which is worse
        than not having it.

        So a name is scanned only if it is multi-word or an acronym. A single
        word that is genuinely distinctive jargon ("idempotent", "stateless")
        opts in with `scan: true`, which adds the canonical term — but NOT its
        synonyms, since those are exactly where the ordinary English creeps in
        ("login" for authentication, "permissions" for authorization). A
        concept can opt out of prose scanning entirely with `scan: false`.
        """
        if self.scan is False:
            return []
        names = [n for n in self.names if " " in n or (n.isupper() and len(n) > 1)]
        if self.scan is True and self.term not in names:
            names.append(self.term)
        return names


def load() -> list[Concept]:
    raw = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    return [Concept(**c) for c in raw["concepts"]]


def chapter_files() -> list[tuple[int, Path]]:
    """Chapter number → path, in order, for every chapter written so far."""
    out = []
    for path in sorted(CHAPTERS.glob("*.md")):
        try:
            number = int(path.name.split("-", 1)[0])
        except ValueError:
            print(f"skipping unnumbered chapter file: {path.name}", file=sys.stderr)
            continue
        out.append((number, path))
    return out
