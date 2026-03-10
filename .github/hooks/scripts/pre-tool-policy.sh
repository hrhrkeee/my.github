#!/usr/bin/env bash
set -euo pipefail

# Minimal shell-side guardrail. Extend with actual hook payload parsing in your environment.

branch="$(git branch --show-current 2>/dev/null || true)"
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  echo "WARNING: protected branch detected: $branch"
fi

# Soft guidance only; actual command inspection should be wired to the hook payload.
echo "POLICY: do not push unless explicitly requested."
