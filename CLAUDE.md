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

## Absolutes

Distinguish a prescription from an assertion. "Never commit secrets" is a rule
of practice and its force is the point — keep it. "Writing code was never the
difficult part" is a claim about the world, and an absolute there invites a
reader to argue with the sentence instead of absorbing the lesson. When editing,
check `never`, `always`, `only`, `every`, `exactly`, `not negotiable`: keep them
in rules, soften them in claims.

## Build

    make check    # the gate
    make epub / make html / make pdf
    make all      # check + epub + html (pdf needs Pango, see README)

## The afterword is a real chapter, not front matter

`chapters/17-a-note-from-the-author.md` used to be chapter 0, read before
Chapter 1. It moved to the end deliberately — it reads better as a closing
reflection than as philosophy in front of a frightened reader's first
question, and it is still narrated in the audiobook (back matter is not).

Because it is now numbered after everything else, it needs no special
treatment from the term linter: every term it uses is already defined by the
time the reader gets there. `check_terms.py` used to carry a chapter-0
exemption for this file specifically; that exemption is gone, on purpose,
because nothing needs it now. Do not re-add a front-matter special case
without checking whether this is still true.

## Audio

`make audiobook` emits a podcastkit project under `build/audiobook/` — derived,
gitignored, one episode per chapter. Rendering it to MP3 needs a TTS backend and
is not wired into CI, because it costs money per character on the paid backends
and hours of CPU on the free ones.

The conversion drops fenced code blocks and excludes the glossary, which is
correct for audio. Bear that in mind when adding prose: anything that exists
*only* inside a code fence will not reach a listener.

## Licences

Manuscript CC BY-NC 4.0; code EUPL-1.2. New files under `scripts/` need an
`SPDX-License-Identifier: EUPL-1.2` header. See `COPYING.md`.
