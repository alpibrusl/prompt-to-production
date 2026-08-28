# The Handoff

> **Part I — The Ground**

You described what you wanted. Something built it. It works.

You are looking at a screen where a thing you imagined is now happening — a form that submits, a list that sorts, a page that shows your data arranged the way you asked for it. Twenty minutes ago it did not exist. There is a particular feeling to this moment, and if you have felt it you know that no description does it justice.

Then comes the second question, and it is much harder than the first: *now what?*

This book is about the gap between those two moments. It is a large gap. It is where most of the actual discipline of software engineering lives, and almost none of it is visible in the thing you just built. The agent handled the part that looks like the work. What it handed you is the part that looks like nothing at all.

## The thing on your screen is not the thing

Here is the first and most important idea in this book, and everything else follows from it.

What the agent wrote is **source code**: text that describes what a program should do. Source code is a recipe. It is instructions, written down, in a form precise enough that a machine can follow them. It is not the meal.

To get from the recipe to something a person can use, a second thing has to happen. The source code gets turned into a **program** — something a computer can actually execute — through a process called a **build**. Cooking the recipe. Depending on the language involved this might take a fraction of a second or several minutes, and it might be so automatic that you never notice it happening. But it happens, every time.

The output of a build is an **artifact**: a file or a package that can be handed to a machine and run. And here is the part people find genuinely surprising the first time: *the artifact is disposable*. You do not keep it. You do not carefully back it up. You can always make another one from the source, and if you can't, something is badly wrong. The recipe is the thing you protect. The meal gets eaten.

Then, finally, that artifact has to be put somewhere it will run continuously, reachable by other people. That is a **deploy**. And the place where the version other people actually use is running has a name that carries more weight than any other word in this book: **production**.

Source code. Build. Artifact. Deploy. Production. Five words, one direction. If you take nothing else from this chapter, take the shape of that arrow, because every later chapter is about something that goes wrong somewhere along it.

## Two kinds of wrong

When you were building on your own screen, there was exactly one way for things to be wrong: the code was wrong. You asked for something, the agent misunderstood, or it made a mistake, and the result did not do what you wanted. You looked at it, you saw it, you asked for a fix.

This kind of wrong is *visible* and *immediate*. You are staring at it.

Now consider a different kind. The code is perfect. Every instruction is correct. And yet:

- It works for you and fails for a user in Argentina.
- It worked yesterday and fails today, though nobody changed anything.
- It works for one person and falls over when forty arrive at once.
- It works, and quietly charges you €2,000 this month instead of €20.
- It works, and has been serving one customer's private data to another for eleven days.

None of these are code problems in the sense you are used to. They are **system** problems — and *system* here means everything that has to be working for a user to get what they came for. The program, yes, but also the machine underneath it, the network in between, the database holding the data, the third-party service you call, the settings that differ between your laptop and the real world, and the assumptions everyone made about how much traffic there would be.

You own the system. Not just the code.

This is the actual handoff. The agent gave you code. The system is yours, and it was yours from the moment a real person could reach it.

## Why nobody told you this

It is worth being precise about why this gap exists, because it is not because engineers were hiding anything.

Software engineering as a profession is maybe seventy years old. For most of that time, the only way to get code was to write it, and writing it took years to learn. By the time someone could produce a working program, they had absorbed — slowly, mostly by suffering — everything else: that you keep a history of changes, that you never test on the live system, that secrets do not go in the source, that you need to know when things break before your customers tell you.

None of that was taught as a separate subject. It came bundled. It was the water.

What has changed is that the bundle came apart. You can now get working code without the years, which is genuinely wonderful, and it means the water is gone. Nobody removed it deliberately. It simply was never a separate thing that could be handed to you, so when the code arrived without it, no one noticed the omission.

The people who could tell you are often the worst placed to. Ask an experienced engineer what you need to know and you will get either a shrug — because to them it is not knowledge, it is just how things are — or a firehose of specifics about tools you have no reason to care about. The general shape is hard to see from inside.

