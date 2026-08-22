<!-- Modernization assessment contract:
- This is the five-minute document. A reader should understand scope and risk without opening the inventories.
- Preserve headings and order. Omit a section only when the INCLUDE WHEN comment says to.
- Verdict uses configured statuses only: go, go-with-conditions, no-go.
- Conditions and blockers name the first slice, not global unresolved counts.
- Cite PATH / DEP / IMP / RISK / DEC IDs. Do not restate their tables.
- One evidence grade per claim.
- Current state lives in cells. No prose changelog.
-->

# Modernization Assessment

**Legacy repo:** `{path or repository URL}`
**Source stack:** `{language} {version} / {framework}`
**Target stack:** `{language} {version} / {framework}`
**Date:** `{YYYY-MM-DD}`
**Verdict:** `{go | go-with-conditions | no-go}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Owner:** Migration Strategist (`/assess-modernization`)

## Summary

{One paragraph: what the legacy system is, whether the port is feasible, oracle tier, the candidate first slice (`XP-NNN` IDs), and the conditions that bind *that* slice. End with where to look next (usually the migration plan or a DEC ID).}

---

## 1. Scope snapshot

| Item | Count / value | Where the detail lives |
|------|---------------|------------------------|
| Active execution paths | `{N}` | Path inventory |
| Suspected-dead / unknown / retired | `{N}` | Path inventory appendix |
| Dependencies | `{N}` (`no-route` `{N}`, `undecided` `{N}`) | Dependency inventory |
| Highest-severity impedance | `{IMP-NNN or none}` | Impedance analysis |
| Oracle tier | `{T1/T2/T3}` | Oracle strategy |
| Candidate first slice | `{XP-NNN, …}` | Will be the first migration-plan row |

## 2. Feasibility verdict

| Dimension | Result | Condition if not pass |
|-----------|--------|------------------------|
| Setup and runnability | `{pass/conditional/fail}` | `{condition or none}` |
| Path inventory completeness | `{pass/conditional/fail}` | `{condition or none}` |
| First-slice dependency routes | `{pass/conditional/fail}` | `{DEP-NNN / DEC-NNN that bind the first slice}` |
| Impedance for first slice | `{pass/conditional/fail}` | `{IMP-NNN}` |
| Oracle and parity | `{pass/conditional/fail}` | `{tier consequence}` |
| Security containment | `{pass/conditional/fail}` | `{condition or none}` |

Do not fail a dimension because *other* paths have unresolved dependencies.

## 3. Risk register

| ID | Risk | Likelihood | Impact | Evidence | Mitigation | Owner | Retire when |
|----|------|------------|--------|----------|------------|-------|-------------|
| RISK-NNN | `{risk}` | `{low/medium/high}` | `{low/medium/high}` | `{grade}` `{citation}` | `{mitigation}` | `{owner}` | `{condition}` |

Keep only risks that affect the verdict or the first slice. Later-slice risks belong in that slice's prerequisite table.

## 4. Conditions to start the first slice

- [ ] `{condition, citing DEP-NNN / DEC-NNN / RISK-NNN}`

Global unresolved items that do not bind the first slice are not listed here.

## 5. Walking-skeleton feasibility

**Result:** `{normal skeleton viable | black-box first slice required | no executable slice yet}`

- **Smallest useful executable path:** `{XP-NNN}`
- **Why this result:** `{one to three sentences}`
- **Revisit when:** `{condition}`

## 6. Tensions

Cite the canonical row. Do not restate the conflict.

| Canonical ID | Kind | Required resolution |
|--------------|------|---------------------|
| `{XP-NNN / DEP-NNN / IMP-NNN / DEF-NNN}` | `{docs vs code / owner decision / no-route}` | `{question}` |

Write `None.` when the assessment introduces no new tension.

## Links

- Path inventory: `{pathInventoryDoc}`
- Dependency inventory: `{dependencyInventoryDoc}`
- Dependency graph: `{dependencyGraphDoc}`
- Impedance analysis: `{impedanceDoc}`
- Oracle: `{oracleDoc}`
- Decision register: `{decisionRegisterDoc}`
