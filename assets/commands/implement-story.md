# implement-story

This directs the Implementer to implement the given user story. Before acting, resolve the workflow profile and use its story paths, decisions directory, review gate, QA result values, and status vocabulary. The story document in the configured features directory (default `docs/features/`) is the spec — read it fully before writing any code. Also read every ADR linked from the story's **Linked architecture decisions** section.

## Steps

1. Find the story document at the configured story glob (default `docs/features/{STORY-ID}-*.md`).
2. Read the entire story document and linked ADR files in the configured decisions directory (default `docs/decisions/ADR-*.md`).
3. **Pre-flight (before any code):** Output a **Requirement traceability** table: each binding constraint (from section 4 and ADRs) → planned **module / package / API** → first file you will touch. If any row cannot be filled, **stop** and ask; do not substitute a different dependency or storage layer.
4. Set the header `**Status**:` to the configured active story status (default `In Progress`).
5. Follow the **Implementation Order** section for sequencing.
6. After completing each acceptance criterion, check its box (`- [ ]` → `- [x]`) in the story document immediately.
7. When all criteria are checked, set the header `**Status**:` to the configured complete story status (default `Complete`).
8. Output the end-of-session summary: files changed, criteria completed, **How implemented** (libraries, APIs, where data is read/written), how to verify locally, and final status.

**Rules:** Do not silently replace persistence, transport, or named dependencies versus the story or ADRs. If you hit a conflict or impossibility, stop with a **Conflict report** (cite doc sections).

If you cannot find the story document, stop and tell the user — do not improvise a plan.

## What to do next

Once Status is the configured complete value (default `Complete`, every AC box is checked), run `/review-story {STORY-ID}` as a soft gate before QA. The review writes the configured story-review artifact and emits the configured summary line (default `REVIEW SUMMARY:`). Phase Z's `Z6` requires that line to satisfy the configured review gate before `/qa-story` is run.

Workflow tail defaults to `/implement-story` → `/review-story` → (configured review pass) `/qa-story` → (all configured QA pass) `/document-story`. On configured review block, address the listed actions and re-run it. On configured QA fail/blocked, run `/fix-from-qa {STORY-ID}` and re-verify.

This command will be available in chat with /implement-story.
It expects one argument, the story ID, like so: `/implement-story {STORY-ID}`.
