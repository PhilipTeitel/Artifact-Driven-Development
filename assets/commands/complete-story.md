# complete-story

Orchestrates the tail of the SDLC for a single story after planning: implementation, review gate, QA verification, and documentation updates. For each phase, read and follow the corresponding command spec under `~/.cursor/commands/` (`implement-story.md`, `review-story.md`, `qa-story.md`, `document-story.md`, `fix-from-qa.md`) as the source of truth for steps and rules.

## Preconditions

- A story document exists at `docs/features/{STORY-ID}-*.md` in the **target project** (typically produced by `/plan-story`).
- If the story file is missing, stop and tell the user to run `/plan-story` first — do not invent scope.

## Sequence

1. **`/implement-story {STORY-ID}`** — Execute per `implement-story.md` until the story header `**Status**:` is `Complete` and acceptance criteria boxes match that completion.

2. **`/review-story {STORY-ID}`** — Repeat in a loop until the gate **passes**:
   - **Pass** means: `docs/features/{STORY-ID}-review.md` exists, its first line is the single-line `REVIEW SUMMARY:`, and that summary shows **zero** `high` or `critical` findings (Phase Z / Z6). The written `Gate result` must be `Pass`.
   - **On Block:** Address **Required actions before QA** from the review (code or tests per findings), then re-run `/review-story {STORY-ID}`. Do not proceed to QA while the review still blocks.

3. **`/qa-story {STORY-ID}`** — Repeat in a loop until **all** criteria are `PASS`:
   - **On any `FAIL` or `BLOCKED`:** Run `/fix-from-qa {STORY-ID}` per `fix-from-qa.md`, then re-run `/qa-story {STORY-ID}` until the evidence matrix is all `PASS`.

4. **`/document-story {STORY-ID}`** — Run once QA is fully green, per `document-story.md`.

5. **Record completion baseline** — Fill the story's `## 10. Completion Metadata` section:
   - completion date
   - completion ref (`git rev-parse --short HEAD` when available, otherwise the current branch/ref or `TBD: not committed`)
   - final `REVIEW SUMMARY:` line
   - final QA command and all-PASS result summary
   - docs handoff result from `/document-story`

6. **`/validate-story {STORY-ID} complete`** — Run the validation gate after metadata is written. If it reports `FAIL` or `BLOCKED`, fix the story documentation or missing evidence and re-run validation before calling the story complete.

## Output

End with a short summary: story ID, final review gate result, QA pass confirmation, completion ref, docs touched by `/document-story`, and `/validate-story` result.

This command is available in chat with `/complete-story`.
It expects one argument, the story ID, like so: `/complete-story BUG-1`.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
