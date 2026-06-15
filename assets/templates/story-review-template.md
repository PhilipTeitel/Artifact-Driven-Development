<!--
Per-story review contract:
- This file is produced by /review-story (or /review-diff for arbitrary base refs).
- It is a focused, lightweight audit limited to the changed surface — not a full-repo audit.
- Save as `docs/features/{STORY-ID}-review.md`.
- The auditor agent owns this template.
- The first non-comment line MUST be a single-line, machine-checkable "REVIEW SUMMARY" so QA and Phase Z (Z6) can grep it.
- Use the same finding ID prefixes as the full audit (`SEC-#`, `REL-#`, `API-#`, `TEST-#`); when both a full audit and a per-story review exist, IDs may overlap but are scoped to their own file (no cross-file renumbering).
- Findings list must use bullets per finding, not a single table — same as `audit-template.md` Detailed Findings.
- Severity is required on every finding; confidence is required on every non-`TEST-#` finding.
-->

REVIEW SUMMARY: result={Pass|Block} TEST-critical={N} TEST-high={N} SEC-critical={N} SEC-high={N} REL-critical={N} REL-high={N} API-critical={N} API-high={N}

# Story Review: {STORY-ID} — {Story Title}

**Reviewed against:** `docs/features/{STORY-ID}-{slug}.md`
**Date:** {YYYY-MM-DD}
**Mode:** `/review-story` | `/review-diff <base-ref>`
**Gate result:** `Pass` | `Block`

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

If the diff includes files **not** listed in Section 7, list them under "Out-of-plan changes" below — do not silently include them in scope.

### Out-of-plan changes

- `path/to/file` — short reason / recommendation (likely needs to be added to Section 7 or reverted)

---

## Findings

(One subsection per category with at least one finding; categories with no findings can be written as `None.`. Use bullets per finding — never a single category-spanning table.)

### Test Coverage (`TEST-#`)

(Required checks, per `~/.cursor/agents/auditor.md` per-story rubric:
- every AC ID in the story has a referenced test file in Section 8a, the file exists, and at least one test name matches and runs;
- every adapter in Section 4b has at least one non-mock integration test in Section 8a that exists and runs;
- every `Sn` from the linked refined requirements that this story implements is traceable to a test name in the changed surface (substring or annotation).)

#### TEST-1. { Short title }
- Severity:
- AC / Sn / Adapter affected:
- Missing or weak test:
- Why it matters:
- Lightest-weight way to add it:
- Verification gap:

### Reliability (`REL-#`)
None.

### Security (`SEC-#`)
None.

### API Contracts (`API-#`)
None.

---

## Required actions before QA

(Populate only when **Gate result = Block**. Each item must reference a finding ID and a concrete remediation step. The implementer should run `/fix-from-qa`-style red-first repair to address them, then re-run `/review-story`.)

- `TEST-1` — add the integration test for `SqliteExampleStore` cited in Phase Y; current evidence is a mock.
- `REL-1` — handle the unawaited promise in `services/foo.ts:42`.

---

## Notes

(Optional — context the implementer should know but that does not block the gate.)

- ...

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
