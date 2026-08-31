# The Minimum Bar — checklist with inspection guidance

This is the checklist from *Prompt to Production*, chapter 16 ("The Minimum
Bar"), verbatim in substance. Each item below is tagged with how the skill
should actually resolve it:

- **[checkable]** — go look. There's a real file, config, or command that
  settles it. Report a genuine done/not-done, not an impression.
- **[ask-human]** — this describes something that *happened* (an event, a
  decision, an organizational fact), not something configured. No amount of
  repo-reading proves it. Always ask; never infer a "done" from adjacent
  configuration existing.
- **[mixed]** — part of it is checkable (does the mechanism exist), part
  isn't (was it actually exercised, or is a related decision-fact still
  open). Report the checkable part honestly, then still ask about the rest.

The "inspect" notes are starting points, not an exhaustive procedure — use
judgment about what's available in a given project (language, hosting
platform, whether GitHub tools are accessible, etc.).

## Not losing things

- **Everything is in version control, with a remote copy that is not your
  laptop.** [checkable] — `git remote -v` returns a real hosted remote
  (GitHub/GitLab/etc.), not empty and not another local path.
- **The main branch is protected: no direct pushes, changes arrive by pull
  request.** [checkable, platform-dependent] — a repo-hosting platform
  setting, not visible from the working tree. Check via the platform's API
  if a tool for it is available; otherwise ask.
- **The database is backed up automatically, and a restore has actually
  been performed — not configured, performed.** [mixed] — "backed up
  automatically" is checkable (look for a backup job/cron/managed-DB backup
  setting in infra config). "A restore has actually been performed" is not
  — a backup job existing is not evidence anyone has ever restored from it.
  Always ask this part directly.
- **You know how long a restore takes, because you timed it.** [ask-human]
  — a fact about an event. Ask; don't infer from RTO documentation alone.

## Not leaking things

- **No secrets in the repository, checked in the history, not just current
  files.** [checkable] — scan the working tree AND `git log -p` (or a tool
  like gitleaks/trufflehog if available) for credential-shaped strings, not
  only `.gitignore` compliance going forward. A clean current tree with
  secrets buried in old commits still fails this.
- **Production secrets are in a secret manager, not a file.** [checkable if
  infra-as-code exists] — look for references to a secrets manager (AWS
  Secrets Manager, Vault, etc.) vs. plaintext values in committed env files.
- **Staging and production use different credentials.** [mixed] — checkable
  if IaC defines distinct credentials per environment; otherwise ask.
- **Every endpoint returning someone's data checks that the caller is
  entitled to it — on the backend.** [checkable, needs real reading] — the
  most judgment-heavy checkable item. Read route/controller code for
  endpoints that return user-scoped data and confirm each has a backend
  authorization check, not just a frontend one. Name specific endpoints
  that are missing it, don't generalize.
- **HTTPS everywhere, including between your own services.** [checkable] —
  look for forced-TLS config at the load balancer/ingress/service level.
- **Dependency vulnerability scanning is on.** [checkable] — Dependabot
  config, `npm audit`/`pip-audit`/similar in CI, Snyk, etc.
- **No personal data or secrets in logs.** [checkable, partial] — spot-check
  logging call sites for obvious PII/secret patterns. Report this as
  spot-checked, not exhaustive — say so rather than implying full coverage.

## Knowing what is happening

- **Errors are reported somewhere you will see them, with enough context to
  debug.** [checkable] — an error-tracking SDK/config (Sentry or similar).
- **Logs are collected somewhere searchable, not only on a machine that
  will disappear.** [checkable] — centralized logging config (CloudWatch,
  Datadog, ELK, etc.), not just `console.log` to a single instance.
- **An uptime check runs from outside your infrastructure.** [mixed] —
  checkable if referenced in IaC; otherwise typically an external service
  not visible from the repo — ask.
- **One dashboard shows traffic, error rate, and p95 latency.** [mixed] —
  same pattern: checkable if dashboard-as-code exists, otherwise ask.
- **Two or three alerts exist, on symptoms, that you would genuinely want
  to be woken for.** [mixed] — checkable if alerting is defined in IaC;
  otherwise ask, and push back gently if the answer is "we have alerts on
  everything" — the book's point is that too many alerts is its own failure.
