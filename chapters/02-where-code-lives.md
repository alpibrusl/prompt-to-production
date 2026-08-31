# Where Code Lives

Somewhere on your computer there is now a folder — Ledgerly's, say, or whatever you called yours. Inside it are files with names like `app.py` or `index.tsx` or `main.go`, arranged in subfolders, some of which you did not ask for and do not recognise.

This chapter is about that folder: what is in it, why it is shaped that way, and the one part of it that is not really yours.

## The folder is a repository

The folder holding a project's source code is called a **repository** — repo, in speech, always.

That word is doing more work than "folder" does, and the difference matters. A folder holds the current version of some files. A repository holds the current version *and the complete history of every change ever made*. Every edit, who made it, when, and why. Not just the last few. All of it, from the first line onward, permanently.

The right image is not a folder. It is a workshop with a perfect logbook: the bench holds what you are working on now, and the logbook records every single thing that has ever been done at that bench, in order, recoverable.

That history is what makes the next chapters possible, and it is the reason a repository is not merely a place to put things. Chapter 4 is entirely about it. For now: the folder is a repository, the history is the point, and everything inside it that matters is plain text.

The **codebase** is a related word you will hear constantly — it means all the source code of a project considered as one body. "The codebase is a mess" is a statement about the code; "the repository is a mess" is more likely a statement about how it is organised or how its history was kept.

## Why there are so many languages

Open a few of those files and you will notice they are written in something that is not English but is trying to be readable. That is a **programming language**: a notation for writing source code, with fixed rules about what counts as a valid instruction.

The obvious question, and one people are strangely reluctant to ask out loud, is why there are so many of them. Hundreds in use. Dozens in common use. It looks like a failure of coordination.

It is not. Languages were designed for different jobs, at different times, under different constraints, and the differences are real:

- **JavaScript and TypeScript** run inside web browsers. For a long time nothing else did, which is why they are everywhere on the web regardless of their merits. TypeScript is JavaScript with an added layer that catches a category of mistakes before the program runs.
- **Python** was designed to be readable and quick to write. It dominates data work, scripting, and machine learning, and it is a common choice for the back half of web applications.
- **Go** and **Rust** were built for programs that must be fast and handle enormous load without falling over. Rust in particular is designed to make an entire category of memory bugs impossible.
- **Java** and **C#** are the languages of large, long-lived corporate systems, where the priority is that a hundred people can work on the same thing for a decade.
- **SQL** is not really in the same family. It is a language for asking questions of stored data, and you will meet it in Chapter 3.

A typical modern application uses several at once — one for the part in the browser, one for the part on the server, SQL for the data — and that is normal rather than a sign of disorder.

There is a distinction worth having, because it explains a class of confusion later. Some languages are **compiled**: the source is translated ahead of time, in a build step, and what you deploy is the translation rather than the original source. Go and Rust translate all the way to machine instructions the processor runs directly. Java and C# translate to an intermediate form that still needs a runtime (the JVM, the .NET runtime) to run it — a real build step either way, just not quite the same destination. Others are **interpreted**: the source is read and executed on the fly by another program, with no separate translation step, so what you deploy is the source itself. Python and JavaScript work this way.

The practical consequence: with a compiled language, a whole class of mistakes is caught before anything runs, because the translation refuses to complete. With an interpreted language, you find out when the line is reached, possibly in front of a user. Neither is better. It is a trade between speed of discovery and speed of change, and both camps are fully convinced.

You do not need to choose. Your agent will use whatever is conventional for what you are building. What you need is to not be startled when a project has files in four languages, and to know that "it compiles" means a mistake did not happen rather than that the thing works.

## The part of the folder that is not yours

Now look at the subfolder you did not ask for. Depending on the language it is called `node_modules`, or `venv`, or `vendor`, and it is enormous — frequently far larger than everything you and the agent wrote put together.

That is other people's code.

A **library** is a package of somebody else's code, built so your code can use it without you understanding its insides. If you need to send an email, or resize an image, or work out what date it will be in ninety days accounting for leap years and time zones, you do not write that. Somebody solved it years ago, carefully, and published the solution. You use theirs.

A library your project needs in order to work is a **dependency**. The name is exact and worth taking seriously: you depend on it. If it breaks, your project breaks. If it changes in a way you did not expect, your project changes. If the person maintaining it stops, you have a problem that is now yours.

A **framework** is a large library with a stronger opinion. Rather than offering you tools you call when you like, it supplies the overall shape of an application and leaves you to fill in the parts specific to your problem. React, Django, Rails, Next.js are frameworks. The distinction is sometimes summarised as: you call a library, a framework calls you.

The **package manager** is the tool that fetches all of this. You say you need a particular library; it downloads that library, and everything that library needs, and everything *those* need, down as many levels as it takes. `npm` for JavaScript, `pip` or `uv` for Python, `cargo` for Rust. This is why the folder is enormous. You asked for four things and got eleven hundred.

## The number that should give you pause

Here is a real and typical shape for a modest web application: you and the agent wrote perhaps three thousand lines. The dependencies amount to somewhere between two hundred thousand and several million lines, written by hundreds of people you have never met, most of whom have no idea you exist.

That whole tree — everything your program depends on, directly and through other dependencies — is your **supply chain**.

Most of it is **open source**: source code published for anyone to read, use and modify, under a licence that sets the conditions. This is one of the genuinely remarkable things about the industry. An extraordinary quantity of critical infrastructure is maintained by volunteers and given away, and essentially every company on earth runs on it.

