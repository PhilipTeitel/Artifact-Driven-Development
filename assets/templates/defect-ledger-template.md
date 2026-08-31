<!-- Defect ledger contract:
- Every DEF-NNN names one or more XP-NNN IDs. Refuse a system-wide question that the methodology says has no system-wide answer.
- Valid decisions: reproduce-faithfully, fix-now, fix-later. Open means the human has not decided yet (M3).
- Owner policy that is not a path mismatch belongs in the decision register (DEC-NNN), not here.
- Current state lives in the Decision cell. No prose changelog.
- Open defects bind only the paths they name. They do not gate other slices.
-->

# Defect Ledger

**Legacy repo:** `{path}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Archaeologist (`/ledger-defects`); human decides

## Summary

{One paragraph: how many defects are open, which ones bind the next slice, and whether any proposed defect was rejected as mis-posed. Point at XP IDs, not at global policy questions.}

---

## 1. Defect decisions

| ID | Defect / mismatch | Affected XP | Evidence | Decision | UAT impact | Story / DEC |
|----|-------------------|-------------|----------|----------|------------|-------------|
| DEF-NNN | `{description of THIS path's behavior}` | `{XP-NNN}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` | `{open \| reproduce-faithfully \| fix-now \| fix-later}` | `{impact}` | `{STORY-ID / DEC-NNN / TBD}` |

If a requested defect is "what is the global numeric tolerance?", do not file it. Record `DEC-NNN` that comparison is per path, and put the bound on that path's REQ (section 4b / Constraints).

## 2. Reproduce faithfully

| DEF ID | Expected port behavior | Parity fixture | Rationale |
|--------|------------------------|----------------|-----------|
| DEF-NNN | `{bug-compatible output}` | `{FIX-NNN}` | `{why UAT requires this}` |

Write `None.` when no row uses this decision.

## 3. Fix now

| DEF ID | Corrected expectation | Acceptance criterion | Approval source |
|--------|-----------------------|----------------------|-----------------|
| DEF-NNN | `{new expected behavior}` | `{AC ID/TBD}` | `{user/date/source}` |

Write `None.` when no row uses this decision.

## 4. Fix later

| DEF ID | Deferred backlog item | Why deferred | Guardrail |
|--------|-----------------------|--------------|-----------|
| DEF-NNN | `{story/backlog ref}` | `{reason}` | `{test/docs note}` |

Write `None.` when no row uses this decision.

## 5. Open defect decisions

- [ ] `{DEF-NNN} — binds {XP-NNN}`

## Links

- Path details: `{pathGlob}`
- Decision register: `{decisionRegisterDoc}`
- Oracle: `{oracleDoc}`
- Migration plan: `{migrationPlanDoc}`
