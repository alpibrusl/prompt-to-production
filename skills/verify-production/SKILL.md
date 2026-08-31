---
name: verify-production
description: Use this skill before telling a non-engineer user that code, a feature, or a project is "done," "working," "ready," "production-ready," or "safe to ship/launch/go live" — and whenever the user directly asks something like "is this ready," "can I ship this," "are we good to go live," "is this safe to launch," or "what's left before real users touch this." Runs the pre-launch checklist from the book *Prompt to Production* against the actual project — real files, CI config, git history — instead of a general impression, and is explicit about which items it verified versus which it can't and must ask a human about. Do not use it for routine mid-task coding work (refactoring, debugging one failing test, writing a function) that isn't heading toward a readiness verdict — only when a readiness or shipping claim is about to be made or has been asked for.
---

# Verify Production

This skill exists because "it works" and "it's ready for real users" are
different claims, and an agent that only checks the first one while
implying the second is doing the exact thing the book *Prompt to
Production* (this repo's own manuscript, under `chapters/`) teaches
non-engineers to watch out for. This skill is that book's closing
checklist, run by the agent on itself, before the human ever has to ask
for it.

## The one rule that matters more than the checklist

The checklist items split into two kinds, and treating them the same way
defeats the whole point of this skill:

- **Checkable facts** — something a file, a config, or a command can
  actually settle. Go look. Report a real verdict.
- **Facts about something that *happened*** — a restore that was
  performed, a rollback that was rehearsed, a person who is known to be on
  the hook when things break. No amount of reading the repository proves
  these. A backup job existing in the infra config is evidence someone
  *configured* backups, not that anyone has ever *restored* from one — and
  those are different claims with very different risk if you're wrong.

Marking the second kind "done" because the machinery for it exists is the
single most misleading thing this skill could do, because it's exactly the
gap the book spends a whole chapter on: readiness is not a property of the
software, it's a relationship between the software and what's being asked
of it, and the events nobody has actually rehearsed are where that
relationship breaks first. When in doubt about which kind an item is,
`references/minimum-bar-checklist.md` tags every item explicitly.

## Workflow

1. **Decide the scope.** If this is a genuine pre-launch review (the user
   is asking "are we ready," or context makes clear real users are about to
   show up), run the full checklist. If it's a lighter sanity check mid-
   conversation, the short version (5 items, in
   `references/minimum-bar-checklist.md`) covers the highest-leverage gaps
   for a fraction of the effort. If it's ambiguous, ask which is wanted
   rather than guessing — a full pass on a throwaway prototype wastes the
   user's time, and a short pass on something handling real payments
   understates the risk.

2. **Read `references/minimum-bar-checklist.md`** for the full item list,
   each one tagged `[checkable]`, `[ask-human]`, or `[mixed]`, with
   inspection notes for what "checkable" actually means for that item.

3. **For checkable items, actually inspect the project** — read the
   relevant files, run safe read-only commands (`git log`, `git remote -v`,
   grep for patterns, look for CI/IaC config), rather than answering from a
   general impression of the codebase. Name what you found, specifically
   — "no workflow under `.github/workflows` runs on `pull_request`" is
   useful; "tests might not run automatically" is not.

4. **For ask-human and the human half of mixed items, actually ask** —
   don't silently assume a restore was tested just because backups are
   configured, and don't skip the question because it feels like it should
   be fine. If the user's answer is confident but vague ("yeah we tested
   that a while back"), it's fine to record that as their answer — the
   skill's job is to make sure the question got asked, not to interrogate
   the human's honesty.

5. **Report the results** using the format below, then close with the
   book's own framing question, because it's what determines how seriously
   to take whatever gaps turned up.

## Output format

For each section of the checklist actually run (full or short), a table
with one row per checklist item — resist splitting a `[mixed]` item into
two rows even though it has a checkable half and an ask-human half; the
guidance below keeps it to one row without burying either half.

| Item | Status | Detail |
|---|---|---|
| Secrets in repo history | ❌ Not done | `git log -p` shows an AWS key committed in `a3f9c1` (later removed but still in history) |
| Database backed up and restore actually performed | ❓ Ask | Automated snapshot found in `infra/db.tf` — but that only covers the backup half. Whether a restore has ever actually been performed is not visible from the repo; confirm with the team. |
| Outbound retry logic is backed off and safe to repeat | ➖ N/A | No outbound calls to third parties exist in this codebase yet — nothing to configure. Worth revisiting the moment an integration is added. |
| ... | | |

Four statuses, used honestly rather than squeezed to fit three:

- **✅ Done** — checkable, and it checks out.
- **❌ Not done** — checkable, and it's missing or fails.
- **➖ N/A** — the thing the item protects against doesn't exist yet in this
  project (no database, no outbound calls, no personal data collected) —
  don't call this "not done," which would imply a gap that isn't actually
  there. Say plainly what's missing that would make the item apply.
- **❓ Ask** — the whole item, or the part that actually matters, is a fact
  only a human can confirm. This is also the right status for a `[mixed]`
  item whose checkable half passed but whose human half is still open —
  the item isn't genuinely done until both halves are, so don't let a
  passing checkable half round up to ✅. Use the Detail column to say
  exactly what was found versus what's still an open question, so a reader
  skimming only the Status column doesn't miss that something real is
  still unconfirmed.

Then close with, verbatim or close to it:

> **What happens when this breaks, and who is harmed?**
>
> That's what decides how urgent the gaps above actually are. The same
> missing item is a Tuesday for a weekend prototype and a real liability
> for something holding customer data or payments — answer it before
> deciding what to fix first.

Don't soften a real gap to make the summary sound better, and don't treat
an "ask-human, unconfirmed" item as equivalent to a checked failure — say
plainly that it's unconfirmed and needs a real answer, not a guess from
either side.
