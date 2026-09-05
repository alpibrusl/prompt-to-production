# Contributing

*Prompt to Production* is a manuscript kept as source, built by
[content-kit](https://github.com/alpibrusl/content-kit). Corrections and
improvements are welcome — this page is what makes one easy to merge.

## Read this first: two licences

This repository holds two kinds of work under two different licences, and
which one applies to your change decides what you are agreeing to:

| what | licence | means |
|---|---|---|
| `chapters/`, `glossary.yaml` | **CC BY-NC 4.0** | share and adapt with credit, no commercial use |
| `Makefile`, `style.css`, `cohort/`, `scripts/`, CI | **EUPL-1.2** | use, modify and redistribute, including commercially |

[`COPYING.md`](COPYING.md) is the authority on the split. By opening a pull
request you agree your contribution is licensed under whichever of the two
covers the files you touched.

## Setting up

```bash
python -m pip install "bookkit @ git+https://github.com/alpibrusl/content-kit@main#subdirectory=packages/bookkit"
python -m pip install "cohortkit @ git+https://github.com/alpibrusl/cohort-kit@main"
```

Building the PDF also needs Pango, which is a system library rather than a
Python one — `brew install pango` on macOS, `apt install libpango-1.0-0
libpangoft2-1.0-0` on Debian.

## What CI will check

```bash
make check         # the concept ledger: no term used before it is defined
make prose         # house style, warnings only
make cohort-check  # the curriculum against this book's chapters
make epub && make pdf
```

`make check` exits non-zero and will fail the build. `make prose` never fails
a build, but `make prose-fix` applies the mechanical corrections and you should
run it.

## The concept ledger

`glossary.yaml` is the book's canon: every term it teaches, the one definition
it commits to, and the one analogy it uses for that idea throughout. `make
check` lints the manuscript against it.

Introducing a term in prose without adding it to the ledger will fail. So will
using one before the chapter that defines it, unless the reference is
signposted forward. This is deliberate — it is the discipline the book asks of
its reader, applied to the book.

## Derived files are not source

`GLOSSARY.md`, `WORKED-EXAMPLE.md` where it exists, and everything under
`build/` are generated and gitignored. Edit `glossary.yaml` and the generator
scripts, never their output — a pull request editing a derived file will be
overwritten by the next `make`.

## Prose changes

**Match the voice.** `CLAUDE.md` has a `## Voice` section written down
precisely so "sound like the other chapters" is something a contributor can
actually act on. It is short and worth reading before rewriting a paragraph.

**Keep the examples this book's own.** The four volumes share an argument in
places and a running example in three of them, and `bookkit check duplication
--against ../prompt-to-evidence` measures how much. Parallel reasoning is
fine; the same sentences are not.

**Numbers must reproduce.** Every figure in this book comes from a fixture that
generates it. If you change one, say which command produces it.

## Reporting a problem

Open an issue. For a factual error, quote the sentence and say what is wrong
with it — that is a more useful issue than a suggested rewrite, because the
correction and the wording are separate decisions.
