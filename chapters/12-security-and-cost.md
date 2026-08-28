# Two Ways to Lose Everything

Two subjects in one chapter, because they share a shape: both are quiet until they are catastrophic, both are cheap to handle early and ruinous to handle late, and neither is visible in a working application.

You can build something that functions perfectly and be destroyed by either.

## Part one: security

This is not a security book, and finishing it will not make you a security engineer. What it can do is cover the handful of mistakes that account for most real breaches at small companies — because they are not sophisticated attacks. They are the same few oversights, repeatedly.

### Who you are, and what you may do

Two words that sound similar, mean different things, and are confused constantly.

**Authentication** is establishing who someone is. Logging in.

**Authorization** is establishing what that person is allowed to do.

Authentication is the one people get right, because it is visible — there is a login page, it either works or it does not. Authorization is where the breaches are, because it is invisible: nothing on screen tells you that user 4471 can fetch user 4472's invoice by changing a number in the address bar.

That specific bug — where an identifier in a request is not checked against who is asking — is one of the most common serious vulnerabilities on the web. It requires no skill to find. Someone changes `/invoices/8812` to `/invoices/8813` out of curiosity and sees a stranger's data.

**Every request that touches data belonging to someone must check that the caller is entitled to it.** Not the interface — the backend, as Chapter 3 insisted. Every single one. This is the highest-value security question in this book and it is worth asking about every endpoint you have.

### Least privilege

**Least privilege** means granting every person and program exactly the access it needs and nothing more.

A hotel keycard that opens your room, the gym, and nothing else. Not a master key, because the point of a keycard is what happens when it is lost.

In practice this means: the application's database user can read and write the tables it uses and cannot drop them. The service that sends email has permission to send email and not to read your storage. A developer has access to staging; access to production is deliberate, narrower, and logged.

The reason is not distrust. It is blast radius, from Chapter 11, applied to compromise: when something is breached — a leaked key, a compromised dependency, a mistake — least privilege decides whether you lose one thing or everything. The default in most cloud setups is far too permissive, because permissive is what makes things work on the first try, and nobody comes back to narrow it.

### Encryption, and what it does not do

**Encryption in transit** — TLS, the padlock in the browser — scrambles data while it moves across a network so it is unreadable if intercepted. This is essentially free now, automatic on every serious platform, and there is no excuse for any part of your system not using it, including internal calls between your own services.

**Encryption at rest** scrambles stored data so a stolen disk or database file is useless without the key. Most managed databases offer it as a checkbox. Tick it.

Now the important part, because encryption is where false confidence lives: **neither protects you from a stolen credential.** If someone has your database password, encryption at rest is irrelevant — they connect legitimately and the database decrypts everything for them, as designed. If someone has a user's session token, TLS is irrelevant — they make properly encrypted requests as that user.

Encryption protects against interception and theft of the physical thing. It does nothing about someone walking in the front door with a valid key. Which is why Chapter 5's rules about secrets carry more weight than any encryption setting.

### The code you did not write

Chapter 2 introduced the supply chain: hundreds of packages by people you have never met.

A **vulnerability** is a known flaw that lets someone do something they should not. They are published with identifiers — CVE numbers — so everyone can check whether they are affected. Some are trivial. Some let an attacker run arbitrary code on your server, and those get names and news coverage.

**Patching** is upgrading dependencies to versions where known vulnerabilities are fixed. It is ongoing work rather than a task that completes, and the practical approach is:

- Turn on automated dependency scanning. GitHub does this for free; it opens a pull request when a dependency you use has a published vulnerability.
- Update regularly and in small batches. A project that has not been updated in two years cannot be updated safely in an afternoon — everything moved at once, and you will be debugging six incompatibilities simultaneously.
- Treat "an attacker can run code on your server" as an emergency, and a flaw in a tool that only ever runs on your laptop as routine.

The other supply chain risk is a package that is malicious rather than flawed. Defences are modest but real: commit the lockfile so you get the version you reviewed rather than whatever is newest, be suspicious of packages with few users solving trivial problems, and check the name — attackers publish packages named one character away from popular ones and wait for a typo.

### Personal data

**Personal data** — PII — is data that identifies a living person. Names, emails, addresses, IP addresses, and much more than people assume.

