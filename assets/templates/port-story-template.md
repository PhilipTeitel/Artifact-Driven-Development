<!-- Port story contract:
- Based on the standard user-story template, with modernization-specific provenance and parity sections.
- Every covered BEH-NNN must have evidence grade, citation, oracle fixture or acceptance-data source, and Phase P coverage.
- Phase P is mandatory before Phase Y. Z8 is mandatory in Phase Z.
-->

# {STORY-ID}: {Story Title}

**Story**: {As a ... I want ... so that ...}
**Epic**: {Epic number} — {Epic name}
**Size**: {Small | Medium | Large}
**Status**: Open
**Modernization slice:** `{strangler | phased-rewrite | big-bang-parallel-run}`
**Structure fidelity:** `{preserve-then-refactor | refactor-now}`

---

## 1. Summary

{What legacy capability this story ports and why this slice is next.}

### 1a. Domain model touchpoints

| Purpose / domain section | Terms / entities / fields / invariants touched | Evidence |
|--------------------------|-----------------------------------------------|----------|
| `{docs/PURPOSE.md or docs/DOMAIN.md section}` | `{items}` | `{grade + citation}` |

### 1b. Legacy source touchpoints

| Legacy artifact | Role in story | Evidence grade | Citation | Notes |
|-----------------|---------------|----------------|----------|-------|
| `{legacy path/doc/release note}` | `{behavior/source/oracle/defect}` | `{E1/E2/E3/E4/E5}` | `{path:line or section}` | `{notes}` |

## 2. Linked architecture decisions (ADRs)

- `{decisionsDir}/ADR-NNN-slug.md` — `{decision}`

## 3. Definition of Ready (DoR)

- [ ] Purpose and domain touchpoints are current.
- [ ] Covered `BEH-NNN` artifacts have evidence grades and citations.
- [ ] No covered behavior is `E4 inferred` or `E5 unknown` unless a user decision is recorded below.
- [ ] Oracle tier and fixtures / acceptance data are documented.
- [ ] Defect-ledger decisions are recorded for known mismatches.
- [ ] Linked ADRs are `Accepted` or this story is explicitly a spike.

## 4. Binding constraints (non-negotiable)

- `{target stack, process boundary, persistence, dependency substitution, or parity tolerance constraint}`

## 4b. Ports & Adapters

| Port | Adapter | Boundary owned | Contract test | Integration test |
|------|---------|----------------|---------------|------------------|
| `{Port}` | `{Adapter}` | `{boundary}` | `{test}` | `{test}` |

## 5. API Endpoints + Schemas

| Endpoint / schema | Purpose | Request / input | Response / output | Covers |
|-------------------|---------|-----------------|-------------------|--------|
| `{route/schema/command}` | `{purpose}` | `{input}` | `{output}` | `{BEH-NNN/Sn}` |

## 6. Frontend Flow

### 6a. User path

{Screen or interaction path if applicable. Write `None.` if not UI-facing.}

### 6b. State and error handling

{State transitions, validation, and user-visible errors.}

### 6c. Legacy parity notes

{Formatting, ordering, culture, numeric precision, or bug-compatible behavior that the UI must preserve.}

## 7. File Touchpoints

### Files to CREATE

- `{path}` — `{purpose}`

### Files to MODIFY

- `{path}` — `{purpose}`

### Files to leave UNCHANGED

- `{path}` — `{reason}`

## 8. Acceptance Criteria Checklist

### Phase A: Ported behavior

- [ ] **A1** — {Criterion title}
  - {Observable new-system behavior}
  - Evidence: `path/to/file.test.ts::test_name_A1(runner)`
  - Covers: `{BEH-NNN}`, `{S1}`

### Phase P: Parity

{Mandatory for port stories. Every covered `BEH-NNN` must have at least one Phase P criterion. Each P criterion must cite an oracle fixture or acceptance-data source, tolerance / normalization rule, and defect-ledger decision when applicable.}

