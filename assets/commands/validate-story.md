# validate-story

Validate that a story document is structurally consistent with the configured story template (default `~/.cursor/templates/user-story-template.md`) and that its evidence, completion metadata, and post-complete follow-up ledger are coherent. Before acting, resolve the workflow profile and use its story glob, template path, methodology, status vocabulary, QA values, review summary format, lane names, and reviews directory.

Use this as a lightweight quality gate after `/plan-story`, before `/implement-story`, after `/complete-story`, or after `/patch-story` / `/reconcile-story`.

## Inputs

- A story document matching the configured story glob (default `docs/features/{STORY-ID}-*.md`).
- Optional mode:
  - `ready` — validate planning readiness before implementation.
  - `complete` — validate completion metadata and review/QA evidence.
  - `followups` — validate post-complete ledger entries.
  - default — run all applicable checks based on story status.

## Steps

1. Find and read the story document using the configured story glob. If missing, stop and report the configured blocked value (default `BLOCKED`).
2. Read the configured story template for the required section contract.
3. Verify required sections exist in order:
   - Summary
   - Linked architecture decisions (ADRs)
   - Definition of Ready (DoR)
   - Binding constraints
   - Ports & Adapters
   - API Endpoints + Schemas
   - Frontend Flow
   - File Touchpoints
   - Acceptance Criteria Checklist
   - Test Plan
   - Risks & Tradeoffs
   - Implementation Order
   - Completion Metadata
   - Post-complete Follow-up Ledger
4. Parse all acceptance criteria IDs from markdown task items (`- [ ] **A1**` / `- [x] **A1**`) and verify each has exactly one `Evidence:` line.
5. Verify every AC ID appears in Section 8a Test Plan `Covers AC`.
6. Verify every Test Plan row has a file/test reference or an explicit non-test evidence note for manifest/static/script checks.
7. If Section 4b lists ports or adapters, verify:
   - each port has at least one configured contract test row (default `contract`)
   - each adapter has at least one configured integration test row (default `integration`)
   - Phase Y contains a `(binding)` criterion citing non-mock evidence for each adapter
8. If the story status is the configured complete value, verify:
   - all acceptance criteria are checked
   - `Completion Metadata` is filled with no placeholder values except an explicitly justified `TBD`
   - final review summary starts with the configured review summary label (default `REVIEW SUMMARY:`)
   - QA result states all criteria passed using the configured pass value or links to the all-pass evidence
9. If the follow-up ledger has rows beyond the example row, verify each row has:
   - sequential ID (`F1`, `F2`, ...)
   - date
   - allowed change class from the configured workflow lanes (defaults include `story-followup`, `trivial-code`, and `docs-only`)
   - files touched
   - verification command or inspection proof, or `TBD` plus a required next command
   - change ref — commit SHA, PR URL, `uncommitted`, or justified `TBD`
   - review ref — `none` or a path under the configured reviews directory
   - AC impact field
10. Output a Story Validation Matrix with one row per check:
   - Check
   - Result (configured QA-style values; defaults: `PASS` / `FAIL` / `BLOCKED`)
   - Evidence
   - Fix recommendation

## Result Semantics

- Configured pass value (default `PASS`): the story is internally consistent for the requested mode.
- Configured fail value (default `FAIL`): the story exists but has missing or inconsistent content.
- Configured blocked value (default `BLOCKED`): required files or evidence cannot be found.

## Examples

- `/validate-story {STORY-ID}`
- `/validate-story {STORY-ID} ready`
- `/validate-story {STORY-ID} complete`
- `/validate-story {STORY-ID} followups`

This command is available in chat with `/validate-story`.
It expects a story ID and optional mode.
