# inventory-dependencies

Inventory every external legacy dependency and classify whether a target-stack route exists. Before acting, resolve the workflow profile and use its configured dependency inventory path, dependency inventory template, source stack, target stack, evidence grades, and decision-register path.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured dependency inventory (default `docs/modernization/dependency-inventory.md`) using the configured dependency inventory template (default `~/.cursor/templates/dependency-inventory-template.md`).

## Inputs

- Legacy repo path and source stack.
- Target language, version, and framework when known.
- Optional architecture or platform constraints.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured dependency inventory template.
2. Inventory runtime, framework, package, native, database, UI, deployment, OS, vendored, and build dependencies from code, manifests, lockfiles, installers, and docs.
3. Record version (known or unknown), license, support status, and exactly one disposition per row:
   - `available` — a credible target-stack equivalent exists.
   - `reimplementable` — no direct equivalent, but the needed behavior is bounded enough to rewrite.
   - `undecided` — an owner decision is needed; write the question in **Decision needed**.
   - `no-route` — no known replacement. This binds paths that use the dependency, not the whole program.
4. Give every row exactly one evidence grade and a citation.
5. Do not use `blocked`. Owner-pending (`undecided`) and dead-end (`no-route`) must not look identical.
6. **README hub.** If `## Modernization` exists, update only the Artifact index row **Dependency inventory**. Do not edit Lane status or other rows. Do not create the section.

## Hard rules

- Do not silently approve a replacement because a modern package exists.
- Dispositions are snapshot classifications. Later substitution choices are `DEC-NNN` rows via `/record-decision`, not cell edits.
- After `Status: Snapshot`, append Errata or produce `vN+1`. Do not rewrite a row to "available" because a decision was later made.
- Omit unused sections. Do not write N/A rows.
- Binding target-stack replacements still need an ADR, recommended rather than silently chosen.

## Outputs

- Configured dependency inventory.
- Summary of `no-route` and `undecided` counts, the questions that need `/record-decision`, and suggested next command (`/map-dependency-graph`).

## Examples

- `/inventory-dependencies /path/to/legacy-repo target: C# .NET 8`
- `/inventory-dependencies @docs/vendor-list.md`

This command is available in chat with `/inventory-dependencies`.
It expects a legacy repo path or configured legacy repo path and target-stack information when available.
