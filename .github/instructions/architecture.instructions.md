---
applyTo: "src/**,app/**,lib/**,packages/**"
---

# Architecture instructions

## Scope
These instructions apply when the change affects structure, boundaries, dependencies, or lifecycle behavior.

## Required behavior
- Identify the impacted architectural boundary before editing files.
- Prefer explicit seams between policy, orchestration, IO, and UI.
- Keep dependency direction stable; do not introduce upward or cyclic dependencies without an ADR.
- When a change crosses module boundaries, update `docs/architecture/views/` and consider an ADR in `docs/adr/`.

## Design pattern guidance
- Propose one primary pattern and at least one rejected alternative.
- Justify the choice in terms of:
  - testability
  - change frequency
  - dependency control
  - runtime complexity
  - migration cost
- Prefer composition over inheritance unless inheritance materially simplifies extension without hiding state transitions.

## Implementation rules
- Keep state mutation localized and observable.
- Prefer narrow interfaces at boundaries.
- If introducing adapters, factories, policies, repositories, observers, states, or strategies, document the role each class or module plays.
- Avoid combining domain policy and integration details in the same module.

## Required outputs
- Note which architectural view changed.
- Note whether an ADR was created or intentionally skipped.
