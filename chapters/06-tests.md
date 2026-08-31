# The Question You Ask Automatically

Of all the practices in this book, automated testing is the one that most reliably gets skipped by people building with an agent, and the one whose absence is most expensive.

The reasoning for skipping it is understandable. Tests are extra code. They do not do anything a user sees. Writing them feels like a detour from building the thing. And the agent produced working code without them, so what exactly are they for?

Here is what they are for, and it is not what most explanations lead with.

## Tests are not for finding bugs

A **test** is a small program that runs your program, checks it did the right thing, and reports pass or fail without a human watching.

The naive account is that tests catch mistakes. They do, sometimes. But if that were the whole story they would be a poor investment, because for the mistake to be caught you must have anticipated it, and if you anticipated it you would probably have avoided it.

The real value is different, and much larger: **tests are what let you change things.**

Consider the position you are in without them. Your application works. You want to add a feature. The agent changes six files. Does anything else still work?

You do not know. You cannot know. You can click around the parts you remember, which covers perhaps a fifth of what the system does, and then you deploy and find out from your users.

Now the same situation with a decent test suite. The agent changes six files. You run the tests. Forty seconds later you know that the other hundred and forty things the system does still do them. Not because someone was clever, but because somebody wrote the question down once and now it gets asked automatically, forever, for free.

That is the analogy worth keeping: **a test is a question you write down once and can then ask forever.**

Without tests, every change is a gamble whose stakes rise as the system grows. With them, changing things is routine. The difference compounds — a project without tests becomes progressively harder to change until people are frightened of it, and a project with them stays workable. This is why experienced engineers are insistent about testing in a way that can seem disproportionate. They are not being fastidious. They have been trapped in the first kind of project.

The specific reason this matters *more* when an agent writes the code, not less: you did not write it, so you have no memory of what it touches. Your intuition about what a change might break — the thing an experienced engineer relies on — does not exist. The test suite is that intuition, externalised and made explicit.

## What a test looks like

Tests are simpler than people imagine. Almost all of them have three steps, and once you see the pattern you can read a test even if you cannot write one.

```python
def test_discount_applies_to_invoice_total():
    invoice = Invoice(items=[Item(price=100), Item(price=50)])  # arrange
    invoice.apply_discount("SAVE10")                              # act
    assert invoice.total == 135                                   # assert
```

This is Ledgerly's own test, more or less — an early-customer discount applied to an invoice total.

Set up a known situation. Do the thing. State what must be true afterwards.

That last line is the **assertion** — the statement of what must hold. If `total` is anything other than `135`, the assertion fails, the test fails, and you get told precisely which expectation was violated.

The known starting situation is a **fixture**. It matters that it is known and identical every run; a test that starts from whatever happens to be lying around gives a different answer each time and tells you nothing.

All of a project's tests, run together as one gate, are the **test suite**.

## The three kinds, and how much of each

Tests come in layers, and the difference is how much of the real system each one exercises.

A **unit test** checks one small piece of logic in isolation, with everything around it faked. Does the discount calculation give the right number? No database, no network. These run in milliseconds, you can have thousands, and when one fails it points at exactly one function. Their weakness is that they prove nothing about whether the pieces fit together — every part can be individually correct while the whole is broken.

An **integration test** exercises several real pieces together: your code plus an actual database, say. Slower — seconds rather than milliseconds — but it catches the class of failure unit tests are blind to, which is the wiring.

An **end-to-end test** drives the whole system the way a user would, from the screen inward. It opens a real browser, clicks the real button, and checks the real result. The most convincing kind by far, and the most expensive: slow to run, slow to write, and the most prone to breaking for reasons that have nothing to do with your code.

The standard advice is to have many unit tests, some integration tests, and a few end-to-end tests covering only the paths that genuinely must never break — signing up, logging in, paying. This shape is conventionally drawn as a pyramid, and the reasoning is economic rather than aesthetic: you want most of your checking to be fast enough to run constantly.

The failure mode at each extreme is real. All unit tests and nothing else: every component works, the application does not. Everything end-to-end: the suite takes forty minutes, so people stop running it, so it stops mattering.

**Faking the surroundings.** A **mock** — also stub, fake, test double — is a stand-in for a real dependency during a test. When your code calls a payment provider, the test substitutes something that pretends to be one, so the test is fast and does not charge anyone. Necessary, and worth one caution: a mock encodes your *belief* about how the real thing behaves. If that belief is wrong, your test passes and production fails, and it will be a genuinely confusing hour.

## The blind spot you cannot test your way out of

Everything above was true ten years ago. This part is not.

When you ask an agent to write a feature and then ask the same agent to write tests for it, something happens that has no equivalent in the world these practices came from: **the code and the tests are produced by the same mind, from the same reading of your request.**

If that reading was wrong, both are wrong in the same direction. The implementation does the wrong thing; the test asserts that it does the wrong thing; the suite goes green. You have not gained a check — you have gained a very confident second opinion from the same source.

