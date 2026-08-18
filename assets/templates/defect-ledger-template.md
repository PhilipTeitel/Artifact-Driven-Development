<!-- Defect ledger contract:
- Every known or suspected legacy defect needs a decision before affected parity criteria can pass.
- Valid decisions: reproduce-faithfully, fix-now, fix-later.
- If a section has no content yet, write `None yet.`.
-->

# Defect Ledger

**Legacy repo:** `{path}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Defect decisions

| ID | Defect / mismatch | Affected behavior | Evidence | Decision | UAT impact | Backlog / story |
|----|-------------------|-------------------|----------|----------|------------|-----------------|
| DEF-NNN | `{description}` | `{BEH-NNN/Sn}` | `{grade + citation}` | `{reproduce-faithfully/fix-now/fix-later}` | `{impact}` | `{STORY-ID/TBD}` |

## 2. Reproduce faithfully

| DEF ID | Expected port behavior | Parity fixture | Rationale |
|--------|------------------------|----------------|-----------|
| DEF-NNN | `{bug-compatible output}` | `{FIX-NNN}` | `{why UAT requires this}` |

## 3. Fix now

| DEF ID | Corrected expectation | Acceptance criterion | Approval source |
|--------|-----------------------|----------------------|-----------------|
| DEF-NNN | `{new expected behavior}` | `{AC ID/TBD}` | `{user/date/source}` |

## 4. Fix later

| DEF ID | Deferred backlog item | Why deferred | Guardrail |
|--------|-----------------------|--------------|-----------|
| DEF-NNN | `{story/backlog ref}` | `{reason}` | `{test/docs note}` |

## 5. Open defect decisions

- [ ] `{DEF-NNN or behavior needing a decision}`

## 6. Links

- Behavior catalog: `{behaviorGlob}`
- Oracle: `{oracleDoc}`
- Migration plan: `{migrationPlanDoc}`

*Created: {YYYY-MM-DD}*
