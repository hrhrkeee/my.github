---
applyTo: "docs/**,README.md,CHANGELOG.md"
---

# Documentation instructions

## Documentation is a first-class output
- When behavior changes, update the nearest spec in `docs/specs/`.
- When architecture or workflow changes, update `docs/architecture/`.
- When operation or troubleshooting changes, update `docs/runbooks/`.
- When a new term or renamed concept appears, update `docs/glossary/`.
- When a known failure pattern or regression is discovered, update `docs/regressions/`.

## Writing rules
- Prefer explicit contracts over narrative prose.
- Use stable terminology across specs, tests, and diagrams.
- State assumptions, invariants, non-goals, and migration constraints clearly.
- Prefer small, local edits to the nearest authoritative document over adding duplicate notes elsewhere.

## Change tracking
- Mention which code paths or modules each doc change corresponds to.
- When a design decision is non-trivial, link the spec change to an ADR.
- Do not leave TODO markers without an owner, condition, or follow-up trigger.
