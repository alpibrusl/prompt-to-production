# Writing the Setup Down

Chapter 7 was about what you rent. This one is about how you arrange it, and the answer is the same answer this book keeps giving in different costumes: *write it down so it can be reproduced, rather than doing it by hand and hoping*.

## The thing everybody does first

**Provisioning** is creating the infrastructure a system needs — machines, databases, networks, permissions — and wiring it together.

Every cloud provider offers a web console for this. You log in, you click through some forms, you choose sizes from dropdowns, you press create. Twenty minutes later you have a running database and a machine to talk to it.

This is called **ClickOps**, and the name is faintly disparaging, which is unfair to how sensible it is the first time. It is fast, it is discoverable, and for exploring what a service even does it is exactly right.

The problem is not the first twenty minutes. It is month four.

By month four you have clicked through perhaps forty screens across several services. Somebody adjusted a setting during an incident and did not write it down. A permission was widened to make something work and never narrowed again. Now:

**Nobody knows what exists.** There are resources running that nobody remembers creating and nobody dares delete, because they might be load-bearing. You are paying for them.

**Nobody can rebuild it.** If the account were lost, or you needed an identical copy for staging, the honest estimate is days of archaeology, and the result would differ in ways you would find out about at the worst moment.

**Nobody can see what changed.** Something broke on Tuesday. Was it a code change or did somebody adjust a setting? The code has a full history — Chapter 4 — and the infrastructure has none. You are debugging with half the evidence missing.

**Staging is not like production.** They were clicked together on different days by different people. Chapter 5's environment parity, quietly gone.

None of this arrives as a crisis. It accumulates, and one day you notice you are afraid to touch the infrastructure.

## Writing it down instead

**Infrastructure as code** — IaC — means describing the infrastructure you want in files kept under version control, and letting a tool make reality match the description.

A written recipe instead of cooking from memory. Anyone can reproduce the dish, you can see exactly what changed between versions, and the knowledge is not confined to whoever happened to cook it last time.

The file says something like: a database of this size, running this version, with backups kept thirty days; two copies of the application container with this much memory; a load balancer in front; and these three things may talk to each other and nothing else may talk to any of them. You run the tool, and it creates all of it. You change a number, run it again, and it changes only what differs.

Every benefit above inverts:

- **What exists** is whatever the files say, and you can read them.
- **Rebuilding** is running the tool against a different account. Minutes.
- **What changed** is a diff in the repository, with a message saying why, reviewed before it happened.
- **Staging and production** are built from the same description with different sizes — genuinely comparable, because they are generated from one source.

The tools are Terraform and its fork OpenTofu (the common choice, works across providers), Pulumi (the same idea in a normal programming language), and each provider's own — CloudFormation on AWS, Bicep on Azure. For small projects, some platforms let a single committed file describe the whole deployment, which is IaC in every meaningful sense even if nobody calls it that.

## The three ideas that make it work

Beyond "write it down", three concepts do the real work, and they are worth understanding because they explain the tooling's behaviour.

### Declarative

**Declarative** means describing the end state you want and letting the tool work out the steps. The opposite — **imperative** — means listing the steps yourself.

Imperative: create a machine, then install this, then set that, then start the service.

Declarative: there should be a machine of this size, running this image, with these settings.

The difference matters because of what happens on the second run. An imperative script run twice tries to create the machine twice. A declarative description applied twice looks at what exists, sees it already matches, and does nothing.

### Idempotent

Which is the property called **idempotent**: safe to repeat. Running it twice leaves you in the same place as running it once.

The analogy to keep, and it is the clearest one available: a light switch labelled ON. Pressing it again does not make the room brighter. Compare a switch labelled TOGGLE, where pressing twice returns you to darkness and you need to know the current state to predict the outcome.

Idempotence is why you can run the tool without fear, and why "did that already apply?" stops being a question you need to answer. It shows up throughout engineering — in Chapter 11 it is what makes automatic retries safe rather than dangerous — and it is one of the genuinely load-bearing words in the vocabulary.

### State and drift

To know what to change, the tool keeps a **state file**: its record of what it believes it has already created.

This introduces one operational obligation. The state file must be shared and locked, stored centrally rather than on somebody's laptop, so two people cannot apply changes simultaneously and produce a record that matches neither. Every tool supports this; it is a setup step, and skipping it is the most common way an IaC setup becomes a mess.

**Drift** is the gap that opens when reality stops matching the description — because somebody changed something by hand. Usually during an incident, at 3am, for a good reason, and then never brought back into the file.

Drift is corrosive because it makes the description a lie while it still looks authoritative. Someone reads the file, believes it, and acts on it. The tools can detect drift; ask for that check to run regularly, and treat a hand-change as something that must be written back into the files the next morning.

## The safety mechanism

The single most important habit here is small, and it is the reason IaC is safe to use even when you cannot read every line.

Every one of these tools can show you a **plan**: a preview of exactly what it would change if you let it, before anything happens. Twelve things to create, three to modify, one to destroy — itemised.

**Read the plan. Especially the destroys.**

You do not need to understand every resource to notice that a plan you expected to add a setting is proposing to destroy a database. That is a genuinely common near-miss: some changes cannot be applied in place, so the tool's solution is to replace the resource, and replacing a database means creating an empty one.

The plan is where that gets caught. It is one of the few places in this book where a person who cannot read the underlying code can still perform the critical safety check, because the summary is in plain language and the dangerous word is *destroy*.

## What this buys you

**Reproducibility** — the property that the same inputs produce the same system, on any day, by anyone — is the thread running through this whole book, and it is worth naming now that you have seen it three times.

The lockfile in Chapter 2 made dependency installation reproducible. Containers in Chapter 7 made the runtime environment reproducible. Infrastructure as code makes the surrounding system reproducible. Chapter 9 makes the path to production reproducible.

The same instinct every time: *do not do it by hand; describe it, commit the description, let a machine execute it*. It is what separates a system you own from one you are merely near.

## Being honest about the cost

IaC has real costs and it is worth naming them, because the enthusiastic version of this chapter would be dishonest.

It is slower to start. Clicking through a console takes twenty minutes; expressing the same thing in files takes an afternoon the first time.

It has a learning curve, and the error messages are not kind.

It is genuinely awkward for one-off exploration. Trying out a service to see what it does does not need a committed description.

So a proportionate position: explore in the console, and once you know what you want, write it down and rebuild it from the files. Anything that production depends on belongs in the files. A scratch experiment does not, provided everyone knows it is scratch and it is deleted afterwards.

## What to ask for

> "Is our infrastructure defined in code, or was it clicked together? If it's clicked, what would it take to describe the important parts in files?"

You are not necessarily asking for the whole thing to be converted. You are finding out which world you are in, because it changes what every later question means.

> "Show me the plan before applying it, and walk me through anything being destroyed or replaced."

The habit. Ask for it every time, and keep asking after you feel silly asking.

> "Where is the state file, and is it shared and locked?"

A short question that catches the single most common structural mistake.

> "Could we build a complete copy of production in a fresh account from what is committed? What is missing?"

The real test of whether you have infrastructure as code or just some files. The gap in the answer is the actual state of things.
