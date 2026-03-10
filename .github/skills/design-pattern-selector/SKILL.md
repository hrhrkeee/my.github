---
name: design-pattern-selector
description: Select and justify a design pattern based on the requested change, extension pressure, testability, and dependency direction. Use this when structure or behavior changes are non-trivial.
license: Proprietary - project local use
---

Use this skill when a change alters structure, state flow, extensibility, boundary design, or dependency management.

## Objectives
- Select an appropriate design pattern.
- Reject unsuitable alternatives explicitly.
- Keep the design simple but maintainable.

## Evaluation dimensions
- change frequency
- boundary clarity
- testability
- dependency control
- runtime complexity
- migration cost

## Candidate pattern catalog
Refer to `catalogs/pattern-selection-catalog.md`.

## Required output
- Problem statement
- Selected pattern
- Rejected alternatives
- Trade-offs
- Files/modules likely to change
- Whether an ADR is required

## Documentation rule
If the pattern decision is not obvious or introduces a new architectural seam, update or create an ADR.
