---
name: test-maintenance
description: Analyze test impact and maintain tests across unit, integration, e2e, contract, regression, fixtures, helpers, and golden files. Use this whenever implementation changes can affect behavior.
license: Proprietary - project local use
---

Use this skill whenever code changes may affect observable behavior.

## Objectives
- Determine what tests to add, update, or remove.
- Keep test structure scalable.
- Preserve meaningful regression protection.

## Test impact process
1. Read the changed code and the nearest existing tests.
2. Classify impact:
   - unit
   - integration
   - e2e
   - contract
   - regression
3. Determine fixture/helper/golden changes.
4. Remove obsolete tests and data files.
5. Run the smallest sufficient validation first, then expand if risk warrants it.

## Supporting resources
- `templates/test-impact-analysis.md`
- `checklists/test-change-checklist.md`

## Required output
- impacted test levels
- files added/updated/removed
- validations run
- remaining blind spots
