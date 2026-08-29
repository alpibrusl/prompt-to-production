# Directing the Work

> **Part V — Working With the Agent**

Everything so far has been vocabulary and consequence. This chapter turns it back into instructions: how to ask for work, how to judge what comes back, and how to say no.

You now know roughly a hundred and forty things exist that you did not know existed at the start. That knowledge is only worth something if it changes what you ask for.

## The asymmetry

Start with the thing that governs all of this.

**An agent will build almost anything you ask for and will rarely tell you what you forgot to ask for.**

This is not a defect. It is a direct consequence of how it works: you asked a question, it answered that question, well. It is not withholding the rest. The rest was never in scope, because you did not put it there.

Which means your leverage is mostly in the asking. The code will usually be fine, and where it is not, the tests and reviews of earlier chapters are what catch it. Whether the *system* is fine depends on whether the request included the things this book has spent twelve chapters naming.

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

## Reviewing at speed

Chapter 4 named the shift plainly: an agent can produce four thousand lines in thirty seconds, your reading speed has not changed, and review is now the only bottleneck left. The six questions above assume you are sitting with one diff. In practice you will not get one diff — you will get a session that produces ten or twenty of them before lunch, and "read every line of every one closely" is advice that cannot survive contact with that volume. Followed literally, it produces the opposite of what it promises: a reviewer too worn down by the fifth diff to look hard at the one that actually mattered.

### Not every diff earns the same read

The fix is not reading faster. It is reading unevenly, on purpose, using the logic Chapter 11 uses for blast radius: spend attention where a mistake is expensive, not evenly across everything that happens to arrive.

Before deciding how hard to look, three questions decide the depth:

- Does this touch money, authentication, or someone else's personal data?
- Is it hard to undo once it has run?
- Could it run in production, unattended, before a person would notice?

Any yes earns the full six-question pass from the previous section, read closely, no exceptions. All no — a copy change, a new internal report, a rename — earns a real look rather than a rubber stamp, but not the same minutes. This is not laziness dressed up as a system; it is the same proportional attention Chapter 11 asks for during an incident, applied before one happens instead of during it.

### Four patterns worth stopping for

Whatever the depth of the pass, four things are worth specifically watching for, because they are quiet, common, and none of them require reading the implementation — only the claim being made about it.

**Confidence that is not evidence.** "This library handles that." "This is safe to run twice." "The API returns X." Said with the same flat certainty whether the agent has verified it or is pattern-matching from something similar it has seen before, and you cannot tell which from the tone alone. When a sentence like this is load-bearing for a decision you are about to make and move on from, check the one line of documentation or run the one command rather than trusting the sentence. The check is usually faster than the argument you would have later if it was wrong.

**A simple problem solved with a complicated one.** More configuration, more layers, more "so this can be extended later" than the request needed. Sometimes this is right — software does eventually grow into the abstraction. The question that separates the two cases is one this chapter already gave you, for scope: if you cannot get a one-sentence reason for a piece existing, ask for it. An MVP that quietly grew three configuration options nobody asked for is scope creep wearing an engineering justification.

**A dependency that arrived uninvited.** Chapter 2 covered why a dependency is a relationship, not a favour — the cost does not show up until later, which is exactly why it needs to be caught now. Watch for it appearing as a side effect: "added a small library to handle X" inside a diff about something else entirely. Ask the same question Chapter 2 asks at the start of a project, every time it happens rather than only then: what does it save us, and would we notice if it disappeared.

**A decision re-derived from scratch, possibly differently.** Chapter 4 already made the structural point — nothing survives between conversations except what is written down. The failure this produces is not the agent saying "I don't remember." It is the agent confidently reasoning to an answer again, with no sign anything changed, and sometimes arriving somewhere slightly different than it did last month. If a project has a decision that must not silently drift — a pricing rule, a data-retention period, who is allowed to see what — write it down somewhere read at the start of every session. A decision that only exists in an old commit is a decision that will eventually be re-made.

None of these four ask you to read code. They ask whether a specific *claim* holds up — which is the register this whole chapter has stayed in since the first page, and it is the only one that scales past the first diff of the morning.

## When you cannot judge the choice

Here is a situation that will happen to you within a week of starting anything real.

The agent stops and offers you a choice. Postgres or MongoDB. REST or GraphQL. A monolith or separate services. Vercel or AWS. It lays out three options with trade-offs, all of which sound reasonable, none of which you can evaluate, and it waits.

