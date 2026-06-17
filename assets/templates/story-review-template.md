<!--
Per-story review contract:
- This file is produced by /review-story (or /review-diff for arbitrary base refs).
- It is a focused, lightweight audit limited to the changed surface — not a full-repo audit.
- Save using the configured story-review or diff-review path (defaults: `docs/features/{STORY-ID}-review.md` or `docs/reviews/diff-...md`).
- The auditor agent owns this template.
- The first non-comment line MUST use the configured machine-checkable review summary label and format (default "REVIEW SUMMARY") so QA and the configured quality gate can grep it.
- Use configured category-specific finding ID prefixes. Defaults are `TEST-#` for Test Coverage, `REL-#` for Reliability, `SEC-#` for Security, and `API-#` for API Contracts. When both a full audit and a per-story review exist, IDs may overlap but are scoped to their own file (no cross-file renumbering).
- Findings list must use bullets per finding, not a single table — same as `audit-template.md` Detailed Findings. Every finding subsection item must be headed as `#### PREFIX-#. { Short title }` using that section's prefix.
- Severity is required on every finding; confidence is required on every non-`TEST-#` finding.
- `None.` is an exclusive empty-state marker: include it only when a subsection has no findings, and do not include it alongside findings, evidence summaries, or positive assertions.
-->

REVIEW SUMMARY: result={Pass|Block} TEST-critical={N} TEST-high={N} SEC-critical={N} SEC-high={N} REL-critical={N} REL-high={N} API-critical={N} API-high={N}

# Story Review: {STORY-ID} — {Story Title}

**Reviewed against:** `{configured story path, default docs/features/{STORY-ID}-{slug}.md}`
**Date:** {YYYY-MM-DD}
**Mode:** `/review-story` | `/review-diff <base-ref>`
**Gate result:** `{configured review pass value}` | `{configured review block value}` (defaults: `Pass` | `Block`)

---

## Scope

- Story ID:
- Linked refined requirements (Sn IDs in scope):
- Files in scope (from Section 7 "Files to CREATE/MODIFY" intersected with `git diff` when available):
  - `path/to/file` — created
  - `path/to/file` — modified
- Tests in scope (from Section 8a Test Plan):
  - `path/to/test::name`
- Adapters in scope (from Section 4b):
  - `AdapterName` for port `PortName`

{If the diff includes files **not** listed in Section 7, list them under "Out-of-plan changes" below — do not silently include them in scope.}

### Out-of-plan changes

- `path/to/file` — short reason / recommendation {likely needs to be added to Section 7 or reverted}

---

## Findings

{Keep every category subsection. If a category has no findings, write exactly `None.` as the only content below that heading. If a category has findings, omit `None.` and list each finding as `#### PREFIX-#. { Short title }` using that category's prefix. Use bullets per finding — never a single category-spanning table. Put non-finding context in `## Notes`, not in `## Findings`.}

### Test Coverage {`TEST-#`}

{Required checks, per the configured auditor per-story rubric:
- every AC ID in the story has a referenced test file in Section 8a, the file exists, and at least one test name matches and runs;
- every adapter in Section 4b has at least one non-mock integration test in Section 8a that exists and runs;
- every `Sn` from the linked refined requirements that this story implements is traceable to a test name in the changed surface (substring or annotation).}

#### TEST-1. { Short title }
- Severity:
- AC / Sn / Adapter affected:
- Missing or weak test:
- Why it matters:
- Lightest-weight way to add it:
- Verification gap:

### Reliability {`REL-#`}

#### REL-1. { Short title }
- Severity:
- Confidence:
- AC / Sn affected:
- Files and lines:
- Evidence checked:
- Failure mode:
- Root cause:
- Minimal safe fix:
- Regression test idea:
- Verification:

### Security {`SEC-#`}

#### SEC-1. { Short title }
- Severity:
- Confidence:
- AC / Sn affected:
- Files and lines:
- Evidence checked:
- Failure mode or exploit scenario:
- Root cause:
- Minimal safe fix:
- Regression test idea:
- Verification:

### API Contracts {`API-#`}

#### API-1. { Short title }
- Severity:
- Confidence:
- AC / Sn affected:
- Files and lines:
- Evidence checked:
- Affected behavior or contract:
- Failure mode:
- Minimal safe fix:
- Backward-compatibility or migration notes:
- Regression test idea:
- Verification:

---

## Required actions before QA

{Populate only when **Gate result = Block**. Each item must reference a finding ID and a concrete remediation step. The implementer should run `/fix-from-qa`-style red-first repair to address them, then re-run `/review-story`.}

- `TEST-1` — add the integration test for `SqliteExampleStore` cited in Phase Y; current evidence is a mock.
- `REL-1` — handle the unawaited promise in `services/foo.ts:42`.

---

## Notes

{Optional — context the implementer should know but that does not block the gate.}

- ...
