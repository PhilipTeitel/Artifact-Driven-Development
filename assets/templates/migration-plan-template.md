<!-- Migration plan contract:
- Staging, slice order, and per-slice prerequisites. Global inventories do not gate a slice.
- Each slice row names only the DEP-NNN, DEC-NNN, and DEF-NNN IDs that bind that slice.
- Check off resolved prerequisites in the slice row or the ADD story, not in analysis snapshots.
- Later slices may be inventory XP IDs until /trace-path has run for them.
- Forecast confidence must be recalibrated after the first completed slice.
- Current state lives in cells. No prose changelog.
- Recommend ADRs; do not take over Architect-owned ADR files.
-->

# Migration Plan

**Legacy repo:** `{path}`
**Source stack:** `{sourceStack}`
**Target stack:** `{targetStack}`
**Strategy:** `{strangler | phased-rewrite | big-bang-parallel-run}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Migration Strategist (`/plan-migration`)

## Summary

{One paragraph: chosen strategy, first slice and its prerequisites, oracle implication, and the next command (usually `/document-legacy` scoped to the first slice's XP IDs).}

---

## 1. Strategy decision

| Strategy | Selected? | Why / why not | ADR |
|----------|-----------|---------------|-----|
| strangler | `{yes/no}` | `{reason}` | `{ADR-NNN/TBD/none}` |
| phased-rewrite | `{yes/no}` | `{reason}` | `{ADR-NNN/TBD/none}` |
| big-bang-parallel-run | `{yes/no}` | `{reason}` | `{ADR-NNN/TBD/none}` |

## 2. Binding assumptions

| Assumption | Source | Risk if wrong | Validation |
|------------|--------|---------------|------------|
| `{assumption}` | `{DEC-NNN / ADR-NNN / ASSESSMENT}` | `{risk}` | `{proof}` |

## 3. Slice plan

Each slice follows recover → refine → (design when the accumulating REQ set warrants it) → plan → implement → QA. A slice may start when **its** prerequisites are resolved, even if other slices still have open `undecided` dependencies.

| Slice | Objective | XP IDs | Prerequisites | Structure fidelity | Oracle evidence | Exit criteria | Forecast |
|-------|-----------|--------|---------------|--------------------|-----------------|---------------|----------|
| `{STORY-ID or slice name}` | `{objective}` | `{XP-NNN}` | `{DEP-NNN / DEC-NNN / DEF-NNN + resolved/unresolved}` | `{preserve-then-refactor/refactor-now}` | `{FIX-NNN / T3 data / TBD until REQ 4b}` | `{criteria}` | `{size/confidence}` |

Prerequisites list only IDs that bind this slice. Do not paste global blocker counts.

## 4. Per-slice ADD loop

| Slice | Recover | Refine | Design | Implement | QA |
|-------|---------|--------|--------|-----------|-----|
| `{slice}` | `/trace-path` `{XP-NNN}` | `/refine-feature` → `REQ-NNN` | `{/design-application delta, or none if design already covers this REQ}` | `/plan-story` then `/complete-story` | Gate 8, including `parity` rows |

## 5. Recommended ADRs

| Decision | Suggested ADR | Status | Affected slices |
|----------|---------------|--------|-----------------|
| `{target stack / process boundary / persistence / integration / cutover}` | `{ADR-NNN or title}` | `{recommended / Proposed / Accepted}` | `{slice}` |

Architect writes or accepts ADR files. This table is a trigger list.

<!-- INCLUDE WHEN cutover, coexistence, or rollback is a real project concern.
     OMIT ENTIRELY for a library port with no live cutover. -->

## 6. Cutover and coexistence

| Concern | Plan | Rollback | Owner |
|---------|------|----------|-------|
| `{routing / data sync / batch window / manual fallback}` | `{plan}` | `{rollback}` | `{owner}` |

## 7. Forecast and recalibration

| Milestone | Initial estimate | Confidence | Recalibration trigger |
|-----------|------------------|------------|-----------------------|
| `{first slice / remaining inventory}` | `{estimate}` | `{low/medium/high}` | `{first completed slice / parity defect rate}` |

## 8. Deferred modernization debt

| Debt item | Why preserved initially | Refactor trigger | Backlog item |
|-----------|-------------------------|------------------|--------------|
| `{legacy structure}` | `{reason}` | `{trigger}` | `{story/TBD}` |

Write `None.` when the first slices do not preserve debt on purpose.

## Links

- Assessment: `{assessmentDoc}`
- Decision register: `{decisionRegisterDoc}`
- Dependency graph: `{dependencyGraphDoc}`
- Defect ledger: `{defectLedgerDoc}`
- Oracle: `{oracleDoc}`
