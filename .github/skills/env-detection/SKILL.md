---
name: env-detection
description: Detect and summarize the project execution environment from the repository with project/environment/environment.yaml as the primary source of truth. Use this before risky implementation or validation.
license: Proprietary - project local use
---

Use this skill before implementation, test execution, or command recommendations.

## Objectives
- Detect the build/test/lint/format/runtime environment reliably.
- Distinguish configured facts from inferred facts.
- Prevent dangerous guessing.

## Detection order
1. `project/environment/environment.yaml`
2. CI workflow files under `.github/workflows/`
3. package/build manifests
4. tool configuration files
5. container definitions
6. runtime entrypoints

## Output rules
- Record confirmed facts separately from inferred facts.
- Write inferred summaries to `project/environment/detected-environment.md`.
- Do not overwrite `environment.yaml` without explicit user intent or review process.

## Helper resources
- `scripts/detect-environment.sh`
- `templates/detected-environment-template.md`
