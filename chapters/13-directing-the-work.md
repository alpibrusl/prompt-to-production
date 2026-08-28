# Directing the Work

> **Part V — Working With the Agent**

Everything so far has been vocabulary and consequence. This chapter turns it back into instructions: how to ask for work, how to judge what comes back, and how to say no.

You now know roughly a hundred and forty things exist that you did not know existed at the start. That knowledge is only worth something if it changes what you ask for.

## The asymmetry

Start with the thing that governs all of this.

**An agent will build almost anything you ask for and will rarely tell you what you forgot to ask for.**

This is not a defect. It is a direct consequence of how it works: you asked a question, it answered that question, well. It is not withholding the rest. The rest was never in scope, because you did not put it there.

Which means your leverage is almost entirely in the asking. The code will be fine. Whether the *system* is fine depends on whether the request included the things this book has spent twelve chapters naming.

## Say what done means

A **specification** is a written statement of what should be built and how you will know it was. **Acceptance criteria** are the specific, checkable conditions that decide whether the work is finished.

The distinction between a vague request and a good one is not length. It is whether it contains anything falsifiable.

Vague:

> "Add user authentication."

Better:

> "Add email and password authentication. Passwords hashed with bcrypt, never stored or logged in plain text. Login is rate limited to five attempts per email per fifteen minutes. Sessions expire after thirty days. There is a password reset by email link, valid for one hour, single use. Write tests for: successful login, wrong password, expired session, reset link reuse, and rate limit triggering. Nothing new goes in the repository as a secret."

The second is longer, but notice what it actually is. Every clause is a thing from an earlier chapter. Hashing and rate limiting from Chapter 12. Not logging secrets from Chapters 5 and 10. Tests including failure cases from Chapter 6. It is not a technical specification — you did not specify a single implementation choice — it is a *completeness* specification, and it is written entirely in vocabulary you now have.

Write acceptance criteria before the work, not after. Criteria written afterwards describe what was built, which is not the same thing and never catches anything.

## Small pieces

**Scope** is the agreed boundary of what a piece of work includes. **Scope creep** is that boundary moving quietly while nobody says so.

Ask for small things. A request that touches one area, that you can describe in a few sentences, that produces a change you can look at in one sitting.

The reason is not process hygiene. It is that a large change is genuinely unreviewable — by you, and honestly by anyone. A change touching thirty files does something you did not ask for, always, and neither you nor the agent will notice, because the noticing budget was spent by file eight.

Small changes also fail cheaply. If a change to one thing breaks, you know what broke it. If a change to nine things breaks, you have an investigation. This is Chapter 4's argument for small commits and Chapter 11's argument for small blast radius, arriving in the form of a working habit.

**Minimum viable product** — MVP — is the smallest version that genuinely tests whether the idea works. And it is worth being precise about what it reduces, because this term is abused: an MVP is a deliberate reduction in *features*, never a reduction in the standards of the next chapter. Fewer things, done properly. Not everything, done badly. "It's just an MVP" is not a reason to skip backups, secrets handling, or authorization checks — it is a reason to have three screens instead of twelve.

## Reviewing what you cannot read

Chapter 4 promised this and here it is.

You cannot read the code well enough to verify it is correct. That is simply true and pretending otherwise helps nobody. But you can read a *diff* — the lines added and removed — for shape, and shape tells you more than people expect. Six questions, none of which require understanding the code:

**Does the size match the request?** You asked for a date format change; the diff touches twenty-two files. Something else happened. It might be legitimate; ask what.

**Are there files you do not recognise?** New dependencies, new configuration, new credentials-shaped things. Each deserves a sentence of explanation.

**Does anything look like a secret?** A long random string in a source file is worth asking about every time, even when the answer is innocent. Chapter 5.

**Did tests change?** New feature with no new tests is a gap. Existing tests *modified* is the one to look at hardest — sometimes a test is corrected, and sometimes a test is loosened until it passes, and those look identical in a diff. Ask which.

