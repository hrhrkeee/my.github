#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

echo "== environment markers =="
find "$ROOT" -maxdepth 2 \
  \( -name "package.json" -o -name "pyproject.toml" -o -name "poetry.lock" -o -name "go.mod" -o -name "Cargo.toml" -o -name "*.sln" -o -name "*.csproj" -o -name "Gemfile" -o -name "Makefile" -o -name "Taskfile*" -o -name "Dockerfile*" -o -name "docker-compose*" -o -path "*/.github/workflows/*" \) \
  -print | sort

echo
echo "== environment.yaml =="
if [[ -f "$ROOT/project/environment/environment.yaml" ]]; then
  sed -n '1,220p' "$ROOT/project/environment/environment.yaml"
else
  echo "project/environment/environment.yaml not found"
fi
