#!/usr/bin/env bash
set -euo pipefail

# Minimal placeholder policy script.
# Extend this to inspect prompt payloads if your execution environment passes them in.

branch="$(git branch --show-current 2>/dev/null || true)"
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  echo "WARNING: current branch is protected ($branch). Create a working branch before committing."
fi
