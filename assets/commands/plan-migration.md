# plan-migration

Plan the modernization staging strategy, slice order, and per-slice prerequisites after assessment. Before acting, resolve the workflow profile and use its configured migration plan path, migration plan template, assessment path, path inventory, dependency graph, impedance analysis, decision register, oracle path, defect ledger path, design doc, ADR directory, staging strategies, and structure-fidelity choices.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured migration plan document (default `docs/modernization/migration-plan.md`) using the configured migration plan template (default `~/.cursor/templates/migration-plan-template.md`). Recommend ADRs; do not take over Architect-owned ADR files. If a new owner choice is required, tell the user to run `/record-decision` — this command does not write the decision register.

## Inputs

- Accepted modernization assessment.
- Path inventory, dependency graph, impedance analysis, decision register, oracle doc.
- Recovered purpose, domain model, path details, and refined requirements when available. Later slices may be inventory IDs only.
- Target language, version, and framework.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured migration plan and ADR templates.
2. Read the accepted assessment, inventories, graph, impedance analysis, decision register, oracle, defect ledger, and target-stack notes.
3. Choose a staging strategy from the configured strategies (`strangler`, `phased-rewrite`, `big-bang-parallel-run`) or stop if none fits.
4. Define slices in dependency order from the graph. Each slice lists `XP-NNN` IDs and a prerequisite table of only the `DEP-NNN`, `DEC-NNN`, and `DEF-NNN` IDs that bind **that** slice.
5. Do not gate a slice on global unresolved counts. A path with no `no-route` dependency and no open `DEC-NNN` in its row may be first.
6. Record the per-slice loop: recover → refine (`REQ-NNN`) → design (holistic, when the accumulating REQ set warrants it) → `/plan-story` → `/complete-story`.
7. Recommend ADRs for target stack, process boundaries, persistence, dependency substitutions, integration model, and cutover.
8. Document cutover/rollback only when the project has a live cutover. Omit that section for a library port with none.
9. **README hub.** Update the Artifact index row **Migration plan**. Set **Lane status** to `Phase: Planning`, `Gate: M4 pending` (or `M4 accepted` if the user already approved in-session), first/current slice from the plan, and Next command (usually `/document-legacy` scoped to that slice). Do not rewrite analysis index rows or design sections.

## Hard rules

- Do not plan implementation of a slice whose listed prerequisites are unresolved `E4` / `E5` path-detail claims without a `DEC-NNN`.
- Do not promise a target date without forecast confidence and a recalibration trigger.
- Do not convert a monolith to services/events by default.
- Do not edit analysis snapshots to reflect slice status. Check off prerequisites in the slice row.
- Recalibrate forecast after the first completed port slice using measured effort and parity defect rate.

## Outputs

- Configured migration plan.
- Recommended ADR titles.
- Open `DEC-NNN` IDs the user should record.
- Summary of staging strategy, first slice, that slice's prerequisites, and suggested next command (`/document-legacy` scoped to the first slice).

## Examples

- `/plan-migration @docs/modernization/ASSESSMENT.md target: C# .NET 8`
- `/plan-migration @docs/modernization/decision-register.md`

This command is available in chat with `/plan-migration`.
It expects an assessment and target-stack context.
