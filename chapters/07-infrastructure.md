# What You Are Actually Renting

> **Part III — Shipping It**

Your program — Ledgerly, still — needs a computer to run on. Somebody else's, continuously, reachable from the internet, and you will pay for it monthly.

That much is obvious. What is not obvious is that there are four or five quite different things you might rent, they differ enormously in cost and in how much work they leave you, and the choice is usually made in the first ten minutes of a project by whoever set it up — which, now, may be an agent that was not asked to explain itself.

## The word "server", twice

A **server** in the sense used there is a *role*: a program that waits for requests and answers them. A **server** in the sense used here is a *machine*: a computer, somewhere, that runs your program continuously. You will also hear it called a box, a host, an instance, or a node.

The role runs on the machine. One machine can run several server roles; one server role can run across many machines. Which meaning is intended is almost always clear from context, and when it is not, ask — engineers are so used to the ambiguity they stop noticing it.

A **cloud provider** is a company that rents you these machines by the minute: Amazon Web Services, Google Cloud, Microsoft Azure, and a large second tier including DigitalOcean, Hetzner, Fly, Render and Railway. The first three are vast and can do anything, at the cost of considerable complexity. The others are smaller, simpler, and frequently a much better fit for a small application than the reflex choice of AWS.

## The ladder

There are roughly five levels, and they trade control against work in a consistent direction.

<div style="margin:1.6rem 0;">
<svg viewBox="0 0 660 300" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="ptp7-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
<path d="M0,0 L6,3 L0,6" fill="none" stroke="#1a1a1a" stroke-width="1.1"/>
</marker>
</defs>
<line x1="30" y1="255" x2="30" y2="30" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp7-arrow)"/>
<text x="36" y="24" text-anchor="start" font-family="EB Garamond, Georgia, serif" font-size="10.5" letter-spacing="0.06em" fill="#9a9a9a">MORE CONTROL</text>
<line x1="30" y1="255" x2="640" y2="255" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp7-arrow)"/>
<text x="640" y="272" text-anchor="end" font-family="EB Garamond, Georgia, serif" font-size="10.5" letter-spacing="0.06em" fill="#9a9a9a">LESS OPERATIONAL WORK</text>
<rect x="55" y="205" width="108" height="42" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="109" y="230" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-weight="600" fill="#1a1a1a">PHYSICAL MACHINE</text>
<rect x="175" y="163" width="108" height="42" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="229" y="188" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12" font-weight="600" fill="#1a1a1a">VM</text>
<rect x="295" y="121" width="108" height="42" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="349" y="146" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12" font-weight="600" fill="#1a1a1a">CONTAINER</text>
<rect x="415" y="79" width="120" height="42" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="475" y="100" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-weight="600" fill="#1a1a1a">MANAGED</text>
<text x="475" y="114" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-weight="600" fill="#1a1a1a">SERVICE</text>
<rect x="547" y="37" width="108" height="42" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="601" y="62" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="11" font-weight="600" fill="#1a1a1a">SERVERLESS</text>
<text x="330" y="290" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-style="italic" fill="#444">Each rung up trades a little more control for a little less to maintain.</text>
</svg>
</div>

**A physical machine.** An actual computer in an actual building. Almost nobody starts here anymore. Mentioned only because it is the thing everything else is pretending to be.

**A virtual machine.** A software-simulated computer running on a share of a real one, with its own operating system. This is what you get when you rent "a server" — an EC2 instance, a Droplet, a Compute Engine instance. You get a whole machine to yourself, and with it responsibility for everything on it: security updates, the language runtime, the web server, the certificates, disk space, log rotation.

Maximum control, maximum ongoing work. A virtual machine that nobody maintains for a year is a security incident waiting for a date.

**A container.** This one deserves the space it gets below.

**A managed service.** Something you would otherwise run yourself — a database, a queue, a cache, a search index — operated by the provider for a fee. You do not install it, patch it, back it up, or get woken when its disk fills.

Managed services are usually the right call and people resist them because the sticker price looks high next to running it yourself. That comparison is wrong, and predictably so: it counts the machine and not the hours. A managed database at €50 a month against a €10 machine looks like a bad deal until the first time the €10 database needs restoring from a backup at 2am and you discover the backups were never configured. **Pay for managed databases.** If this book gives you one piece of infrastructure advice, that is it.

**Serverless.** You hand over a piece of code and the provider runs it on demand, charging per execution. There are still servers; you just never meet them.

Think of paying per photocopy at a print shop rather than buying the copier. Wonderful for work that is occasional or wildly uneven — you pay nothing while nothing is happening, and it scales without you thinking about it. Less good for constant heavy load, where per-execution pricing gets expensive, and it comes with real constraints: a time limit per execution, and a delay when a piece of code that has been idle is started up again, called a cold start.

