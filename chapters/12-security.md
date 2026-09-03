# Who Is Allowed to Do This

This is not a security book, and finishing it will not make you a security engineer. What it can do is cover the handful of mistakes that account for most real breaches at small companies — because they are not sophisticated attacks. They are the same few oversights, repeatedly.

## Who you are, and what you may do

Two words that sound similar, mean different things, and are confused constantly.

**Authentication** is establishing who someone is. Logging in.

**Authorization** is establishing what that person is allowed to do.

Authentication is the one people get right because it is visible — there is a login page, it either works or it does not. Authorization is where the breaches are because it is invisible: nothing on screen tells you that user 4471 can fetch user 4472's invoice by changing a number in the address bar.

That specific bug — where an identifier in a request is not checked against who is asking — is one of the most common serious vulnerabilities on the web. It requires no skill to find. Someone changes `/invoices/8812` — the same invoice Chapter 10's logs showed being created — to `/invoices/8813` out of curiosity and sees a stranger's data.

**Every request that touches data belonging to someone must check that the caller is entitled to it.** Not the interface — the backend, as Chapter 3 insisted. Every single one. This is the highest-value security question in this book and it is worth asking about every endpoint you have.

In practice, the check is almost always the same shape: whatever identifier arrives in the request, verify it belongs to — or is otherwise permitted for — the caller, before doing anything with it. Not after, and not "we'll add it once it matters." Test it directly, on every endpoint that accepts an identifier: log in as one account, try to fetch or modify a record belonging to another. If it works, you have just found, for free, the same bug an attacker finds first.

## Storing a password

A password must never be stored as the thing the user typed. If your database is ever read by someone who should not have it — a breach, a careless backup, an ex-employee — a table of plain passwords hands over every account at once, and because people reuse passwords, it often hands over accounts on other services too.

**Password hashing** turns a password into a fixed-length value that cannot practically be reversed back into the original, using an algorithm made deliberately slow — slow enough that checking one login is instant, but trying millions of guesses against a stolen table takes years rather than hours. What you store is the hash. Never the password.

Ordinary encryption is the wrong tool here, even though it sounds similar. Encryption is designed to be reversed by whoever holds the key; a password should never be recoverable by anyone, including you. The property that matters is that hashing is one-way on purpose.

The current recommendation is **argon2id**. **bcrypt** is older, still acceptable, and considerably weaker against an attacker with modern hardware. Do not write this yourself — every mainstream language has a maintained library for it, and hand-rolled hashing is a specialist skill that is easy to get subtly wrong in ways that only surface after a breach.

## Least privilege

**Least privilege** means granting every person and program exactly the access it needs and nothing more.

A hotel keycard that opens your room, the gym, and nothing else. Not a master key, because the point of a keycard is what happens when it is lost.

In practice this means: the application's database user can read and write the tables it uses and cannot drop them. The service that sends email has permission to send email and not to read your storage. A developer has access to staging; access to production is deliberate, narrower, and logged.

The reason is not distrust. It is blast radius, from Chapter 11, applied to compromise: when something is breached — a leaked key, a compromised dependency, a mistake — least privilege decides whether you lose one thing or everything. The default in most cloud setups is far too permissive because permissive is what makes things work on the first try, and nobody comes back to narrow it.

## Encryption, and what it does not do

**Encryption in transit** — TLS, the padlock in the browser — scrambles data while it moves across a network so it is unreadable if intercepted. This is essentially free now, automatic on every serious platform, and there is no excuse for any part of your system not using it, including internal calls between your own services.

**Encryption at rest** scrambles stored data so a stolen disk or database file is useless without the key. Most managed databases offer it as a checkbox. Tick it.

Now the important part because encryption is where false confidence lives: **neither protects you from a stolen credential.** If someone has your database password, encryption at rest is irrelevant — they connect legitimately and the database decrypts everything for them, as designed. If someone has a user's session token, TLS is irrelevant — they make properly encrypted requests as that user.

Encryption protects against interception and theft of the physical thing. It does nothing about someone walking in the front door with a valid key. Which is why Chapter 5's rules about secrets carry more weight than any encryption setting.

## The code you did not write

Chapter 2 introduced the supply chain: hundreds of packages by people you have never met.

A **vulnerability** is a known flaw that lets someone do something they should not. They are published with identifiers — CVE numbers — so everyone can check whether they are affected. Some are trivial. Some let an attacker run arbitrary code on your server, and those get names and news coverage.

**Patching** is upgrading dependencies to versions where known vulnerabilities are fixed. It is ongoing work rather than a task that completes, and the practical approach is:

- Turn on automated dependency scanning. GitHub does this for free; it opens a pull request when a dependency you use has a published vulnerability.
- Update regularly and in small batches. A project that has not been updated in two years cannot be updated safely in an afternoon — everything moved at once, and you will be debugging six incompatibilities simultaneously.
- Treat "an attacker can run code on your server" as an emergency, and a flaw in a tool that only ever runs on your laptop as routine.

The other supply chain risk is a package that is malicious rather than flawed. Defences are modest but real: commit the lockfile so you get the version you reviewed rather than whatever is newest, be suspicious of packages with few users solving trivial problems, and check the name — attackers publish packages named one character away from popular ones and wait for a typo.

## Personal data

**Personal data** — PII — is data that identifies a living person. Names, emails, addresses, IP addresses, and much more than people assume.

Collecting it puts you under legal obligations regardless of your size or intentions. Under GDPR, and similar laws elsewhere, individuals have rights to see, correct, export and delete their data; you must have a lawful basis for holding it; you may be required to report a breach within 72 hours; and where the data physically sits — Chapter 7's regions — is a compliance question, not a technical preference.

The single most effective strategy is unfashionable and works: **collect less.** Data you never held cannot leak, cannot be subpoenaed, cannot be mishandled, and needs no deletion process. Before adding a field, ask what it is for. "It might be useful later" is how a small application ends up holding dates of birth it has never once used and now must protect forever.

Practical minimums: never log personal data (Chapter 10), never put real production data in staging without scrubbing it, know which of your third-party services receive personal data, and be able to actually delete a user when they ask — which is harder than it sounds once their data is in six places and three backups.

## Two more, briefly

**Rate limiting** caps how many requests one caller may make in a period. Without it, one user — or one bug, or one bored person — can consume everything you have. It is also what makes password guessing impractical, and it should be on your login endpoint before anything else.

An **audit log** is an append-only record of who did what and when, kept for investigation rather than debugging. You want one for administrative actions: who deleted the account, who changed the permission, who exported the data. The moment you need it, nothing else substitutes, and it cannot be added retroactively.

## What to ask for

> "For every endpoint that returns data about a specific user or record — do we check the caller is entitled to it, on the backend?"

The most valuable security question in this book.

> "How are passwords stored? If it's anything other than a hash from a maintained library, that changes today."

A yes/no question with a specific, checkable answer, and one of the few in this book worth interrupting other work for.

> "Turn on dependency vulnerability scanning, and show me anything currently flagged as high or critical."

Fifteen minutes, permanent benefit.

> "What personal data do we collect, where does it live, and could we delete a specific user completely if asked?"

Uncomfortable and better asked now than by a regulator.
