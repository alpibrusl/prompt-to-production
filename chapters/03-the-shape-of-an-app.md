# The Shape of an App

Almost every application you are likely to build has the same three parts. Different names, different technologies, same shape. Once you can see it, a great deal of what engineers say to each other stops being opaque.

## Somebody asks, somebody answers

Start with the smallest possible version of the idea.

A **client** is the side that asks for something. Your browser is a client. A phone app is a client. Another program calling your service is a client.

A **server** is the side that receives the asking and answers. Note carefully: this is a *role*, not a machine. A server, in this sense, is a program that sits waiting for questions and produces answers. It happens to run on a computer, and in Chapter 7 we will talk about that computer — which is confusingly also called a server. Two meanings, same word. The industry has made its peace with this and so must you. When it matters, this book will say "the server role" or "the machine".

One message from a client asking for something is a **request**. The server's answer is a **response**. That is the entire interaction, repeated billions of times a second across the world, and essentially all of web software is arrangements of it.

The rules for how requests and responses are written and sent are **HTTP**. When you see HTTPS, it is that same HTTP wrapped in an additional layer — TLS — that encrypts the connection and checks you're actually talking to the server you think you are, before any HTTP even starts. Chapter 12 explains what that does and does not protect you from.

Every response carries a status code, and you know some already. `200` means fine. `404` means the thing you asked for does not exist. `500` means the server broke while trying to answer — that one is *your* fault, not the caller's, and the distinction is built into the numbering: the `4xx` range means the request was bad, the `5xx` range means the server was.

## The three parts

The **frontend** is what the user sees and touches: the screens, the buttons, the layout, everything that happens in the browser or the phone. It is a client.

The **backend** is what the user never sees: the rules, the logic, the decisions, the part that knows a discount code has expired or that this account may not see that document. It plays the server role.

The **database** is where the data lives so that it survives. This is the part that people newest to this reliably underestimate, so it is worth being blunt: without it, everything your application knows disappears the moment the program stops. And programs stop constantly — they are restarted for deployments, moved between machines, killed when a machine fails. The database is the only part that remembers.

Why split it into three? Because each part has a genuinely different job, and because of one specific security fact that is the most important sentence in this chapter:

**Anything on the frontend is under the user's control.**

Not "should be treated as if it were". *Is.* The code runs on their computer. They can read it, modify it, and send whatever they like to your backend regardless of what your interface allows. Every browser has developer tools built in; using them takes no skill.

So if your frontend hides the "delete" button for users who are not administrators, and your backend does not separately check that the caller is an administrator, then you do not have a permission system. You have a decoration. Someone will send the delete request directly, and it will work.

This single misunderstanding is behind an enormous share of real security failures at small companies. It is not a subtle attack. It is somebody noticing that the lock was drawn on the door rather than installed in it.

The rule: **the backend must re-check everything.** Every permission, every price, every limit. The frontend's checks exist to give the user a decent experience — telling them the field is wrong before they submit. The backend's checks exist because the frontend cannot be trusted, ever, at all.

<div style="margin:1.6rem 0;">
<svg viewBox="0 0 620 210" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="ptp3-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
<path d="M0,0 L6,3 L0,6" fill="none" stroke="#1a1a1a" stroke-width="1.1"/>
</marker>
</defs>
<rect x="10" y="40" width="170" height="82" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="95" y="68" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="15" font-weight="600" fill="#1a1a1a">FRONTEND</text>
<text x="95" y="85" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="11" fill="#666">(client)</text>
<text x="95" y="102" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" fill="#8a3324">under the user's control</text>
<line x1="33" y1="107" x2="157" y2="107" stroke="#8a3324" stroke-width="1.1" stroke-dasharray="3,3"/>
<rect x="225" y="40" width="170" height="82" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="310" y="68" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="15" font-weight="600" fill="#1a1a1a">BACKEND</text>
<text x="310" y="85" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="11" fill="#666">(server)</text>
<path d="M266,98 l4,5 l8,-9" fill="none" stroke="#8a3324" stroke-width="1.3"/>
<text x="288" y="104" text-anchor="start" font-family="EB Garamond, Georgia, serif" font-size="10.5" fill="#666">re-checks everything</text>
<rect x="440" y="40" width="170" height="82" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="525" y="68" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="15" font-weight="600" fill="#1a1a1a">DATABASE</text>
<text x="525" y="102" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" fill="#666">the only part that remembers</text>
<line x1="182" y1="68" x2="223" y2="68" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp3-arrow)"/>
<line x1="223" y1="90" x2="182" y2="90" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp3-arrow)"/>
<text x="202" y="58" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" fill="#666">request</text>
<text x="202" y="113" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" fill="#666">response</text>
<line x1="397" y1="68" x2="438" y2="68" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp3-arrow)"/>
<line x1="438" y1="90" x2="397" y2="90" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp3-arrow)"/>
<text x="417" y="58" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" fill="#666">writes</text>
<text x="417" y="113" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10" fill="#666">reads</text>
<text x="310" y="160" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-style="italic" fill="#444">Anything the frontend claims about itself can be forged — the backend is the only checkpoint that counts.</text>
</svg>
</div>

