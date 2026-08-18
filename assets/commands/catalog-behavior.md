# catalog-behavior

Recover user-visible legacy behavior into `BEH-NNN` artifacts that can later feed `/refine-feature`. Before acting, resolve the workflow profile and use its configured behavior glob, behavior catalog template, evidence grades, legacy repo path, intent ledger, oracle doc, defect ledger, and scenario ID pattern.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write behavior artifacts under the configured behavior location (default `docs/modernization/behaviors/BEH-NNN-*.md`) using the configured behavior catalog template (default `~/.cursor/templates/behavior-catalog-template.md`). Use the next sequential `BEH-NNN`; do not renumber existing files.

## Inputs

- Legacy repo path, documentation, release notes, user guides, support scripts, screenshots, or observed runs.
- Optional named behavior, entrypoint, screen, batch job, command, or module.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured behavior catalog template.
2. Read the legacy map, intent ledger, oracle doc, defect ledger, and source material the user points to.
3. Identify one or more user-visible behaviors and assign `BEH-NNN` IDs.
4. For each behavior, capture actors, triggers, inputs, units, constraints, outputs, side effects, edge cases, error behavior, rules, invariants, citations, evidence grades, and draft Gherkin.
5. Link oracle fixtures, known defects, and unanswered provenance gaps.
6. Set status to `Ready for Requirements` only when no covered behavior depends on unresolved `E4` / `E5` evidence.

## Hard rules

- Do not turn behavior catalog entries into design or story docs.
- Do not claim a behavior is business-intended merely because code does it.
- Do not hide weak evidence; mark `E4 inferred` or `E5 unknown` explicitly.
- If code, docs, and run output disagree, write a **Tensions / conflicts** list.

## Outputs

- One or more configured `BEH-NNN` behavior files.
- Summary listing new behavior IDs, evidence grade distribution, unresolved blockers, and suggested next command.

## Examples

- `/catalog-behavior @docs/user-guide.md screen: pricing calculator`
- `/catalog-behavior /path/to/legacy-repo entrypoint: batchImport`

This command is available in chat with `/catalog-behavior`.
It expects source material or a behavior/entrypoint to inspect.
