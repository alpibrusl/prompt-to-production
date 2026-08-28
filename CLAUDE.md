# Project conventions

## Author identity — do not guess

The author of this book is:

    Alfonso Sastre <alfonso@alpibru.com>

Use exactly this for `book.yaml`, for git commit authorship, and anywhere else
an author is named. Do not infer a surname from an email address, an org name,
or a GitHub handle — an earlier session did exactly that and put a fabricated
name on the title page, the copyright page and the EPUB metadata.

If a field about a real person is unknown, leave it blank and ask. That applies
to the author bio too: `author.bio` is deliberately empty, and the
`about_author` back-matter section is commented out in `book.yaml` until there
is a real bio to print. Do not write one.

## The manuscript is source

Markdown in `chapters/` is the source; everything in `build/` is derived and
gitignored, as is `GLOSSARY.md`. Never edit `GLOSSARY.md` — it is generated from
`glossary.yaml` by `make glossary`.

## The concept ledger and the gate

`glossary.yaml` is the canon: every term the book teaches, with one definition,
one committed analogy, the defining chapter, and prerequisite terms.

`make check` lints the manuscript against it and exits 8 on error. It runs in
CI on every push and pull request. When adding prose:

- Define a term before using it, or signpost the forward reference explicitly
  with "(Chapter N)" — the linter allows a signposted one and rejects a bare one.
- Add any new term to `glossary.yaml` rather than defining it only in prose.
- Keep an analogy consistent with the one the ledger commits to.

## Build

    make check    # the gate
    make epub / make html / make pdf
    make all      # check + epub + html (pdf needs Pango, see README)

## Licences

Manuscript CC BY-NC-SA 4.0; code EUPL-1.2. New files under `scripts/` need an
`SPDX-License-Identifier: EUPL-1.2` header. See `COPYING.md`.
