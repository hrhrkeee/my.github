#!/usr/bin/env bash
set -euo pipefail

changed="$(git diff --name-only 2>/dev/null || true)"

if [[ -z "$changed" ]]; then
  exit 0
fi

code_changed=0
docs_changed=0
tests_changed=0
diagram_changed=0

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  [[ "$file" == src/* || "$file" == app/* || "$file" == lib/* || "$file" == packages/* ]] && code_changed=1
  [[ "$file" == docs/* || "$file" == README.md || "$file" == CHANGELOG.md ]] && docs_changed=1
  [[ "$file" == tests/* ]] && tests_changed=1
  [[ "$file" == docs/architecture/diagrams/* ]] && diagram_changed=1
done <<< "$changed"

if [[ $code_changed -eq 1 && $docs_changed -eq 0 ]]; then
  echo "WARNING: code changed but no docs changed. Verify this is intentional."
fi

if [[ $code_changed -eq 1 && $tests_changed -eq 0 ]]; then
  echo "WARNING: code changed but no tests changed. Verify this is intentional."
fi

if [[ $code_changed -eq 1 && $diagram_changed -eq 0 ]]; then
  echo "INFO: no diagram changes detected. Verify architecture/flow was unaffected."
fi
