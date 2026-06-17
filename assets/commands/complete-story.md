# complete-story

Orchestrates the tail of the SDLC for a single story after planning: implementation, review gate, QA verification, and documentation updates. Before acting, resolve the workflow profile (target project `.cursor/workflow.config.yml`, then user `~/.cursor/workflow.config.yml`) and use its command directory, story paths, review gate, QA result values, and status vocabulary. For each phase, read and follow the corresponding command spec under the configured command directory (defaults: `implement-story.md`, `review-story.md`, `qa-story.md`, `document-story.md`, `fix-from-qa.md`) as the source of truth for steps and rules.

## Preconditions

- A story document exists at the configured story glob in the **target project** (default `docs/features/{STORY-ID}-*.md`, typically produced by `/plan-story`).
- If the story file is missing, stop and tell the user to run `/plan-story` first — do not invent scope.

## Sequence

1. **`/implement-story {STORY-ID}`** — Execute per `implement-story.md` until the story header `**Status**:` is the configured complete value (default `Complete`) and acceptance criteria boxes match that completion.

2. **`/review-story {STORY-ID}`** — Repeat in a loop until the gate **passes**:
   - **Pass** means: the configured story-review artifact exists, its first line is the configured summary line (default `REVIEW SUMMARY:`), and that summary satisfies the configured review gate (default: zero `high` or `critical` findings for gated categories). The written `Gate result` must be the configured pass value (default `Pass`).
   - **On Block:** Address **Required actions before QA** from the review (code or tests per findings), then re-run `/review-story {STORY-ID}`. Do not proceed to QA while the review still blocks.

3. **`/qa-story {STORY-ID}`** — Repeat in a loop until **all** criteria have the configured pass result (default `PASS`):
   - **On any configured fail or blocked result** (defaults: `FAIL` or `BLOCKED`): Run `/fix-from-qa {STORY-ID}` per `fix-from-qa.md`, then re-run `/qa-story {STORY-ID}` until the evidence matrix is all pass.

4. **`/document-story {STORY-ID}`** — Run once QA is fully green, per `document-story.md`.

5. **Record completion baseline** — Fill the story's `## 10. Completion Metadata` section:
   - completion date
   - completion ref from the configured completion-ref strategy (default `git rev-parse --short HEAD`, otherwise the current branch/ref or `TBD: not committed`)
   - final configured review summary line
   - final QA command and all-PASS result summary
   - docs handoff result from `/document-story`

6. **`/validate-story {STORY-ID} complete`** — Run the validation gate after metadata is written. If it reports the configured fail or blocked values, fix the story documentation or missing evidence and re-run validation before calling the story complete.

## Output

End with a short summary: story ID, final review gate result, QA pass confirmation, completion ref, docs touched by `/document-story`, and `/validate-story` result.

This command is available in chat with `/complete-story`.
It expects one argument, the story ID, like so: `/complete-story {STORY-ID}`.
