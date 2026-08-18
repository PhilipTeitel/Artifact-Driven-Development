# ledger-defects

Record known, suspected, or discovered legacy defects and decide whether the port should reproduce, fix now, or fix later. Before acting, resolve the workflow profile and use its configured defect ledger path, defect ledger template, behavior glob, oracle path, evidence grades, and defect policy.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured defect ledger (default `docs/modernization/defect-ledger.md`) using the configured defect ledger template (default `~/.cursor/templates/defect-ledger-template.md`).

## Inputs

- Known bug reports, support notes, user decisions, behavior artifacts, oracle mismatches, or suspicious legacy behavior.
- Optional `BEH-NNN`, fixture, or story IDs.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured defect ledger template.
2. Record each defect or suspected mismatch as `DEF-NNN`; do not renumber existing IDs.
3. Link affected `BEH-NNN`, scenarios, fixtures, and evidence.
4. Ask for or record the required decision: `reproduce-faithfully`, `fix-now`, or `fix-later`.
5. For `fix-later`, create or reference a deferred backlog item.
6. For `reproduce-faithfully`, record the bug-compatible expected output that parity tests must preserve.

## Hard rules

- Do not decide that a mismatch is a bug without user or source evidence.
- Do not silently fix legacy behavior during the port.
- If a defect decision affects acceptance criteria, flag the affected story or requirement.
- Mismatches without decisions block affected Phase P parity criteria.

## Outputs

- Configured defect ledger.
- Summary of new decisions, open decisions, affected behaviors, and suggested next command.

## Examples

- `/ledger-defects BEH-003 "rounding mismatch is accepted legacy behavior"`
- `/ledger-defects @support/known-issues.md`

This command is available in chat with `/ledger-defects`.
It expects defect evidence or a behavior/mismatch to classify.
