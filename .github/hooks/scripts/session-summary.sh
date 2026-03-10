#!/usr/bin/env bash
set -euo pipefail

echo "SESSION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Branch: $(git branch --show-current 2>/dev/null || echo unknown)"
echo "Changed files:"
git diff --name-only 2>/dev/null || true
echo
echo "Recent commits:"
git log --oneline -n 5 2>/dev/null || true
