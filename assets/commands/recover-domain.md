# recover-domain

Recover the product purpose and domain model from legacy behavior, documentation, release notes, and intent evidence. Before acting, resolve the workflow profile and use its configured purpose path, domain path, purpose template, domain template, behavior glob, intent ledger, legacy map, defect ledger, and evidence grades.

**Command-agent binding:** This command is role-bound to `agents.modeler`. Before executing any step, load the configured Modeler agent definition and follow it as binding role context.

This directs the Modeler agent in **Legacy recovery mode**. It writes or updates the configured purpose document (default `docs/PURPOSE.md`) and configured domain model (default `docs/DOMAIN.md`) using the existing purpose and domain templates rather than creating modernization-specific replacements.

## Inputs

- Behavior catalog, user documentation, release notes, intent ledger, and legacy map.
- Optional existing purpose or domain model to reconcile.

## What the Modeler will do

1. Resolve the workflow profile and read the configured purpose and domain templates.
2. Read the configured behavior catalog, intent ledger, legacy map, defect ledger, and any user-supplied docs.
3. Extract purpose-level statements, domain terms, entities, fields, invariants, lifecycles, relationships, and consistency boundaries.
4. Carry evidence grades and citations into the relevant `Source` fields.
5. Mark `E4 inferred` and `E5 unknown` items as open questions when they affect design or story planning.
6. Emit **Tensions / conflicts** when legacy implementation names, user documentation, and observed behavior disagree.

## Hard rules

- Do not invent domain meaning from implementation structure.
- Do not create architecture, backlog, stories, or APIs.
- Do not silently approve inferred domain terms; open questions block downstream work for the affected scope.
- Preserve existing approved purpose/domain content unless the user explicitly supersedes it.

## Outputs

- Configured purpose artifact.
- Configured domain model artifact.
- Summary listing source material consumed, recovered purpose/domain decisions, weak-evidence blockers, and suggested next command.

## Examples

- `/recover-domain @docs/modernization/behaviors/`
- `/recover-domain @docs/modernization/intent-ledger.md @docs/user-guide.md`

This command is available in chat with `/recover-domain`.
It expects recovered behavior or intent source material.
