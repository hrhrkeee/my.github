---
name: spec-sync
description: Synchronize specifications, ADRs, runbooks, glossary, and architecture views with implementation changes. Use this whenever behavior, contracts, workflows, or architecture have changed.
license: Proprietary - project local use
---

Use this skill whenever code changes alter behavior, contracts, workflows, or architectural boundaries.

## Objectives
- Keep documentation authoritative.
- Avoid implementation/documentation drift.
- Preserve rationale, not just final outcomes.

## Sync process
1. Identify what changed:
   - behavior
   - inputs/outputs
   - schema/data shape
   - runtime flow
   - failure handling
   - operational procedures
2. Map the change to the nearest authoritative docs:
   - `docs/specs/`
   - `docs/adr/`
   - `docs/runbooks/`
   - `docs/glossary/`
   - `docs/architecture/views/`
3. Apply local updates rather than creating duplicate documents.
4. If terminology changed, update glossary entries.
5. If architecture changed, coordinate diagram updates.

## Templates
- `templates/spec-update-template.md`
- `templates/adr-template.md`

## Required output
- changed behavior summary
- docs updated
- docs intentionally unchanged and why
