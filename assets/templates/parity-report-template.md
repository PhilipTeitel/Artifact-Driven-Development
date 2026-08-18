PARITY SUMMARY: result={Pass|Block} PAR-critical={N} PAR-high={N} PROV-critical={N} PROV-high={N} mismatches={N} blocked={N} oracleTier={T1|T2|T3}

<!-- Parity report contract:
- First non-comment line must be PARITY SUMMARY.
- One row per Phase P criterion and covered BEH-NNN.
- Do not claim parity above the configured oracle tier.
-->

# Parity Report: {STORY-ID} — {Story Title}

**Date:** `{YYYY-MM-DD}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Result:** `{Pass | Block}`

---

## 1. Scope

| Story criterion | Behavior | Oracle source | New-system command / test |
|-----------------|----------|---------------|---------------------------|
| P1 | `{BEH-NNN}` | `{FIX-NNN / acceptance data}` | `{test or command}` |

## 2. Results matrix

| BEH | AC | Fixture / data | Tolerance | Legacy result | New result | Result | Defect decision |
|-----|----|----------------|-----------|---------------|------------|--------|-----------------|
| BEH-NNN | P1 | `{FIX-NNN}` | `{rule}` | `{value/path}` | `{value/path}` | `{match/within-tolerance/mismatch/blocked}` | `{DEF-NNN/none}` |

## 3. Mismatches

| ID | BEH | Description | Severity | Reconciled? | Required action |
|----|-----|-------------|----------|-------------|-----------------|
| PAR-NNN | `{BEH-NNN}` | `{mismatch}` | `{critical/high/medium/low}` | `{yes/no + DEF-NNN}` | `{action}` |

## 4. Provenance gaps

| ID | BEH / artifact | Gap | Severity | Required decision |
|----|----------------|-----|----------|-------------------|
| PROV-NNN | `{BEH-NNN}` | `{missing grade/citation or E4/E5}` | `{critical/high/medium/low}` | `{decision}` |

## 5. Commands and evidence

| Command / inspection | Result | Evidence excerpt |
|----------------------|--------|------------------|
| `{command}` | `{pass/fail/blocked}` | `{excerpt}` |

## 6. Notes

{Residual risk, oracle limitations, and UAT implications.}

*Created: {YYYY-MM-DD}*
