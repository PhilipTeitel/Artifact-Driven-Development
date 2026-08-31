# trace-path

Recover what one execution path (or a tight group of related triggers) actually does. Before acting, resolve the workflow profile and use its configured path glob, execution-path detail template, evidence grades, path inventory, dependency graph, defect ledger path, and legacy repo path.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result under the configured paths directory (default `docs/modernization/paths/XP-NNN-*.md`) using the configured execution-path detail template (default `~/.cursor/templates/execution-path-detail-template.md`). Use the `XP-NNN` already assigned in the path inventory; do not invent a parallel ID scheme.

## Inputs

- One `XP-NNN` ID, or a named group of related paths that are the same operation with different triggers.
- Path inventory and legacy repo.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured execution-path detail template.
2. Trace the path's sequence of operations, internal callees, external `DEP-NNN` uses, data flow, and actual error handling.
3. Give every claim exactly one evidence grade and a citation. Split mixed-grade statements into separate rows.
4. Include a sequence diagram only when there are 3+ actors or an async hop. Include store/file rows only when this path uses a store.
5. If behavior looks wrong, add or cite a `DEF-NNN`. Do not decide reproduce vs fix.
6. Set status to `Ready for Requirements` only when no claim that would bind planning remains `E4` / `E5` without a listed open question.
7. Write the one-paragraph summary. Do not add port status, slice progress, or decision preambles.
8. **README hub.** Update only the Artifact index row **Path details** (set Status to the count of files under `docs/modernization/paths/`). Do not edit Lane status.

## Hard rules

- Describe what the legacy path does, not what the port should do.
- Do not invent control flow across missing code. Mark unrecoverable steps as `E5 unknown`.
- Do not edit analysis inventories to "update" them with findings from this path. If the inventory is factually wrong, append Errata there (same owner) or produce `vN+1`.
- After `Status: Snapshot`, append Errata or produce `vN+1`.
- Do not edit the legacy repo.
- Do not catalog paths outside the requested scope.

## Outputs

- One configured path-detail file (or one file for a tight group).
- Summary of weakest grade, open questions, `DEF-NNN` citations, and suggested next command (`/recover-domain` or `/ledger-defects` or `/refine-feature`).

## Examples

- `/trace-path XP-001`
- `/trace-path XP-001 XP-002 group: linspace-family`

This command is available in chat with `/trace-path`.
It expects one or more `XP-NNN` IDs from the path inventory.
