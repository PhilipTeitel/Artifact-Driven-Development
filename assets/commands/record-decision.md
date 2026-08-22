# record-decision

Record a human porting decision in the decision register. Before acting, resolve the workflow profile and use its configured decision register path, decision register template, and evidence grades.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured decision register (default `docs/modernization/decision-register.md`) using the configured decision register template (default `~/.cursor/templates/decision-register-template.md`). This command is the only writer of that artifact.

## Inputs

- The question to decide, or an existing `DEC-NNN` to update.
- The human's answer when one has been given.
- Affected `XP-NNN`, `DEP-NNN`, `IMP-NNN`, `DEF-NNN`, and slice IDs.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured decision register template.
2. If the register does not exist, create it from the template.
3. Add a `DEC-NNN` row, or update the Answer / Status cells of an existing row. Do not renumber IDs.
4. Status is `open` until the human has answered, then `decided`. `open` is not `no-route`.
5. Put current state in the Answer and Status cells. Do not add a prose history above the table.
6. Do not copy the answer into analysis snapshots. Later artifacts cite `DEC-NNN`.
7. **README hub.** Update the Artifact index row **Decision register**. Update **Lane status** only when the decision changes the next command or M1/M4 gate (for example first-slice conditions now resolved). Do not edit analysis index rows.

## Hard rules

- Do not invent the answer. If the human has not decided, leave Status `open` and Answer `TBD`.
- Defect reproduce / fix-now / fix-later belongs in `/ledger-defects`, not here. Cite `DEF-NNN` when a porting decision depends on one.
- Binding target-stack design still needs an ADR, written by the Architect. Cite `ADR-NNN` in Affects when relevant.
- Do not edit path inventory, dependency inventory, graph, or impedance rows to reflect this decision.

## Outputs

- Updated decision register.
- Summary of new or changed `DEC-NNN` IDs, which slices they bind, and suggested next command.

## Examples

- `/record-decision "Port XP-001 first?" answer: yes affects: XP-001`
- `/record-decision DEC-003 answer: "comparison is per path, not global"`

This command is available in chat with `/record-decision`.
It expects a question or `DEC-NNN` and, when available, the human's answer.