This is not hypothetical, and it is not rare. It is the default outcome when the misunderstanding is in the *requirement* rather than in the code. Suppose you asked Ledgerly's agent for a discount that applies to the invoice total, and it understood "the total before tax". It will implement that, and its test will assert `135` for exactly the arithmetic it already believes in. Every test passes. Everything is wrong. Nothing anywhere will tell you.

Tests written by a human have the same weakness in principle, which is why review by a second person exists. What is new is the *scale and confidence*: a single agent can produce implementation, tests, and a persuasive explanation of why they are correct, all sharing one flawed premise, in under a minute.

Four things narrow the gap, none perfect:

**Write the acceptance criteria yourself, first.** Chapter 14 is about this properly. If you state the expected answer — "a 10% discount on a €150 order leaves €135, and shipping is charged on top" — then the test is written against *your* sentence rather than the agent's inference. This single habit fixes more of this problem than the other three combined.

**Ask for tests from the specification, not from the code.** "Write tests for this function" invites the agent to read the implementation and describe it back. "Write tests for these acceptance criteria, without looking at how it was implemented" is a different request, and it produces different tests.

**Supply the failure cases yourself.** You may not know how to implement anything, but you know your business. What happens with a discount code that expired yesterday? With a negative quantity? With the same code used twice? Those are the cases where an agent's assumptions are least reliable and your knowledge is most reliable, and they are exactly where you should spend your attention.

**Be suspicious of a suite that has never failed.** If a test has passed on every run since it was written, it has demonstrated nothing except that it runs. The regression rule from the last section is partly a defence against this: a test written to reproduce a real bug has, at least once, been proven capable of failing.

None of this makes agent-written tests worthless. They catch typos, broken wiring, and the regressions of Chapter 6's main argument perfectly well, and having them beats not having them by a wide margin. What they cannot do is tell you that you asked for the wrong thing. **That check has no automated form. It is yours.**

## Regressions and the fixing rule

A **regression** is a failure in something that used to work. It is the most demoralising category of bug because it means you went backwards, and because it tends to arrive in something nobody was thinking about.

There is one practice that repays itself more than any other in this chapter, and it is small enough to adopt today:

**When you find a bug, write a test that fails because of it. Then fix it.**

The test now fails, proving it genuinely reproduces the problem. Then the fix makes it pass, proving the fix works. And the test stays, so that particular bug cannot quietly return without the suite noticing.

Do this consistently and your test suite grows in exactly the places your system is weak — shaped by real failures rather than by guesses about where problems might live. It is the cheapest possible way to build a suite that is actually about your system.

## Coverage, honestly

**Test coverage** is the percentage of your code that runs at least once when the suite runs.

It is useful and it is routinely misunderstood, so be precise about what it means: coverage measures *what is not tested*. It does not measure what is correct. A line can be executed by a test that asserts nothing about it, and it counts as covered.

So: low coverage is genuine evidence of a problem. Somewhere between 60% and 80% is a reasonable place for most projects, and the untested part should not be the part that handles money or permissions. But 100% coverage is not a goal worth pursuing — it is achieved by writing tests for things that cannot fail, which costs time and adds noise. And a high number tells you nothing about quality on its own. Coverage is a smoke detector, not a safety certificate.

## Flaky tests, and why they are urgent

A **flaky test** passes and fails on the same code, unpredictably. Usually because it depends on timing, or on the order tests run in, or on something outside itself like a network call.

Flakiness is the most dangerous condition a test suite can be in, and it deserves more alarm than it usually gets. A suite that fails randomly teaches everyone to re-run it and carry on. Once that habit exists, a *real* failure gets the same treatment — re-run, shrug, merge — and the suite has become worse than useless, because it provides confidence without providing checking.

Treat a flaky test as broken. Fix it or delete it. The one thing never to do is leave it failing intermittently while everyone learns to ignore it.

## Where tests fit

Tests are only worth having if they run automatically. A suite that requires someone to remember will be forgotten in a fortnight.

Chapter 9 covers this properly, but the shape is: every proposed change runs the suite automatically, and a failure blocks the merge. No exceptions and no override, because an override that exists gets used at 6pm on a Friday.

This is the connection back to Chapter 4. The pull request is where the tests report. That is what makes the PR a gate rather than a formality.

## What to ask for

> "Write tests for this before we move on. Cover the normal path, the obvious ways it can fail, and the edge cases."

Say this while each feature is being built, not later. Retrofitting tests onto a finished system is genuinely unpleasant work, and it is the single most common reason projects never get them.

> "Write a test that fails because of this bug, then fix it."

The regression rule. Ask for it in exactly this order, every time.

> "What is our coverage, and which important parts are not covered?"

The second half of that question is the one that matters. A number alone is not information; "the payment logic has no tests" is.

> "Are any of our tests flaky? If so, fix them or delete them."

> "Write these tests from the acceptance criteria I gave you, not from the code you wrote. And list the cases you decided not to cover."

The second sentence is the useful one. It surfaces the assumptions that would otherwise be invisible, and it is where you will most often find that you and the agent understood the request differently.

Ask occasionally. Flakiness accumulates quietly, and by the time it is obvious the habit of ignoring failures has already formed.