- [ ] **P1** — Legacy output for `{BEH-NNN}` matches the new implementation within `{tolerance}`
  - Oracle: `{FIX-NNN or acceptance-data source}`
  - Tolerance / normalization: `{numeric/text/order/time rule}`
  - Defect decision: `{DEF-NNN reproduce-faithfully | fix-now | fix-later | none}`
  - Evidence: `tests/parity/{story-id}.test.ts::parity_BEH_NNN_P1(runner)`

### Phase Y: Binding & stack compliance

- [ ] **Y1** — **(binding)** {Restate binding constraint or adapter row}
  - {Verification statement}
  - Evidence: `tests/integration/example-adapter.test.ts::real_adapter_Y1(runner)`

### Phase Z: Quality Gates

- [ ] **Z1** — `{stack.buildCommand}` passes with zero build/type errors
- [ ] **Z2** — `{stack.lintCommand}` passes (or only has pre-existing warnings)
- [ ] **Z3** — Configured type policy passes (default: no `any` types in any new or modified file)
- [ ] **Z4** — Configured shared type import policy passes (default: imports from shared use `@shared/types` alias, not relative paths)
- [ ] **Z5** — New or modified code includes appropriate logging for errors and significant operations per the implementer's logging guidelines
- [ ] **Z6** — `/review-story {STORY-ID}` satisfies the configured review gate, including zero high or critical `TEST-#`, `SEC-#`, `REL-#`, `API-#`, `MODEL-#`, `PAR-#`, or `PROV-#` findings
- [ ] **Z7** — `/review-story {STORY-ID}` satisfies the configured model-fidelity gate
- [ ] **Z8** — `/verify-parity {STORY-ID}` satisfies the configured parity gate and writes the configured parity report

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Covers BEH | Notes |
|---|-------|------------------|-----------|-----------|------------|-------|
| 1 | unit | `path/to/file.test.ts::test_name_A1` | A1 | S1 | BEH-NNN | happy path |
| 2 | parity | `tests/parity/{story-id}.test.ts::parity_BEH_NNN_P1` | P1 | S1 | BEH-NNN | oracle fixture `{FIX-NNN}` |
| 3 | integration | `tests/integration/example-adapter.test.ts::real_adapter_Y1` | Y1 | S1 | BEH-NNN | real adapter, not mocked |

## 8b. Parity Plan

| BEH ID | Evidence grade | Oracle / fixture | Tolerance | Defect decision | Acceptance data gap |
|--------|----------------|------------------|-----------|-----------------|---------------------|
| BEH-NNN | `{E1/E2/E3/E4/E5}` | `{FIX-NNN / T3 data}` | `{rule}` | `{DEF-NNN/none}` | `{none/question}` |

## 9. Risks & Tradeoffs

| Risk | Impact | Mitigation | Evidence |
|------|--------|------------|----------|
| `{risk}` | `{impact}` | `{mitigation}` | `{grade + citation}` |

## Implementation Order

1. Create or enable parity fixture/test for `P1` and observe it fail for the expected reason.
2. Implement supporting types and ports.
3. Implement adapters and integration evidence.
4. Implement behavior.
5. Run parity, targeted tests, build, lint, review, and QA.

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed by | `{agent/user}` |
| Completion ref | `{commit SHA / PR URL / TBD if not committed}` |
| Review ref | `{story review path}` |
| QA ref | `{QA output / command}` |
| Parity ref | `{parity report path}` |

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Change ref | Review ref | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|------------|------------|-------------|-----------|
| F1 | `{YYYY-MM-DD}` | `{story-followup / trivial-code / docs-only}` | `{one sentence}` | `{paths}` | `{command or proof}` | `{commit SHA, PR URL, or "uncommitted" / "TBD"}` | `{none / review path}` | `{none / docs path}` | `{none / affected AC}` |

*Created: {YYYY-MM-DD} | Port story template*
