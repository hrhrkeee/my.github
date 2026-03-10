# Architecture diagram guidelines

## Recommended viewpoints
- system context
- container / subsystem
- runtime flow
- failure / retry flow
- ownership / responsibility map

## Naming
- Use repository terminology exactly.
- Prefer stable names over transient ticket phrasing.
- Label external systems explicitly.

## Layout guidance
- Keep flow direction consistent within a diagram.
- Avoid crossing connectors when possible.
- Use grouping to show ownership or bounded contexts.
- Separate control flow from data flow if both are complex.

## Maintenance
- Update the nearest existing source file first.
- Keep diagram scope narrow; prefer multiple clear diagrams over one overloaded diagram.
