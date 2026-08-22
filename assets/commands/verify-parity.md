# verify-parity

Verify a port story's Phase P criteria against the path test plan and write a parity report. Before acting, resolve the workflow profile and use its configured story glob, parity report pattern, parity report template, oracle path, path glob, path test-plan glob, defect ledger path, QA result values, and review gate values.

**Command-agent binding:** This command is role-bound to `agents.qa`. Before executing any step, load the configured QA agent definition and follow it as binding role context.

Write the detailed result to the configured parity report path (default `docs/modernization/parity/{STORY-ID}-parity.md`) using the configured parity report template (default `~/.cursor/templates/parity-report-template.md`).

## Inputs

- Story ID.
- Optional mode:
  - `targeted` — run only the Phase P evidence for the story. Default.
  - `report-only` — inspect existing outputs and update the report.

## Steps

1. Resolve the workflow profile and find the story using the configured story glob.
2. Read the story, especially `Phase P`, `8b. Parity Plan`, covered `XP-NNN`, and defect decisions.
3. Read the matching path test plans, the oracle doc (tier only), and the defect ledger.
4. For each `P` criterion:
   - confirm the oracle fixture or acceptance-data source exists and matches the oracle tier;
   - run the cited parity test or inspect the cited evidence;
   - compare using the **path test plan's** comparison rule, not a global default;
   - if the path test plan has no comparison rule, mark `BLOCKED` and return to `/plan-path-tests`;
   - reconcile mismatches to `DEF-NNN` decisions.
5. Write the parity report with the `PARITY SUMMARY:` first line.
6. **README hub.** Update only the Artifact index row **Parity reports** (count of files under `docs/modernization/parity/`). Do not edit Lane status, backlog, or path test plans.
7. Return QA-style results for each `P` criterion and identify whether `Z8` can pass.

## Result semantics

- `PASS` when every Phase P criterion has valid evidence and all mismatches are within the path's comparison rule or reconciled to a defect decision.
- `FAIL` when comparison proves an unreconciled mismatch.
- `BLOCKED` when fixtures, oracle tier, evidence, comparison rule, or defect decisions are missing.

## Hard rules

- Do not claim parity above the configured oracle tier.
- Do not treat a user-visible mismatch as acceptable without a `DEF-NNN` decision.
- Do not use broad build/test success as a substitute for oracle comparison.
- Do not edit code, story checkboxes, or path test plans.
- Do not edit README sections other than the Parity reports index row.
- Do not apply a workflow-profile numeric hint as the binding rule.

## Output

Return a Parity Evidence Matrix:

| P criterion | Result | Oracle evidence | New evidence | Comparison rule | Defect decision | Report row |
|-------------|--------|-----------------|--------------|-----------------|-----------------|------------|

Also return the parity report path and whether `Z8` is passable.

## Examples

- `/verify-parity CALC-1`
- `/verify-parity IMPORT-1 report-only`

This command is available in chat with `/verify-parity`.
It expects a story ID.
