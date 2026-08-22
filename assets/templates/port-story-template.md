<!-- Port story contract:
- Based on the standard user-story template, with modernization provenance and parity sections.
- Slice prerequisites are copied from the migration-plan row and checked off here. Do not edit analysis snapshots.
- Every covered XP-NNN must have a path detail, a path test plan, singular evidence grades, and Phase P coverage — unless no fixture exists, in which case do not invent a parity criterion.
- Comparison rules come from the path test plan, not a global default.
- Phase P is mandatory before Phase Y when a fixture or acceptance-data source exists. Z8 is mandatory in Phase Z.
- INCLUDE §5 only when the path exposes an HTTP/RPC/message API. INCLUDE §6 only when UI-facing. Omit entirely otherwise — do not write "None." placeholders for whole sections.
-->

# {STORY-ID}: {Story Title}

**Story**: {As a ... I want ... so that ...}
**Epic**: {Epic number} — {Epic name}
**Size**: {Small | Medium | Large}
**Status**: Open
**Modernization slice:** `{strangler | phased-rewrite | big-bang-parallel-run}`
**Structure fidelity:** `{preserve-then-refactor | refactor-now}`
**Execution paths:** `{XP-NNN, …}`

---

## 1. Summary

{One paragraph: which paths this story ports, why this slice is next, and the comparison rule that will prove it. Do not retell the global inventories.}

### 1a. Domain model touchpoints

| Purpose / domain section | Terms / entities / fields / invariants touched | Evidence |
|--------------------------|-----------------------------------------------|----------|
| `{docs/PURPOSE.md or docs/DOMAIN.md section}` | `{items}` | `{grade}` `{citation}` |

### 1b. Legacy source touchpoints

Taken from the path detail. One grade per row.

| Legacy artifact | Role in story | Evidence grade | Citation |
|-----------------|---------------|----------------|----------|
| `{legacy path/doc}` | `{behavior/source/oracle/defect}` | `{E1\|E2\|E3\|E4\|E5}` | `{path:line or section}` |

## 2. Linked architecture decisions (ADRs)

- `{decisionsDir}/ADR-NNN-slug.md` — `{decision}`

Also cite `DEC-NNN` from the decision register when a porting choice (not a target-design choice) binds this story.

## 3. Definition of Ready (DoR)

- [ ] Purpose and domain touchpoints are current.
- [ ] Covered `XP-NNN` path details exist and use singular evidence grades.
- [ ] Path test plans exist; comparison rules are per path.
- [ ] No covered claim is `E4 inferred` or `E5 unknown` unless a `DEC-NNN` accepts it.
- [ ] Oracle tier is compatible with the planned Phase P evidence.
- [ ] Defect-ledger decisions are recorded for known mismatches on these paths.
- [ ] Slice prerequisites below are resolved.
- [ ] Linked ADRs are `Accepted` or this story is explicitly a spike.

## 3b. Slice prerequisites

Copied from the migration-plan row. Check off here. Do not edit the path inventory, dependency inventory, graph, or impedance analysis.

| ID | Kind | What must be true | Status |
|----|------|-------------------|--------|
| `{DEP-NNN / DEC-NNN / DEF-NNN}` | `{dependency / decision / defect}` | `{the condition that unblocks implementation}` | `{unresolved / resolved}` |

## 4. Binding constraints (non-negotiable)

- `{target stack, process boundary, persistence, dependency substitution, or per-path comparison rule}`

## 4b. Ports & Adapters

| Port | Adapter | Boundary owned | Contract test | Integration test |
|------|---------|----------------|---------------|------------------|
| `{Port}` | `{Adapter}` | `{boundary}` | `{test}` | `{test}` |

Write a one-line "no integration boundary" note in this table's first row when none apply, then omit extra rows.

<!-- INCLUDE WHEN this slice exposes an HTTP, RPC, or message API. OMIT ENTIRELY otherwise. -->

## 5. API Endpoints + Schemas

| Endpoint / schema | Purpose | Request / input | Response / output | Covers |
|-------------------|---------|-----------------|-------------------|--------|
| `{route/schema/command}` | `{purpose}` | `{input}` | `{output}` | `{XP-NNN/Sn}` |

<!-- INCLUDE WHEN this slice is UI-facing. OMIT ENTIRELY otherwise. -->

## 6. Frontend Flow

### 6a. User path

{Screen or interaction path.}

### 6b. State and error handling

{State transitions, validation, and user-visible errors.}

### 6c. Legacy parity notes

{Formatting, ordering, culture, or bug-compatible UI behavior from the path test plan.}

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
  - Covers: `{XP-NNN}`, `{S1}`

### Phase P: Parity

Mandatory when a fixture or acceptance-data source exists for a covered path. Each P criterion cites the path test plan's oracle source, comparison rule, and defect decision. If the test plan says no fixture exists, do not write a P criterion that pretends one does.

- [ ] **P1** — Legacy output for `{XP-NNN}` matches the new implementation under `{comparison rule from the path test plan}`
  - Oracle: `{FIX-NNN or acceptance-data source}`
  - Comparison: `{exact / tolerance-based with bound / semantic}`
  - Defect decision: `{DEF-NNN reproduce-faithfully | fix-now | fix-later | none}`
  - Evidence: `tests/parity/{story-id}.test.ts::parity_XP_NNN_P1(runner)`

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

| # | Level | File::test name | Covers AC | Covers Sn | Covers XP | Notes |
|---|-------|------------------|-----------|-----------|-----------|-------|
| 1 | unit | `path/to/file.test.ts::test_name_A1` | A1 | S1 | XP-NNN | happy path |
| 2 | parity | `tests/parity/{story-id}.test.ts::parity_XP_NNN_P1` | P1 | S1 | XP-NNN | `{FIX-NNN}` + comparison rule from path test plan |
| 3 | integration | `tests/integration/example-adapter.test.ts::real_adapter_Y1` | Y1 | S1 | XP-NNN | real adapter, not mocked |

## 8b. Parity Plan

Copied from the path test plan. Do not invent a tighter or looser rule here.

| XP ID | Evidence grade | Oracle / fixture | Comparison rule | Defect decision | Acceptance data gap |
|-------|----------------|------------------|-----------------|-----------------|---------------------|
| XP-NNN | `{E1\|E2\|E3\|E4\|E5}` | `{FIX-NNN / T3 data}` | `{rule and bound}` | `{DEF-NNN/none}` | `{none/question}` |

## 9. Risks & Tradeoffs

| Risk | Impact | Mitigation | Evidence |
|------|--------|------------|----------|
| `{risk}` | `{impact}` | `{mitigation}` | `{grade}` `{citation}` |

Cite RISK/IMP/DEC IDs rather than restating them.

## Implementation Order

1. Create or enable the parity test for `P1` from the path test plan and observe it fail for the expected reason.
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
