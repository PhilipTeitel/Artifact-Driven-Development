# S1-3: Implement `/wiki-ingest` Cursor command

**Story**: Ship the `/wiki-ingest` slash command so a Cursor agent can ingest one markdown source or a directory (interactive or batch), update wiki pages and `index.md`, append to `log.md`, and record paths in `wiki/.ingested.json` without modifying vault sources.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Large
**Status**: Complete

---

## 1. Summary

This story delivers **ingest** for Stage 1: `.cursor/commands/wiki-ingest.md`. The agent reads `wiki/SCHEMA.md` for workflows and excludes, processes markdown **outside** the wiki subdirectory, and maintains wiki artifacts per [ADR-003](ADR-003-vault-wiki-layout.md).

**Interactive mode (S6):** User supplies a source file path; agent summarizes takeaways for review, then writes/updates wiki pages, `index.md`, `log.md`, and `.ingested.json`.

**Batch mode (S7):** User invokes with batch intent (documented flag phrase, e.g. `batch` or `--batch` in the command args); agent processes all `.md` files in a directory sequentially without interactive prompts, skips excludes and already-ingested sources.

**Tracking (S12):** After successful ingest, append `{ "relative/path.md": "ISO8601Z" }` under `.ingested.json` → `sources` (create file with `"version": 1` on first ingest).

**Immutability (S5):** Source files and all markdown outside `wiki/` remain read-only.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) **S5**, **S6**, **S7**, **S12**, **S13** (ingest log entries). **S8**, **S9**, **S11** (provider selection) are N/A for Stage 1 (Cursor LLM). **S1**, **S2** are satisfied by S1-2 init.

**Depends on:** [S1-1](S1-1-wiki-schema-template.md), [S1-2](S1-2-init-wiki-command.md). **Blocks:** S1-6.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | `.ingested.json` format, excludes, log format, source immutability |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `WikiStoragePort` write boundaries; ingest sidecar methods |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Stage 1 behavior must match future `IngestUseCase` |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs are **Accepted**; S1-2 init command is **Complete** or fixtures exist for manual QA
- [x] Section 4 and 4b filled; 4b states no Python adapters
- [x] Section 8a covers **S5**, **S6**, **S7**, **S12**, **S13** in **Covers Sn**
- [x] Phase Y **(binding)** criteria cite `scripts/verify-wiki-ingest-command.sh`
- [x] **S8**, **S9**, **S11**, **S18** out of scope in Summary

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Command file at `.cursor/commands/wiki-ingest.md` (slash name `/wiki-ingest`).
2. **Y2** — Agent must read `wiki/SCHEMA.md` **Excludes** before selecting sources; skip matching paths (S7).
3. **Y3** — Interactive ingest requires user review of takeaways before writing wiki pages unless user explicitly waives in chat.
4. **Y4** — Batch ingest processes only `.md` files under the given directory; no prompts between files (S7).
5. **Y5** — `.ingested.json` keys are vault-relative paths with forward slashes; values are ISO 8601 UTC timestamps (S12).
6. **Y6** — Batch re-ingest skips paths already in `.ingested.json` and reports them as skipped (S12).
7. **Y7** — Log append uses `## [YYYY-MM-DD] ingest | {title}` (S13).
8. **Y8** — No writes outside `wiki/` except creating/updating files under `wiki/` (S5).
9. **Y9** — Wiki links use `[text](path)` only — no `[[wikilinks]]` in new pages (SCHEMA conventions).

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** Ingest I/O is performed by the Cursor agent following command instructions. Stage 2 implements `IngestUseCase` and filesystem/LLM adapters in **S2-8**.

---

## 5. API Endpoints + Schemas

No HTTP API.

**`.ingested.json` (created/updated by ingest):**

```json
{
  "version": 1,
  "sources": {
    "daily/2026-05-01.md": "2026-06-01T12:00:00Z"
  }
}
```

**Command arguments (documented in command file):**

| Arg | Required | Description |
|-----|----------|-------------|
| `path` | yes | Source file or directory relative to vault root |
| `batch` | no | When set, enable S7 batch behavior |

---

## 6. Frontend Flow

Not applicable — no web UI.

### 6a. Interactive ingest flow

```
/wiki-ingest path/to/note.md
├── Require initialized wiki (SCHEMA present)
├── Read source (read-only)
├── Present takeaways → user confirms/edits
├── Write/update wiki pages + index + log
└── Update .ingested.json
```

### 6b. Batch ingest flow

```
/wiki-ingest daily/ --batch
├── List *.md recursively under path
├── Filter excludes + .ingested.json
├── For each file: ingest without prompts
└── Summary: processed / skipped / failed
```

### 6c. States

| State | Behavior |
|-------|----------|
| Wiki not initialized | Direct user to `/init-wiki` |
| Source excluded | Skip with reason |
| Already ingested (batch) | Skip with reason |
| Success | Updated wiki + sidecar |

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `.cursor/commands/wiki-ingest.md` | Ingest command spec |
| 2 | `scripts/verify-wiki-ingest-command.sh` | Binding verifier |
| 3 | `test/fixtures/ingested-v1.json` | Golden `.ingested.json` for verifier grep tests (optional) |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S1-3; list ingest verifier under Available Scripts |

### Files UNCHANGED

