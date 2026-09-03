# Knowing What It Is Doing

> **Part IV — Living With It**

Your application is deployed. People are using it. What is it doing right now?

For most people building their first real system, the honest answer is: no idea. It appears to work because loading the page works. Whether it is slow for some users, failing for others, or quietly dropping every tenth order is invisible.

The way you find out is a customer email. Sometimes days later. Sometimes never — most people who hit a broken thing just leave, and you never learn that they came.

## The two words

**Monitoring** is watching for the failures you already thought of. Is the server up? Is disk usage above 90%? Is the error count above ten per minute? Known signals, known thresholds.

**Observability** is how well you can work out what a running system is doing from the outside, *including for problems nobody anticipated*. It is a property of the system rather than a tool you buy: can you answer a new question about production without deploying new code to answer it?

The distinction sounds academic and is not. Monitoring answers "is it broken in one of the ways I predicted". Observability answers "why is it behaving strangely" when the strangeness is novel — which is what real problems are, because the predicted ones get fixed.

The image to hold is a car dashboard versus opening the bonnet. You should be able to tell what is wrong while still driving. Pulling over, opening the engine and poking at it is what you do when the dashboard tells you nothing — and in software, "opening the bonnet" often means adding logging and deploying again, while the problem is happening.

## Three kinds of signal

Three things, complementary, commonly called the three pillars. You need all three eventually and they answer different questions.

### Logs

A **log** is a timestamped line a program writes about something it just did.

```
2026-08-28 14:32:07 INFO  invoice 8812 created for user 4471, total 42.50
2026-08-28 14:32:09 ERROR payment failed for invoice 8812: card declined
```

Ledgerly's own logs, on an ordinary Friday. Invoice 8812 will come up again in Chapter 12, for a different reason.

A diary: one entry per event, in order. Logs are the most detailed signal and the most useful when you already know roughly where to look. They are poor at telling you something is wrong — nobody reads them continuously — and excellent at telling you what happened once you have a thread to pull.

Two things separate useful logs from noise.

**Levels.** `DEBUG`, `INFO`, `WARN`, `ERROR`. The level lets you filter, and the point of filtering is that you can run production at `INFO` and turn on `DEBUG` when investigating. A system that logs everything at one level is a system where the important lines are invisible.

**Structure.** **Structured logging** means writing logs as machine-readable fields rather than sentences:

```json
{"level":"error","event":"payment_failed","invoice_id":8812,"reason":"card_declined"}
```

Uglier to read, vastly more useful. You can now ask "how many payments failed for this reason today, by hour" — a question you simply cannot ask of English sentences without regret. Ask for structured logging from the start; converting later is tedious and nobody gets round to it.

And a rule with legal weight, from Chapter 12: **never log secrets or personal data.** Logs are copied, shipped to third-party services, and kept for months. A password or a full card number in a log line is a breach sitting in a place nobody thinks of as a database.

### Metrics

A **metric** is a number about your system sampled over time. Requests per second, error count, memory used, queue depth.

Vital signs: a pulse tells you something is wrong long before a diary entry does. Metrics are cheap to store, cheap to query, easy to chart, and they are what alerts are built on. Their limitation is the mirror of their strength — a metric tells you *that* something changed, never *why*. It is the number that wakes you; the logs and traces are what you then read.

The metrics almost every system should have, sometimes called the golden signals:

- **Latency** — how long things take, from the user's point of view rather than the server's.
- **Traffic** — how much is being asked of you.
- **Errors** — the **error rate**, the proportion of requests that failed.
- **Saturation** — how full the thing is. Memory, disk, connections.

### Traces

A **trace** is a record of one request's entire journey across every service it touched, with the time spent at each stop. A parcel's tracking history: every depot, with timestamps.

When your system is one program, traces add little over logs. When a request passes through a frontend, two backend services, a database and a third-party API, a trace is the only thing that answers "which of those five was slow?" without guesswork. If you are not there yet, note the word and move on.

## Averages lie

One statistical point that matters more than any other in this chapter.

If someone tells you average response time is 200 milliseconds, you have learned almost nothing useful.

Suppose 95 requests take 50ms and 5 take 3 seconds. The average is about 200ms and looks healthy. But one user in twenty is waiting three seconds, and if that user is your biggest customer, or every user with a large account, then your system is bad in a way the average is actively hiding.

