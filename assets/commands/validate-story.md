# validate-story

Validate that a story document is structurally consistent with the configured story template (default `~/.cursor/templates/user-story-template.md`, or the port-story template when the story is a modernization port) and that its evidence, model-fidelity references, completion metadata, and post-complete follow-up ledger are coherent. Before acting, resolve the workflow profile and use its story glob, template path, purpose path, domain path, methodology, status vocabulary, QA values, review summary format, lane names, and reviews directory.

**Command-agent binding:** This command is role-bound to `agents.qa`. Before executing any step, load the configured QA agent definition and follow it as binding role context.

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
2. Read the configured story template for the required section contract. If the story has `**Modernization slice:**` or `Phase P: Parity`, use the configured port-story template instead and apply the extra port-story checks in step 8b.
3. Verify required sections exist in order. Omit API Endpoints and Frontend Flow when the template says they do not apply (port stories may omit them entirely). Do not fail a port story for missing those sections when they were correctly omitted.
   - Summary (including Domain model touchpoints; port stories also need Legacy source touchpoints)
   - Linked architecture decisions (ADRs)
   - Definition of Ready (DoR)
   - Slice prerequisites (port stories only)
   - Binding constraints
   - Ports & Adapters
   - API Endpoints + Schemas (omit when not an HTTP/RPC/message slice)
   - Frontend Flow (omit when not UI-facing)
   - File Touchpoints
   - Acceptance Criteria Checklist
   - Test Plan
   - Parity Plan (port stories only)
   - Risks & Tradeoffs
   - Implementation Order
   - Completion Metadata
   - Post-complete Follow-up Ledger
4. Parse all acceptance criteria IDs from markdown task items (`- [ ] **A1**` / `- [x] **A1**`) and verify each has exactly one `Evidence:` line.
5. Verify every AC ID appears in Section 8a Test Plan `Covers AC`.
6. Verify every Test Plan row has a file/test reference or an explicit non-test evidence note for manifest/static/script checks.
7. Verify model-fidelity readiness:
   - if the story is not explicitly creating or bootstrapping the configured purpose/domain artifacts, the configured purpose document and domain model exist or are linked as approved prerequisites
   - the story lists the domain terms, entities, invariants, lifecycles, or consistency boundaries it touches, or explicitly states that none apply
   - Phase Z contains the configured model-fidelity criterion (default `Z7`) requiring zero high or critical `MODEL-#` findings
8. If Section 4b lists ports or adapters, verify:
   - each port has at least one configured contract test row (default `contract`)
   - each adapter has at least one configured integration test row (default `integration`)
   - Phase Y contains a `(binding)` criterion citing non-mock evidence for each adapter
8b. If this is a port story, also verify:
   - every covered `XP-NNN` appears in Section 1b with exactly one evidence grade
   - slice prerequisites name only `DEP-NNN` / `DEC-NNN` / `DEF-NNN` IDs and are marked resolved for `ready` / `complete`
   - Section 8a has a **Covers XP** column
   - `## 8b. Parity Plan` comparison rules come from the path test plan, not a global default
   - Phase P exists when a fixture or acceptance-data source exists; Z8 exists in Phase Z
   - no covered claim is `E4` or `E5` without a cited `DEC-NNN`
9. If the story status is the configured complete value, verify:
   - all acceptance criteria are checked
   - `Completion Metadata` is filled with no placeholder values except an explicitly justified `TBD`
   - final review summary starts with the configured review summary label (default `REVIEW SUMMARY:`)
   - final review summary includes `MODEL-critical=0` and `MODEL-high=0` when model fidelity is required
   - QA result states all criteria passed using the configured pass value or links to the all-pass evidence
   - for port stories, Completion Metadata includes a parity ref to a report whose first non-comment line is `PARITY SUMMARY:`
10. If the follow-up ledger has rows beyond the example row, verify each row has:
   - sequential ID (`F1`, `F2`, ...)
   - date
   - allowed change class from the configured workflow lanes (defaults include `story-followup`, `trivial-code`, and `docs-only`)
   - files touched
   - verification command or inspection proof, or `TBD` plus a required next command
   - change ref — commit SHA, PR URL, `uncommitted`, or justified `TBD`
   - review ref — `none` or a path under the configured reviews directory
   - AC impact field
11. Output a Story Validation Matrix with one row per check:
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
