#!/usr/bin/env bash
set -euo pipefail

echo "== current branch =="
git branch --show-current || true
echo

echo "== status =="
git status --short || true
echo

echo "== diff stat =="
git diff --stat || true
echo

echo "== recent history =="
git log --oneline -n 20 || true
