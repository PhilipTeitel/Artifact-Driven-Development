# ledger-defects

Record known, suspected, or discovered legacy defects scoped to execution paths, and record whether the port should reproduce, fix now, or fix later. Before acting, resolve the workflow profile and use its configured defect ledger path, defect ledger template, path glob, oracle path, evidence grades, and defect policy.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured defect ledger (default `docs/modernization/defect-ledger.md`) using the configured defect ledger template (default `~/.cursor/templates/defect-ledger-template.md`).

## Inputs

- Known bug reports, support notes, user decisions, path details, oracle mismatches, or suspicious legacy behavior.
- Optional `XP-NNN`, fixture, or story IDs.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured defect ledger template.
2. Record each defect or suspected mismatch as `DEF-NNN`; do not renumber existing IDs.
3. Require one or more `XP-NNN` IDs. A defect that names no path cannot be discharged by completing any path.
4. Refuse a defect that asks a system-wide question the methodology says has no system-wide answer (for example a single numeric tolerance for every path). Tell the caller to record a `DEC-NNN` that comparison is per path, and put the bound on that path's REQ (section 4b / Constraints).
5. Ask for or record the required decision: `reproduce-faithfully`, `fix-now`, or `fix-later`. Leave Decision `open` until the human answers.
6. For `fix-later`, create or reference a deferred backlog item. For `reproduce-faithfully`, record the bug-compatible expected output.
7. **README hub.** Update only the Artifact index row **Defect ledger**.

## Hard rules

- Do not decide that a mismatch is a bug without user or source evidence.
- Do not silently fix legacy behavior during the port.
- Open defects bind only the paths they name. They do not gate other slices.
- Owner policy that is not a path mismatch belongs in `/record-decision`, not here.
- Current state lives in the Decision cell. Do not add a prose history above the table.

## Outputs

- Configured defect ledger.
- Summary of new decisions, open decisions for the current slice, refused mis-posed defects, and suggested next command.

## Examples

- `/ledger-defects XP-001 "endpoint is exact in binary64; leave undecided"`
- `/ledger-defects @support/known-issues.md`

This command is available in chat with `/ledger-defects`.
It expects defect evidence and the `XP-NNN` it affects.
