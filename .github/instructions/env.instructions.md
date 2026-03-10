---
applyTo: "project/environment/**,.github/workflows/**,Dockerfile*,docker-compose*,compose.*,Makefile,Taskfile*,package.json,pyproject.toml,go.mod,Cargo.toml,*.sln,*.csproj,*.xcodeproj,*.xcworkspace"
---

# Environment instructions

## Source of truth
- Read `project/environment/environment.yaml` before making implementation decisions.
- If the file is incomplete, inspect repo markers and CI files before guessing commands.
- Record inferred commands and assumptions in `project/environment/detected-environment.md`.

## Detection order
1. `project/environment/environment.yaml`
2. CI workflow files
3. package/build manifests
4. formatter/linter configuration
5. container and service definitions
6. version-management files

## Safety
- Do not silently rewrite `environment.yaml` based on inference alone.
- Distinguish confirmed commands from inferred commands.
- Summarize the minimum build, test, lint, format, and runtime commands relevant to the current change.
