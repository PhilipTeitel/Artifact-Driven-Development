<!-- Behavior catalog contract:
- One BEH-NNN artifact per user-visible behavior or black-box slice.
- Every fact needs an evidence grade and citation.
- Draft Gherkin becomes input to /refine-feature.
-->

# BEH-NNN: {Behavior title}

**Status:** Draft | Ready for Requirements | Superseded
**Evidence grade:** `{E1 verified | E2 documented | E3 code-derived | E4 inferred | E5 unknown}`
**Legacy surfaces:** `{screens/commands/jobs/APIs/files}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Summary

{What the user can observe. Do not describe implementation unless it is the observable contract.}

## 2. Actors and triggers

| Actor / system | Trigger | Preconditions | Evidence |
|----------------|---------|---------------|----------|
| `{actor}` | `{action}` | `{state/data}` | `{grade + citation}` |

## 3. Inputs

| Input | Type / format | Units | Range / constraints | Required? | Evidence |
|-------|---------------|-------|----------------------|-----------|----------|
| `{input}` | `{type}` | `{units}` | `{constraints}` | `{yes/no}` | `{grade + citation}` |

## 4. Outputs and side effects

| Output / side effect | Type / format | Precision / ordering | Destination | Evidence |
|----------------------|---------------|----------------------|-------------|----------|
| `{output}` | `{type}` | `{precision}` | `{screen/file/db/API}` | `{grade + citation}` |

## 5. Rules and invariants

| Rule | Evidence | Open question? |
|------|----------|----------------|
| `{rule}` | `{grade + citation}` | `{yes/no}` |

## 6. Error handling and edge cases

| Case | Legacy behavior | Evidence | Defect decision |
|------|-----------------|----------|-----------------|
| `{case}` | `{behavior}` | `{grade + citation}` | `{DEF-NNN/none/TBD}` |

## 7. Draft Gherkin

```gherkin
Given {precondition}
And   {additional context, if needed}
When  {action the persona takes}
Then  {observable outcome the user can verify}
And   {additional outcome, if needed}
```

## 8. Legacy code and documentation citations

| Source | Lines / section | Claim supported | Evidence grade |
|--------|-----------------|-----------------|----------------|
| `{path}` | `{lines/section}` | `{claim}` | `{E1/E2/E3/E4/E5}` |

## 9. Oracle fixtures

| Fixture | Input | Expected output | Tolerance / normalization | Evidence |
|---------|-------|-----------------|---------------------------|----------|
| `{FIX-NNN}` | `{path/value}` | `{path/value}` | `{rule}` | `{grade + citation}` |

## 10. Open questions

- [ ] `{question}`

## 11. Links

- Intent ledger: `{intentLedgerDoc}`
- Legacy flow: `{flowsDir}`
- Defect ledger: `{defectLedgerDoc}`

*Created: {YYYY-MM-DD}*