You have no basis to choose. None. The words are not the problem — you could look each of them up — the problem is that the trade-off is between consequences you have never experienced.

This section is what to do in that moment, and it is not "go and learn databases".

### Refuse the menu

The first move is to notice what has happened. **A menu is a decision being handed back to you by the party better equipped to make it.**

The agent has read more about these options than you will in a decade. Presenting them as a neutral list is not deference; it is an abdication, and it is often a sign that the question was not thought about very hard. So push it back:

> "Pick one. Tell me why, tell me what you are trading away, and tell me what would make you change your mind."

That last clause matters more than the others. A recommendation with no stated conditions is a preference. A recommendation that says "choose this unless you expect more than a few thousand writes a second, in which case reconsider" is a piece of engineering you can actually hold on to — and check against later.

### Convert the question into one you can answer

You cannot evaluate "Postgres versus MongoDB". You can evaluate consequences, and you are in fact better placed than the agent to weigh those, because they are consequences for *you*.

Five questions do most of the work, and none of them require knowing what the options are:

**"Which of these is hardest to undo, and what would undoing it cost?"**
This is the single most useful question in this section. Most decisions are cheap to reverse and deserve about a minute of your attention. A few are expensive — the database, the cloud provider, the shape of your data — and those deserve real time. A **reversible decision** is one you can walk back later for roughly the cost of the work; an irreversible one changes what is possible afterwards. Spend your worry proportionally, and notice that the agent will present both kinds in exactly the same tone.

**"Which is the boring, common choice?"**
Ask this without embarrassment. The widely-used option has more documentation, more answers to more questions, more people who can be hired to help, and — not incidentally — the agent itself has seen vastly more of it, so its advice about that option will be better. Novelty is a real cost, and you pay it alone, in the dark, at the moment something breaks. For a first system, "what would most teams do here?" is a better question than "what is best?"

**"What does each cost per month now, and at ten times this size?"**
Concrete, checkable, and yours to judge. It also flushes out the option that is free until it suddenly is not.

**"Which of these adds something I have to operate?"**
Every component you run yourself is a thing that can break at three in the morning — Chapter 11's whole subject. An option that hands the operating to somebody else, as a managed service, is often worth real money for that reason alone, and the cost of running it is rarely in the comparison as presented.

**"What happens if we simply do not decide this now?"**
A surprising share of these choices are premature. If the honest answer is "nothing, for six months", then defer it, and by the time you must choose you will know things you do not know today.

### Lock-in

One thing worth naming because it hides inside otherwise sensible choices: **lock-in** is how hard it would be to leave. Some options are easy to adopt and very hard to walk away from — because your data ends up in a shape only they read, or because the way you build assumes their particular way of doing things.

Lock-in is not automatically bad. Accepting it in exchange for not operating something yourself is frequently the right trade for a small team. But it should be a decision rather than a discovery, and "how hard would it be to leave this later?" is a question you can ask and understand the answer to.

### When to spend money on a human

Refusing the menu handles most cases. A few genuinely warrant a real engineer, for an hour, paid:

- The decision is expensive or impossible to reverse.
- It commits you to a recurring cost that scales with success.
- It touches money, or other people's personal data.
- It locks you to one vendor for the foreseeable future.

Those four are where a wrong answer compounds for years, and an hour of somebody who has lived through the consequences is the best-value money in this entire book. You are not buying a decision; you are buying a sanity check on the reasoning you already have.

### The point

"I do not know enough to judge this" is a complete and respectable position. It is also not the end of the conversation.

The move is not to go and learn the subject. It is to **change the question into one you can answer** — about reversibility, cost, operational burden, and how hard it would be to leave. Those are business questions wearing technical clothes, and you were always the right person to answer them.

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

> "Anything in here you are not fully certain about? Any dependency that snuck in that I did not ask for? Anything more complicated than the request needed?"

A direct pass at the four patterns above, asked in one breath rather than hunted for line by line. It works because it asks about the claim, not the code — and it is worth asking every time volume is high, not only when something feels off.

> "Keep this change small. If it needs to touch more than a few files, tell me why first."

> "Don't give me a menu. Pick one, tell me why, tell me what you are trading away, and tell me what would make you change your mind."

For any choice you cannot evaluate. The last clause is the one that turns a preference into something you can check against later.

> "Which of these is hardest to undo, what does each cost per month, and which one adds something I have to operate myself?"

Three questions you can answer even when the options mean nothing to you.
