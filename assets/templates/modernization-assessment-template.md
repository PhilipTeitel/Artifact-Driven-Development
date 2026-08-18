<!-- Modernization assessment contract:
- Preserve headings and order.
- Use configured evidence grades for all facts.
- Use configured assessment statuses only: go, go-with-conditions, no-go.
- If a section has no content yet, write `None yet.`.
-->

# Modernization Assessment

**Legacy repo:** `{path or repository URL}`
**Source stack:** `{language} {version} / {framework}`
**Target stack:** `{language} {version} / {framework}`
**Date:** `{YYYY-MM-DD}`
**Verdict:** `{go | go-with-conditions | no-go}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`

---

## 1. Executive summary

{One-page summary of feasibility, confidence, highest blockers, and required conditions.}

## 2. Evidence consumed

| Source | Type | Coverage | Evidence grade | Notes |
|--------|------|----------|----------------|-------|
| `{path}` | `{docs/code/release-notes/history/run output}` | `{scope}` | `{E1/E2/E3/E4/E5}` | `{notes}` |

## 3. Feasibility verdict

| Dimension | Result | Evidence | Decision / condition |
|-----------|--------|----------|----------------------|
| Setup and runnability | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Documentation adequacy | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Dependency viability | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Translation gap | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Oracle and parity | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Security containment | `{pass/conditional/fail}` | `{citation}` | `{condition}` |
| Planning confidence | `{pass/conditional/fail}` | `{citation}` | `{condition}` |

## 4. Risk register

| ID | Risk | Likelihood | Impact | Evidence | Mitigation | Owner | Condition to lower/retire |
|----|------|------------|--------|----------|------------|-------|---------------------------|
| RISK-NNN | `{risk}` | `{low/medium/high}` | `{low/medium/high}` | `{grade + citation}` | `{mitigation}` | `{owner}` | `{condition}` |

## 5. Obstacles and blockers

| Obstacle | Severity | Evidence | Affected phase | Required decision |
|----------|----------|----------|----------------|-------------------|
| `{obsolete dependency / unstructured code / security isolation / missing docs}` | `{critical/high/medium/low}` | `{grade + citation}` | `{assessment/recovery/design/implementation/UAT}` | `{decision}` |

## 6. Walking-skeleton feasibility

**Result:** `{normal skeleton viable | black-box first slice required | no executable slice yet}`

- **Evidence:**
- **Smallest useful executable path:**
- **If black-box first slice is required, why:**
- **Conditions to revisit skeleton planning:**

## 7. Oracle classification

| Tier | Selected? | Evidence | Consequence |
|------|-----------|----------|-------------|
| T1 executable | `{yes/no}` | `{citation}` | Legacy-vs-new parity can run repeatedly. |
| T2 recorded | `{yes/no}` | `{citation}` | Use frozen fixture corpus; cannot assume repeated legacy execution. |
| T3 documented-only | `{yes/no}` | `{citation}` | Parity is not independently provable; require user acceptance data. |

## 8. Conditions to proceed

- [ ] `{condition}`

## 9. Tensions / conflicts

| Conflict | Sources | Impact | Required resolution |
|----------|---------|--------|---------------------|
| `{docs vs code vs run output}` | `{citations}` | `{impact}` | `{question/decision}` |

## 10. Links

- Legacy map: `{legacyMapDoc}`
- Intent ledger: `{intentLedgerDoc}`
- Dependency ledger: `{dependencyLedgerDoc}`
- Translation gaps: `{translationGapDoc}`
- Oracle: `{oracleDoc}`
- Defect ledger: `{defectLedgerDoc}`

*Created: {YYYY-MM-DD} | Source stack: {sourceStack} | Target stack: {targetStack}*
