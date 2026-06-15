# S1-4: Implement `/wiki-query` Cursor command

**Story**: Ship the `/wiki-query` slash command so a Cursor agent answers natural-language questions using `wiki/index.md` and wiki pages, prints a cited answer, and optionally files a new wiki page only after explicit user confirmation.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story implements **query** for Stage 1 via `.cursor/commands/wiki-query.md`. The agent follows the **Query** workflow in `wiki/SCHEMA.md`: read `index.md` first, open relevant wiki pages, synthesize an answer with citations, present it in chat, then ask whether to file the answer as a new wiki page.

**Filing (S8):** If the user confirms, the agent creates a new page under `wiki/`, updates `index.md`, and appends a `query` entry to `log.md`. If the user declines, **no wiki files change** after the answer was produced (read-only query path).

**Log format (S13):** Filed queries append `## [YYYY-MM-DD] query | {title}`.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) **S8**, **S13**. **S5** applies when filing (writes only under `wiki/`). **S6**, **S7**, **S9** are other commands.

**Depends on:** [S1-2](S1-2-init-wiki-command.md); wiki with at least one ingested page for meaningful smoke (S1-3). **Blocks:** S1-6.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Index-first navigation, log format, wiki-only writes |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Query read/write boundaries on index and pages |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Parity with future `QueryUseCase` (S2-9) |

---

## 3. Definition of Ready (DoR)

- [x] ADRs **Accepted**; init command available
- [x] Section 4, 8a complete; **S8**, **S13** in **Covers Sn**
- [x] Phase Y cites `scripts/verify-wiki-query-command.sh`
- [x] **S6**, **S7**, **S9**, **S11**, **S18** out of scope in Summary

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Command at `.cursor/commands/wiki-query.md`.
2. **Y2** — Agent must read `wiki/index.md` before reading individual wiki pages (index-first, S8).
3. **Y3** — Answer includes citations to wiki page paths (markdown links or explicit paths).
4. **Y4** — Filing requires explicit user confirmation in chat; default is no filing.
5. **Y5** — On filing: create page, update `index.md`, append log with `query` operation (S13).
6. **Y6** — On decline: no new/modified wiki files after answer (S8).
7. **Y7** — No modification of vault sources outside `wiki/` (S5).
8. **Y8** — No vector/RAG/embeddings — navigation via index and page reads only (README non-goal).

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** Stage 2 `QueryUseCase` lands in **S2-9**.

---

## 5. API Endpoints + Schemas

No HTTP API.

**Command arguments:**

| Arg | Required | Description |
|-----|----------|-------------|
| `question` | yes | Natural-language question (remainder of command invocation) |

**Example filed page naming:** `wiki/queries/2026-06-01-topic-slug.md` (agent discretion; flat `wiki/` also allowed per SCHEMA).

---

## 6. Frontend Flow

Not applicable — no web UI.

### 6a. Query flow

```
/wiki-query {question}
├── Require wiki/SCHEMA.md + index.md
├── Read index.md → select pages
├── Read pages → synthesize answer + citations
├── Print answer in chat
├── Ask: file as new wiki page? (yes/no)
├── If yes: write page, index, log
└── If no: stop (no further writes)
```

### 6c. States

| State | Behavior |
|-------|----------|
| Empty wiki | Answer explains no pages; no filing |
| Answer only | No wiki mutations |
| Filing confirmed | New page + index + log |
| Filing declined | No mutations post-answer |

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `.cursor/commands/wiki-query.md` | Query command spec |
| 2 | `scripts/verify-wiki-query-command.sh` | Binding verifier |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S1-4; Available Scripts entry |

### Files UNCHANGED

- Ingest/lint commands — separate stories
- `templates/wiki/*` — unless query workflow clarification needed in SCHEMA (prefer command-only)

---

## 8. Acceptance Criteria Checklist

### Phase A: Command presence

- [x] **A1** — `.cursor/commands/wiki-query.md` exists
  - Evidence: `scripts/verify-wiki-query-command.sh::A1_command_exists`

### Phase B: Index-first query (S8)