## The contract between the parts

The frontend and the backend need an agreement about what can be asked and what comes back. That agreement is an **API**.

Think of a service counter with a fixed order form. You may ask for anything on the form, in the format the form requires. You may not ask for something not on it, and you may not ask in your own words. The form is the contract: it constrains you, and in exchange it guarantees you a defined answer.

One specific address within an API — one thing you can ask for or do — is an **endpoint**. `/users/42` and `/orders` and `/login` are endpoints.

The data usually travels as **JSON**, a plain-text format for structured information that both people and programs can read:

```json
{
  "id": 42,
  "name": "Ada Lovelace",
  "roles": ["admin"],
  "active": true
}
```

That is all JSON is. Names, values, nesting. If you can read that, you can read most of what moves between the parts of your system, which is more useful than it sounds — a great deal of debugging is looking at one of these and noticing that a field you expected is missing.

APIs matter beyond your own frontend. When your application sends email through a third party, takes payments, or asks a language model a question, it does so by calling somebody else's API. Your backend is a client then. The role flips depending on which conversation you are looking at, and getting comfortable with that flip is most of understanding how services fit together.

## What the system remembers

**State** is everything a system remembers between one request and the next. Your logged-in status. The contents of a cart. A half-finished form.

State is where difficulty lives. A system with no memory is easy to reason about; every question has one answer. The moment something is remembered, you have to ask where it is remembered, what happens if that place is lost, and what happens when two things change it at once.

**Stateless** describes a design where each request carries everything needed to answer it, and the server remembers nothing between requests. This sounds like a limitation and is in fact a gift, for a reason that becomes central in Chapter 7: if no copy of your server remembers anything, then every copy is interchangeable. Any of them can answer any request. You can run twenty and lose nineteen without anybody noticing.

If instead each copy remembers who is logged in, then a user who happens to hit a different copy is mysteriously logged out, and adding capacity makes things worse rather than better.

Stateless does not mean nothing is remembered. It means *the server* does not remember; the database does. This is precisely why the split exists.

## Structure and change in the database

The declared structure of your data — what tables exist, what fields they have, what is allowed in each — is the **schema**. Ledgerly's `invoices` table has an id, a customer, an amount, a due date; the customer field cannot be empty.

The schema is not paperwork. It is enforcement. A well-specified schema makes whole categories of bad data impossible, and the database will refuse to store something that violates it. Getting the schema right early is one of the highest-leverage things you can do because everything downstream inherits its assumptions.

Which raises the obvious problem: your understanding will change, and you will need to alter it. Adding a field to a table that already holds fifty thousand rows is not editing a document. Those rows exist. What is the new field's value for them?

The answer is a **migration**: a recorded, ordered change to the schema, written down as a file and applied the same way in every copy of your system. Migration seventeen adds the field with a default; migration eighteen makes it required once every row has one.

Migrations are the database equivalent of the lockfile from Chapter 2 — the same instinct, one layer down. Do not change it by hand; record the change so it can be replayed identically everywhere. A schema that was altered by hand in one place and not another is one of the more unpleasant problems to unpick, because the code is correct and the data is not, and the error messages point at the wrong thing.

Two warnings, both from experience rather than theory:

**Migrations should be reversible where possible.** If applying number eighteen breaks production, you want a way back that is not "restore last night's backup and lose today".

**Deleting a column is not like deleting a file.** Once it is gone, the data in it is gone. The safe pattern is to stop using it, wait, confirm nothing broke, and remove it in a later change.

## A cache, and the trouble with it

One more term because you will meet it early and it explains a specific kind of confusion.

A **cache** is a copy of an expensive answer, kept somewhere fast so the same question does not have to be worked out twice. If your homepage runs a heavy calculation to produce a list, you can compute it once, keep the result for five minutes, and serve it instantly to everyone who asks in the meantime.

Caching is the most reliable way to make a slow system fast. It is also the source of a specific maddening experience: you change something, you check, and it has not changed. You change it again. Still not changed. Twenty minutes later, it changes on its own.

That is a cache, somewhere between you and the answer, still serving the old copy. Possibly in your browser, possibly in your application, possibly at a network layer you did not know existed.

Every cache is a trade of freshness for speed. The trade is often worth it. But when something in your system is inexplicably out of date, "what is cached, and for how long?" is the first question to ask, and it saves a great deal of time that would otherwise go into looking for a bug that is not there.

## What to ask for

> "Draw me the shape of this application: what runs in the browser, what runs on the server, what is in the database, and what third-party services we call."

Ask for this early and keep the answer. It is the map you will use for the rest of the project, and it tends to expose surprises — a service you forgot you were paying for, a piece of logic that ended up on the wrong side of the divide.

> "Which of our permission checks happen on the backend, and not only in the interface?"

This is the question from the middle of this chapter, and it is the single highest-value thing in this book to ask early. If the honest answer is that the checks are only in the frontend, you have found a real problem while it is still cheap.

> "Is the server stateless? If a request went to a different copy, would anything break?"

You are not expected to fix it. You are checking that somebody thought about it before Chapter 7 makes it urgent.
