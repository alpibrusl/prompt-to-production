# You Are the Single Point of Failure

Two months from now, you take a genuine two-week holiday, properly offline. While you are gone, a customer reports that exports have stopped including tax numbers — a rule that was added deliberately, for one specific customer, for a specific legal reason, six weeks ago. Nobody else knows why the rule exists. It is not in a comment. The commit message says "fix export." It is not in your head either, by the time you are asked, because six weeks is long enough to forget a thing you never wrote down.

The agent you ask to look into it reads the code, finds the rule, and explains confidently what it does. It cannot tell you why, because *why* was never in the code to begin with. It was in a conversation that ended in June.

## You are the redundancy

Chapter 11 defined a **single point of failure** as a component whose failure takes everything with it, and it named one on the way past almost as an aside: *"One person who knows how the deployment works — that one counts, and people forget it does."* This chapter is that sentence, taken seriously.

In a system built by a team, knowledge is redundant more or less by accident. Three engineers have opinions about why the pricing logic is shaped the way it is, and even if two of them are wrong about the details, one of them remembers enough. That redundancy is not a policy anyone chose. It is a side effect of having several people who were in the room.

You do not have that side effect. You have one person who was in every room — every conversation with the agent, every decision, every "let's do it this way for now" — and that person is you. Nothing else in the system holds what you hold. Not the code, which shows *what* was decided but rarely *why*. Not the agent, which was there for each conversation individually and holds none of them in relation to each other.

## Bus factor

**Bus factor** is the number of people who could disappear from a project before it stalls — named for the notion of being hit by a bus, and used dryly in engineering because the alternative is not thinking about it at all.

Most advice about it is aimed at teams: get it above one, cross-train, document the parts only one person understands. That advice assumes the fix is *another person*. You may not have one. What you have instead is an agent that can execute a plan the moment it exists, and can hold none of the reasoning behind it a session later.

This makes your bus factor exactly one, in a way that is structural rather than circumstantial. It is not a gap you failed to close. It is the shape of building this way, and pretending otherwise is how the tax-number rule happens.

## Why the agent cannot cover for you

It is tempting to think of the agent as a colleague who can pick up your work while you are out. It cannot, and the reason is not competence.

A human colleague who does not remember a decision says so. "I don't recall why we did it that way — let me check." That sentence is useful information: it tells you to go looking elsewhere. An agent that does not have a decision in its context does not reliably produce that sentence. It produces a plausible-sounding account instead, built from the code and from general knowledge of how such things are usually done, delivered in exactly the same confident register as something it actually knows. Chapter 14 named this pattern already: *confidence that is not evidence.* This is where it costs you the most, because there is no colleague in the loop to notice the tell.

A person forgetting is a gap you can usually see. An agent re-deriving is a gap disguised as an answer.

## Externalizing what only you know

The fix is not to remember harder. It is to move the decisions that must not silently drift out of your head and into something every session reads, so continuity does not depend on your availability, your memory, or which agent happens to be running.

Not everything qualifies — most choices are cheap to redo or reverse, and writing all of them down is how a project ends up with a document nobody reads. What belongs here is narrower: a pricing rule with a reason behind it, a data-retention period, who is allowed to see what, why the boring option was rejected in favour of the unusual one. The test is the one from Chapter 13: if getting it wrong later would be expensive or hard to undo, it earns a place in writing. Everything else can stay a conversation.

Two properties matter more than where exactly it lives:

**It has to be read automatically, not found.** A decision in a six-month-old commit or a chat log you would have to search for is not externalized in any way that helps at 3am, or on a Tuesday when someone else is doing the work instead of you. It needs to be somewhere the agent is told to read at the start of every session, by default, without being asked.

**Stale is worse than absent.** A note that says the rule was removed last year, when it was not, will be trusted exactly as much as a true one — the confidence looks identical from the outside. An out-of-date record actively misleads in a way a missing one does not; missing at least prompts a question. Treat the file the way Chapter 4 treats the lockfile: update it in the same change that makes it wrong, not sometime after.

## The test

Here is the version of this that does not require imagining a holiday: **could someone else — or you, in six months, having genuinely forgotten — pick this project up from what is written down alone?**

That is not a rhetorical question. It is answerable today, and Chapter 16 asks it directly: *if only you can build it, the project's continuity is a property of your availability.* This chapter is the reasoning behind that one line. A system nobody but you can explain is not fully built yet, whatever it does in production, because the part that is missing is the part that survives you being unavailable — which is, eventually, everyone's situation, on a long enough timeline.

## What to ask for

> "List every decision in this project you can only explain because I told you, in this conversation, at some point. For each one — is it written down anywhere you'd read it automatically next session?"

The direct version of the test above. The gaps it finds are usually few, and usually the ones that would have mattered.

> "If I disappeared for a month starting today, what would the next person — human or agent — get wrong first?"

A different angle on the same question, and often surfaces a different answer, because it forces a specific failure into view rather than a general audit.

> "Is anything in our written notes actually out of date? Check it against what the code does now."

Worth asking periodically, not just once. A stale record is the failure mode that looks fine right up until it does not.
