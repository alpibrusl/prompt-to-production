# Environments and Secrets

There is a phrase engineers use, always with a particular weary tone: *it works on my machine*.

It is a joke about a real and constant problem. Software that behaves perfectly in one place and fails in another, for reasons that have nothing to do with the code, because the two places were not the same in some way nobody thought to check.

This chapter is about deliberately having several places, keeping them honestly similar, and handling the one category of setting that can ruin you.

## Several copies on purpose

An **environment** is one complete running copy of your system, kept separate from the others so that what happens in it affects nothing else.

The analogy to hold: a dress rehearsal versus opening night. Same play, same cast, same script — utterly different consequences for a mistake.

Ledgerly, like most projects, has two or three:

**Local** is the copy running on your own computer, for your eyes only. Break it freely; nobody notices. Its data is fake.

**Staging** is a copy built to resemble production as closely as possible, where a change can be watched before real users meet it. Its data is fake, or a scrubbed copy of real data with the personal parts removed.

**Production** is the one real users touch. Real data, real money, real consequences.

The single rule that makes environments worth having is this: **a change reaches production only after it has been somewhere else first.** Local, then staging, then production. Never straight to the last one.

Small projects sometimes skip staging, and that is a defensible choice when the cost of a bad deploy is low. What is not defensible is skipping the separation between local and production — which people do more often than you would think, usually by accident, usually by pointing a local copy at the real database because it was easier than setting up a fake one. Then a test run of a script that deletes old records deletes the real ones. This story is common enough to be a genre.

## Why they drift apart

Environments that start identical do not stay identical, and the divergence is where "works on my machine" is born.

Your laptop has a different operating system from the server. It has a different version of the language runtime because you installed yours in March and the server's was set up in January. It has files sitting around from previous experiments. Its database contains twelve rows; production's contains four hundred thousand, and the query that returns instantly on twelve takes ninety seconds on four hundred thousand. Your network is fast and local; production's calls cross the internet and sometimes time out.

**Environment parity** is the word for how closely your environments resemble each other, and it is best understood as a measure of *how much what you observed in one tells you about another*. Low parity means your testing was theatre.

Two things buy most of the available parity, and both are covered later because both are large:

- **Containers** (Chapter 7) package the program together with much of the runtime environment it depends on, eliminating most of the "different versions installed" gap in one move — though not differences in the underlying kernel, CPU architecture, or whatever it talks to over the network.
- **Infrastructure as code** (Chapter 8) means each environment is built from the same written description rather than assembled by hand, making silent configuration drift far harder — not impossible, if someone changes something by hand outside that description, but much easier to catch when they do.

The thing you can do today, before either of those, is more modest and still worth it: know how your environments differ, and be honest about what your testing therefore proves. A change tested against twelve rows has not been tested for speed. It has been tested for correctness only, and you should say so rather than pretend otherwise.

## Configuration: the same code, different settings

If the same artifact is going to run in three places, something has to differ because the database address is not the same in each. That something is **configuration** — the settings that differ between environments, kept outside the code.

The rule is: **build once, configure per environment.** The exact same artifact goes to staging and to production. Only its configuration differs.

This matters more than it sounds. If you build a separate artifact per environment, then what you tested in staging is not what you deployed to production — it is a sibling of it, built from the same source, possibly with a different dependency version resolved on a different day. All the confidence you bought by testing in staging leaks away. One artifact, promoted through the environments, keeps that confidence intact.

Configuration usually reaches a program through **environment variables**: named values handed to it by whatever starts it. `DATABASE_URL`, `PORT`, `LOG_LEVEL`. Locally they typically live in a file called `.env`; in production they are set by the platform.

## Secrets

A **secret** is a value that grants access to something — a password, a key, a token, a certificate. Anyone holding it can act as you.

The analogy, and it is exact: a house key. You would not photocopy your house key into the blueprints you publish on the internet. That is the entirety of the advice, and yet.

