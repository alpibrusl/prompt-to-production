"""Generate GLOSSARY.md from glossary.yaml.

The ledger is source; the glossary is a build artifact. Editing GLOSSARY.md by
hand would create exactly the drift this book spends a chapter warning about,
which is why it is in .gitignore.

Prototypes the generated-glossary back matter proposed in alpibrusl/content-kit#11.
"""

# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

from pathlib import Path

from ledger import ROOT, load


def main() -> int:
    concepts = sorted(load(), key=lambda c: c.term.lower())
    lines = [
        "# Glossary",
        "",
        "Every term this book teaches, with the definition it commits to.",
        "The chapter number is where the term is introduced.",
        "",
    ]
    for c in concepts:
        definition = " ".join(c.definition.split())
        entry = f"**{c.term}** *(ch. {c.defined_in})*"
        if c.aka:
            entry += f" — also called {', '.join(c.aka)}"
        lines.append(entry)
        lines.append("")
        lines.append(f": {definition}")
        if c.analogy:
            lines.append(f"  *{' '.join(c.analogy.split())}*")
        lines.append("")

    out = Path(ROOT / "GLOSSARY.md")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} — {len(concepts)} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