**Is anything deleted that you did not expect?** Removed error handling, removed validation, a removed check. Deletions are quieter than additions and more often wrong.

**Does the description match what happened?** A PR titled "fix typo" containing a schema migration is the highest-signal thing you will ever see in a code review, and it does not require reading a line of the code.

Then, the questions that are not about the diff at all — the ones this book equipped you for:

> "What happens if this is called twice?" (Chapter 8, 11)
> "What happens if the service it calls does not respond?" (Chapter 11)
> "Does this check the caller is allowed to do it, on the backend?" (Chapter 3, 12)
> "How would I know if this broke in production?" (Chapter 10)
> "Can this be rolled back?" (Chapter 9)

None require reading code. All catch real problems.

## Debt

**Technical debt** is the accumulated cost of shortcuts, paid as slowness every time you change the system afterwards.

The metaphor is a loan, and it is worth using properly rather than as a general term for "code I dislike". Taking a loan is often correct — you get something now and pay later, which is exactly right when there is a deadline or when you are not yet sure the feature will survive. It becomes dangerous only when nobody is tracking the balance.

The interest is real and compounds. Every shortcut makes the next change slower. A project that has taken shortcuts for a year is one where a small feature takes three weeks and nobody can explain why to anyone outside.

So: take debt deliberately, say out loud that you are taking it, and write down what it was. "We are hardcoding this list for now because we do not know if this feature will survive; if it does, it needs to come from the database." That sentence, in a commit message or an issue, is the difference between a decision and a mess.

**Refactor** means changing how code is written without changing what it does, to make the next change easier. It is how debt gets repaid. And notice the dependency: refactoring is only safe when tests exist to prove nothing moved — otherwise you are rewriting working code with no way to know if it still works. This is Chapter 6's argument, arriving with money attached.

## Working in loops

**Iteration** is one cycle of building a small piece, putting it in front of reality, and adjusting.

The specific failure this prevents is building for three months against your own assumptions and discovering at the end that the thing nobody wanted was built beautifully. Working software in front of a real user, early, is the only reliable way to find out that your assumptions were wrong while it is still cheap.

A rhythm that works:

1. Smallest useful version of one thing, with acceptance criteria written first.
2. Agent builds it, with tests.
3. Review the diff for shape; ask the five questions.
4. Merge through the pipeline; deploy behind a feature flag if it is risky.
5. Watch it — Chapter 10 — with a real user if you can.
6. Next thing.

Not sophisticated. It is what almost every functional software team does, and the discipline is entirely in doing it in small pieces rather than large ones.

## Saying no

Last, the thing that is genuinely hard and rarely written down.

The agent will confidently suggest approaches. Most will be reasonable. Some will be wrong for your situation in ways it cannot know, because it does not know your budget, your users, your legal exposure, or how much operational work you can absorb.

It is legitimate — and often correct — to say:

> "That is more infrastructure than we need. What is the simplest thing that works for a hundred users?"

> "I don't want another dependency for this. Can we do it without?"

> "Do not refactor that while fixing this. One change at a time."

> "Stop. Explain what you are about to do before doing it."

That last one is worth using more than feels natural. An explanation costs seconds; an unwanted change to your infrastructure costs an afternoon and sometimes a database.

The role you are in is not junior. You are not a novice being helped by an expert. You are the person who is accountable for the system, directing someone who is faster than you at writing code and has no stake in the outcome. Those are different jobs, and the second one does not outrank the first.

## What to ask for

> "Before you build this, tell me what you are going to do and what you would need to change. Then wait."

Turn a large request into a plan you can react to. The single most useful habit in this chapter.

> "Give me acceptance criteria for this before we start, including the failure cases."

Makes "done" checkable, and reliably surfaces a case neither of you had considered.

> "Explain this diff to me in plain language. What changed, what could break, and what did you decide that I should know about?"

The review question for someone who cannot read every line. That last clause matters most — it invites disclosure of judgement calls that are invisible in a diff.

> "Keep this change small. If it needs to touch more than a few files, tell me why first."