That shape is what this book is.

## What you actually need

Let me be honest about the scope of the claim here, because there is a lot of dishonest writing in this area.

This book will not teach you to program. You will not finish it able to read a complicated piece of code and say whether it is good. That is a real skill, it takes real time, and pretending otherwise would waste yours.

What it will do is give you the **vocabulary and the map**. By the end you will know what the parts of a system are called, what each is for, what goes wrong with each, and what "done properly" looks like — well enough to ask for it. That turns out to be most of the value, for a specific reason:

**An agent will build almost anything you ask for, and will rarely tell you what you forgot to ask for.**

Ask for a login page and you will get a login page. Whether you also get password hashing, a way to reset a forgotten password, a record of who logged in when, and a cap on how many passwords can be tried per minute — that depends entirely on whether you knew those things existed.

The agent is not withholding. It is answering the question you asked. The skill you need is not writing code. It is knowing which questions exist.

## The arc of this book

The chapters follow the life of a thing you build, roughly in the order the problems arrive.

**Part I — The Ground** is what you are looking at right now. Where code lives, why there are so many languages, and how the pieces of a typical application fit together. Three chapters of pure orientation.

**Part II — Keeping It** is about not losing or breaking what you have: recording every change so any mistake is reversible, keeping separate copies of your system so you can try things without risk, and writing checks that catch a break before a person does.

**Part III — Shipping It** is about getting the thing to other people reliably: what you are actually renting when you rent a computer, why the setup should be written down rather than clicked together, and how a change should travel from your screen to production.

**Part IV — Living With It** is the part nobody warns you about, and where the real cost of skipping the earlier parts arrives. Knowing what your system is doing. Handling the night it breaks. Not being ruined by a security mistake or a surprise bill.

**Part V — Working With the Agent** turns all of it back into instructions: how to specify work, how to look at a change you cannot fully read, and a plain checklist of what must be true before real people touch what you built.

You can read it straight through, and it is written to be read that way — each chapter assumes the ones before it and nothing else. You can also come back to a chapter when its problem finds you, which, honestly, is how most people will use it.

## A note on the words

There is a lot of jargon ahead. Roughly a hundred and fifty terms, and every one of them will be defined the first time it appears and collected in the glossary at the back.

I want to say something about jargon, because people apologise for it too readily. Jargon is not a barrier that engineers erected to keep you out. Mostly it is *compression*: a word that saves a sentence. "Idempotent" (Chapter 8) is not showing off; it means "safe to run twice", and once you have the word you can express in one adjective a property that would otherwise take a paragraph and get muddled.

The reason jargon feels exclusionary is not the words. It is that people use them without ever having been told what they mean, and asking feels like an admission. So the words become a membership test rather than a tool.

There is no test here. Every term gets defined, in ordinary language, once, and then used consistently. When I commit to an analogy for something — and I will, for the ideas where a good analogy does more work than a definition — I will use the same one every time, rather than reaching for a fresh metaphor each chapter and quietly leaving you to reconcile them.

That consistency is enforced, incidentally, by a program. This book is written in the same way the book describes: the text is source, kept in a repository (Chapter 2) with its full history, checked automatically for terms used before they are defined, and built into what you are reading by a pipeline. If a chapter uses a word it has not yet taught, the build fails. That is not a gimmick. It is the cheapest possible demonstration that the ideas in here are not theory.

## One thing to take from this chapter

If you remember a single sentence, make it this one:

**The code is what the agent gives you. The system is what your users meet, and it is yours.**

Everything that follows is an answer to the question of what owning a system actually involves.

## What to ask for

At the end of each chapter I will suggest things to ask your agent, phrased the way you can actually say them. Here is the first, and it is deliberately modest:

> "Before we add anything else — walk me through what this project currently consists of. What are the pieces, what runs where, and what would need to be true for someone other than me to use it?"

You will not understand every word of the answer yet. Ask it anyway, and keep the reply. By the end of this book you will be able to read it, and it is a useful thing to have watched change.
