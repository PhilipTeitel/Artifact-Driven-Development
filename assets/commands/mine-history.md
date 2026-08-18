# mine-history

Mine legacy documentation, release notes, commit history, changelogs, help text, and issue exports for intent-bearing evidence. Before acting, resolve the workflow profile and use its configured legacy repo path, intent ledger path, intent ledger template, evidence grades, and behavior naming pattern.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition and follow it as binding role context.

Write the result to the configured intent ledger (default `docs/modernization/intent-ledger.md`) using the configured intent ledger template (default `~/.cursor/templates/intent-ledger-template.md`).

## Inputs

- Legacy repo path, if not configured.
- Optional documentation, release note, ticket export, or transcript paths.
- Optional time range or tag range for history mining.

## What the Archaeologist will do

1. Resolve the workflow profile and read the configured intent ledger template.
2. Read supplied docs, release notes, changelogs, help files, tickets, and commit/tag history.
3. Extract statements that explain why behavior exists, what users rely on, what changed, and which defects were intentionally fixed or preserved.
4. Assign evidence grades: docs and release notes are usually `E2 documented`; commit-message-only or naming-derived intent is usually `E4 inferred`; source diffs can be `E3 code-derived`.
5. Link intent statements to `BEH-NNN`, domain terms, requirements, or `TBD`.
6. Emit **Tensions / conflicts** when docs, history, code, or observed behavior disagree.

## Hard rules

- Do not treat commit messages as verified user intent without corroboration.
- Do not write requirements, design, or story files.
- Do not discard weak evidence; record it as `E4 inferred` or `E5 unknown`.

## Outputs

- Configured intent ledger document.
- Summary of strongest intent sources, weak or inferred intent, conflicts, and suggested next command.

## Examples

- `/mine-history /path/to/legacy-repo @docs/release-notes/`
- `/mine-history /path/to/legacy-repo v2.0..main`

This command is available in chat with `/mine-history`.
It expects a legacy repo path or configured legacy repo path, and may accept source-material paths.