Collecting it puts you under legal obligations regardless of your size or intentions. Under GDPR, and similar laws elsewhere, individuals have rights to see, correct, export and delete their data; you must have a lawful basis for holding it; you may be required to report a breach within 72 hours; and where the data physically sits — Chapter 7's regions — is a compliance question, not a technical preference.

The single most effective strategy is unfashionable and works: **collect less.** Data you never held cannot leak, cannot be subpoenaed, cannot be mishandled, and needs no deletion process. Before adding a field, ask what it is for. "It might be useful later" is how a small application ends up holding dates of birth it has never once used and now must protect forever.

Practical minimums: never log personal data (Chapter 10), never put real production data in staging without scrubbing it, know which of your third-party services receive personal data, and be able to actually delete a user when they ask — which is harder than it sounds once their data is in six places and three backups.

### Two more, briefly

**Rate limiting** caps how many requests one caller may make in a period. Without it, one user — or one bug, or one bored person — can consume everything you have. It is also what makes password guessing impractical, and it should be on your login endpoint before anything else.

An **audit log** is an append-only record of who did what and when, kept for investigation rather than debugging. You want one for administrative actions: who deleted the account, who changed the permission, who exported the data. The moment you need it, nothing else substitutes, and it cannot be added retroactively.

## Part two: cost

Now the second way to lose everything, which is less dramatic and more common.

Cloud costs are unusual: you can incur an enormous bill without any warning, in a matter of hours, through a mistake rather than success. The stories are real, well documented, and mostly not about growth.

### What actually generates a bill

The intuition most people bring is that you pay for computers. You pay for four things, and the machines are frequently the smallest.

**Compute** — machines running. Predictable, and the part everyone thinks of.

**Storage** — data at rest. Cheap per gigabyte, and it only grows, because deleting things requires a decision and nobody makes it.

**Data transfer**, and specifically **egress**: data leaving the provider's network. This is the surprising one. Moving data *in* is usually free; moving it *out* costs meaningfully per gigabyte, and it is where genuinely shocking bills come from. An application serving video or large images without a content delivery network in front can produce an egress bill several times its compute bill.

**Per-request pricing** on managed and serverless things. Fractions of a cent each, which is nothing until something calls it in a loop.

### How the bad ones happen

The pattern is consistent, and it is almost never "we grew too fast":

- A retry loop with no backoff — Chapter 11 — hammering a paid API a million times overnight.
- A function that triggers on a file being written, and writes a file.
- A test environment spun up for an experiment and left running for four months.
- Logging at `DEBUG` in production, generating terabytes, at per-gigabyte ingestion pricing.
- A public storage bucket found by scrapers, serving egress to the world.
- A key leaked from a repository (Chapter 5) used to run mining machines in a region you have never used.

Note how many of these are Chapter 11's or Chapter 5's problems presenting as a financial one. A bill is often the first *visible* symptom of a correctness problem.

### What to do about it

**Set a budget alert on day one.** Every provider supports it. Pick a number several times your expected spend and have it email you. This takes four minutes and is the difference between a €200 surprise and a €40,000 one.

A **cost anomaly** alert — a sudden jump relative to normal, not an absolute threshold — is better still, because it catches a tenfold increase in week one before it compounds for thirty days. Treat it exactly like an operational alert from Chapter 10: something is wrong, find out what.

Then, less urgently: tag resources so spend can be attributed to something; review the bill monthly, itemised, looking for things you do not recognise; delete unused resources rather than leaving them; and put a content delivery network in front of anything large and public, which is usually the single largest cost saving available.

**Know your unit cost.** What does one user, or one order, cost you to serve? Most small teams have no idea, and it is the number that tells you whether your pricing works at ten times the scale. It is also the number that makes a cost conversation concrete rather than anxious.

## What to ask for

> "For every endpoint that returns data about a specific user or record — do we check the caller is entitled to it, on the backend?"

The most valuable security question in this book.

> "Turn on dependency vulnerability scanning, and show me anything currently flagged as high or critical."

Fifteen minutes, permanent benefit.

> "What personal data do we collect, where does it live, and could we delete a specific user completely if asked?"

Uncomfortable and better asked now than by a regulator.

> "Set up a budget alert and a cost anomaly alert on the cloud account."

Do it today. It is the cheapest insurance available.

> "What is our biggest cost line, and what is our cost per user?"

If nobody knows, that is the finding.
