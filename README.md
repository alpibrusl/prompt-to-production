# Prompt to Production

**The software engineering your AI agent assumes you already know.**

A short book for people who can now get working software without having learned
to program — founders, product managers, designers, analysts — and who have
discovered that working code is not the same thing as a system you can run.

It teaches the vocabulary and the map: what the parts of a system are called,
what each is for, what goes wrong with each, and what "done properly" looks
like. Not how to write code. How to *ask for* what you now know exists.

> An agent will build almost anything you ask for, and will rarely tell you what
> you forgot to ask for.

## Contents

| | Part | Chapters |
|---|---|---|
| **I** | The Ground | The handoff · where code lives · the shape of an app |
| **II** | Keeping It | Version control · environments and secrets · tests |
| **III** | Shipping It | Infrastructure · infrastructure as code · CI/CD |
| **IV** | Living With It | Observability · when it breaks · security and cost |
| **V** | Working With the Agent | Directing the work · the minimum bar |

Roughly 24,000 words and 146 defined terms, all collected in a generated
glossary.

## The book is source

The manuscript is Markdown. The EPUB and PDF are build artifacts — derived from
the source, never committed, rebuilt on demand. This is
[bookkit](https://github.com/alpibrusl/content-kit)'s premise, and it is also
the book's own subject, so the repository is a small worked example of what the
book describes.

```bash
pip install "content-kit-core @ git+https://github.com/alpibrusl/content-kit@main#subdirectory=packages/core"
pip install "bookkit[epub] @ git+https://github.com/alpibrusl/content-kit@main#subdirectory=packages/bookkit"

make check     # lint the manuscript against the concept ledger
make epub      # → build/prompt-to-production.epub
make html      # → build/prompt-to-production.html
make all       # check + build everything
```

## The concept ledger

`glossary.yaml` is the book's canon: every term it teaches, the one definition
it commits to, the one analogy it uses for that idea, which chapter defines it,
and which terms must be understood first.

```yaml
- term: "idempotent"
  aka: ["idempotence", "idempotency"]
  definition: >-
    Safe to repeat: running it twice leaves you in the same place as running
    it once.
  analogy: "A light switch labelled ON — pressing it again does not make the room brighter."
  depends_on: ["declarative"]
  defined_in: 8
  scan: true
```

Two things are generated from it, so the definition exists in exactly one place:

- **`GLOSSARY.md`** — the back matter, built by `make glossary`. Not committed.
- **`make check`** — the continuity gate, described below.

## The gate

A book that teaches jargon has one dominant editorial failure mode: using a term
before defining it. `scripts/check_terms.py` makes that a build failure rather
than a thing a proofreader might notice.

| rule | | |
|---|---|---|
| `term-used-before-defined` | error | a term appears in prose before its chapter, with no signpost |
| `term-never-defined` | error | a `depends_on` entry no concept defines |
| `term-defined-twice` | error | two concepts claim the same name |
| `prerequisite-inversion` | error | A depends on B, but A is defined first |
| `orphan-concept` | warning | in the ledger, never used in the prose |

It exits `8` on error, following bookkit's convention, and runs on every pull
request. Two deliberate design choices keep it quiet enough to be trusted:

**Signposted forward references are allowed.** "Containers (Chapter 7) package
the program…" is good writing, not an error — the reader is told exactly where
the definition lives. An *unsignposted* forward reference is the error, because
that is the one that strands a reader.

**Only distinctive names are scanned.** Ordinary English words — "test", "plan",
"state", "image" — appear constantly in prose that is not about the concept, and
flagging them would train everyone to ignore the gate, which is worse than not
having one. Multi-word terms and acronyms are scanned automatically; a single
word that is unambiguous jargon opts in with `scan: true`.

## Relationship to content-kit

This repository is downstream of
[alpibrusl/content-kit](https://github.com/alpibrusl/content-kit) and does not
modify it. bookkit is genre-neutral by design; the book-specific machinery lives
here.

The ledger and the linter are working prototypes of two proposals filed against
content-kit, built against real data rather than designed in the abstract:

- [#9](https://github.com/alpibrusl/content-kit/issues/9) — a genre-aware canon with a `Concept` model. `glossary.yaml` is that model, populated.
- [#10](https://github.com/alpibrusl/content-kit/issues/10) — genre-aware continuity rules. `check_terms.py` implements the term rules.
- [#11](https://github.com/alpibrusl/content-kit/issues/11) — a generated glossary as back matter. `build_glossary.py` does it locally.

If those land upstream, this repository deletes `scripts/` and gains a
`bible.yaml`. Two findings from writing the book are already fed back into the
issues: forward references need a signpost escape hatch, and prose scanning must
be conservative about ordinary English or the gate becomes noise.

## Licence

Manuscript: [CC BY-NC-SA 4.0](COPYING.md). Code: [EUPL-1.2](LICENSE), the
same licence as content-kit, so the prototypes here can move upstream without a
relicensing question. See [COPYING.md](COPYING.md).
