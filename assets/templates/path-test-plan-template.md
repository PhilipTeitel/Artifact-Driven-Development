<!-- Path test plan contract:
- Per execution path. This is the source for port-story Phase P and 8b Parity Plan.
- Comparison rules are decided here. Do not defer to a global numeric default.
- If no fixture exists, do not invent a parity criterion. Say how the path will be verified instead.
- One evidence grade per oracle/source row.
- Omit unused scenario groups. Do not write N/A rows.
- QA verifies via /verify-parity; QA does not edit this file.
-->

# Test Plan: XP-NNN {Path title}

**Execution path:** `{XP-NNN}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Architect (`/plan-path-tests`)

## Summary

{One paragraph: how this path will be shown correct, which comparison rule applies, and whether a fixture already exists. If it does not, say so — do not assign a parity criterion that cannot be run.}

---

## 1. Oracle strategy

| Question | Answer |
|----------|--------|
| How is correctness verified for this path? | `{legacy executable / recorded fixture / documented expectation / user acceptance data}` |
| Fixture / data | `{FIX-NNN path, or none}` |
| Linked scenarios | `{S1, S2, … or none yet}` |

Do not claim a stronger oracle than `docs/modernization/oracle.md`.

## 2. Comparison rules

| Output kind | Rule | Bound / notes | Decision |
|-------------|------|---------------|----------|
| `{numeric / text / order / semantic / exact}` | `{exact \| tolerance-based \| semantic}` | `{e.g. ulp, abs, rel, trim, or "documented meaning"}` | `{DEC-NNN or this plan}` |

There is no project-wide numeric tolerance gate. If a rule is missing, this path is not implementation-ready.

## 3. Happy path

| ID | Input | Expected output | Source | Evidence |
|----|-------|-----------------|--------|----------|
| H1 | `{input}` | `{output}` | `{FIX-NNN / doc / code}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` |

## 4. Edge cases

| ID | Case | Expected legacy behavior | Source | Evidence |
|----|------|--------------------------|--------|----------|
| E1 | `{case from the path detail}` | `{behavior}` | `{FIX-NNN / detail §6}` | `{grade}` `{citation}` |

Take cases from the path detail. Do not invent new legacy behavior.

<!-- INCLUDE WHEN the path has observable failure modes. OMIT ENTIRELY otherwise. -->

## 5. Error and failure scenarios

| ID | Failure | Expected legacy behavior | Source | Evidence |
|----|---------|--------------------------|--------|----------|
| F1 | `{bad input / missing dep / overflow}` | `{behavior}` | `{citation}` | `{grade}` `{citation}` |

## 6. Defects that bind this plan

| DEF ID | Decision | Effect on expected output |
|--------|----------|---------------------------|
| DEF-NNN | `{reproduce-faithfully \| fix-now \| fix-later}` | `{what the test asserts}` |

Write `None.` when no defect binds this path.

## 7. Open test-planning questions

- [ ] `{question that prevents writing Phase P}`

## Links

- Path detail: `{pathDetailDoc}`
- Oracle: `{oracleDoc}`
- Defect ledger: `{defectLedgerDoc}`
- Port story: `{storyDoc or TBD}`
