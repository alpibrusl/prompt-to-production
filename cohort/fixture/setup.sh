#!/usr/bin/env bash
# Generates a fresh copy of the teaching fixture — a small invoicing service
# standing in for Ledgerly, the company this book's chapters follow.
#
# The fixture exists to be audited, and an audit is only worth running if the
# answers differ. An earlier version of this script created tests/ and
# .github/workflows/ empty, which meant every checkable item on the Minimum Bar
# came back "not done": every student produced the same wall of ❌, and the one
# skill the checklist is built around — telling a real ✅ from a plausible-
# looking one — never got exercised.
#
# So the plants below are chosen to make all four verdicts reachable:
#
#   ✅ done            a committed lockfile, real tests, CI that runs them on
#                      every pull request, .gitignore that covers .env
#                      (Chapters 2, 6, 9)
#
#   ❓ ask / mixed     backups configured in infra/ and never once restored;
#                      a runbook that exists and says nothing. Both look done
#                      from the repository and are not. This is the fixture's
#                      centre of gravity — Chapter 11's whole subject, and the
#                      distinction verify-production is built to protect.
#
#   ❌ not done        a Stripe-style secret committed, then "removed" but
#                      still live in history (Chapter 5); the unauthorized
#                      invoice endpoint Chapter 12 narrates, on the same
#                      invoice number Chapter 10's logs showed; no dependency
#                      scanning; no error tracking (Chapters 10, 12)
#
#   ➖ not applicable  the service makes no outbound third-party calls, so
#                      "retries backed off and safe to repeat" has nothing to
#                      apply to. A student who marks that ❌ has misread the
#                      item; the honest answer is N/A (Chapter 11)
#
# Usage: fixture/setup.sh [output-dir]   (default: ./ledgerly-invoicing)
#
# Run this fresh before each session that uses it — see sessions.yaml's
# facilitator_notes on session 3 for why a clean checkout matters. The
# generated repo is disposable and gitignored; this script is the source.

set -euo pipefail

OUT="${1:-./ledgerly-invoicing}"

if [ -e "$OUT" ]; then
  echo "error: $OUT already exists — remove it or pass a different output path" >&2
  exit 1
fi

mkdir -p "$OUT"
cd "$OUT"

git init -q -b main
git config user.email "fixture@ledgerly.example"
git config user.name "Ledgerly Engineering"

mkdir -p src tests infra docs .github/workflows

# --- the application -------------------------------------------------------
# Two things are deliberate and neither is announced in the generated code.
#
# The invoice endpoint checks nothing about who is asking (Chapter 12). An
# earlier version of this script labelled it in a comment — "Chapter 12's bug,
# live" — which handed the student the finding and left nothing to audit.
# Session 3 tells them only "audit this before it ships"; the fixture has to
# hold up its end of that.
#
# And there is no outbound HTTP anywhere, which makes the retry/backoff item a
# genuine ➖ rather than a ❌ — the only way to practise the difference between
# "missing" and "does not apply".
cat > src/app.js <<'EOF'
const express = require('express');
const { getInvoice, listInvoices } = require('./store');
const app = express();

app.get('/invoices/:id', (req, res) => {
  res.json(getInvoice(req.params.id));
});

app.get('/health', (req, res) => {
  res.json({ ok: true });
});

app.listen(3000);

module.exports = { app, listInvoices };
EOF

cat > src/store.js <<'EOF'
const INVOICES = {
  '8812': { id: '8812', customer: 'acme-ltd', amount: 4200, currency: 'EUR' },
  '8813': { id: '8813', customer: 'brightline', amount: 1750, currency: 'EUR' },
};

function getInvoice(id) {
  return INVOICES[id] || null;
}

function listInvoices() {
  return Object.values(INVOICES);
}

module.exports = { getInvoice, listInvoices };
EOF

# --- ✅ tests that actually exist and actually pass -------------------------
cat > tests/store.test.js <<'EOF'
const assert = require('node:assert');
const { test } = require('node:test');
const { getInvoice, listInvoices } = require('../src/store');

test('returns an invoice by id', () => {
  assert.strictEqual(getInvoice('8812').customer, 'acme-ltd');
});

test('returns null for an unknown id', () => {
  assert.strictEqual(getInvoice('nope'), null);
});

test('lists every invoice', () => {
  assert.strictEqual(listInvoices().length, 2);
});
EOF

cat > package.json <<'EOF'
{
  "name": "ledgerly-invoicing",
  "version": "1.0.0",
  "description": "Ledgerly's invoicing service",
  "scripts": {
    "test": "node --test tests/"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF

# --- ✅ a committed lockfile (Chapter 2) ------------------------------------
cat > package-lock.json <<'EOF'
{
  "name": "ledgerly-invoicing",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "ledgerly-invoicing",
      "version": "1.0.0",
      "dependencies": { "express": "^4.18.0" }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-FIXTUREONLYNOTAREALINTEGRITYHASH00000000000000000000000000000=="
    }
  }
}
EOF

# --- ✅ CI that runs the tests on every pull request (Chapter 9) ------------
# Note what it does NOT do: no dependency scanning, no deploy, no rollback.
cat > .github/workflows/ci.yml <<'EOF'
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
EOF

# --- ❓ backups: configured, never exercised (Chapter 11) -------------------
# The most important plant in the fixture. Everything a repository can show is
# present and correct; the thing that matters is not in the repository at all.
cat > infra/backups.tf <<'EOF'
# Automated nightly snapshots of the invoicing database.
# Configured 2025-11-04. Retention 30 days.
resource "aws_db_instance" "invoices" {
  identifier              = "ledgerly-invoices"
  engine                  = "postgres"
  backup_retention_period = 30
  backup_window           = "03:00-04:00"
  skip_final_snapshot     = false
}
EOF

# --- ❓ a runbook that exists and says nothing ------------------------------
cat > docs/runbook.md <<'EOF'
# Runbook

## If the service is down

TODO

## If the database is unreachable

TODO

## Who to call

TODO
EOF

cat > README.md <<'EOF'
# Ledgerly Invoicing Service

Handles invoice creation and lookup. See `.env.example` (not yet added)
for required configuration.

    npm ci && npm test
EOF

# --- ❌ the secret, committed and then "removed" (Chapter 5) ----------------
cat > .env <<'EOF'
STRIPE_SECRET_KEY=sk_live_FAKEKEYFORTRAININGONLY00000000000000
EOF

git add -A
git commit -q -m "Initial commit: invoicing service"

echo ".env" > .gitignore
git rm --cached .env -q
git add -A
git commit -q -m "Remove .env from tracking"

git add -A
git commit -q --allow-empty -m "Add nightly database snapshots"

echo "generated fixture at $OUT"
echo
echo "planted for the audit — the four verdicts are all reachable:"
echo "  ✅  lockfile committed, tests present and passing, CI runs them on every PR"
echo "  ❓  infra/backups.tf configures snapshots; nothing shows a restore was ever run"
echo "  ❓  docs/runbook.md exists and every section says TODO"
echo "  ❌  the Stripe key is still in history: git -C $OUT log -p -- .env"
echo "  ❌  GET /invoices/:id checks nothing about who is asking"
echo "  ➖  no outbound third-party calls, so retry/backoff has nothing to apply to"
