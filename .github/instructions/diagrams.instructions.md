---
applyTo: "docs/architecture/diagrams/**,docs/architecture/views/**"
---

# Diagram instructions

## Canonical formats
- The editable source of truth is `.drawio`.
- The review- and browser-friendly export is `.drawio.svg`.
- Keep both the source and export aligned in the same change set when the architecture or flow changes.

## Storage
- Editable sources live in `docs/architecture/diagrams/source/`.
- Exported artifacts live in `docs/architecture/diagrams/export/`.

## Update rules
- Update diagrams when components, dependencies, runtime flow, ownership, lifecycle, or failure handling changes.
- Keep node names aligned with the terms used in specs and code.
- Prefer one responsibility per diagram. Split oversized diagrams by viewpoint.
- Document the reason for the update in the nearest architecture view or ADR.

## Quality rules
- Minimize visual clutter.
- Use consistent naming for services, adapters, policies, stores, and external systems.
- Avoid decorative shapes that do not encode information.
