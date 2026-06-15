# patch-story

Apply a small, verified follow-up to a story that is already `Complete` without reopening the full `/plan-story` -> `/complete-story` workflow.

Use this for `story-followup`, `trivial-code`, or `docs-only` changes that are clearly tied to one completed story: polish, small bug fixes, copy tweaks, local debugging discoveries, targeted test repairs, or documentation corrections. Do **not** use it for new capabilities, binding constraint changes, adapter/port changes, API contract changes, persistence/auth changes, broad refactors, or changes that invalidate original acceptance criteria; route those to `/plan-story` or `/review-diff` instead.

## Inputs

- A story document at `docs/features/{STORY-ID}-*.md`.
- A concise description of the requested follow-up change.
- Optional: changed files already present in the working tree.

## Steps

1. Find and read the story document. If it is missing, stop and tell the user to run `/plan-story` first.
2. Confirm the story header has `**Status**: Complete`. If it is `Open` or `In Progress`, stop and use `/implement-story` or `/fix-from-qa` instead.
3. Classify the change using `~/.cursor/AGENTS.md` rule 1b:
   - `story-followup`
   - `trivial-code`
   - `docs-only`
4. Check whether the change touches any binding constraint, ADR-backed decision, port/adapter row, API contract, auth boundary, persistence layer, or original acceptance criterion semantics.
   - If yes, stop with a **Route escalation** note and recommend a new story or `/review-diff`.
   - If no, continue with the lightweight follow-up path.
5. Identify the smallest file set to modify and the smallest verification command or inspection that proves the follow-up.
6. For behavior changes, preserve the red-first rule at the smallest reasonable scale: reproduce the bug or add/tighten the focused test first, observe the failure, implement the fix, then observe the pass. For `trivial-code` and `docs-only`, record the explicit exception in the summary.
7. Do not edit original acceptance criteria text or uncheck completed criteria. If the follow-up exposes that a completed criterion was wrong, stop and emit a **Conflict report**.
8. Append one row to `## 11. Post-complete Follow-up Ledger` in the story:
   - next sequential follow-up ID (`F1`, `F2`, ...)
   - date
   - change class
   - intent
   - files touched
   - verification command or inspection proof
   - change ref — commit SHA, PR URL, or `uncommitted` / `TBD` with justification (use `git rev-parse HEAD` when the follow-up is committed)
   - review ref — `none`, or the path to `docs/reviews/...` when `/review-diff` was run for this follow-up
   - docs impact
   - AC impact (`none` unless a criterion needs a new story)
9. Update docs only when the follow-up changes setup, API behavior, user-visible behavior that docs describe, or operational procedures.
10. Run `/validate-story {STORY-ID} followups` after the ledger row is appended. Fix story-document drift before finishing.
11. Output a short summary: story ID, follow-up ID, change class, files changed, verification run, change ref, review ref, docs impact, validation result, and whether original ACs were unchanged.

## Review

Run `/review-diff` only when the change is not obviously local, affects security/reliability/API behavior, touches test infrastructure, or the risk classification is unclear. Otherwise the ledger entry plus targeted verification is sufficient.

## Examples

- `/patch-story OTO-2 fix empty-state copy after QA walkthrough`
- `/patch-story CHAT-4 debug retry spinner that remains visible after success`
- `/patch-story FND-1 docs-only: correct dev server port in README`

This command is available in chat with `/patch-story`.
It expects a story ID and a short follow-up description.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
