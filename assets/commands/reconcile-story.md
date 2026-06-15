# reconcile-story

Classify existing working-tree drift and reconcile it with a story document. Use this when a story is `Complete` but there are tracked or untracked changes from debugging, polish, or follow-up work that are not reflected in the story documentation.

This command does **not** assume the drift is safe. It maps changed files to a workflow lane first, then either appends follow-up ledger entries, recommends `/patch-story`, or escalates to `/review-diff` / a new story.

## Inputs

- Optional: a story ID (`{STORY-ID}`) if the user believes the drift belongs to one completed story.
- Optional: a base ref for diff inspection. Default is the project's main branch (`main` or `master`, auto-detected).

## Steps

1. Inspect the working tree:
   - `git status --short`
   - `git diff --stat`
   - `git diff --name-status <base-ref>...HEAD` when a base ref is available
   - include untracked files from `git status --short`
2. If a story ID was provided, find and read `docs/features/{STORY-ID}-*.md`.
3. If no story ID was provided, compare changed file paths against story Section 7 file touchpoints and recent story completion metadata where available. If the match is ambiguous, stop and ask the user which story owns the drift.
4. For each changed file or coherent group of files, classify the drift using `~/.cursor/AGENTS.md` rule 1b:
   - `story-followup`
   - `trivial-code`
   - `docs-only`
   - `hotfix-diff`
   - `full-story`
5. Check for escalation triggers:
   - binding constraints, ADRs, ports/adapters, persistence/auth, API contracts, broad refactors, or changed acceptance-criterion semantics
   - If any trigger is present, do not append a ledger entry. Output a **Route escalation** note and recommend `/review-diff` or a new story.
6. For drift that cleanly belongs to one completed story and stays inside `story-followup`, `trivial-code`, or `docs-only`:
   - verify the story is `Complete`
   - identify the minimal verification already run or still needed
   - resolve change ref from `git rev-parse HEAD` when committed, otherwise `uncommitted` or `TBD` with justification
   - append one row per coherent follow-up to `## 11. Post-complete Follow-up Ledger` (include `Review ref` as `none` unless `/review-diff` produced an artifact for this follow-up)
7. If verification is missing, leave the ledger row's `Verification` field as `TBD` and output the exact command or inspection needed before the row can be considered complete. The same `TBD` allowance applies to `Change ref` when the follow-up is not yet committed.
8. If docs changed without code, record the docs impact and verification note.
9. If code changed without matching tests and the change is behavioral, recommend `/patch-story {STORY-ID}` to add/tighten the focused test before implementation is considered reconciled.
10. When ledger rows are added, run `/validate-story {STORY-ID} followups` and include the result in the summary.

## Output

Return a Drift Reconciliation Summary:

- story ID or `unassigned`
- changed files grouped by classification
- ledger entries added or recommended
- verification still needed
- validation result when a ledger entry was added
- route escalations
- recommended next command (`/patch-story`, `/review-diff`, `/plan-story`, or none)

## Examples

- `/reconcile-story OTO-2`
- `/reconcile-story`
- `/reconcile-story CHAT-4 origin/main`

This command is available in chat with `/reconcile-story`.
It accepts an optional story ID and optional base ref.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
