# The Minimum Bar

The argument comes first because a checklist you do not believe in is one you will skip on the day it matters.

## What "ready" means

There is a moment coming when you have something that works and you want real people to use it. The question you will ask is "is it ready?", and the honest answer is that readiness is not a property of the software. It is a relationship between the software and what you are asking of it.

A prototype shown to three friendly users, holding no real data, that can be thrown away, needs almost none of what follows. A thing handling other people's money or personal information needs all of it. Most projects are somewhere between, and the useful question is not "am I finished" but:

**What happens when this breaks, and who is harmed?**

Everything below follows from your answer. If the honest reply is "I lose an afternoon", most of this is optional. If it is "a customer loses their data" or "we are in breach of a law", none of it is.

The tempting phrase to be wary of is *it's just an MVP*. Chapter 14 drew the line and it is worth restating because it is the specific rationalisation that leads to the bad version of this: an MVP reduces **features**, not **standards**. Three screens instead of twelve, absolutely. Three screens with no backups, no authorization checks and the database password in the repository is not a smaller product. It is the same product with a hidden liability attached.

## The bar

Before real users touch it. Roughly in order of what will hurt first.

### Not losing things

- [ ] Everything is in version control, with a remote copy that is not your laptop.
- [ ] The main branch is protected: no direct pushes, changes arrive by pull request.
- [ ] The database is backed up automatically, and **a restore has actually been performed** — not configured, performed.
- [ ] You know how long a restore takes because you timed it.

Backups that have never been restored are an untested belief, and the day you test them for the first time should not be the day you need them.

### Not leaking things

- [ ] No secrets in the repository. Checked in the history, not just the current files.
- [ ] Production secrets are in a secret manager, not a file.
- [ ] Staging and production use different credentials.
- [ ] Every endpoint returning someone's data checks that the caller is entitled to it — on the backend.
- [ ] HTTPS everywhere, including between your own services.
- [ ] Dependency vulnerability scanning is on.
- [ ] No personal data or secrets in logs.

The authorization line is the one to be strictest about. It is the most common serious breach at small companies and the least visible from the outside.

### Knowing what is happening

- [ ] Errors are reported somewhere you will see them, with enough context to debug.
- [ ] Logs are collected somewhere searchable, not only on a machine that will disappear.
- [ ] An uptime check runs from outside your infrastructure.
- [ ] One dashboard shows traffic, error rate, and p95 latency.
- [ ] Two or three alerts exist, on symptoms, that you would genuinely want to be woken for.
- [ ] A budget alert and a cost anomaly alert are set on the cloud account.

The budget alert takes four minutes and is the cheapest item on this entire list.

### Being able to change it

- [ ] Tests exist for the paths that must not break: signup, login, payment, whatever your equivalent is.
- [ ] Tests run automatically on every pull request and block the merge when red.
- [ ] The lockfile is committed.
- [ ] One command deploys. One command rolls back.
- [ ] **The rollback has been performed at least once, deliberately, when nothing was wrong.**

### Being able to rebuild it

- [ ] The important infrastructure is described in files, not only clicked into a console.
- [ ] Someone other than you could set up the project from the repository, following written instructions.
- [ ] There is a written note of what exists and what it costs.

The second one is a good test with an uncomfortable answer. If only you can build it, then the project's continuity is a property of your availability — Chapter 15's whole subject.

### Not being ruined by a bad night

- [ ] You know the single points of failure and have decided which are acceptable.
- [ ] External calls have a defined behaviour when they do not respond.
- [ ] Retries are backed off and limited, and what they retry is safe to repeat.
- [ ] A runbook exists for the two or three most likely failures.
- [ ] You know who is responsible when it breaks, even if that is always you.

### If you hold personal data

- [ ] You know what you collect, why, and where it physically lives.
- [ ] You can delete a specific person's data completely when asked.
- [ ] You have a lawful basis for holding it and have said so somewhere public.
- [ ] You know what you would do in the first 72 hours after a breach.

## The short version

If that is too much to hold, there is a version that fits on a card. These five have the worst consequence-to-effort ratio in the whole book — each takes under an hour and each prevents a category of disaster:

1. **Backups, with one restore actually performed.**
2. **No secrets in the repository, ever, checked through the history.**
3. **A budget alert on the cloud account.**
4. **Errors reported somewhere you will see them.**
5. **A rollback you have rehearsed.**

An afternoon. Genuinely.

## What Ledgerly needed

Chapter 1 opened with a thing that worked, twenty minutes after it hadn't, and offered to call it Ledgerly if a name helped. If you've been picturing it since, you've now watched it collect most of the list above one chapter at a time — mostly by nearly failing to.

Chapter 10 watched invoice 8812 arrive in the logs, an ordinary Friday. Chapter 12 came back to that same invoice from the other direction — the identifier sitting unchecked in a URL, one digit away from a stranger's bill. Chapter 15 was the rule nobody wrote down: a tax-number export added for one customer, six weeks gone from anyone's memory by the time it broke, on a holiday, for a system with exactly one person who could explain it.

None of these arrived as a single dramatic failure. Each was a small, ordinary gap — a check missing on the backend, a decision left in a conversation instead of a file — that cost an afternoon rather than the business, because something in an earlier chapter caught it before it compounded. That is what the bar above is actually for: not preventing the mistake, which happens anyway, but keeping it small enough to be a Tuesday rather than the reason a freelancer stops trusting Ledgerly with their invoices.

## What you have

You began this book able to get working code and unable to say what surrounded it. That has changed, and it is worth being clear about what changed and what did not.

You cannot write the code. You still cannot fully read it. Neither was the goal, and neither is what the job requires.

What you can do now is name the parts, know what goes wrong with each, ask questions whose answers are checkable, and recognise the difference between a thing that works and a thing that will keep working. You can read a diff for shape. You can tell whether a plan is about to destroy a database. You can look at an average response time and ask for the p99 instead. You can hear "it's just an MVP" and know which corners that does and does not license.

That is the actual job, and it always was. Writing code was never the *whole* difficulty of software engineering — some of it is genuinely hard, and always will be. But it was the part that took longest to learn, which made the two easy to confuse. Agents have removed much of the time. They have not removed the judgement, and the judgement is what this book has been about.

## The last thing

One habit, above all the others, that will keep serving you after the specifics here are out of date.

When something works, before moving on, ask:

> **"What happens when this breaks, and how will I know?"**

That question contains most of this book. It assumes failure rather than hoping against it — Chapter 11. It asks about observability — Chapter 10. It implies a recovery path — Chapter 9. It leads to blast radius, to backups, to authorization, to everything else because everything else is an answer to some version of it.

Ask it about every piece of what you build. The answer does not always have to be impressive. Sometimes "it breaks, I find out from a monitoring email, and I roll back in two minutes" is completely sufficient.

What matters is that there is an answer, and that you chose it — rather than finding out, at three in the morning, what it was going to be.

## What to ask for

One last time:

> "Walk me through this checklist against our project. For each item: done, not done, or not applicable — and if not applicable, why."

Ask before your first real users. Ask again when you get serious. The gaps are your work queue, in priority order, and unlike most work queues this one is finite.