Secrets look exactly like ordinary configuration. `DATABASE_URL` and `LOG_LEVEL` sit next to each other in the same file, and one of them is a key to everything you own. The similarity is the trap, and it is why this is worth its own section rather than a footnote.

### What goes wrong

The failure is almost always the same, and it is not exotic:

1. A key is needed to make something work.
2. It gets put directly in a source file because that works immediately.
3. Everything works. The key is forgotten.
4. Six months later, the repository is made public, or a contractor is given access, or the project is copied into a new one, and the key goes with it.
5. Somebody finds it.

Step five is faster than people expect. There are bots that continuously scan every new public commit on GitHub for anything shaped like a credential. Keys have been found and used within *seconds* of being pushed. Not hours.

And because Git history is permanent — Chapter 4 — deleting the key in a later commit does not remove it. It remains in the history, one command away, and by the time anyone gets around to properly rewriting that history, a bot may already have copied, cached, or scraped it.

**Removing a leaked secret from Git history does not make that credential safe again.** Rewriting history stops new clones from seeing it. It does nothing about the copy a bot already made. The only fix that actually closes the door is rotating or revoking the credential itself — treat "leaked" as a one-way state the moment it happens, not something a later cleanup commit undoes.

The bill that follows a leaked cloud key is a specific and well-documented horror. Somebody uses your account to run a large number of machines mining cryptocurrency, and you find out five days later.

### The rules

**Secrets never go in the repository.** Not in source, not in configuration files, not in comments, not "temporarily", not in a file you intend to delete before pushing.

**A `.env` file is for local only, and it must be in `.gitignore`.** Every project should have a committed `.env.example` listing the *names* of the variables with fake values, so a newcomer knows what is needed without being handed anything real.

**Production secrets live in a secret manager.** A **secret manager** — AWS Secrets Manager, Google Secret Manager, HashiCorp Vault, or your hosting platform's built-in equivalent — stores secrets encrypted, hands them only to things allowed to have them, and records every access. Your platform almost certainly has one, and using it is a settings page rather than a project.

**Different secrets per environment.** Staging must never hold production's keys. If it does, then staging is production for anyone who compromises it, and you have carefully built a weaker copy of your real system with the same keys in it.

**Rotate when in doubt.** **Rotation** is replacing a secret with a new one and retiring the old, so a leaked value stops being useful. If a key might have been exposed, rotate it. Do not investigate first and rotate after — investigation takes hours during which the key still works, and rotation doesn't have to wait for the investigation to finish. It is genuinely close to free when the secret lives in a secret manager everything fetches live; it is not free when it's a plain value baked into an environment variable, because every running instance that has the old value needs to actually pick up the new one, and a sloppy rotation there can turn a leak into an outage of its own — one more reason the secret manager above is worth setting up before you need it in a hurry.

**Never send a secret through chat or email.** It will sit in that history as long as the repository would have.

### If it has already happened

Assume every project has done this at least once. The response, in order:

1. **Rotate the key immediately.** Before anything else, including finding out whether it was used. The old value must stop working.
2. **Check what was done with it.** Cloud providers (Chapter 7) keep access records. Look for activity you do not recognise, in regions you do not use.
3. **Remove it from history properly**, or if the repository has never been public and the key is now dead, accept that a dead key in history is not an emergency.
4. **Put the real one in a secret manager**, so this specific mistake cannot recur.

The order is the point. Rotate first. Everything else can wait ten minutes; the key cannot.

## What to ask for

> "Scan this repository for anything that looks like a secret — keys, tokens, passwords, connection strings — including in the history and in any config or example files."

The first thing to ask on any project. It takes a minute and it is the highest-value minute in this book.

> "Move every secret out of the code into environment variables, add `.env` to `.gitignore`, and create a `.env.example` with the names and fake values."

A small, well-defined piece of work with a clear finish, and it converts a permanent exposure into a solved problem.

> "What differs between my local setup and production? Versions, data size, anything installed in one and not the other."

This is the "works on my machine" question asked in advance. The answer tells you exactly how much your local testing is worth — which may be a lot, but you should know rather than assume.