- [x] **B1** — Command requires reading `index.md` before other wiki pages
  - Evidence: `scripts/verify-wiki-query-command.sh::B1_index_first_s8`

- [x] **B2** — Command requires synthesized answer with citations to wiki pages
  - Evidence: `scripts/verify-wiki-query-command.sh::B2_citations_s8`

### Phase C: Filing gate (S8)

- [x] **C1** — Command requires explicit user confirmation before creating/updating wiki files for filing
  - Evidence: `scripts/verify-wiki-query-command.sh::C1_confirm_filing_s8`

- [x] **C2** — Command states that if user declines, no wiki files are modified after the answer
  - Evidence: `scripts/verify-wiki-query-command.sh::C2_decline_no_writes_s8`

- [x] **C3** — On confirm: create page, update `index.md`, append log
  - Evidence: `scripts/verify-wiki-query-command.sh::C3_filing_updates_s8`

### Phase D: Immutability (S5)

- [x] **D1** — Command forbids modifying sources outside `wiki/`
  - Evidence: `scripts/verify-wiki-query-command.sh::D1_immutability_s5`

### Phase E: Log format (S13)

- [x] **E1** — Filed query log heading uses operation `query`
  - Evidence: `scripts/verify-wiki-query-command.sh::E1_log_format_s13`

### Phase F: No RAG

- [x] **F1** — Command forbids embedding/vector search; index + page reads only
  - Evidence: `scripts/verify-wiki-query-command.sh::F1_no_vector_rag`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Full verifier exit 0
  - Evidence: `scripts/verify-wiki-query-command.sh::Y1_full(bash scripts/verify-wiki-query-command.sh)`

### Phase Z: Quality Gates

- [ ] **Z1**–**Z5** — **N/A**
- [x] **Z6** — `/review-story S1-4` zero high/critical

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-wiki-query-command.sh::A1_command_exists` | A1, Y1 | S14 | |
| 2 | integration | `scripts/verify-wiki-query-command.sh::B1_index_first_s8` | B1 | S8 | |
| 3 | integration | `scripts/verify-wiki-query-command.sh::B2_citations_s8` | B2 | S8 | |
| 4 | integration | `scripts/verify-wiki-query-command.sh::C1_confirm_filing_s8` | C1 | S8 | |
| 5 | integration | `scripts/verify-wiki-query-command.sh::C2_decline_no_writes_s8` | C2 | S8 | |
| 6 | integration | `scripts/verify-wiki-query-command.sh::C3_filing_updates_s8` | C3 | S8 | |
| 7 | integration | `scripts/verify-wiki-query-command.sh::D1_immutability_s5` | D1 | S5 | |
| 8 | integration | `scripts/verify-wiki-query-command.sh::E1_log_format_s13` | E1 | S13 | |
| 9 | integration | `scripts/verify-wiki-query-command.sh::F1_no_vector_rag` | F1 | — | README alignment |

**Out of scope Sn:** S1–S7, S9–S12, S16–S19, S18 (S1-6).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Agent files without asking | Command uses MUST/STOP language on confirmation |
| 2 | Sparse index | Command allows reading all `wiki/*.md` if index empty, but must still open index first |
| 3 | Long answers unsuitable as pages | User can decline filing; suggest summary page title |

---

## Implementation Order

1. Write `.cursor/commands/wiki-query.md`.
2. Implement `scripts/verify-wiki-query-command.sh`.
3. Run verifier until green.
4. Manual smoke on vault with ingested content: query → decline (no new files) → query → accept filing.
5. **Final verify** — grep `log.md` for `query` operation line.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-01 |
| Completion ref | `7e4e517` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-wiki-query-command.sh` |
| QA result | 11/11 criteria PASS (A1, B1, B2, C1, C2, C3, D1, E1, F1, Y1; Z1–Z5 N/A; Z6 via review gate) |
| Docs handoff | README: project structure (`wiki-query.md`), Getting Started verify line, backlog S1-4 → Complete |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-01 | Story: S1-4 | Epic: 1 — Stage 1 — Cursor daily driver*
