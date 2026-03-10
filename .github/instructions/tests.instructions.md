---
applyTo: "tests/**,**/*test*,**/*spec*"
---

# Test instructions

## Test organization
- Place tests by responsibility:
  - `tests/unit/`
  - `tests/integration/`
  - `tests/e2e/`
  - `tests/contract/`
  - `tests/regression/`
  - `tests/fixtures/`
  - `tests/helpers/`
  - `tests/golden/`
- Keep fixtures reusable and minimal.
- Keep helpers generic and side-effect free.

## Change rules
- Every behavioral change must evaluate test impact.
- Add, update, or remove tests in the same change set as the implementation.
- Remove obsolete tests, fixtures, and golden files when they no longer match the product contract.
- Do not keep redundant tests that only duplicate lower-level coverage.

## Coverage expectations
For impacted behavior, consider:
- positive path
- negative path
- boundary conditions
- compatibility or contract behavior
- regression coverage for previously observed bugs

## Reporting
- State what level of tests changed and why.
- State what was not tested and why.
