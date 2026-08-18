<!-- Translation gap contract:
- Fill the seeded source-family matrix for the relevant legacy stack before adding project-specific gaps.
- Each GAP-NNN must include migration pattern and verification strategy.
- If a section has no content yet, write `None yet.`.
-->

# Translation Gap Analysis

**Source stack:** `{language} {version} / {framework}`
**Target stack:** `{language} {version} / {framework}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Gap summary

| Category | Highest risk | Blocking gaps | Notes |
|----------|--------------|---------------|-------|
| `{language/runtime/framework/data/build/ops}` | `{critical/high/medium/low}` | `{GAP-NNN}` | `{notes}` |

## 2. Gap register

| ID | Source construct / behavior | Target analogue | Risk | Migration pattern | Verification strategy | Blocks skeleton? | Evidence |
|----|-----------------------------|-----------------|------|-------------------|-----------------------|------------------|----------|
| GAP-NNN | `{construct}` | `{target analogue or none}` | `{critical/high/medium/low}` | `{preserve/wrap/rewrite/refactor}` | `{parity/unit/integration/manual}` | `{yes/no}` | `{grade + citation}` |

## 3. Seeded Fortran gaps

| Source construct | Target concern | Default risk | Verification note | Project GAP |
|------------------|----------------|--------------|-------------------|-------------|
| `COMMON` / global shared state | Lifetime, mutability, threading, module boundaries | high | Characterize stateful scenarios and initialization order | `{GAP-NNN/TBD}` |
| `EQUIVALENCE` / storage aliasing | Memory reinterpretation and hidden coupling | critical | Add golden fixtures around affected numeric/data paths | `{GAP-NNN/TBD}` |
| Implicit typing | Silent type assumptions | high | Compile warnings plus field-by-field parity data | `{GAP-NNN/TBD}` |
| Column-major arrays | Indexing and layout mismatch | high | Array-shape fixtures and boundary tests | `{GAP-NNN/TBD}` |
| `GOTO` / unstructured control flow | Flow recovery and test slicing | high | Trace flow before refactor; black-box first if needed | `{GAP-NNN/TBD}` |
| Fixed-form I/O | Formatting and width-sensitive output | high | Text fixture normalization and exact-format tests | `{GAP-NNN/TBD}` |
| `real*4` / `real*8` numeric semantics | Precision, rounding, overflow, BLAS/LAPACK behavior | critical | Numeric tolerance ADR and parity corpus | `{GAP-NNN/TBD}` |

## 4. Seeded C gaps

| Source construct | Target concern | Default risk | Verification note | Project GAP |
|------------------|----------------|--------------|-------------------|-------------|
| Pointer arithmetic | Bounds, aliasing, ownership | critical | Memory-shape fixtures and fuzz/regression tests | `{GAP-NNN/TBD}` |
| Unions / casts | Reinterpretation and serialization compatibility | high | Binary fixture round-trip tests | `{GAP-NNN/TBD}` |
| Manual memory management | Lifetime and error paths | high | Leak/error-path characterization where possible | `{GAP-NNN/TBD}` |
| `#ifdef` build variants | Hidden product variants | high | Inventory compiled variants before planning | `{GAP-NNN/TBD}` |
| Undefined-behavior reliance | Non-portable observed behavior | critical | Decide reproduce vs fix; record defect decisions | `{GAP-NNN/TBD}` |
| Native libraries | ABI and platform coupling | high | Wrapper or replacement integration tests | `{GAP-NNN/TBD}` |

## 5. Seeded legacy Java gaps

| Source construct | Target concern | Default risk | Verification note | Project GAP |
|------------------|----------------|--------------|-------------------|-------------|
| EJB 2.x / container services | Transactions, security, lifecycle | high | Contract tests around service boundaries | `{GAP-NNN/TBD}` |
| Struts/JSP action lifecycle | Request binding, validation, view state | high | UI/API parity scenarios for form flows | `{GAP-NNN/TBD}` |
| Container-managed transactions | Transaction scope mismatch | high | Integration tests for commit/rollback behavior | `{GAP-NNN/TBD}` |
| Raw collections / `Vector` | Type assumptions and synchronization | medium | Characterization tests around collection semantics | `{GAP-NNN/TBD}` |
| App-server config | Naming, pooling, JNDI, deployment descriptors | high | Environment parity checklist | `{GAP-NNN/TBD}` |

## 6. Seeded .NET Framework gaps

| Source construct | Target concern | Default risk | Verification note | Project GAP |
|------------------|----------------|--------------|-------------------|-------------|
| AppDomains | Isolation and plugin lifecycle | high | Process-boundary ADR and lifecycle tests | `{GAP-NNN/TBD}` |
| .NET Remoting | Transport, serialization, object lifetime | critical | Replace with explicit API/event contract and parity tests | `{GAP-NNN/TBD}` |
| WCF | Binding semantics, duplex callbacks, auth | high | Contract tests against selected target transport | `{GAP-NNN/TBD}` |
| WebForms | ViewState, postback lifecycle, server controls | high | UI scenario parity and state transition tests | `{GAP-NNN/TBD}` |
| GAC / machine.config | Deployment and dependency resolution | medium | Build/deploy reproducibility checks | `{GAP-NNN/TBD}` |
| `ConfigurationManager` | Config source and reload behavior | medium | Config fixture and environment tests | `{GAP-NNN/TBD}` |
| Culture-dependent parsing | Locale, numeric/date formatting | high | Locale fixture corpus and explicit culture policy | `{GAP-NNN/TBD}` |

## 7. Target-stack notes

| Target feature | Helps with | Risk introduced | ADR / story |
|----------------|------------|-----------------|-------------|
| `{framework feature}` | `{gap}` | `{risk}` | `{ADR-NNN/STORY-ID/TBD}` |

## 8. Open translation questions

- [ ] `{question}`

## 9. Links

- Dependency ledger: `{dependencyLedgerDoc}`
- Migration plan: `{migrationPlanDoc}`
- ADRs: `{decisionsDir}`

*Created: {YYYY-MM-DD}*