## Containers

A **container** is your program packaged together with everything it needs to run, in a standard wrapper that any host can start without knowing what is inside.

The analogy is the actual shipping container, and it is worth taking seriously because it explains why they took over. Before standardised shipping containers, loading a ship meant handling barrels and crates and sacks individually, and every port needed to know what it was handling. After, the outside is always the same size and shape. The crane does not care whether it holds bananas or car parts. The ship does not care. The truck does not care. Only the contents differ, and only the sender and receiver need to know them.

A container does that for software. Inside is your code, the right version of the language runtime, every dependency, and the system libraries it expects. Outside is a standard interface every host understands. The machine running it needs to know nothing about what is inside.

The consequence, and the reason this is in Part III rather than a footnote: **it runs identically everywhere.** The thing you ran on your laptop is bit-for-bit the thing running in production. This is the largest single improvement to environment parity available to you, and it closes most of Chapter 5's "works on my machine" gap in one move.

The vocabulary is small:

- A **container image** is the built, frozen contents — the artifact you deploy. A running copy of an image is a container. Image is to container as recipe is to meal, one level up from Chapter 1.
- A **registry** is where built images are stored and fetched from, the way a repository stores source.
- A `Dockerfile` is the text file describing how to build the image. It is source, and it belongs in your repository.

Docker is the tool everyone means when they say containers. There are others; they are compatible.

**Orchestration** is software that decides which containers run on which machines, restarts them when they die, and moves them when a machine fails. Kubernetes is the dominant one, and here is the honest guidance: **you almost certainly do not need it.** Kubernetes is superb at running hundreds of services across dozens of machines for a team with people dedicated to it. For one application and a small team it is a second full-time system to operate, and the failure mode is a project where more effort goes into the orchestration than the product. Every major provider offers a "run this container" service that does the useful 90% with none of that. Start there.

## When one machine is not enough

At some point one machine cannot serve everyone. There are two directions out, and they are not equivalent.

**Vertical scaling** is giving one machine more power. Simple — often a dropdown and a restart — and it runs out. There is a largest machine, and you will pay disproportionately for it.

**Horizontal scaling** is running more copies of your program. It does not run out, and it is the reason Chapter 3 made a point about statelessness. If each copy remembers who is logged in, then a user bouncing between copies is randomly logged out, and adding copies makes things worse. If the copies remember nothing and the database remembers everything, then any copy can serve any request and you can run three or three hundred.

**This is why stateless design matters, and it is the payoff for that section.** Getting it right early costs nothing. Retrofitting it is a rewrite.

Distributing requests across copies is the job of a **load balancer**: the component that receives incoming traffic and spreads it across the running copies, skipping any that report themselves unhealthy. The host at a restaurant door, sending each arrival to whichever till is open — and, importantly, not to the till that just closed.

## Where in the world

Two more terms because they have consequences beyond the technical.

A **region** is the geographic location of the data centre your system runs in. It determines how long requests take for your users — physics is not negotiable, and a request from Madrid to Virginia and back cannot be fast — and, more importantly, which laws apply to your data. If your users are European and their personal data sits in a US region, you have a legal question, not a performance one. Chapter 12 returns to this.

An **availability zone** is one physically separate data centre within a region. Running across several means one building's power failure is not your outage. Most managed services offer this as a checkbox. Tick it.

## Choosing, briefly

You are not going to make this decision alone, but you should be able to recognise a bad one.

For most small applications in 2026, a reasonable default is: **your application in containers on a platform that runs containers for you, and a managed database.** Not a hand-maintained virtual machine, because of the ongoing work. Not Kubernetes, because of the complexity. Not a self-run database, because of the night it breaks.

The signs that something has gone wrong in the choosing:

- Setting up a new environment takes days, or only one person can do it.
- Nobody can say what is running on a particular machine.
- The database is on the same machine as the application. When one is under strain, both are.
- There is exactly one of everything, and no answer to what happens if it stops.

## What to ask for

> "What are we running on, what does each piece cost per month, and what happens if each one fails?"

Three questions in one, and the third is the one that reveals things. "It would go down and I would notice from a customer email" is a real answer, and sometimes an acceptable one — but it should be a decision rather than a discovery.

> "Is our database managed, with automated backups? When was a restore last tested?"

An untested backup is a belief, not a fact — Chapter 16 has the fuller version of this rule.

> "Are we running more than one copy, and is the application stateless enough for that to work?"

The Chapter 3 question, arriving at the moment it becomes concrete.

> "Do we need Kubernetes for this, honestly? What would we lose with a simpler container platform?"

Ask this if the word appears. Sometimes the answer is genuinely yes. It should be argued rather than assumed.
