# The Path to Production

There is a moment in every project where getting a change to users stops being simple and starts being frightening. Usually it arrives with the first real customer — Ledgerly's first paying freelancer, say.

The difference between teams that ship confidently many times a day and teams that batch changes into a nervous Thursday release is not talent, and it is not the size of the company. It is whether the path from a change to production is automated and identical every time, or improvised.

## Continuous integration

**Continuous integration** — CI, always — means automatically building and testing every change as soon as it is proposed.

Someone opens a pull request. Within a minute and without anyone asking, a machine takes that branch, installs everything, builds it, and runs the whole test suite. A few minutes later the PR shows a green tick or a red cross.

The name comes from the problem it solved. Before CI, people worked separately for weeks and then combined — "integrated" — their work, and the combining was reliably horrible, because a fortnight of incompatible assumptions all surfaced at once. Doing it continuously means each change meets the others while it is still small.

The value for you, specifically, is more direct. **CI is where you find out that the code the agent wrote actually works** — not on your machine, with your setup and your leftover files, but on a clean machine with nothing but what is committed.

That distinction is worth dwelling on. A **runner** is the machine executing these jobs, and it is a fresh, temporary one each time. It has nothing installed except what your project says it needs. So CI catches, automatically and immediately, an entire family of problems your laptop hides: a dependency you installed by hand months ago and never added to the project, a file that works because it happens to exist on your disk, a step that only works because you did something once and forgot.

If it passes on a clean machine, it will probably work on the server. If it only passes on yours, you have learned something important and cheap.

## The pipeline

The fixed sequence of automated steps a change passes through on its way to production is a **pipeline**.

An assembly line with inspection points: nothing reaches the shop floor except by travelling down it. Each **job** is one unit of work — install, build, test, deploy — and they run in a defined order, some in parallel.

A typical one:

```
1. install dependencies      (from the lockfile — Chapter 2)
2. lint and format check     (style consistency)
3. run unit tests            (fast — Chapter 6)
4. run integration tests     (slower)
5. build the container image (Chapter 7)
6. push image to registry
7. deploy to staging         (Chapter 5)
8. run smoke tests
9. deploy to production      (with approval, or automatically)
```

This book's own repository has a small version of exactly this, and one of its steps is a check that no chapter uses a term before defining it. Same principle, different subject: a rule you care about, enforced by a machine rather than by remembering.

<div style="margin:1.6rem 0;">
<svg viewBox="0 0 740 200" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="ptp9-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
<path d="M0,0 L6,3 L0,6" fill="none" stroke="#1a1a1a" stroke-width="1.1"/>
</marker>
</defs>
<rect x="4" y="60" width="96" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="52" y="82" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">INSTALL &amp;</text>
<text x="52" y="96" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">LINT</text>
<line x1="100" y1="86" x2="126" y2="86" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp9-arrow)"/>
<rect x="126" y="60" width="104" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="178" y="76" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9" font-weight="600" fill="#1a1a1a">UNIT &amp;</text>
<text x="178" y="88" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9" font-weight="600" fill="#1a1a1a">INTEGRATION</text>
<text x="178" y="100" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9" font-weight="600" fill="#1a1a1a">TESTS</text>
<line x1="178" y1="60" x2="178" y2="38" stroke="#8a3324" stroke-width="1.4"/>
<text x="178" y="30" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" fill="#8a3324">gate</text>
<line x1="230" y1="86" x2="256" y2="86" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp9-arrow)"/>
<rect x="256" y="60" width="112" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="312" y="82" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">BUILD &amp; PUSH</text>
<text x="312" y="96" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">IMAGE</text>
<line x1="368" y1="86" x2="394" y2="86" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp9-arrow)"/>
<rect x="394" y="60" width="100" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="444" y="82" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">DEPLOY TO</text>
<text x="444" y="96" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">STAGING</text>
<line x1="494" y1="86" x2="520" y2="86" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp9-arrow)"/>
<rect x="520" y="60" width="90" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="565" y="82" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">SMOKE</text>
<text x="565" y="96" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" font-weight="600" fill="#1a1a1a">TESTS</text>
<line x1="565" y1="60" x2="565" y2="38" stroke="#8a3324" stroke-width="1.4"/>
<text x="565" y="30" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" fill="#8a3324">gate</text>
<line x1="610" y1="86" x2="636" y2="86" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp9-arrow)"/>
<rect x="636" y="60" width="60" height="52" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="666" y="82" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" font-weight="600" fill="#1a1a1a">DEPLOY</text>
<text x="666" y="96" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" font-weight="600" fill="#1a1a1a">TO PROD</text>
<line x1="666" y1="60" x2="666" y2="38" stroke="#8a3324" stroke-width="1.4"/>
<text x="666" y="30" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" fill="#8a3324">gate</text>
<text x="350" y="140" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" fill="#666">1 install &#183; 2 lint &#183; 3 unit tests &#183; 4 integration tests &#183; 5 build image</text>
<text x="350" y="156" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="9.5" fill="#666">6 push &#183; 7 staging &#183; 8 smoke tests &#183; 9 production</text>
<text x="350" y="185" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-style="italic" fill="#444">An assembly line with inspection points: nothing reaches the shop floor except by travelling down it.</text>
</svg>
</div>

