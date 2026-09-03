# The Bill You Didn't See Coming

You can build something that functions perfectly — Ledgerly is up, taking invoices, nothing broken — and still be destroyed by it: cloud costs are unusual in that you can incur an enormous bill without any warning, in a matter of hours, through a mistake rather than success. The stories are real, well documented, and mostly not about growth.

## What generates a bill

The intuition most people bring is that you pay for computers. You pay for four things, and the machines are frequently the smallest.

**Compute** — machines running. Predictable, and the part everyone thinks of.

**Storage** — data at rest. Cheap per gigabyte, and it only grows because deleting things requires a decision and nobody makes it.

**Data transfer**, and specifically **egress**: data leaving the provider's network. This is the surprising one. Moving data *in* is usually free; moving it *out* costs meaningfully per gigabyte, and it is where genuinely shocking bills come from. An application serving video or large images without a content delivery network in front can produce an egress bill several times its compute bill.

**Per-request pricing** on managed and serverless things. Fractions of a cent each, which is nothing until something calls it in a loop.

## How the bad ones happen

The pattern is consistent, and it is almost never "we grew too fast":

- A retry loop with no backoff — Chapter 11 — hammering a paid API a million times overnight.
- A function that triggers on a file being written, and writes a file.
- A test environment spun up for an experiment and left running for four months.
- Logging at `DEBUG` in production, generating terabytes, at per-gigabyte ingestion pricing.
- A public storage bucket found by scrapers, serving egress to the world.
- A key leaked from a repository (Chapter 5) used to run mining machines in a region you have never used.

Note how many of these are Chapter 11's or Chapter 5's problems presenting as a financial one. A bill is often the first *visible* symptom of a correctness problem.

## What to do about it

**Set a budget alert on day one.** Every provider supports it. Pick a number several times your expected spend and have it email you. This takes four minutes and is the difference between a €200 surprise and a €40,000 one.

A **cost anomaly** alert — a sudden jump relative to normal, not an absolute threshold — is better still, because it catches a tenfold increase in week one before it compounds for thirty days. Treat it exactly like an operational alert from Chapter 10: something is wrong, find out what.

Then, less urgently: tag resources so spend can be attributed to something; review the bill monthly, itemised, looking for things you do not recognise; delete unused resources rather than leaving them; and put a content delivery network in front of anything large and public, which is usually the single largest cost saving available.

**Know your unit cost.** What does one user, or one order, cost you to serve? Most small teams have no idea, and it is the number that tells you whether your pricing works at ten times the scale. It is also the number that makes a cost conversation concrete rather than anxious.

## What to ask for

> "Set up a budget alert and a cost anomaly alert on the cloud account."

Do it today. It is the cheapest insurance available.

> "What is our biggest cost line, and what is our cost per user?"

If nobody knows, that is the finding.
