<!--
Audit report contract:
- Use this template exactly.
- Keep all headings and heading order exactly as written.
- Do not remove sections, even when they are empty.
- If a section has no content yet, write `None yet.` under that heading.
- Do not introduce new top-level sections.
- Do not replace the `Detailed Findings` subsections with tables.
- Under `Detailed Findings`, each finding must use the bullet fields defined for its category.
- `Findings Summary` and `Execution Log` may use markdown tables; the detailed finding sections may not.
- Every finding must appear in both `Findings Summary` and the matching `Detailed Findings` subsection.
- Every selected fix must appear in both `Fix Plan` and `Execution Log`.
- The `Decision` field in each detailed finding is the source of truth for triage.
- Every non-`TEST-#` finding must include `Severity`, `Confidence`, and `Evidence checked`.
- `Decision: fix now` means the finding belongs in `Fix Plan -> Selected Fixes`.
- `Decision: defer` means the finding belongs in `Deferred Findings` and must include `Why not now`.
-->

# Audit Report

## Scope And Timebox
- Scope: `whole-repo` | `package: <name>` | `paths: [<list>]`
- Repository:
- Stack(s) detected:
- Time budget (optional):
- Goal:
- Constraints:
- Highest-priority verification commands:

## System Map
### Architecture
- Apps/services:
- Shared libraries:
- External dependencies:
- Highest-risk boundaries:

### Review Coverage
- Deeply reviewed packages:
- Lightly reviewed packages:
- Not inspected yet:
- Risk hotspots:
- Safest likely fix candidates:

### Data Flow
- Ingress:
- Validation:
- Core business logic:
- Persistence and side effects:
- Egress:

### Build System
- Workspace manager and task runner:
- Root scripts:
- Package build/typecheck flow:
- TypeScript config relationships:
- CI entrypoints:

### Test Infrastructure
- Test frameworks:
- Test locations:
- Unit vs integration boundaries:
- Smallest useful verification commands:

## Findings Summary
Use category-specific IDs:
- `API-#` for API contract findings
- `DB-#` for database findings
- `REL-#` for reliability findings
- `SEC-#` for security findings
- `PERF-#` for performance findings
- `TOOL-#` for tooling findings
- `TEST-#` for test coverage recommendations

Every finding must include a severity. Use one of: `critical`, `high`, `medium`, `low`.
Every non-`TEST-#` finding must include a confidence. Use one of: `high`, `medium`, `low`.
Order findings by severity descending within each category.
The `Fix now?` column must match the finding's `Decision` field.
Severity rubric:
- `critical`: broad production breakage, hard-stop delivery risk, or directly exploitable behavior with severe impact
- `high`: likely production issue or exploitable defect with meaningful blast radius
- `medium`: real defect or risk with bounded blast radius or preconditions
- `low`: worthwhile but lower-impact issue, weak trigger, or narrow edge case
Confidence rubric:
- `high`: directly supported by code/config and a concrete trigger or verification path
- `medium`: strongly suggested by code/config with one assumption that should be called out
- `low`: plausible but incomplete evidence; prefer omitting unless it materially affects triage
For deferred non-`TEST-#` findings, use `Why not now` values like `broad blast radius`, `unclear reproduction`, `needs environment access`, `cross-service change`, `insufficient time`, or `other: ...`.

| ID | Category | Severity | Confidence | Short title | Fix now? | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| API-1 | API Contracts |  |  |  |  |  |
| DB-1 | Database |  |  |  |  |  |

## Detailed Findings
Each audit command should update only its assigned subsection below and the summary rows for findings it adds or changes.
Every detailed finding must include the same severity shown in `Findings Summary`.
Deferred non-`TEST-#` findings must include a concise `Why not now`.
Do not use tables in this section.

### API Contracts
#### API-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Affected behavior or contract:
- Failure mode or exploit scenario:
- Root cause:
- Minimal safe fix:
- Behavior to preserve:
- Backward-compatibility or migration notes:
- Regression test idea:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Reliability
#### REL-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Failure mode:
- Trigger conditions:
- Root cause:
- Minimal safe fix:
- Behavior to preserve:
- Regression test idea:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Database
#### DB-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Affected schema, query, or data path:
- Failure mode or integrity/performance risk:
- Root cause:
- Minimal safe fix:
- Behavior to preserve:
- Regression test idea:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Security
#### SEC-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Exploit scenario:
- Root cause:
- Minimal safe fix:
- Behavior to preserve:
- Backward-compatibility or migration notes:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Performance
#### PERF-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Why this is on a hot or scalable path:
- Expected impact:
- Root cause:
- Minimal safe fix:
- Behavior to preserve:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Tooling
#### TOOL-1. { Short title }
- Severity:
- Confidence:
- Files and lines:
- Evidence checked:
- Affected package, script, or CI job:
- Failure or workflow risk:
- Root cause:
- Minimal safe fix:
- Verification:
- Related finding IDs or overlaps:
- Decision: `fix now` | `defer`
- Why not now: `n/a` for `fix now`; otherwise a short reason

### Test Coverage Recommendations
#### TEST-1. { Short title }
- Severity:
- Finding or issue ID (`TEST-#`):
- Missing regression test:
- Why it matters:
- Exact code path protected:
- Lightest-weight way to add it:
- Verification gap:

## Fix Plan
### Selected Fixes
Populate this section only from non-`TEST-#` findings whose `Decision` is `fix now`.
#### API-1
- Why this ranks well for the assessment:
- Expected fix size:
- Narrowest files to change:
- Existing tests to anchor on:
- Lightest new or updated regression test:
- Smallest validation commands:
- Behavior to preserve:
- Commit message:

### Test Coverage Support
- Link each selected fix to the regression test recommendation that protects it.

## Issue Execution Loop
For each selected issue:
1. Restate the bug or risk and the behavior that must stay the same.
2. Find the narrowest code path and the nearest existing tests.
3. Add or update the lightest regression test that proves the intended behavior.
4. Implement the minimal safe fix.
5. Run the smallest relevant checks first, then broader package or root checks only if needed.
6. Summarize the change in `Execution Log`.
7. Commit immediately with a concise message focused on intent.

## Execution Log
| Issue | Code change summary | Tests updated | Commands run | Result | Commit |
| --- | --- | --- | --- | --- | --- |
| API-1 |  |  |  |  |  |

## Deferred Findings
Populate this section only from non-`TEST-#` findings whose `Decision` is `defer`.
- `API-2`: `broad blast radius` - short note on why it should be reported now and fixed later

## Root Causes
1.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
