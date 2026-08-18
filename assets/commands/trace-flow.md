# trace-flow

Trace one legacy behavior, entrypoint, screen, command, job, or batch flow from ingress through business logic, persistence, and egress. Before acting, resolve the workflow profile and use its configured flows directory, legacy flow template, evidence grades, behavior glob, legacy repo path, and translation gap path.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result under the configured flows directory (default `docs/modernization/flows/`) using the configured legacy flow template (default `~/.cursor/templates/legacy-flow-template.md`).

## Inputs

- A `BEH-NNN` ID, entrypoint, screen, command, job, or source file path.
- Optional trace depth or scope limit.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured legacy flow template.
2. Read the named behavior artifact and relevant legacy source, docs, and configuration.
3. Trace the flow from trigger to observable output, citing legacy locations.
4. Add sequence and state diagrams when enough evidence exists.
5. Mark unrecoverable regions explicitly and explain their impact on parity, skeleton planning, or refactoring.
6. Link translation gaps and target design implications without choosing the final design.

## Hard rules

- Do not invent control flow across missing or unreadable code.
- Do not omit unrecoverable regions.
- Do not refactor the legacy flow in the document; describe what exists and what it implies.
- Mermaid diagrams must avoid custom colors, styles, click events, and ambiguous node IDs.

## Outputs

- Configured legacy-flow document.
- Summary listing traced path, ambiguous regions, key data movement, and suggested next command.

## Examples

- `/trace-flow BEH-001`
- `/trace-flow entrypoint: src/main/oldcalc.c`

This command is available in chat with `/trace-flow`.
It expects a behavior ID, entrypoint, or source path.
