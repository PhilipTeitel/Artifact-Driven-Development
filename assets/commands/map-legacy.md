# map-legacy

Map a legacy repository before assessing modernization feasibility. Before acting, resolve the workflow profile and use its configured legacy repo path, modernization directory, legacy map template, evidence grades, source stack, and target stack.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured legacy map document (default `docs/modernization/legacy-map.md`) using the configured legacy map template (default `~/.cursor/templates/legacy-map-template.md`). Treat the legacy repo as read-only. If no legacy repo path is configured or supplied as an argument, stop and ask the user for it.

## Inputs

- Legacy repo path, if not configured in `modernization.legacyRepoPath`.
- Optional source stack and target stack notes.
- Optional scope, such as `whole-repo`, `package: <name>`, or `paths: [<list>]`.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured legacy map template.
2. Inspect only the legacy repo and user-supplied source material. Do not infer requirements from unrelated projects.
3. Detect languages, runtimes, frameworks, build files, deployment files, entrypoints, external interfaces, data stores, file formats, and existing tests.
4. Record coverage honestly as deep, light, skipped, or unknown.
5. Identify complexity and setup hotspots without choosing a migration strategy.
6. Write or update the configured legacy map document, preserving template headings.

## Hard rules

- Do not edit the legacy repo.
- Do not propose target architecture, slice order, or replacement dependencies.
- Every non-obvious fact must include a configured evidence grade and citation.
- If a section has no evidence yet, write `None yet.` rather than guessing.

## Outputs

- Configured legacy map document.
- Short summary listing inspected areas, skipped areas, likely setup blockers, and suggested next command.

## Examples

- `/map-legacy /path/to/legacy-repo`
- `/map-legacy /path/to/legacy-repo paths:src,docs`

This command is available in chat with `/map-legacy`.
It expects a legacy repo path unless one is configured in the workflow profile.