A **percentile** fixes this. **p95 latency** is the time within which 95% of requests finished; **p99** is 99%. If p50 is 40ms and p99 is 4 seconds, then most people have a fine experience and one in a hundred requests is terrible — and since a single page might make twenty requests, a meaningful share of *page loads* are terrible.

**Look at p95 and p99. Averages hide the people having the worst time**, and those people are the ones who leave.

## Dashboards and alerts

A **dashboard** is a screen of charts assembled to answer, at a glance, whether the system is healthy. You want one, it should fit on one screen, and it should show the golden signals. A dashboard with forty charts is a dashboard nobody reads.

An **alert** is an automated message to a human when a signal crosses a threshold. Not every alert needs to be urgent — plenty are fine to review the next morning as a list — but a smaller set are worth *paging* someone for: interrupting them immediately, day or night. Alerts are where good intentions most often produce something actively harmful, so here is the rule for that smaller, urgent set:

**Every alert that pages someone should be worth waking them for.**

An alert that pages someone and needs no action teaches everyone that pages need no action. Do that twenty times and you have trained your team — or yourself — to dismiss the notification without reading it. The one that matters then arrives into a habit of ignoring them. This is not hypothetical; it is the mechanism behind a large share of "why did nobody notice for six hours".

Alert on symptoms users feel, not on internal curiosities, and reserve paging for the ones that genuinely can't wait. "Error rate above 5% for five minutes" is worth paging for. "CPU at 80%" is not — a system at 80% CPU serving everyone correctly is a system doing its job, and belongs on the dashboard, not in anyone's pocket at 2am.

A **health check** is a small endpoint whose only purpose is to answer "am I working?", so a load balancer or orchestrator can stop sending traffic to a copy that is not. Make it check the things the application actually needs — can it reach the database? — rather than merely returning "yes", which a completely broken process will happily do.

## Promises with numbers in them

The last idea here is what turns all this from data into decisions.

A **service level objective** — SLO — is a target for how good the service will be, stated as a number over a window. "99.9% of requests succeed, measured monthly." "95% of page loads complete within 500 milliseconds."

Three related terms: an SLI is the measurement, an SLO is your internal target, and an SLA is a contractual promise with financial penalties. You almost certainly want SLOs and almost certainly do not yet have an SLA.

An SLO is a promise with a number in it — the only kind you can be held to, and, more usefully, the only kind that settles arguments. "The site feels slow lately" is not actionable. "p95 checkout latency is 1.4 seconds against an objective of 800 milliseconds" is.

From it comes the **error budget**: the amount of failure your objective permits. At 99.9% monthly, you may be down about 43 minutes. That is not an embarrassment to hide; it is a budget to spend.

The reframing is genuinely useful. If you have spent little of the budget, you are being too cautious — ship faster, take more risk. If you have burned it in the first week, stop shipping features and fix reliability. A number that both sides of a "should we ship or stabilise" argument agree on in advance is worth a great deal, and it is one of the few good answers to that argument that does not depend on who is more forceful.

Do not set 99.99% because it sounds impressive. Each nine costs disproportionately more, and an objective you routinely miss is worse than none, because it teaches everyone to ignore it — the same failure as the noisy alert, one level up.

## The smallest version worth having

For a small application, in rough order of value:

1. Errors reported somewhere you will see them, with the details attached. A dedicated error-tracking service takes fifteen minutes to add and is the highest-value item on this list by a distance.
2. Structured logs, collected somewhere searchable — not only on the machine, which disappears when the machine does.
3. An uptime check from outside your infrastructure, hitting a real page every minute. Outside matters: a check running inside your own system cannot tell you your system is unreachable.
4. One dashboard: traffic, error rate, p95 latency.
5. Two or three alerts, on symptoms, that you would genuinely want to be woken for.

An afternoon. It is the difference between finding out from your monitoring and finding out from a customer, and that difference is most of what "running a system" means.

## What to ask for

> "If the application started failing right now, how would I find out?"

The whole chapter in one question. If the answer is "a user would tell you", that is the problem, and it is fixable this afternoon.

> "Add error tracking, and make sure errors include enough context to debug — which user, which request, what input."

The single highest-value change here.

> "Show me p95 and p99 latency, not the average."

Ask this every time someone shows you a performance number.

> "Which of our alerts actually page someone, and would each one genuinely be worth waking me at 3am?"

Prune ruthlessly. A short list of real pages beats a long list nobody reads.
