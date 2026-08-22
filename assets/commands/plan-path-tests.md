# plan-path-tests

Plan how a single execution path will be verified during the port. Before acting, resolve the workflow profile and use its configured path test-plan glob, path test-plan template, path glob, oracle path, defect ledger path, requirements directory, and evidence grades.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

Write the result under the configured test-plans directory (default `docs/modernization/test-plans/XP-NNN-tests.md`) using the configured path test-plan template (default `~/.cursor/templates/path-test-plan-template.md`).

## Inputs

- One `XP-NNN` path detail.
- Linked `REQ-NNN` / `Sn` scenarios when they exist.
- Oracle doc, defect ledger, decision register.

## Preconditions

- `/trace-path` has produced a path detail for this `XP-NNN`.
- Prefer running after `/refine-feature` so `Sn` IDs exist. If they do not, write scenario IDs as `TBD` and do not invent Gherkin.

## What the Architect will do

1. Resolve the workflow profile and read the configured path test-plan template.
2. Read the path detail, oracle tier, and any `DEF-NNN` / `DEC-NNN` that bind this path.
3. Record happy-path, edge, and error scenarios taken from the path detail — not invented legacy behavior.
4. State the oracle strategy for this path and the comparison rule (`exact`, `tolerance-based` with the actual bound, or `semantic`).
5. If no fixture or acceptance-data source exists, say so. Do not assign a parity criterion that cannot be run.
6. Do not use a workflow-profile numeric hint as the binding rule. If no per-path rule can be written, leave an open question and do not mark the path implementation-ready.
7. **README hub.** Update only the Artifact index row **Path test plans** (count of files). Do not edit Lane status.

## Hard rules

- Comparison is per path. There is no global tolerance gate.
- Do not claim a stronger oracle than `docs/modernization/oracle.md`.
- QA verifies this plan via `/verify-parity`; this command does not write the parity report.
- Keep the document short. It exists to feed Phase P, not to retell the path detail.

## Outputs

- Configured path test plan.
- Summary of comparison rule, fixture gaps, and suggested next command (`/plan-port-story`).

## Examples

- `/plan-path-tests XP-001`
- `/plan-path-tests XP-001 @docs/requirements/REQ-001-linspace.md`

This command is available in chat with `/plan-path-tests`.
It expects an `XP-NNN` whose path detail exists.
