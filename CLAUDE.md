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
  "Chapters 6 and 7" and "Chapters 7 through 10" count as signposts too.
- Add any new term to `glossary.yaml` rather than defining it only in prose.
- Keep an analogy consistent with the one the ledger commits to.
- A single-word term that is unambiguous jargon opts into prose scanning with
  `scan: true`. Do not opt in an ordinary English word — the gate is only worth
  having while it is quiet enough to be believed. If a term's *alias* is the
  ordinary word, scan the distinctive name alone: `scan: ["known-answer test"]`.
- A chapter that deliberately introduces no term belongs in `teaches_no_terms`,
  with a comment saying why. Do not invent a term to silence that warning.

## Scope: this book does not teach reading code

Chapter 1 says "This book will not teach you to program," and the afterword
closes by naming what the book teaches instead — specify before building,
demand tests, make the pipeline the only path, watch the system rather than
inspect it, keep a way back — as the things "you do *instead of* understanding."

A reader has asked for the opposite: a Part on understanding the code, not just
the systems. It is the most natural request this book will ever receive, and it
was declined deliberately. Comprehension is not the skill this series hands
back; verification is, and promising the first would contradict the argument the
whole set rests on.

What the book already offers instead is Chapter 14's six questions for reading a
*diff* for shape — which is not "learning to program" and is worth pointing a
disappointed reader at. Do not add a code-reading chapter, and do not soften
Chapter 1's sentence into an implied promise.

## Ledgerly is shared canon

Ledgerly appears in *Production*, *Ledger* and *Decision*. It is one company,
not three companies with the same name, and a reader who buys two books will
notice. **Prompt to Ledger owns the fixture**; the other books consume it and
must not invent figures that contradict it.

| | |
|---|---|
| what it is | an invoicing tool for freelancers |
| cash in the bank | €180,000 |
| monthly costs | €35,000, or €42,000 once the already-committed hire lands |
| monthly revenue | €20,000, growing 4% a month |
| burn | costs *minus* revenue — €15,000 before that hire, €22,000 after |
| runway | **eleven months** |
| a fully loaded engineer | €7,000 a month |
| the seed round | €500,000 at a €2,000,000 pre-money valuation |

Two traps, both of which the series has already fallen into once:

**Runway is eleven, not twelve and not eighteen.** *Ledger* Chapter 9 walks
through all three: eighteen is what the agent *reported*, twelve is the naive
cash-divided-by-burn arithmetic, and eleven is the honest figure once 4% growth
and the committed hire are in the model. Quoting twelve as Ledgerly's runway
states the number that book exists to correct.

**Burn means costs minus revenue.** *Ledger* defines it that way and computes
with it. Using "burn" for gross monthly costs gives the same word two meanings
across the series, which is the one thing a concept ledger is meant to prevent.

Any new figure must be *computable* from the table above. Ledger's Chapter 9
recomputes correctly from these inputs, and so should anything added later.

## Absolutes

Distinguish a prescription from an assertion. "Never commit secrets" is a rule
of practice and its force is the point — keep it. "Writing code was never the
difficult part" is a claim about the world, and an absolute there invites a
reader to argue with the sentence instead of absorbing the lesson. When editing,
check `never`, `always`, `only`, `every`, `exactly`, `not negotiable`: keep them
in rules, soften them in claims.

## Voice

The house voice, written down because "sound like the other chapters" is not
something anyone — a person or an agent — can act on.

It is deliberately *not* an imitation of a named writer. A reader suggested one
as a reference and the register she was pointing at is right: practical,
concrete, unpretentious, example-first. But "is this Osmani enough?" has no
answer, so it cannot be checked, taught, or handed to an agent, and an agent
told to imitate a person produces pastiche. What follows is the same target,
stated as rules that can actually be applied.

**Explain the thing; do not announce that you are about to.** This is the one
that matters most, and the one this manuscript gets wrong most often. "This
chapter is that path." "Now the shape." "Here is what they are for." "The last
idea here is what turns all this from data into decisions." Every one of these
is the narrator stepping out from behind the material to describe the material.
Cut the announcement and start with the content — the reader can see a new
section beginning; they do not need to be told that one is beginning. A
transition earns its place only when it carries information the next paragraph
does not, which is rare.

**One metaphor, stated once, and never explained.** An analogy that has to be
unpacked over the following three sentences was not doing its job in the first
one. The ledger already commits each concept to a single analogy; using it means
dropping it in and moving on, not returning to admire it. Where an image has a
famous source, either credit it or do not use it — an unattributed allusion
reads as borrowed profundity to every reader who recognises it.

**Concrete before abstract, always.** Name the file, the command, the number,
the amount of time. "The budget alert takes four minutes" beats any sentence
about the importance of cost awareness. Ledgerly exists so that every claim in
the book has somewhere specific to land; use it rather than reaching for a
hypothetical.

**Prescriptions may be absolute; claims about the world may not.** See
[Absolutes](#absolutes) above — the distinction is load-bearing and predates
this section.

**Jargon is compression, not decoration.** A word that saves a sentence earns
its place. Define it once, in the chapter the ledger assigns it, and then use it
plainly without re-explaining or apologising for it.

**Write to a capable reader who happens not to know this yet.** Not a beginner
to be protected, not a peer to be impressed. No flattery, no "as we all know",
no warnings that a topic is about to get difficult. Say the thing.

**Sentence rhythm.** Vary it, and let the short sentence be a real one rather
than a drum-beat. A one-line paragraph is a strong instrument with a small
budget: it is right for a definition, for the gloss under a suggested prompt,
and occasionally for a line the chapter genuinely turns on. It is wrong as a
way to make an ordinary transition sound consequential.

### The mechanical part

`make prose` checks what a machine can honestly check, and reports warnings
only — prose is not a build failure. `make prose-fix` applies the corrections
that need no judgement.

- **No comma before a restrictive because-clause.** "Worth knowing by name
  because it is the answer" — not "by name, because". The comma belongs only
  when the main clause is negative (where it changes the meaning) or when the
  clause is a genuine afterthought. This one is a Spanish habit carried into
  English, and a reader spotted it before the linter did.
- **No "because … is not because."** Two because-clauses in a sentence are fine
  when they are a pair ("not because X, but because Y"); they are hard to follow
  when the second is the predicate of the first.

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
time the reader gets there. The term linter used to carry a chapter-0
exemption for this file specifically; that exemption is gone, on purpose,
because nothing needs it now. It is also no longer this repository's to
re-add — the linter is `bookkit check terms` upstream — so if a
front-matter special case ever looks necessary again, check whether this is
still true first, and then make the case upstream rather than forking it.

## Audio

`make audiobook` emits a podcastkit project under `build/audiobook/` — derived,
gitignored, one episode per chapter. Rendering it to MP3 needs a TTS backend and
is not wired into CI, because it costs money per character on the paid backends
and hours of CPU on the free ones.

The conversion drops fenced code blocks and excludes the glossary, which is
correct for audio. Bear that in mind when adding prose: anything that exists
*only* inside a code fence will not reach a listener.

## Licences

Manuscript CC BY-NC 4.0; code EUPL-1.2. New code files in this repository (the
`Makefile`, `style.css`, CI workflows) need an `SPDX-License-Identifier:
EUPL-1.2` header. See `COPYING.md`.
