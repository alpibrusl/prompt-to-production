# The Night It Breaks

**02:13.** Ledgerly's deployment succeeds, your agent reports. It did. Everything it was asked to check came back green.

**02:14.** Customers cannot log in. Nobody tells you, because it is two in the morning where you are, and the people affected are in a timezone where it is the middle of the afternoon and they have simply gone somewhere else.

**02:41.** A support email arrives. You read it at 08:30.

**08:32.** You start looking. The site loads fine. Logging in fails, but only for accounts created before last March — which you do not discover for another hour, because your own account was created last week and works perfectly.

**09:50.** You establish that something in yesterday's deployment is responsible. You would like to go back to the previous version. You discover three things in quick succession: you are not certain which version was running on Monday, nobody has ever run the rollback command, and the change included a database migration you are not sure can be undone.

**11:20.** Fixed. Six hours of a working day gone, and almost none of them spent on the repair.

That last point is the one worth sitting with. The bug itself took ninety seconds to find once somebody looked at the right thing. Everything else — the six hours — was the absence of what this chapter is about: knowing quickly, having a way back, and having decided in advance who looks.

It will break. Not as a possibility to guard against, but as a certainty to prepare for.

This is the chapter people skip, because preparing for failure feels pessimistic when you are trying to build something. It is the opposite. Every system of any size fails regularly; the ones you think of as reliable are not the ones that do not break, they are the ones that break invisibly and recover before you notice. Amazon fails. Google fails. Your bank fails. The difference between them and a system that ruins a weekend is entirely in the preparation.

## Failure is normal

Start by accepting the premise, because everything else follows from it.

Machines fail. Disks fill. Networks partition. Third-party services go down without warning — and their status page will say everything is fine, because the status page is updated by a human who does not know yet. Certificates expire, always at the least convenient moment. A dependency's new version breaks something subtle. A customer uploads a 900-megabyte file to a field you assumed would hold a phone number. Somebody runs a well-intentioned script against the wrong environment.

None of these are exotic. They are Tuesday.

The engineering response is not to prevent all failure — that is unaffordable and, past a point, impossible. It is to make failure *small, visible, and quick to recover from*. Every practice below is one of those three.

## Limiting the damage

**Blast radius** is how much is harmed when one thing fails. It is the central question in every design decision you will now make, and it is worth training yourself to ask it reflexively: *if this breaks, what else breaks?*

A **single point of failure** is a component whose failure takes everything with it. One database with no replica. One machine running everything. One third-party service in the path of every request. One person who knows how the deployment works — that one counts, and people forget it does.

**Graceful degradation** is designing so that losing one part costs you one feature rather than the whole service. If the recommendations service is down, the shop should still take orders without recommendations. If the email provider is down, the order should still be placed and the confirmation queued.

This is almost always a choice made in code, and it is almost always cheap at the time and expensive to retrofit. The question to ask about any external call is: *what should happen if this does not answer?* If the answer is "the whole page fails", that should be a decision rather than an accident.

**Retries** are the most common tool here, and the most commonly misused. A **retry** is automatically trying a failed operation again, and the right way is with **exponential backoff** — wait one second, then two, then four, then eight — plus a limit on attempts.

Naive retries make outages worse in a way that is worth understanding because it is counterintuitive. A service slows down. Every client retries immediately. The service now receives triple the traffic while already struggling, so it slows further, so more requests time out and are retried. A service that was degraded is now completely down, and it stays down after the original cause has passed, because the retry traffic alone is enough to keep it there. This is called a retry storm and it is a genuine, common cause of outages that outlast their trigger.

Backoff spreads the load out. And retries are only safe at all when the operation is **idempotent** — Chapter 8's word, arriving where it matters. Retrying "set status to paid" is fine at any number of repetitions. Retrying "charge this card" without care charges the card twice.

## Handling it when it happens

An **incident** is a period during which the system is not doing what it promised, treated as a thing with a start, an owner, and an end.

That framing is the useful part. Not "something is wrong" as a diffuse anxiety, but a named event with someone responsible and a defined finish. **Severity** is an agreed scale for how bad it is — decided in advance, precisely so nobody has to negotiate urgency while the site is down.

A workable scale for a small team:

