# Keeping Every Version

> **Part II — Keeping It**

You have a working thing — Ledgerly, say. Now you are going to change it, and changing it is where the losses happen.

Not dramatic losses. Ordinary ones: an afternoon of work overwritten, a feature that worked on Tuesday and does not on Thursday with nobody able to say what happened in between, a fix that broke something else and no way back to before the fix.

The system that prevents all of this is called **version control**, and it is the single most valuable piece of engineering practice you can adopt. Not the most sophisticated. The most valuable, by a wide margin because it converts almost every mistake from a loss into an inconvenience.

## What it does

Version control records every change to a codebase as a separate, labelled, reversible step, so that any past state can be recovered exactly.

Read that again with attention on *exactly*. Not approximately. Not "the important files". The precise state of every file at every point in the project's life, restorable in seconds, forever.

The system essentially everyone uses is **Git**. GitHub, GitLab and Bitbucket are hosting services built around Git — places to keep a shared copy — but they are not Git itself. Git runs on your own machine and works perfectly well with no internet connection. This distinction matters mainly because people say "GitHub" when they mean "Git", and you will otherwise be confused about which thing is doing what.

## The unit of history

A **commit** is one recorded change, with a message saying why it was made.

The useful image is a save point in a game. You can always load it again. Everything about that moment is preserved — every file, exactly as it was — and you can return to it at any point in the future, from any machine, having done anything in between.

A commit has three parts worth knowing:

**What changed**, recorded as a **diff** — the exact lines added and removed, shown against what was there before. This is the atom of code review, and it is worth knowing that engineers spend a large fraction of their time reading diffs rather than whole files. The question is almost never "what does this program do"; it is "what did this change do".

**Who made it and when.** Automatic.

**Why**, in the message. This part is not automatic, and it is where the value is. `fix bug` tells a future reader nothing. `Reject signups with a plus-addressed email — was letting one person create unlimited accounts` tells them everything, including a piece of reasoning that exists nowhere else.

Commit messages are the only place in a codebase where *intent* is recorded. The code says what it does. The message says why somebody wanted that. Six months later, when you are staring at a line that makes no sense and wondering whether it is safe to remove, the message is what saves you. Your agent will write serviceable messages if you ask for them and forgettable ones if you do not.

## Working without fear

A **branch** is a separate line of commits — a parallel workbench. The same project, a second surface to work on, so that whatever mess you make does not affect the version everybody else is using.

The branch treated as the current truth of the project is the **main branch**, usually literally called `main`. It is what gets released.

The workflow that follows is the standard one across the industry, and it will be the shape of nearly all your work:

1. Make a branch for the thing you are about to do.
2. Do it. Commit as you go — several small commits, not one enormous one at the end.
3. When it is ready, propose folding it into `main`.
4. Once it is reviewed and the checks pass, **merge** it.

Merging is folding the commits from one branch into another. Most of the time it is uneventful. Occasionally you get a **merge conflict**: two branches changed the same lines, and the system cannot know which version you meant.

A conflict is worth being clear about because it alarms people. It is not damage and it is not a bug. It is the system correctly refusing to guess. Two people made incompatible edits to the same place, and a human has to decide which is right — or that the answer is some combination of both. Your agent can usually resolve them, and you should ask what it chose when the conflict touched anything you care about.

The way to make conflicts rare is not cleverness. It is small branches, merged quickly. A branch that lives for three weeks will conflict with everything; a branch that lives for three hours rarely conflicts with anything.

## The shared copy

Git on your laptop is complete but private. The shared copy everyone syncs to — on GitHub or similar — is the **remote**.

The practical consequence, and it catches people out: **work only exists for other people once it is pushed to the remote.** Committing saves it locally. Pushing publishes it. Ten commits sitting on your laptop are, from everyone else's point of view and from your backup's point of view, nothing at all. If the laptop dies, they die.

Push often. There is no cost.

## Proposing a change

A **pull request** — PR, universally; GitLab says merge request — is a proposal to merge one branch into another, opened for review before it is accepted.

This is where a great deal of engineering actually happens, and it is worth understanding what a PR is *for* because it is doing several jobs at once:

- It shows the complete diff in one place, so a change can be judged as a whole rather than commit by commit.
- It is where automated checks report. Chapter 9 is about those; the important part is that a PR is the natural gate — tests run against the proposed change, and a red result blocks it.
- It is where **code review** happens: somebody other than the author reading the change before it is merged, and saying whether it should be.
- It is a permanent record of the discussion. Two years later, "why on earth is it done this way" often has an answer sitting in a PR comment.