A **gate** is a pipeline step whose failure blocks the change from going further. This is the entire mechanism, and it is worth stating plainly:

**A test that nobody is required to pass is a suggestion.**

Chapter 6 argued for tests. This is where they acquire force. Configure the repository so a red pipeline blocks the merge, with no override — because an override that exists gets used at 6pm on a Friday by someone who is confident, and they are usually right, and the one time they are not is the incident.

## Delivery, deployment, and the difference

The letters CD stand for two different things and people use them interchangeably. They are not the same, and the difference is a decision you should make deliberately.

**Continuous delivery** means every change that passes the pipeline is *ready* to deploy at any moment. The final step is a human pressing a button.

**Continuous deployment** means there is no button. Anything that passes goes to production automatically.

Continuous deployment sounds reckless and mostly is not, for a reason that takes a moment to see: it forces the pipeline to be genuinely trustworthy. If nothing stands between a merge and your users, the tests must be real and the rollback must work. A team whose pipeline actually has that — strong tests, a canary or staged rollout, fast rollback, and the ability to see what's happening in production (Chapter 10) — can end up with *better* safety than a team relying on a manual gate because the gate is doing the job automation should be doing, and doing it worse: a tired person at 6pm is not a good check. That is a claim about a mature pipeline, though, not about removing the button by itself — a thin test suite with no button is worse than a thin test suite with one.

That said: **start with continuous delivery.** Automate everything up to the last step, and press the button yourself. When you have gone a month pressing the button and never once been glad of the chance to say no, you have earned the right to remove it.

## Getting back

Now the most important part of the chapter, and the part most often left until it is needed.

**Rollback** is returning production to the previous known-good version.

It is the single most valuable capability you can have, and it is worthless if it has never been rehearsed. There is a specific and common failure here: everyone assumes rollback works, nobody has tried it, and the first attempt happens during an incident at 11pm when it turns out the previous image was deleted, or the database migration cannot be undone, or nobody knows the command.

**Practise rolling back on a normal Tuesday, when nothing is wrong.** Deploy something harmless, roll it back, time it. That rehearsal is worth more than several days of careful work elsewhere because it converts your worst night from a crisis into a procedure.

Two techniques make it fast and safe:

**Blue-green deployment.** Run the new version alongside the old, then switch traffic across in one step. If it goes wrong, switch back — the old version is still running and still warm. Rollback becomes a redirection rather than a redeployment, and it takes seconds — provided both versions can safely run against the same database at the same moment. A migration that isn't backward-compatible (a renamed column, a newly required field) breaks that assumption: switch back to the old code and it may now be reading or writing data in a shape only the new version understood, turning an easy rollback into new damage instead of undoing the old kind.

**Canary release.** Send a small fraction of traffic — 1%, then 5%, then 25% — to the new version, watching as you go. Most bad deployments are visible in the first minute at 1%, and 1% of your users having a bad minute is a different event from all of them having a bad hour.

Both depend on being able to see whether things are going wrong, which is Chapter 10 and is not optional if you intend to use either.

## Separating shipping from releasing

A **feature flag** removes more deployment anxiety than anything else in this chapter: a switch that turns a feature on or off without deploying. The code for the new thing ships to production but stays dark; you turn it on for yourself, then for a few users, then for everyone — and off again instantly if it misbehaves.

The consequence is that **deploying code and releasing a feature become two separate decisions**. You can deploy the half-finished thing safely because it is switched off. You can release to 5% of users without a deployment. And when something is wrong you turn it off in seconds, which is faster and less disruptive than any rollback.

The cost is honest: every flag is a branch in behaviour, and old flags left permanently on become confusing clutter. Remove them once a feature is settled. Nobody does this reliably; do it anyway.

## The smallest version worth having

If you do nothing else in this chapter, do this. It is perhaps an hour of work and most of the benefit:

1. On every pull request: install, build, run the tests.
2. Make that a required check, so a failure blocks the merge.
3. Have one command that deploys, and one command that rolls back.
4. Run the rollback once, deliberately, before you need it.

That is not an impressive pipeline. It eliminates most of the ways a small project hurts itself.

## What to ask for

> "Set up CI on the repository: on every PR, install from the lockfile, build, and run the tests. Make it a required check."

The foundation, and a well-defined piece of work with a clear finish.

> "What is the rollback procedure, and can we do it right now as a test?"

Ask on a calm day. If the answer involves any thinking, you have found something important.

> "Is there anything about our deploy that is done by hand?"

Any hand step is a step that will be done differently at 2am by someone tired. It does not all have to be fixed today, but it should be known.

> "Can we put this behind a feature flag?"

Worth asking about anything risky. It usually turns a frightening deployment into an ordinary one.
