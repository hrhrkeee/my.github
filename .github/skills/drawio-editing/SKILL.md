---
name: drawio-editing
description: Maintain Draw.io architecture diagrams as editable .drawio sources with synchronized .drawio.svg exports. Use this when architecture, flow, boundary, dependency, or lifecycle visuals must change.
license: Proprietary - project local use
---

Use this skill when implementation changes require architecture or flow diagrams to be updated.

## Objectives
- Keep Draw.io artifacts editable and reviewable.
- Align diagrams with code, specs, and ADRs.
- Reduce context waste by editing only the relevant diagram and viewpoint.

## Canonical storage
- Source of truth: `docs/architecture/diagrams/source/*.drawio`
- Export: `docs/architecture/diagrams/export/*.drawio.svg`

## Process
1. Read the nearest architecture view and spec.
2. Identify which existing diagram should be edited.
3. Update the smallest relevant diagram instead of creating duplicates.
4. Keep names aligned with code and specs.
5. Update the paired export.
6. Record the rationale in the architecture view or ADR.

## Supporting resources
- `templates/diagram-update-checklist.md`
- `examples/architecture-diagram-guidelines.md`

## Additional guidance
- Prefer one responsibility per diagram.
- Split diagrams by viewpoint when they become crowded.
- Use explicit boundaries for services, adapters, stores, policies, and external systems.
