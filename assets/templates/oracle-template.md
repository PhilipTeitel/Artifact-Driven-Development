<!-- Oracle contract:
- Classify the legacy oracle tier before planning parity work.
- T3 documented-only cannot claim independent parity.
- If a section has no content yet, write `None yet.`.
-->

# Legacy Oracle

**Legacy repo:** `{path}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Oracle tier decision

| Tier | Selected? | Evidence | Consequence |
|------|-----------|----------|-------------|
| T1 executable | `{yes/no}` | `{grade + citation}` | Repeated legacy-vs-new comparison is possible. |
| T2 recorded | `{yes/no}` | `{grade + citation}` | Use frozen corpus; do not require live legacy execution in every run. |
| T3 documented-only | `{yes/no}` | `{grade + citation}` | Parity is unprovable; require user acceptance data. |

## 2. Legacy execution environment

| Requirement | Value | Evidence | Notes |
|-------------|-------|----------|-------|
| OS / image | `{value}` | `{grade + citation}` | `{notes}` |
| Runtime / compiler | `{value}` | `{grade + citation}` | `{notes}` |
| Network | `{none/limited/required}` | `{grade + citation}` | `{notes}` |
| Data set | `{fixture/source}` | `{grade + citation}` | `{sanitization}` |
| Secrets | `{none/required/TBD}` | `{grade + citation}` | `{handling}` |

## 3. Containment and security

| Risk | Isolation control | Evidence | Owner |
|------|-------------------|----------|-------|
| `{vulnerable dependency / unsafe input / old runtime}` | `{networkless container/VM/sandbox}` | `{grade + citation}` | `{owner}` |

## 4. Invocation contract

| Behavior | Legacy command / interaction | Inputs | Outputs | Exit / error behavior |
|----------|------------------------------|--------|---------|-----------------------|
| `{BEH-NNN}` | `{command/API/manual steps}` | `{fixture}` | `{output path/value}` | `{expected}` |

## 5. Fixture corpus

| Fixture ID | Behavior | Inputs | Expected legacy output | Evidence grade | Determinism notes |
|------------|----------|--------|------------------------|----------------|-------------------|
| FIX-NNN | `{BEH-NNN}` | `{path/data}` | `{path/value}` | `{E1/E2/E3}` | `{notes}` |

## 6. Tolerances and normalization

| Output kind | Rule | Applies to | Rationale | ADR / decision |
|-------------|------|------------|-----------|----------------|
| Numeric | `{absolute/relative tolerance}` | `{BEH/FIX}` | `{reason}` | `{ADR-NNN/TBD}` |
| Text | `{trim/line endings/case/order}` | `{BEH/FIX}` | `{reason}` | `{ADR-NNN/TBD}` |
| Time / random | `{seed/freeze/window}` | `{BEH/FIX}` | `{reason}` | `{ADR-NNN/TBD}` |

## 7. Determinism hazards

| Hazard | Affected behavior | Control | Evidence |
|--------|-------------------|---------|----------|
| `{timestamp/RNG/locale/order/uninitialized memory}` | `{BEH-NNN}` | `{control}` | `{grade + citation}` |

## 8. Open oracle questions

- [ ] `{question}`

## 9. Links

- Behavior catalog: `{behaviorGlob}`
- Defect ledger: `{defectLedgerDoc}`
- Parity reports: `{parityReportPattern}`

*Created: {YYYY-MM-DD}*
