# plan-port-story

Plan a single modernization port story with provenance and parity criteria. Before acting, resolve the workflow profile and use its configured story file pattern, port story template, behavior glob, oracle path, defect ledger path, migration plan path, translation gap path, purpose path, domain path, requirements directory, decisions directory, status vocabulary, and parity phase.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

This command is the modernization counterpart to `/plan-story`. It writes a story under the configured features directory using the configured port-story template (default `~/.cursor/templates/port-story-template.md`).

## Inputs

- Story ID.
- Linked `BEH-NNN` behavior(s), refined `REQ-NNN` / `Sn` scenarios, or migration-plan slice.
- Migration plan, oracle doc, defect ledger, translation-gap doc, purpose, domain model, and ADRs.

## What the Architect will do

1. Resolve the workflow profile and read the configured port story template.
2. Read the configured purpose, domain model, design doc, migration plan, oracle doc, defect ledger, translation gaps, linked requirements, linked ADRs, and behavior artifacts.
3. Refuse to mark the story ready when covered behavior is `E4 inferred` or `E5 unknown` without a recorded user decision.
4. Fill the story's normal ADD sections: summary, ADRs, DoR, binding constraints, ports/adapters, API/schema, UI flow, file touchpoints, test plan, risks, and implementation order.
5. Add modernization sections: legacy source touchpoints, `8b. Parity Plan`, `Phase P`, and `Z8`.
6. Map every covered `BEH-NNN` to at least one `P` criterion and test-plan row with oracle fixture or acceptance-data source, tolerance, and defect decision.
7. Map adapter and port constraints into Phase Y as usual.
8. Update the configured design doc backlog row with a link to the story when appropriate, preserving completed and in-progress rows.

## Hard rules

- Do not create a port story without parity criteria unless the user explicitly classifies it as a documentation-only or spike story.
- Do not allow Phase P evidence to exceed the oracle tier.
- Do not silently improve legacy behavior; cite the defect ledger for `fix-now` or `reproduce-faithfully`.
- Do not introduce target-stack substitutions without ADR traceability.

## Outputs

- Configured port story file.
- Optional backlog link update in the configured design doc.
- Summary of covered behaviors, parity fixtures, weak-evidence blockers, ADR gaps, and suggested next command.

## Examples

- `/plan-port-story CALC-1 BEH-001 BEH-002`
- `/plan-port-story IMPORT-1 @docs/modernization/migration-plan.md slice: importer-core`

This command is available in chat with `/plan-port-story`.
It expects a story ID and behavior or migration-plan slice.
