---
name: regression-prevention
description: Capture implementation learnings as reusable regression checks and preventive guidance. Use this when fixing defects, addressing incidents, or discovering recurring failure patterns.
license: Proprietary - project local use
---

Use this skill after defects, production incidents, flaky behavior, migration issues, or code review findings that reveal recurring patterns.

## Objectives
- Convert one-off fixes into repeatable safeguards.
- Make similar future failures easier to detect earlier.
- Feed new knowledge into docs and tests, not just memory.

## Process
1. Describe the original failure and trigger.
2. Identify the broken assumption.
3. Identify the earliest signal that could have caught it.
4. Create or update:
   - `docs/regressions/`
   - targeted regression tests
   - checklist entries
   - nearest runbook or spec if needed
5. If the pattern is broadly reusable, promote it into this skill or another skill.

## Supporting resources
- `checklists/regression-checklist.md`
- `templates/regression-entry.md`

## Required output
- failure pattern
- preventive checks
- tests added or updated
- docs updated
