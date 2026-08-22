# plan-port-story

Plan a single modernization port story with provenance, slice prerequisites, and parity criteria. Before acting, resolve the workflow profile and use its configured story file pattern, port story template, path glob, path test-plan glob, oracle path, defect ledger path, decision register path, migration plan path, purpose path, domain path, requirements directory, decisions directory, status vocabulary, and parity phase.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

This command is the modernization counterpart to `/plan-story`. It writes a story under the configured features directory using the configured port-story template (default `~/.cursor/templates/port-story-template.md`).

## Inputs

- Story ID.
- Linked `XP-NNN` path(s), refined `REQ-NNN` / `Sn` scenarios, or migration-plan slice.
- Path details, path test plans, migration plan, oracle doc, defect ledger, decision register, purpose, domain model, and ADRs.

## What the Architect will do

1. Resolve the workflow profile and read the configured port story template.
2. Read the configured purpose, domain model, design doc, migration plan, oracle doc, defect ledger, decision register, linked requirements, linked ADRs, path details, and path test plans.
3. Copy the migration-plan row's prerequisite table into **Slice prerequisites**. Checkoff happens in the story. Do not edit analysis snapshots.
4. Refuse to mark the story ready when a listed prerequisite is unresolved, or when a covered claim is `E4 inferred` or `E5 unknown` without a `DEC-NNN`.
5. Fill the story's normal ADD sections. Omit API and frontend sections entirely when they do not apply.
6. Add modernization sections: legacy source touchpoints (from the path detail, one grade per row), `8b. Parity Plan` (from the path test plan), `Phase P`, and `Z8`.
7. Map every covered `XP-NNN` that has a fixture or acceptance-data source to at least one `P` criterion. If the path test plan says no fixture exists, do not invent a parity criterion.
8. Use the path test plan's comparison rule. Do not apply a global numeric default.
9. Update the configured design doc backlog row with a link to the story when appropriate, preserving completed and in-progress rows.
10. **README hub.** Update the Artifact index row **Port stories** to point at `docs/features/` (or "see Backlog"). Do not edit Lane status or analysis index rows. Do not add design sections; `/design-application` does that.

## Hard rules

- Do not create a port story without parity criteria unless the user explicitly classifies it as a documentation-only or spike story, or the path test plan records that no oracle source exists.
- Do not allow Phase P evidence to exceed the oracle tier.
- Do not silently improve legacy behavior; cite the defect ledger for `fix-now` or `reproduce-faithfully`.
- Do not introduce target-stack substitutions without ADR traceability.
- Do not file or keep a criterion that asks for a system-wide numeric tolerance. Comparison is per path.

## Outputs

- Configured port story file.
- Optional backlog link update in the configured design doc.
- Summary of covered paths, prerequisites, parity fixtures, weak-evidence blockers, ADR gaps, and suggested next command.

## Examples

- `/plan-port-story CALC-1 XP-001`
- `/plan-port-story IMPORT-1 @docs/modernization/migration-plan.md slice: importer-core`

This command is available in chat with `/plan-port-story`.
It expects a story ID and path IDs or a migration-plan slice.
