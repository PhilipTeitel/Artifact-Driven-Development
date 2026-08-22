PARITY SUMMARY: result={Pass|Block} PAR-critical={N} PAR-high={N} PROV-critical={N} PROV-high={N} mismatches={N} blocked={N} oracleTier={T1|T2|T3}

<!-- Parity report contract:
- First non-comment line must be PARITY SUMMARY.
- One row per Phase P criterion and covered XP-NNN.
- Comparison rules come from the path test plan. Do not apply a global numeric default when a path rule is missing; mark BLOCKED.
- Do not claim parity above the configured oracle tier.
-->

# Parity Report: {STORY-ID} — {Story Title}

**Date:** `{YYYY-MM-DD}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Result:** `{Pass | Block}`
**Execution paths:** `{XP-NNN, …}`

## Summary

{One paragraph: whether this story's paths matched the accepted expectation, under which comparison rules, and any DEF-NNN reconciliation. Do not retell other slices.}

---

## 1. Scope

| Story criterion | Path | Oracle source | Comparison rule | New-system command / test |
|-----------------|------|---------------|-----------------|---------------------------|
| P1 | `{XP-NNN}` | `{FIX-NNN / acceptance data}` | `{from path test plan}` | `{test or command}` |

## 2. Results matrix

| XP | AC | Fixture / data | Comparison | Legacy result | New result | Result | Defect decision |
|----|----|----------------|------------|---------------|------------|--------|-----------------|
| XP-NNN | P1 | `{FIX-NNN}` | `{rule}` | `{value/path}` | `{value/path}` | `{match/within-tolerance/mismatch/blocked}` | `{DEF-NNN/none}` |

## 3. Mismatches

| ID | XP | Description | Severity | Reconciled? | Required action |
|----|----|-------------|----------|-------------|-----------------|
| PAR-NNN | `{XP-NNN}` | `{mismatch}` | `{critical/high/medium/low}` | `{yes/no + DEF-NNN}` | `{action}` |

Write `None.` when there are no mismatches.

## 4. Provenance gaps

| ID | XP / artifact | Gap | Severity | Required decision |
|----|---------------|-----|----------|-------------------|
| PROV-NNN | `{XP-NNN}` | `{missing grade/citation or E4/E5}` | `{critical/high/medium/low}` | `{DEC-NNN / user}` |

Write `None.` when there are no provenance gaps.

## 5. Commands and evidence

| Command / inspection | Result | Evidence excerpt |
|----------------------|--------|------------------|
| `{command}` | `{pass/fail/blocked}` | `{excerpt}` |

*Created: {YYYY-MM-DD}*