- **A budget alert and a cost anomaly alert are set on the cloud
  account.** [ask-human, unless IaC defines it] — a cloud-console setting,
  rarely in the repo. The book calls this the cheapest item on the whole
  list — worth naming explicitly if missing.

## Being able to change it

- **Tests exist for the paths that must not break: signup, login, payment,
  or the project's equivalent.** [checkable] — look for tests actually
  covering those specific flows, not just test *files* existing generally.
- **Tests run automatically on every pull request and block the merge when
  red.** [checkable] — CI config plus (if accessible) branch protection
  requiring the check to pass.
- **The lockfile is committed.** [checkable] — `package-lock.json` /
  `yarn.lock` / `poetry.lock` / `Cargo.lock` / equivalent present and
  tracked.
- **One command deploys. One command rolls back.** [checkable] — a deploy
  script or CI workflow exists for each direction.
- **The rollback has been performed at least once, deliberately, when
  nothing was wrong.** [ask-human] — an event fact. A rollback *script*
  existing is not evidence it has ever been run.

## Being able to rebuild it

- **The important infrastructure is described in files, not only clicked
  into a console.** [checkable] — IaC (Terraform, Pulumi, CloudFormation,
  etc.) covering the actual production resources, not a partial subset.
- **Someone other than the primary author could set up the project from the
  repository, following written instructions.** [mixed] — checkable that
  setup instructions exist and look complete (README/CONTRIBUTING); not
  checkable that a second person has actually succeeded with them — ask
  that part.
- **There is a written note of what exists and what it costs.** [checkable]
  — an infra/cost doc, even an informal one.

## Not being ruined by a bad night

- **The single points of failure are known, and which are acceptable has
  been decided.** [ask-human] — a decision, not an artifact. A single-region
  deployment is a fact you can observe; whether that's an *acceptable*
  single point of failure is a judgment call someone has to have made.
- **External calls have a defined behaviour when they do not respond.**
  [checkable] — timeout/circuit-breaker config around outbound HTTP calls
  to third parties.
- **Retries are backed off and limited, and what they retry is safe to
  repeat.** [checkable] — retry logic in code/config; flag retries around
  non-idempotent operations (e.g. payment calls) specifically.
- **A runbook exists for the two or three most likely failures.**
  [checkable] — a runbook doc, even a short one.
- **Someone specific is known to be responsible when it breaks, even if
  that's always the same person.** [ask-human] — organizational fact.

## If personal data is held

Only run this section if the project actually appears to collect or store
personal data (user accounts, contact info, payment details, anything
identifiable) — check for things like a users/customers table or model,
signup/profile endpoints, or fields like email/name/address in the schema
or code. If it's genuinely unclear whether the project handles personal
data, say so explicitly and ask, rather than silently deciding either way
or skipping the section without comment.

- **What is collected, why, and where it physically lives is known.**
  [mixed] — checkable if a data inventory/map doc exists; otherwise ask.
- **A specific person's data can be deleted completely when asked.**
  [mixed] — checkable that a deletion endpoint/script exists; not checkable
  that it's actually complete across every store (backups, analytics,
  third-party processors) — ask about completeness specifically.
- **There is a lawful basis for holding it, stated somewhere public.**
  [checkable] — a public privacy policy page/link exists and states one.
- **What to do in the first 72 hours after a breach is known.** [mixed] —
  checkable if an incident-response doc exists; otherwise ask.

## The short version (five highest-value items)

When a full pass isn't warranted — a quick sanity check mid-conversation
rather than an actual pre-launch review — these five have the worst
consequence-to-effort ratio in the whole list, per the book:

1. Backups exist **and a restore has actually been performed**. [mixed —
   backup mechanism checkable, restore event is ask-human]
2. No secrets in the repository, ever, checked through the full history.
   [checkable]
3. A budget alert on the cloud account. [ask-human, unless IaC defines it]
4. Errors reported somewhere visible. [checkable]
5. A rollback that has actually been rehearsed. [ask-human — the mechanism
   existing is not the same claim]

Notice that three of the five highest-value items are event-facts, not
configuration — that's not a coincidence. The cheapest, highest-leverage
gaps are disproportionately the ones nobody can verify by reading code.
