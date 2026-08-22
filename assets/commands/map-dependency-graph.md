# map-dependency-graph

Build the join table between execution paths and the internal modules plus external dependencies they use. Before acting, resolve the workflow profile and use its configured dependency graph path, dependency graph template, path inventory path, dependency inventory path, evidence grades, and legacy repo path.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured dependency graph document (default `docs/modernization/dependency-graph.md`) using the configured dependency graph template (default `~/.cursor/templates/dependency-graph-template.md`).

## Inputs

- Execution path inventory.
- Dependency inventory.
- Legacy repo path.

## Preconditions

- `/inventory-paths` and `/inventory-dependencies` have produced their artifacts, or the user supplies equivalent inventories.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured dependency graph template.
2. For each `XP-NNN`, record internal modules/functions and `DEP-NNN` IDs the path uses.
3. Build the reverse index: each `DEP-NNN` to the `XP-NNN` IDs that use it.
4. Include a mermaid diagram only when the graph has fewer than 30 nodes.
5. If a used dependency is not in the inventory, stop. Report the missing dependency and tell the caller to run `/inventory-dependencies`. Do not invent `DEP-NNN` IDs.
6. **README hub.** If `## Modernization` exists, update only the Artifact index row **Dependency graph**. Do not create the section.

## Hard rules

- Structure only. Do not write dispositions, slice order, or decisions into this file.
- One evidence grade per row.
- After `Status: Snapshot`, append Errata or produce `vN+1`.
- Do not edit the legacy repo.

## Outputs

- Configured dependency graph.
- Summary of independent paths, widely shared dependencies, missing inventory rows if any, and suggested next command (`/analyze-impedance`).

## Examples

- `/map-dependency-graph`
- `/map-dependency-graph @docs/modernization/execution-path-inventory.md`

This command is available in chat with `/map-dependency-graph`.
It expects the path and dependency inventories to exist.
