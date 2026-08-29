"""Lint the manuscript against the concept ledger.

This is the book's own continuity gate, and a working prototype of the
non-narrative rules proposed in alpibrusl/content-kit#10. It runs in CI, and a
failing rule blocks the merge.

Rules
  ERROR   term-used-before-defined   a term appears in prose before its chapter,
                                     without signposting where it is defined
  ERROR   term-never-defined         a depends_on entry no concept defines
  ERROR   term-defined-twice         two concepts claim the same name
  ERROR   prerequisite-inversion     A depends on B, but A is defined first
  WARN    orphan-concept             in the ledger, never used in prose

Exit codes follow the bookkit convention: 0 clean, 8 precondition failed.

Two deliberate limits, both chosen to keep the gate quiet enough to be trusted:

  * Prose scanning only covers names distinctive enough to search for (see
    Concept.scannable_names). Single common words like "build" or "state" are
    not hunted; the false-positive rate would make the gate useless.

  * A *signposted* forward reference is allowed. "Containers (Chapter 7) package
    the program..." is good writing, not an error — the reader is told exactly
    where the definition lives. A forward reference with no signpost is the
    error, because that is the one that leaves a reader stranded.
"""

# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import re
import sys

from ledger import ROOT, chapter_files, load

EXIT_OK = 0
EXIT_PRECONDITION_FAILED = 8


def name_pattern(name: str) -> str:
    """Match a term, tolerating a simple plural.

    Without this, "environment variable" fails to match the prose phrase
    "environment variables", because the trailing word boundary lands inside
    the plural — which silently turns a real check into no check at all.
    """
    return rf"\b{re.escape(name)}(?:e?s)?\b"


def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def signposts(paragraph: str, chapter: int) -> bool:
    """Whether this paragraph tells the reader where the term is defined."""
    return bool(re.search(rf"chapter\s+{chapter}\b", paragraph, re.I))


def strip_noise(text: str) -> str:
    """Remove the parts of a chapter where a term may legitimately appear early.

    Code blocks, inline code and links are not prose; neither is the glossary
    aside that some chapters use to define a term in place.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text


def main() -> int:
    concepts = load()
    errors: list[str] = []
    warnings: list[str] = []

    # ── term-defined-twice ────────────────────────────────────────────────
    seen: dict[str, str] = {}
    for c in concepts:
        for name in c.names:
            key = name.lower()
            if key in seen and seen[key] != c.term:
                errors.append(
                    f"term-defined-twice: '{name}' is claimed by both "
                    f"'{seen[key]}' and '{c.term}'"
                )
            seen[key] = c.term

    by_term = {c.term: c for c in concepts}

    # ── term-never-defined / prerequisite-inversion ───────────────────────
    for c in concepts:
        for dep in c.depends_on:
            target = by_term.get(dep)
            if target is None:
                errors.append(
                    f"term-never-defined: '{c.term}' depends on '{dep}', "
                    f"which no concept defines"
                )
                continue
            if target.defined_in > c.defined_in:
                errors.append(
                    f"prerequisite-inversion: '{c.term}' (ch. {c.defined_in}) "
                    f"depends on '{dep}' (ch. {target.defined_in}) — "
                    f"the reading order cannot work"
                )

    # ── term-used-before-defined / orphan-concept ─────────────────────────
    chapters = chapter_files()
    prose = {n: strip_noise(p.read_text(encoding="utf-8")) for n, p in chapters}

    def first_hit(
        names: list[str], corpus: dict[int, str] | None = None
    ) -> tuple[int, str] | None:
        if not names:
            return None
        corpus = prose if corpus is None else corpus
        pattern = re.compile("|".join(name_pattern(n) for n in names), re.I)
        for number in sorted(corpus):
            for para in paragraphs(corpus[number]):
                if pattern.search(para):
                    return number, para
        return None

    for c in concepts:
        # Orphan detection looks for EVERY name, including the ordinary-English
        # ones. A term whose only distinctive synonym is unused is not an orphan
        # if the book says "database" on every other page.
        if chapters and first_hit(c.names) is None:
            warnings.append(
                f"orphan-concept: '{c.term}' is in the ledger but never used"
            )
            continue

        # Used-before-defined, by contrast, looks only at the distinctive names,
        # so an ordinary word cannot produce a false failure that blocks a build.
        found = first_hit(c.scannable_names)
        if found is None:
            continue
        number, para = found
        if number >= c.defined_in or signposts(para, c.defined_in):
            continue
        errors.append(
            f"term-used-before-defined: '{c.term}' is used in ch. {number} "
            f"but defined in ch. {c.defined_in} — either move the definition, "
            f"reword, or signpost it with an explicit \"Chapter {c.defined_in}\""
        )

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    print(
        f"\nchecked {len(concepts)} concepts against {len(chapters)} chapters: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return EXIT_PRECONDITION_FAILED if errors else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