You are probably wondering how to review code you cannot fully read. It is a fair question and Chapter 14 answers it properly. The short version: you can read the *shape* of a change long before you can read its contents, and the shape tells you a surprising amount. A PR that claims to fix a typo and touches forty files is worth a question regardless of what those files contain.

## Undoing things

All of it earns its place at the moment you need to undo something.

To **revert** is to undo a change by recording a *new* commit that reverses it, rather than erasing the original. The history keeps both — the mistake and its undoing. This is deliberate. Erasing history means a future reader cannot understand why something was done and then undone, and the second half of that is often the more useful half.

A few situations, and their answers:

**"I broke something and I do not know what I changed."** Ask for the diff of your uncommitted work. Everything you have changed since the last commit, listed. Usually the answer is visible immediately.

**"The last change broke it."** Revert that commit. Seconds.

**"It broke sometime this week and I do not know when."** Git can search history for you — it takes the working version and the broken version and narrows down which commit between them caused it, by bisection. Ask for it by name: *bisect*. It feels like magic the first time.

**"I want to see how this file looked in March."** Ask. It is one command and it is exact.

Every one of these depends on having committed regularly, with useful messages. That is the entire discipline: commit small, commit often, say why. The tooling does the rest.

## What changes when the author is an agent

The workflow above is thirty years old and it assumed something that is no longer true: that producing a change was the slow part.

When a human wrote the code, authorship was the bottleneck. Review was comparatively cheap — a person spent a day writing two hundred lines, and a colleague spent twenty minutes reading them. The ratio worked.

An agent can produce four thousand lines in thirty seconds. Your capacity to review them has not changed at all. **Review is now the bottleneck, and it is the only bottleneck left.**

Three consequences, and they run against the instinct that faster generation means you can relax:

**Small changes matter more, not less.** The temptation is to let a change grow, because growing it is free now. Resist it harder than a human author would have needed to. If you cannot review it, nobody is reviewing it, and an unreviewed change is one that went to production on the strength of an agent's confidence alone.

**The commit message carries more weight, not less.** A human author remembers, for a few weeks, why they did something. An agent remembers nothing between conversations. If the reasoning is not in the message, it exists nowhere — not in anybody's head, not in an old chat window you will never find again. The history is now the *only* record of intent.

**Volume changes what history is for.** Twenty commits a day from one person used to indicate a problem. Now it may just be Tuesday. That makes the ability to bisect — to search history for the change that broke something — more valuable than it has ever been, and it makes small, individually-revertible commits the thing that keeps that ability working.

There is a version of "the agent writes it, so I do not need to be careful" that is exactly backwards. Every practice in this chapter exists to make change safe, and change just got very much cheaper to produce.

## The rules that are actually rules

Almost everything about how teams use Git is a matter of taste. A few things are not.

**Never commit secrets.** Passwords, API keys, tokens, certificates. Chapter 5 is largely about this, but the reason it belongs here is a property of Git specifically: because history is permanent, a secret committed once remains in the history even after you delete it in the next commit. Removing it properly means rewriting history, which is disruptive — and by then it may already have been scraped, so rewriting the history is not the fix on its own. There are bots that watch public repositories for exactly this and act within seconds; treat a leaked secret as compromised and rotate it, regardless of how quickly you clean up the commit.

**Protect the main branch.** Configure the remote so that nobody — including you — can push directly to `main`; everything arrives through a reviewed PR with passing checks. This takes two minutes to set up and eliminates an entire genre of accident.

**Commit the lockfile, ignore the artifacts.** Source and records of decisions go in. Anything a build produces stays out, listed in a `.gitignore` file. The rule of thumb: if it can be regenerated from what is already committed, it does not belong. This book's own repository ignores its glossary file for exactly this reason — it is generated from a data file that *is* committed.

**Write the message for a stranger.** The stranger is you, in a year, with no memory of this week.

## What to ask for

> "Set up branch protection on `main`: no direct pushes, PRs require a passing build."

Do this on day one of any project you intend to keep. It is pure prevention and costs nothing.

> "From now on, work on a branch and open a PR rather than committing straight to main. Keep the commits small, and write messages that say why rather than what."

This is the working agreement. Say it once, early.

> "Has anything sensitive ever been committed to this repository — keys, passwords, tokens? Check the whole history, not just the current files."

Ask this early, and ask it again if you inherit a project. It is much cheaper to find out now than after the repository becomes public.
