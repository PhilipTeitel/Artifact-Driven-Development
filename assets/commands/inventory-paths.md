# inventory-paths

Inventory every executable path in a legacy system before assessing modernization feasibility. Before acting, resolve the workflow profile and use its configured legacy repo path, modernization directory, execution-path inventory template, and evidence grades.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured path inventory document (default `docs/modernization/execution-path-inventory.md`) using the configured execution-path inventory template (default `~/.cursor/templates/execution-path-inventory-template.md`). Treat the legacy repo as read-only. If no legacy repo path is configured or supplied as an argument, stop and ask the user for it.

## Inputs

- Legacy repo path, if not configured in `modernization.legacyRepoPath`.
- Optional scope, such as `whole-repo`, `package: <name>`, or `paths: [<list>]`.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured execution-path inventory template.
2. Inspect the legacy repo for anything that can be triggered: CLI utilities, library API entry points, batch jobs, service endpoints, scheduled tasks, event handlers.
3. Assign `XP-NNN` IDs sequentially. Do not renumber existing IDs.
4. Record trigger, one-line description, and status (`active`, `suspected-dead`, or `unknown`). Use commit history, docs, and references only to classify status — do not produce a separate intent ledger.
5. Put active paths in the main table. Put suspected-dead, unknown, and retired paths in the appendix.
6. Give every row exactly one evidence grade and a citation.
7. Write the one-paragraph summary. Do not narrate table history.
8. **README hub.** Update only the Artifact index row **Execution path inventory** (status + link). Do not edit Lane status, other index rows, or design sections. If the Modernization section does not exist yet, skip the hub and let `/assess-modernization` create it.

## Hard rules

- Do not edit the legacy repo.
- Do not propose target architecture, slice order, or replacement dependencies.
- Do not write "not applicable" rows. Omit unused sections.
- After `Status: Snapshot`, do not edit cells to record later decisions. Append Errata or produce `vN+1`.
- One grade per row. Split mixed-grade claims.

## Outputs

- Configured execution path inventory.
- Short summary: active path count, appendix count, unknown triggers, suggested next command (`/inventory-dependencies`).

## Examples

- `/inventory-paths /path/to/legacy-repo`
- `/inventory-paths /path/to/legacy-repo paths:src,lib`

This command is available in chat with `/inventory-paths`.
It expects a legacy repo path unless one is configured in the workflow profile.
