---
name: git-ops
description: Generate safe branch names, commit messages, and diff summaries using repository history. Use this whenever preparing a branch or commit. Never push unless explicitly requested.
license: Proprietary - project local use
---

Use this skill before branch creation, commit preparation, or change summary generation.

## Objectives
- Keep Git operations aligned with repository history and current diff.
- Standardize branch and commit naming.
- Prevent accidental push or direct work on protected branches.

## Process
1. Read current branch and working tree status.
2. Read recent history (`git log --oneline -n 20` or repository convention).
3. Read current diff summary.
4. Propose:
   - branch name
   - commit message
   - short diff summary
5. If the current branch is `main` or `master`, stop and propose a safe working branch.

## Supporting resources
- `scripts/prepare-commit.sh`
- `templates/commit-message-template.md`

## Rules
- Do not fabricate issue IDs.
- Do not combine unrelated changes into one commit description.
- Never push unless explicitly requested.
