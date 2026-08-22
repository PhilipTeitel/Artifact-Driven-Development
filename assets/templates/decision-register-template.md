<!-- Decision register contract:
- The only place porting decisions live: port / retire / rewrite, dependency substitution, comparison policy, scope.
- Human decides; Migration Strategist records via /record-decision.
- Current state lives in the Answer and Status cells. Do not add a prose history above the table.
- Do not copy these answers into analysis snapshots. Cite DEC-NNN from plans and stories.
- Defect reproduce/fix-now/fix-later stays in the defect ledger (M3). Cite DEF-NNN from here when a porting decision depends on it.
- Binding target-stack design still gets an ADR. Cite ADR-NNN in Affects / notes.
-->

# Decision Register

**Date:** `{YYYY-MM-DD}`
**Owner:** Migration Strategist (`/record-decision`); human decides

## Summary

{One paragraph: how many decisions are open, which ones bind the next slice, and where that slice's prerequisite table lives. Do not retell the inventories.}

---

## 1. Decisions

| ID | Question | Answer | Status | Evidence | Date | Affects |
|----|----------|--------|--------|----------|------|---------|
| DEC-NNN | `{what must be chosen}` | `{the choice, or TBD}` | `{open \| decided}` | `{grade or source}` `{citation}` | `{YYYY-MM-DD}` | `{XP-NNN, DEP-NNN, IMP-NNN, DEF-NNN, slice ID}` |

Status `open` means an owner decision has not been made. That is not `no-route`.

## 2. Open decisions that bind a slice

| DEC ID | Slice / story | What "resolved" means |
|--------|---------------|------------------------|
| DEC-NNN | `{slice or STORY-ID}` | `{the answer that unblocks implementation}` |

Write `None.` when the next slice has no open DEC prerequisites.

## Links

- Migration plan: `{migrationPlanDoc}`
- Defect ledger: `{defectLedgerDoc}`
- ADRs: `{decisionsDir}`