| | meaning | response |
|---|---|---|
| **SEV1** | users cannot use the product; data at risk | drop everything, now |
| **SEV2** | major feature broken, or badly degraded | today |
| **SEV3** | minor or cosmetic, workaround exists | normal work queue |

**On-call** is the named person responsible for responding to alerts during a given period. Even if that is you, every day, name it — because "somebody will notice" is not a plan, and writing it down is what turns it into one.

A **runbook** is written instructions for handling a specific known failure. "The queue is backing up: check X, then Y, then restart Z." Every incident should either use a runbook or produce one. This is how a team stops depending on whoever happens to be awake, and it is how *you* stop depending on remembering, which at 3am you will not.

## What to do first

When something is badly wrong, the instinct is to find out why. Resist it, because it is the wrong order.

**Restore service first. Understand it afterwards.**

Users do not care why it broke. They care that it works. Diagnosis while the system is down is diagnosis under the worst possible conditions — tired, watching the clock, with people asking for updates. Get it working, then investigate calmly with the logs, which are still there.

Which means the first question in an incident is almost always: **did we deploy anything recently?**

The overwhelming majority of incidents are caused by a change. If you deployed within a few hours of it starting, roll back first and ask questions later. Chapter 9 said rollback is worthless if never rehearsed; this is the moment that matters.

**Fix-forward** — repairing by deploying a new fix rather than returning to the previous version — is the alternative, and it is riskier: you are writing code under pressure and deploying it with less testing than usual. Sometimes it is the only option, when a database migration cannot be reversed or the bad version has already written data the old version cannot read. But rollback should be the default, and fix-forward the reasoned exception.

A rough order for the first ten minutes:

1. **Confirm it is real.** Check from outside your own network.
2. **Say something.** Even "we're investigating" — internally, and to users if it is user-visible. Silence is worse than bad news almost every time, and treating this occasion as the exception is usually just nerves talking.
3. **Check recent deployments.** Roll back if plausible.
4. **Check the dependencies.** Is it your cloud provider, your payment processor, your email service? Their status page may lag; their social media is often faster.
5. **Stop the bleeding**, even crudely. Disabling a broken feature beats a broken site.
6. **Only then** work out why.

## Afterwards

A **postmortem** is a written account after an incident: what happened, why, and what will change. **Blameless** means it examines the system that let a person make the mistake, not the person.

That word is not softness, and it is worth understanding the mechanism. The point of a postmortem is to learn what actually happened. In a culture where the outcome is blame, people minimise, omit, and hedge — entirely rationally — and you get a document that is politically safe and factually useless. The information you need is precisely the information a frightened person will not volunteer.

The right model is aviation. The industry got dramatically safer over decades because accident findings are published rather than punished, so pilots report near-misses freely, so problems are found before they kill anyone. If a person could bring the system down with one mistaken command, the finding is not "Ana ran the wrong command". It is that one command could do that, unchecked, and that is a system problem with a system fix.

A postmortem worth writing has: a timeline, the user impact in plain terms, what actually caused it, what made it worse, what made recovery slow, and specific actions with owners. That last part is what separates a postmortem from a story. "We should be more careful" is not an action. "Add a confirmation prompt to the delete command" is.

Write one for anything above SEV3, even alone, even for something small. Especially alone — you have no colleague to remember on your behalf.

## The measure that matters

**Mean time to recovery** — MTTR — is how long, on average, from breaking to being fixed.

For most small systems this is a better target than trying never to break. Chasing zero incidents means slowing down until you barely ship, and it does not work anyway. Cutting recovery from two hours to ten minutes is achievable, and from a user's perspective a ten-minute outage is a hiccup while a two-hour one is a reason to look at a competitor.

Everything that reduces MTTR is worth more than it looks: knowing quickly (Chapter 10), rolling back quickly (Chapter 9), and knowing what to do (a runbook). They compound.

## What to ask for

> "What are the single points of failure in this system?"

Ask on a calm day. The answer is a list of things to fix in priority order, and it is usually shorter than you fear.

> "For each external service we call — what happens if it does not respond? Does the whole page fail?"

This is the graceful-degradation question, and it usually surfaces two or three places where a minor dependency can take down something major.

> "Are our retries backed off and limited? Are the operations being retried safe to repeat?"

Two questions that prevent one bad outage.

> "Write a runbook for the three most likely failures."

A concrete, bounded piece of work, and the thing you will be most grateful for at 3am.