It is also a real exposure, in two directions.

The first is **abandonment**. A library you depend on is maintained by one person. That person gets a new job, or a child, or simply loses interest. The library stops receiving fixes. Nothing breaks immediately — this is the insidious part — but a year later a security flaw is found in it and no fix is coming, and now the problem is yours to solve in a piece of code you have never read.

The second is **malice**. Someone publishes a useful library, waits until thousands of projects depend on it, and then publishes a version containing something that steals credentials. This is not hypothetical; it happens several times a year, and it has hit packages downloaded millions of times a week. Chapter 12 covers what to do about it.

Neither risk is a reason to avoid dependencies. Writing everything yourself is not safer — your own hand-rolled version of something subtle will have worse flaws than the widely-used library, and nobody will be reviewing it. The reason to understand the supply chain is more modest: so that you know it is there, and so that when someone says "we should reduce our dependencies" you understand that this is a real engineering position and not fussiness.

The useful instinct is proportion. A library that saves a week of work is worth it. A library pulled in to save four lines is a bad trade — you have taken on a permanent relationship to save an afternoon.

## The file that pins everything down

There is one more file worth knowing by name, because it is the answer to a question that will otherwise puzzle you.

The question: if a package manager fetches the newest version of everything, and libraries are constantly updated, how does a project built today match one built next month?

The answer is a **lockfile** — `package-lock.json`, `poetry.lock`, `Cargo.lock`, `uv.lock`, depending. It is generated, not written, and it records the exact version of every single dependency actually installed, all eleven hundred of them, right down to the precise release.

With a lockfile, a build next year fetches exactly what a build today fetched. Without one, everyone builds something subtly different and nobody knows why one of them fails.

Two rules follow, and they are close to universal practice for good reason:

**Commit the lockfile.** It belongs in the repository. It is not clutter and it is not a build artifact, despite being generated — it is a record of a decision.

**Never edit it by hand.** It is generated by the package manager and should only ever be changed by the package manager. Editing it directly is how you produce a project that installs differently from what it claims to install.

This is the first appearance of a pattern that runs through the whole book: *make the thing reproducible, then keep the record of how*. You will see it again with environments, with infrastructure, with deployment. It is arguably the single deepest idea in software engineering, and it shows up first in a generated file most people never open.

## What the agent can reach

Open a terminal next to the chat window and the difference between "the agent suggests a command" and "the agent runs a command" disappears. Read a file, run tests, install a package, commit a fix — increasingly, it just does these, without you typing anything yourself.

That is real, not a simulation of it, and it raises a question with two genuinely different parts worth keeping apart: what you allow it to do, and what it can reach at all.

The first is a matter of scope. A command that stays inside your project — editing a file, running its tests — is low-stakes, and a well-built agent gets on with these without asking each time. A command that reaches past the project is a different order of thing: installing something system-wide, changing shell configuration, anything beginning with `sudo`. `sudo apt-get install` is close to the canonical example. It sounds like ordinary maintenance, and it is also a command that can alter the machine outside anything you are building, with full privileges, on your say-so alone. A well-designed agent asks before running one of these rather than assuming an earlier yes still applies, and the correct posture on your side is not "let it run this freely" — it is "let it ask, every time, and read the request before answering." That is not being difficult. It is close to universal practice among careful users, for good reason.

The second part is not about permission at all — it is about whether there is a path there to begin with, and this is where working arrangements genuinely differ. An agent running directly on your laptop, in a terminal or an editor, has the reach of your own user account: your other projects, your files, whatever else lives on that machine, once you say yes. Increasingly, though, the agent is not on your laptop. It is running in a **sandbox** — an isolated space set up somewhere else, holding nothing but the project it was handed for this conversation. Ask that one to check a file in your downloads folder and it cannot, not from refusal but because no path exists from where it is standing to where that file lives. It was never given one.

That is a hard boundary, not a policy one. Where the `sudo` question is a choice you make, this one cannot be argued past — a sandbox with no connection to your laptop stays that way regardless of how the request is phrased. It is also, deliberately, part of the design: a session that can only touch what it was explicitly handed is one where a mistake stays contained, and where nothing survives beyond the conversation that made it unless you were the one who moved it out.

Knowing which situation you are in changes what a request like "just grab it from the file on my desktop" means. To an agent on your laptop it is an instruction. To one in a sandbox somewhere else, there is nothing on the other end of that sentence, and "I don't have access to that" is the honest answer rather than a sign that something is broken.

## What to ask for

> "Show me the dependency list, and for each one tell me in a sentence what it does and whether we would be in trouble if it were abandoned."

You are checking two things: that your agent can justify each one, and that you learn the shape of your own supply chain. An answer like "this saves us implementing date arithmetic, which is genuinely hard to get right" is good. An answer that amounts to "it was convenient" is worth a follow-up.

> "Is the lockfile committed?"

A short question with a yes or no answer, and worth asking once at the start of any project. If the answer is no, the fix takes ten seconds and prevents a category of problem that is miserable to diagnose later.

> "Before you run anything that reaches outside this project's folder — installing something system-wide, changing configuration that is not part of the repo — ask me first, every time, even if I said yes to something similar last time. And tell me plainly: are you running locally or somewhere else, and what can you actually see from there?"

The first half keeps the `sudo` question a live one rather than a standing yes. The second tells you, in one answer, whether "grab it from my desktop" is a request the agent can act on or one it cannot — which saves a confusing round trip the moment you assume the wrong one.
