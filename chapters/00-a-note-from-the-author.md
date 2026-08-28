# A Note from the Human Author

Everything in this book describes how people learned to build software. Every practice in it was invented by humans, for humans.

Tools carry the assumptions of their makers. A hammer assumes a wrist. Version control assumes someone who forgets what they did last Tuesday. Tests assume someone who cannot hold a whole system in their head at once. Code review assumes someone who makes mistakes they cannot see in their own work. Separate environments assume someone who needs a safe place to be wrong. Each of these is an honest accommodation of a human limitation, and each has earned its place over fifty years.

An agent has none of those limitations in the same shape, and it has others we are only beginning to understand. It does not forget between Tuesdays; it forgets between sentences. It does not make the mistakes a tired person makes; it makes confident, fluent, entirely invented ones. Handing it our tools is therefore not a neutral act. It is a choice, and mostly an unexamined one.

I have argued elsewhere — at `alpibru.com/manifesto` — that this is the central error of the current moment: that we are asking agents to be very fast humans when they could be something else, and that the deeper move is to stop treating comprehension as the basis for trust and start treating verification that way. A type system that proves a function cannot touch the network tells you something no amount of careful reading will. Comprehension was a strategy. It is not the only one.

So I should be honest about the status of this book. It is an accurate account of how software is built today. I do not think it is the final form.

But it is worth separating which parts of it are load-bearing and which are scaffolding.

The parts I expect to survive are the ones this book leans on hardest, and that is not a coincidence. Say what "done" means before the work starts. Make the check automatic, and make failing it block. Keep the record of a decision, not just its result. Know what your system is doing without having to read it. Be able to undo. Every one of those is verification, and not one of them asks you to comprehend anything.

The parts I am less sure of are the comprehension-shaped ones. Reading a change line by line. Review as an act of reading. A codebase treated as something you must understand rather than a contract you must satisfy. Those are prosthetics for human memory, and they may not be what an agent needs — or what you need in order to direct one.

Here is the part I find genuinely interesting, and the reason I do not think this book contradicts that argument.

You are reading it because you cannot read the code. That is precisely the position the argument describes: trust that cannot rest on comprehension, because comprehension is not available to you. And notice what this book actually teaches you to do instead. Specify before building. Demand tests. Make the pipeline the only path to production. Watch the system rather than inspect it. Keep a way back. All of that is what you do *instead of* understanding.

You are already living in the world I am describing. You simply arrived at it from the other direction — not because the systems outgrew human comprehension, but because you never had it to begin with.

What does not change, in this book or in that argument, is where responsibility sits. Someone is accountable for a running system, and it is not the agent. Machinery can carry verification. It cannot carry accountability, and no improvement in the machinery will move that line.

Read the rest as the current best answer. Not the final one.

— Alfonso Sastre
