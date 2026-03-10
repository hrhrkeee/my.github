# Implement change

Use the repository strategy files and proceed in this order:

1. Read `.github/copilot-instructions.md`.
2. Read `project/environment/environment.yaml`.
3. Read the nearest relevant specs, tests, ADRs, and architecture views.
4. If requirements are ambiguous, ask targeted clarification questions using the requirement-intake skill logic.
5. If structure changes, evaluate a suitable design pattern using the design-pattern-selector skill logic.
6. Implement the smallest coherent change.
7. Update impacted tests, specs, ADRs, runbooks, glossary entries, and diagrams in the same change set.
8. Prepare a branch name and conventional-style commit message using repository Git history.
9. Do not push unless explicitly requested.

Return:
- assumptions
- implementation plan
- files to change
- tests to add/update/remove
- docs/diagram updates
- validation commands
