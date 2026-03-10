# Update tests

Analyze the implementation diff and perform test impact analysis.

Use this order:
1. Read impacted code and nearest existing tests.
2. Classify impact across unit, integration, e2e, contract, and regression.
3. Add, update, or remove tests in the same change set.
4. Update or remove fixtures, helpers, and golden files as needed.
5. Prefer deterministic checks and smallest sufficient validation first.

Return:
- impacted test levels
- files added/updated/removed
- validation commands
- remaining blind spots
