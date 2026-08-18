<!-- Migration plan contract:
- The accepted assessment, oracle tier, translation gaps, and defect ledger are binding inputs.
- Forecast confidence must be recalibrated after the first completed slice.
- If a section has no content yet, write `None yet.`.
-->

# Migration Plan

**Legacy repo:** `{path}`
**Source stack:** `{sourceStack}`
**Target stack:** `{targetStack}`
**Strategy:** `{strangler | phased-rewrite | big-bang-parallel-run}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Strategy decision

| Strategy | Selected? | Why / why not | Evidence | ADR |
|----------|-----------|---------------|----------|-----|
| strangler | `{yes/no}` | `{reason}` | `{grade + citation}` | `{ADR-NNN/TBD}` |
| phased-rewrite | `{yes/no}` | `{reason}` | `{grade + citation}` | `{ADR-NNN/TBD}` |
| big-bang-parallel-run | `{yes/no}` | `{reason}` | `{grade + citation}` | `{ADR-NNN/TBD}` |

## 2. Binding assumptions

| Assumption | Source | Risk if wrong | Validation |
|------------|--------|---------------|------------|
| `{assumption}` | `{assessment/ADR/REQ/BEH}` | `{risk}` | `{proof}` |

## 3. Slice plan

| Slice | Objective | Covered BEH / Sn | Dependencies | Structure fidelity | Oracle evidence | Exit criteria | Forecast |
|-------|-----------|------------------|--------------|--------------------|-----------------|---------------|----------|
| `{STORY-ID}` | `{objective}` | `{BEH-NNN / S1}` | `{deps}` | `{preserve-then-refactor/refactor-now}` | `{FIX-NNN/T3 acceptance data}` | `{criteria}` | `{size/confidence}` |

## 4. Architecture and ADR implications

| Decision | ADR | Status | Affected slices | Notes |
|----------|-----|--------|-----------------|-------|
| `{target stack / process boundary / persistence / integration / cutover}` | `{ADR-NNN}` | `{Proposed/Accepted/TBD}` | `{STORY-ID}` | `{notes}` |

## 5. Cutover and coexistence

| Concern | Plan | Rollback | Evidence / owner |
|---------|------|----------|------------------|
| `{routing/data sync/batch window/manual fallback}` | `{plan}` | `{rollback}` | `{evidence/owner}` |

## 6. Data and parity strategy

| Data / behavior | Legacy source | New source | Comparison | Tolerance | Defect policy |
|-----------------|---------------|------------|------------|-----------|---------------|
| `{BEH/data}` | `{source}` | `{source}` | `{method}` | `{rule}` | `{DEF-NNN/none}` |

## 7. Forecast and recalibration

| Milestone | Initial estimate | Confidence | Evidence | Recalibration trigger |
|-----------|------------------|------------|----------|-----------------------|
| `{milestone}` | `{estimate}` | `{low/medium/high}` | `{basis}` | `{first completed slice / parity defect rate}` |

## 8. Deferred modernization debt

| Debt item | Why preserved initially | Refactor trigger | Backlog item |
|-----------|-------------------------|------------------|--------------|
| `{legacy structure}` | `{reason}` | `{trigger}` | `{story/TBD}` |

## 9. Open decisions

- [ ] `{decision}`

## 10. Links

- Assessment: `{assessmentDoc}`
- Translation gaps: `{translationGapDoc}`
- Defect ledger: `{defectLedgerDoc}`
- Oracle: `{oracleDoc}`
- Design doc: `{designDoc}`

*Created: {YYYY-MM-DD}*
