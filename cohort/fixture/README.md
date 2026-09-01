# The fixture

One seeded repo, reused across Sessions 3, 4, and 7 rather than inventing
new demo material each time — students meet the same broken thing from
different angles.

It's Ledgerly's invoicing service, standing in for the fictional company
the book's own chapters already follow. The unauthorized-access bug it
plants is the exact one Chapter 12 narrates — `GET /invoices/:id` with no
check that the caller actually owns that invoice — using the same invoice
number (8812) Chapter 10's log excerpt already showed students. Anyone
who's read the book meets a familiar bug made concrete, not a new example
to learn from scratch.

## Generate it

```bash
./setup.sh                      # → ./ledgerly-invoicing
./setup.sh /path/to/output       # or choose where
```

Run this **fresh before each session** that uses the fixture, not once at
the start of the cohort. A student who's seen a previous run's fixture
loses the "cold" reaction Session 3's exercise depends on, and nothing
about the fixture is meant to persist between sessions or cohorts.

The generated repo is disposable: this script is the source, the repo it
produces is a build artifact, and `.gitignore` here keeps it out of the
`cohort-kit` repository the same way `build/` stays out of the book's own.

## What's planted, and which session uses it

- **Session 3** — a Stripe-style secret committed, then removed from
  tracking in a later commit but still fully readable via
  `git log -p -- .env`. The point isn't finding it; it's the group
  correctly concluding that removing the file didn't fix anything.
- **Session 4** — `.github/workflows/` and `tests/` are both empty.
  Nothing blocks a bad merge.
- **Session 7** — the unauthorized `/invoices/:id` route, revisited as
  something to catch in review rather than something to go find.
- **Session 8 (capstone)** — a real target for the `verify-production`
  skill, for anyone without a project of their own to point it at.
