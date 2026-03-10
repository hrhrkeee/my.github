# Repository-wide Copilot rules

## Mission
- Solve only the requested scope.
- Prefer repository context over repeating the user's prompt.
- Read relevant code, specs, ADRs, diagrams, tests, and Git history before changing files.

## Requirement handling
- If any requirement is ambiguous, ask targeted questions before implementation.
- State assumptions explicitly when proceeding with incomplete information.
- Do not invent hidden requirements or policy exceptions.

## Design
- Propose an appropriate design pattern when behavior or structure changes.
- Keep the design simple, but not at the expense of extensibility or testability.
- Record non-trivial design decisions in docs or ADRs.

## Documentation
- If behavior, API, schema, workflow, or architecture changes, update the nearest spec.
- If the design decision is non-trivial, update or create an ADR.
- If architecture or flow changes, update the related diagram source and export.

## Testing
- Add, update, or remove tests in the same change set.
- Cover positive, negative, boundary, and regression cases as appropriate.
- Do not leave obsolete tests, fixtures, or golden files behind.

## Environment
- Read `project/environment/environment.yaml` first.
- If the environment file is incomplete, inspect common repo markers and CI files.
- Summarize detected build, test, lint, format, and runtime commands before risky changes.

## Git workflow
- Never work directly on `main` or `master`.
- Use a branch named `copilot/<type>/<scope>-<slug>`.
- Review recent commit history before proposing a commit message.
- Create clear conventional-style commit messages grounded in the actual diff.
- Never push unless explicitly requested.

## Quality gates
- Run the smallest sufficient validation first, then expand if risk is high.
- Prefer deterministic checks and report what was validated.
- Surface remaining risks, assumptions, and unvalidated areas explicitly.

## Output
- Summarize assumptions, changed files, tests, docs, diagrams, and remaining risks.
- When blocked, ask precise questions instead of proceeding blindly.
