#!/usr/bin/env bash
# Generates a fresh copy of the Session 3/4/7 teaching fixture — a small
# invoicing service standing in for Ledgerly, the fictional company this
# book's own chapters follow, with three planted problems mapped straight
# onto the book:
#
#   - a Stripe-style secret committed, then "removed" but still live in
#     git history (Chapter 5's whole subject)
#   - the exact unauthorized-invoice-access bug Chapter 12 narrates —
#     GET /invoices/8812 with no check that the caller is entitled to it,
#     the same invoice number Chapter 10's logs already showed students
#   - empty tests/ and .github/workflows/ directories (Chapter 6, 9)
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

git init -q
git config user.email "fixture@ledgerly.example"
git config user.name "Ledgerly Engineering"

mkdir -p src tests .github/workflows

cat > src/app.js <<'EOF'
const express = require('express');
const app = express();

// Chapter 12's bug, live: nothing here checks that the caller is actually
// entitled to the invoice they're asking for. Change the id in the URL,
// get a stranger's invoice.
app.get('/invoices/:id', (req, res) => {
  res.json(getInvoice(req.params.id));
});

app.listen(3000);
EOF

cat > package.json <<'EOF'
{
  "name": "ledgerly-invoicing",
  "version": "1.0.0",
  "description": "Ledgerly's invoicing service",
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF

cat > .env <<'EOF'
STRIPE_SECRET_KEY=sk_live_FAKEKEYFORTRAININGONLY00000000000000
EOF

git add -A
git commit -q -m "Initial commit: invoicing service"

echo ".env" > .gitignore
git rm --cached .env -q
git add -A
git commit -q -m "Remove .env from tracking"

cat > README.md <<'EOF'
# Ledgerly Invoicing Service

Handles invoice creation and lookup. See `.env.example` (not yet added)
for required configuration.
EOF

git add -A
git commit -q -m "Add README"

echo "generated fixture at $OUT"
echo "the planted secret is still reachable via: git -C $OUT log -p -- .env"
