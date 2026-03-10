---
applyTo: "**"
---

# Git instructions

## Branching
- Never commit directly to `main` or `master`.
- Prefer `copilot/<type>/<scope>-<slug>`.
- If already on a protected branch, stop and request or create a safe working branch.

## History usage
- Inspect recent commit history before proposing a commit message.
- Reuse established wording patterns only when they match the current diff.
- Refer to prior changes when they materially affect compatibility or conventions.

## Commit messages
- Use conventional-style commits unless the repository explicitly uses a different standard.
- Keep the subject grounded in actual changes, not intentions.
- Mention scope only when it is meaningful and stable.

## Push policy
- Never push unless explicitly requested.
- If operating in an environment that auto-creates PRs or pushes branches, state that behavior before use and treat it as an exception path.
