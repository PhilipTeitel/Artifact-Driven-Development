# S1-5: Implement `/wiki-lint` Cursor command

**Story**: Ship the `/wiki-lint` slash command so a Cursor agent health-checks the wiki (contradictions, stale claims, orphans, missing concepts, broken links), prints a report with suggested fixes only, and appends a lint entry to `log.md` without auto-modifying wiki pages.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story delivers **lint** for Stage 1: `.cursor/commands/wiki-lint.md`. The agent follows the **Lint** workflow in `wiki/SCHEMA.md`, inspects wiki pages and cross-references, outputs findings with **suggested** fixes, and appends a log entry. It must **not** apply fixes to wiki pages automatically (S9).

**Log format (S13):** Append `## [YYYY-MM-DD] lint | {title}` with a summary of findings in the body.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) **S9**, **S13**. **S5** — lint must not modify sources outside `wiki/`; lint must not silently rewrite wiki page bodies (report-only).

**Depends on:** [S1-2](S1-2-init-wiki-command.md); richer smoke with ingested wiki (S1-3). **Blocks:** S1-6.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Lint workflow in SCHEMA; log format |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Read wiki; append log only |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Parity with `LintUseCase` (S2-10) |

---

## 3. Definition of Ready (DoR)

- [x] ADRs **Accepted**
- [x] Section 8a covers **S9**, **S13**; Phase Y cites lint verifier
- [x] **S6**, **S8**, **S18** out of scope in Summary

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Command at `.cursor/commands/wiki-lint.md`.
2. **Y2** — Lint checks include: contradictions, stale claims, orphan pages, missing concept pages, missing/broken cross-references (S9).
3. **Y3** — Output is a human-readable report; suggestions are labeled as suggestions, not applied edits.
4. **Y4** — Agent must **not** modify any `wiki/**/*.md` page content except appending to `log.md` (S9).
5. **Y5** — Log append uses `## [YYYY-MM-DD] lint | {title}` (S13).
6. **Y6** — No changes to vault sources outside `wiki/` (S5).
7. **Y7** — Agent reads `wiki/SCHEMA.md` for conventions before linting.

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** Stage 2 `LintUseCase` is **S2-10**.

---

## 5. API Endpoints + Schemas

No HTTP API. Optional command argument: focus area (e.g. `orphans only`) — document as optional free text; not required for MVP.

---

## 6. Frontend Flow

Not applicable.

### 6a. Lint flow

```
/wiki-lint
├── Require wiki/SCHEMA.md
├── Scan wiki pages + index
├── Build report (findings + suggested fixes)
├── Print report in chat
└── Append lint entry to log.md only
```

### 6c. States

| State | Behavior |
|-------|----------|
| Empty wiki | Report “no pages to lint”; still may append log |
| Issues found | Listed with suggestions; no auto-fix |
| Clean wiki | Report success; append log |

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `.cursor/commands/wiki-lint.md` | Lint command spec |
| 2 | `scripts/verify-wiki-lint-command.sh` | Binding verifier |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S1-5; Available Scripts |

---

## 8. Acceptance Criteria Checklist

### Phase A: Command presence

- [x] **A1** — `.cursor/commands/wiki-lint.md` exists
  - Evidence: `scripts/verify-wiki-lint-command.sh::A1_command_exists`

### Phase B: Lint checks (S9)

- [x] **B1** — Command lists all five check categories from S9 (contradictions, stale claims, orphans, missing concepts, missing cross-refs)
  - Evidence: `scripts/verify-wiki-lint-command.sh::B1_check_categories_s9`

- [x] **B2** — Command requires printed report with suggested fixes
  - Evidence: `scripts/verify-wiki-lint-command.sh::B2_report_s9`

### Phase C: No auto-fix (S9)

- [x] **C1** — Command explicitly forbids applying fixes to wiki pages (except `log.md` append)
  - Evidence: `scripts/verify-wiki-lint-command.sh::C1_no_autofix_s9`

### Phase D: Log append (S13)

- [x] **D1** — Command specifies lint log heading with operation `lint`
  - Evidence: `scripts/verify-wiki-lint-command.sh::D1_log_format_s13`

### Phase E: Immutability (S5)

- [x] **E1** — Command forbids modifying markdown outside `wiki/`
  - Evidence: `scripts/verify-wiki-lint-command.sh::E1_immutability_s5`

### Phase F: SCHEMA adherence

- [x] **F1** — Command instructs reading `wiki/SCHEMA.md` first
  - Evidence: `scripts/verify-wiki-lint-command.sh::F1_reads_schema`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Verifier exit 0
  - Evidence: `scripts/verify-wiki-lint-command.sh::Y1_full(bash scripts/verify-wiki-lint-command.sh)`

### Phase Z: Quality Gates

- [ ] **Z1**–**Z5** — **N/A**
- [x] **Z6** — `/review-story S1-5` zero high/critical

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-wiki-lint-command.sh::A1_command_exists` | A1, Y1 | S14 | |
| 2 | integration | `scripts/verify-wiki-lint-command.sh::B1_check_categories_s9` | B1 | S9 | |
| 3 | integration | `scripts/verify-wiki-lint-command.sh::B2_report_s9` | B2 | S9 | |
| 4 | integration | `scripts/verify-wiki-lint-command.sh::C1_no_autofix_s9` | C1 | S9 | |
| 5 | integration | `scripts/verify-wiki-lint-command.sh::D1_log_format_s13` | D1 | S13 | |
| 6 | integration | `scripts/verify-wiki-lint-command.sh::E1_immutability_s5` | E1 | S5 | |
| 7 | integration | `scripts/verify-wiki-lint-command.sh::F1_reads_schema` | F1 | S4 | SCHEMA read |

**Out of scope Sn:** S1–S8, S10–S12, S16–S19, S18 (S1-6).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Agent “fixes” pages anyway | Strong prohibition + review checklist in command |
| 2 | Subjective stale claims | Report as suggestions with evidence quotes |
| 3 | Large wikis timeout | Command allows sampling or lint subset with user opt-in |

---

## Implementation Order

1. Author `.cursor/commands/wiki-lint.md`.
2. Implement `scripts/verify-wiki-lint-command.sh`.
3. Run verifier.
4. Manual smoke: run lint on test vault wiki; verify only `log.md` grew among wiki files.
5. **Final verify** — user can apply a suggested fix manually in a follow-up ingest/query session.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-01 |
| Completion ref | `ddccb1b` (uncommitted working tree; re-run `git rev-parse --short HEAD` after commit) |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-wiki-lint-command.sh` |
| QA result | 9/9 criteria PASS (A1, B1, B2, C1, D1, E1, F1, Y1; Z1–Z5 N/A; Z6 via review gate) |
| Docs handoff | README: project structure (`wiki-lint.md`), Getting Started verify line, backlog S1-5 → Complete |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-01 | Story: S1-5 | Epic: 1 — Stage 1 — Cursor daily driver*
