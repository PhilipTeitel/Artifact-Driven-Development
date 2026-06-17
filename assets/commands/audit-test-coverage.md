# audit-test-coverage

Read the existing test suite and changed code paths. Identify the highest-risk missing regression tests for currently implemented behavior and for the bug fixes under consideration. Before acting, resolve the workflow profile and use its configured audit file, audit template, auditor agent path, and finding prefixes.

Read the configured audit file in the target repo root first and use it as the shared audit state. If it does not exist, create it from the configured audit template.

## Mode

This command runs in **whole-repo audit mode** — it writes into the configured audit file against the repo's `Scope` (`whole-repo`, `package: <name>`, or `paths: [<list>]`).

For per-story reviews of a single feature's changed surface, use `/review-story` instead. The auditor agent applies a stricter rubric in that mode (every AC must have a referenced test that exists and runs; every adapter must have a non-mock integration test; every implemented Gherkin scenario ID must trace to a test name) — see the configured auditor agent's "Per-story test-coverage rubric".

Update only:
- `Detailed Findings` -> `Test Coverage Recommendations`
- `Fix Plan` -> `Test Coverage Support`
- any relevant `Findings Summary` rows when a missing regression test materially affects fix confidence

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only the configured test-coverage finding prefix for rows and headings created by this command (default `TEST-#`).
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a recommendation:
- read the current non-test-prefix findings and prioritize tests that raise fix confidence for the best `fix now` candidates
- avoid duplicate test recommendations that protect the same code path in the same way
- prefer the lightest regression that proves the risky behavior or the intended fix

Search recipes:
- nearest existing tests around each selected fix candidate
- missing assertions on contract edges, error handling, or persistence invariants
- cheap integration tests that cover a cross-package or cross-process boundary better than many unit tests
- adapters of any port that lack a non-mock integration test against the real backing service

Do not ask for broad coverage expansion. Return:
- severity
- the top missing tests
- why each one matters
- the exact code path it protects
- the lightest-weight way to add it
- the verification gap it closes

When a missing regression test materially changes whether an issue is a good fix candidate, reflect that in `Fix Plan` -> `Test Coverage Support` and in any relevant summary guidance.