- `templates/wiki/SCHEMA.md` — S1-1; ingest reads vault copy
- Vault source trees during verifier runs — use dedicated temp dirs in script if needed

---

## 8. Acceptance Criteria Checklist

### Phase A: Command presence

- [x] **A1** — `.cursor/commands/wiki-ingest.md` exists and names `wiki/SCHEMA.md`, excludes, `.ingested.json`, `index.md`, `log.md`
  - Evidence: `scripts/verify-wiki-ingest-command.sh::A1_command_exists`

### Phase B: Interactive ingest (S6)

- [x] **B1** — Command documents read → review → write sequence for a single source file
  - Evidence: `scripts/verify-wiki-ingest-command.sh::B1_interactive_s6`

- [x] **B2** — Command requires updating `index.md` and appending `log.md` on success
  - Evidence: `scripts/verify-wiki-ingest-command.sh::B2_index_log_s6`

### Phase C: Batch ingest (S7)

- [x] **C1** — Command documents batch mode trigger and sequential directory processing without per-file prompts
  - Evidence: `scripts/verify-wiki-ingest-command.sh::C1_batch_s7`

- [x] **C2** — Command documents skip of SCHEMA excludes and already-ingested sources in batch
  - Evidence: `scripts/verify-wiki-ingest-command.sh::C2_skips_s7`

### Phase D: Sidecar tracking (S12)

- [x] **D1** — Command documents `.ingested.json` structure (`version`, `sources`) and vault-relative keys
  - Evidence: `scripts/verify-wiki-ingest-command.sh::D1_ingested_json_s12`

- [x] **D2** — Command states source files are never modified
  - Evidence: `scripts/verify-wiki-ingest-command.sh::D2_source_immutable_s12`

### Phase E: Immutability (S5)

- [x] **E1** — Command forbids writes outside `wiki/`
  - Evidence: `scripts/verify-wiki-ingest-command.sh::E1_immutability_s5`

### Phase F: Log format (S13)

- [x] **F1** — Command specifies ingest log heading `## [YYYY-MM-DD] ingest | {title}`
  - Evidence: `scripts/verify-wiki-ingest-command.sh::F1_log_format_s13`

### Phase G: Link conventions

- [x] **G1** — Command reminds agent: standard markdown links only in new wiki pages
  - Evidence: `scripts/verify-wiki-ingest-command.sh::G1_markdown_links`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Verifier passes all static checks for command + JSON contract
  - Evidence: `scripts/verify-wiki-ingest-command.sh::Y1_full(bash scripts/verify-wiki-ingest-command.sh)`

### Phase Z: Quality Gates

- [x] **Z1**–**Z5** — **N/A** (no app code / no Python package)
- [x] **Z6** — `/review-story S1-3` zero high/critical on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-wiki-ingest-command.sh::A1_command_exists` | A1, Y1 | S14 | command |
| 2 | integration | `scripts/verify-wiki-ingest-command.sh::B1_interactive_s6` | B1 | S6 | review step |
| 3 | integration | `scripts/verify-wiki-ingest-command.sh::B2_index_log_s6` | B2 | S6 | artifacts |
| 4 | integration | `scripts/verify-wiki-ingest-command.sh::C1_batch_s7` | C1 | S7 | batch |
| 5 | integration | `scripts/verify-wiki-ingest-command.sh::C2_skips_s7` | C2 | S7, S12 | skips |
| 6 | integration | `scripts/verify-wiki-ingest-command.sh::D1_ingested_json_s12` | D1, Y1 | S12 | JSON shape |
| 7 | integration | `scripts/verify-wiki-ingest-command.sh::D2_source_immutable_s12` | D2 | S12, S5 | no source writes |
| 8 | integration | `scripts/verify-wiki-ingest-command.sh::E1_immutability_s5` | E1 | S5 | wiki-only writes |
| 9 | integration | `scripts/verify-wiki-ingest-command.sh::F1_log_format_s13` | F1 | S13 | log heading |
| 10 | integration | `scripts/verify-wiki-ingest-command.sh::G1_markdown_links` | G1 | S4 | link rule |

**Out of scope Sn:** S1–S4 (init/schema), S8–S11, S16–S19, S18 (S1-6).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Agent may skip user review | Command marks review as required unless user says “proceed without review” |
| 2 | Large directories in batch | Command caps batch size or requires explicit confirmation for >N files |
| 3 | Exclude parsing differs from Stage 2 | Mirror SCHEMA bullet-list rules; defer strict parser to S2-4 |

---

## Implementation Order

1. Author `.cursor/commands/wiki-ingest.md` (interactive + batch sections).
2. Implement `scripts/verify-wiki-ingest-command.sh` (grep-based checks on command text).
3. Run verifier; fix command until green.
4. Manual smoke: init `test/vault`, ingest one `daily/*.md`, verify sidecar + unchanged source mtime/content.
5. **Final verify** — batch ingest two files; second run skips one.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-01 |
| Completion ref | `a50b06f` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-wiki-ingest-command.sh` |
| QA result | 12/12 criteria PASS (A1, B1, B2, C1, C2, D1, D2, E1, F1, G1, Y1; Z1–Z5 N/A; Z6 via review gate) |
| Docs handoff | README: project structure (`wiki-ingest.md`), Getting Started verify line, backlog S1-3 → Complete |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-01 | Story: S1-3 | Epic: 1 — Stage 1 — Cursor daily driver*
