# S1-2: Implement `/init-wiki` Cursor command

**Story**: Ship the Stage 1 `/init-wiki` slash command and starter templates so a Cursor agent can initialize `wiki/SCHEMA.md`, `index.md`, and `log.md` in a populated Obsidian vault without modifying source notes.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story implements the first **Stage 1 driving adapter** artifact: `.cursor/commands/init-wiki.md`. When the user runs `/init-wiki` with their vault as the workspace, the agent creates the wiki subdirectory (default `wiki/`), copies the canonical schema from [S1-1](S1-1-wiki-schema-template.md), and seeds `index.md` and `log.md` per [ADR-003](ADR-003-vault-wiki-layout.md).

Init must be **idempotent** (S2): existing wiki pages, index content, log history, and an existing `SCHEMA.md` must not be overwritten or destroyed. Only missing required files are created. The agent reports what already existed versus what was added.

**Vault context (S3):** Before writing anything, the command instructs the agent to resolve the vault root by walking parent directories from the workspace root until `.obsidian/` exists **or** `{wiki_dir}/SCHEMA.md` exists. If neither is found, the agent stops with a clear error and creates no partial wiki layout outside a dedicated wiki directory.

**Source immutability (S5):** Init must never modify, delete, or rename markdown outside the wiki subdirectory.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) scenarios **S1**, **S2**, **S3**, **S5**, and **S13** (init log entry format when logging first init). **S4** is satisfied by copying the S1-1 template. **S6–S9**, **S12**, **S14**, **S18** are out of scope (later commands / S1-6).

**Depends on:** [S1-1](S1-1-wiki-schema-template.md) (`templates/wiki/SCHEMA.md` and verifier). **Blocks:** S1-3, S1-4, S1-5, S1-6.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Wiki layout at init, idempotent rules, vault detection, log heading format, template copy source |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Stage 1 command must produce the same artifacts Stage 2 `InitUseCase` will target |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Documents `read_index` / `write_index` / schema paths the command must materialize on disk |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs agree on init artifacts, vault detection, and immutability
- [x] Section 4 (Binding constraints) is filled from ADR-003 and REQ-001 S1–S3, S5
- [x] Section 4b states no Python port/adapter work (Stage 1 command only)
- [x] Section 8a maps every AC ID; **S1**, **S2**, **S3**, **S5**, **S13** appear in **Covers Sn**
- [x] No adapters in Section 4b — hexagonal pairing rule N/A
- [x] Phase Y includes **(binding)** criteria with non-mock evidence via `scripts/verify-init-wiki-command.sh`
- [x] **S4**, **S6–S9**, **S12**, **S14**, **S18** explicitly out of scope in Summary

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Command file lives at `.cursor/commands/init-wiki.md` (Cursor maps filename to `/init-wiki`).
2. **Y2** — Init copies `templates/wiki/SCHEMA.md` from this repo to `{vault}/{wiki_dir}/SCHEMA.md` only when that file is missing; never overwrite an existing vault `SCHEMA.md`.
3. **Y3** — Init creates `index.md` and `log.md` from repo templates only when missing; never overwrite existing index or log body content.
4. **Y4** — Init does not create or modify any file outside `{vault}/{wiki_dir}/` except reporting to the user in chat.
5. **Y5** — Vault resolution follows ADR-003: walk up for `.obsidian/` or `{wiki_dir}/SCHEMA.md`; on failure, stop with actionable error (S3).
6. **Y6** — Default wiki subdirectory name is `wiki/`; command documents optional user override (e.g. “use wiki dir `notes-wiki`”) for parity with future `--wiki-dir` (Stage 2).
7. **Y7** — First-time init appends a log entry with heading `## [YYYY-MM-DD] init | …` per S13; re-init on existing wiki appends a summary entry only if the command completes successfully and does not rewrite prior log lines.
8. **Y8** — `.ingested.json` is **not** created at init (ADR-003; first ingest in S1-3).

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** Stage 1 encodes init behavior in a Cursor command markdown file. Stage 2 `InitUseCase`, `WikiStoragePort`, and `FilesystemWikiStorageAdapter` implement the same filesystem contract in **S2-3** and **S2-4**.

---

## 5. API Endpoints + Schemas

No HTTP API. No TypeScript types.

**Filesystem artifacts created (when missing):**

| Path | Source | Notes |
|------|--------|-------|
| `{wiki_dir}/SCHEMA.md` | `templates/wiki/SCHEMA.md` | Byte-identical copy unless user already has SCHEMA |
| `{wiki_dir}/index.md` | `templates/wiki/index.md` | Empty catalog structure |
| `{wiki_dir}/log.md` | `templates/wiki/log.md` | May be empty; init may append first entry |

**`.ingested.json` shape (reference only — not created here):**

```json
{
  "version": 1,
  "sources": {}
}
```

---

## 6. Frontend Flow

Not applicable — no web UI. The “UI” is Cursor chat output listing created vs existing paths.

### 6a. Agent workflow (logical hierarchy)

```
/init-wiki
├── Resolve vault root (walk-up)
├── Resolve wiki_dir (default wiki/)
├── Ensure wiki_dir/ exists
├── SCHEMA.md  → copy template if missing
├── index.md   → copy template if missing
├── log.md     → copy template if missing
├── Append init log entry (if appropriate)
└── Report summary to user (created / skipped / errors)
```

### 6b. Command inputs

| Input | Required | Default | Notes |
|-------|----------|---------|-------|
| Workspace | yes | Cursor workspace root | Must be vault or contain vault |
| `wiki_dir` | no | `wiki` | User may specify alternate name in command invocation |

### 6c. States

| State | Agent behavior |
|-------|----------------|
| Invalid vault | Error message; no files written |
| Fresh vault | Creates wiki dir + up to three files + init log line |
| Partial wiki | Creates only missing required files; reports skips |
| Complete wiki | No overwrites; reports all present |

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `.cursor/commands/init-wiki.md` | Slash command instructions for agent |
| 2 | `templates/wiki/index.md` | Starter catalog copied at init |
| 3 | `templates/wiki/log.md` | Starter log copied at init |
| 4 | `scripts/verify-init-wiki-command.sh` | Binding verifier for command + templates |
| 5 | `test/vault/.obsidian/` | Obsidian vault stub for S3 / G1 smoke (`G1_smoke_fixture`) |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S1-2 row; add verifier to Available Scripts if missing |

### Files UNCHANGED (confirm no modifications needed)

- `templates/wiki/SCHEMA.md` — owned by S1-1; init copies as-is
- `src/llm_wiki/*` — Stage 2
- User vault content outside `wiki/` — read-only

---

## 8. Acceptance Criteria Checklist

### Phase A: Command file present

- [x] **A1** — `.cursor/commands/init-wiki.md` exists and references `templates/wiki/SCHEMA.md`, `templates/wiki/index.md`, and `templates/wiki/log.md`
  - Evidence: `scripts/verify-init-wiki-command.sh::A1_command_exists`

### Phase B: Starter templates (S1)

- [x] **B1** — `templates/wiki/index.md` exists with a top-level heading and an empty **Pages** (or equivalent) section for future links
  - Evidence: `scripts/verify-init-wiki-command.sh::B1_index_template_s1`

- [x] **B2** — `templates/wiki/log.md` exists and documents append-only usage (may reference SCHEMA for heading format)
  - Evidence: `scripts/verify-init-wiki-command.sh::B2_log_template_s1`

### Phase C: Init behavior documented in command (S1, S2)

- [x] **C1** — Command instructs agent to create `{wiki_dir}/` and copy SCHEMA, index, and log when missing
  - Evidence: `scripts/verify-init-wiki-command.sh::C1_creates_layout_s1`

- [x] **C2** — Command explicitly forbids overwriting existing `SCHEMA.md`, `index.md`, `log.md`, or any other `wiki/**/*.md` page content (S2)
  - Evidence: `scripts/verify-init-wiki-command.sh::C2_idempotent_s2`

- [x] **C3** — Command requires a user-visible summary listing created vs already-present paths
  - Evidence: `scripts/verify-init-wiki-command.sh::C3_reports_summary_s2`

### Phase D: Vault context (S3)

- [x] **D1** — Command documents vault walk-up for `.obsidian/` and `{wiki_dir}/SCHEMA.md` and instructs agent to abort with clear guidance when unresolved
  - Evidence: `scripts/verify-init-wiki-command.sh::D1_vault_detection_s3`

### Phase E: Immutability (S5)

- [x] **E1** — Command states that no markdown outside `{wiki_dir}/` may be created, modified, deleted, or renamed
  - Evidence: `scripts/verify-init-wiki-command.sh::E1_immutability_s5`

### Phase F: Log format on init (S13)

- [x] **F1** — Command instructs append of log heading `## [YYYY-MM-DD] init | {title}` with allowed operation `init` when recording init
  - Evidence: `scripts/verify-init-wiki-command.sh::F1_log_format_s13`

### Phase G: Manual smoke (hermetic fixture)

- [x] **G1** — Documented smoke procedure: run `/init-wiki` against `test/vault` (with `.obsidian/` stub added by implementer if missing) produces `wiki/SCHEMA.md`, `wiki/index.md`, `wiki/log.md` without changing `test/vault/daily/**/*.md`
  - Evidence: `docs/features/S1-2-init-wiki-smoke.md` checklist signed off, or `scripts/verify-init-wiki-command.sh::G1_smoke_fixture` if automated

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Command path and required template references satisfy Section 4 constraints Y1–Y3
  - Evidence: `scripts/verify-init-wiki-command.sh::Y1_command_and_templates(bash scripts/verify-init-wiki-command.sh)`

- [x] **Y2** — **(binding)** S1-1 schema template still passes its verifier (init must not break template source)
  - Evidence: `scripts/verify-wiki-schema-template.sh::Y1_adr003_compliance(bash scripts/verify-wiki-schema-template.sh)`

### Phase Z: Quality Gates

- [x] **Z1** — `npm run build` — **N/A** (no application package yet)
- [x] **Z2** — `npm run lint` — **N/A**; `chmod +x scripts/verify-init-wiki-command.sh` applied
- [x] **Z3** — No `any` types — **N/A**
- [x] **Z4** — `@shared/types` — **N/A**
- [x] **Z5** — Application logging — **N/A** (markdown command + shell verifier)
- [x] **Z6** — `/review-story S1-2` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-init-wiki-command.sh::A1_command_exists` | A1, Y1 | — | command file |
| 2 | integration | `scripts/verify-init-wiki-command.sh::B1_index_template_s1` | B1, Y1 | S1 | index starter |
| 3 | integration | `scripts/verify-init-wiki-command.sh::B2_log_template_s1` | B2, Y1 | S1 | log starter |
| 4 | integration | `scripts/verify-init-wiki-command.sh::C1_creates_layout_s1` | C1, Y1 | S1 | copy instructions |
| 5 | integration | `scripts/verify-init-wiki-command.sh::C2_idempotent_s2` | C2, Y1 | S2 | no overwrite |
| 6 | integration | `scripts/verify-init-wiki-command.sh::C3_reports_summary_s2` | C3 | S2 | user report |
| 7 | integration | `scripts/verify-init-wiki-command.sh::D1_vault_detection_s3` | D1 | S3 | walk-up rules |
| 8 | integration | `scripts/verify-init-wiki-command.sh::E1_immutability_s5` | E1 | S5 | sources read-only |
| 9 | integration | `scripts/verify-init-wiki-command.sh::F1_log_format_s13` | F1 | S13 | init log heading |
| 10 | integration | `scripts/verify-wiki-schema-template.sh::Y1_adr003_compliance` | Y2 | S4 | upstream template |
| 11 | integration | `scripts/verify-init-wiki-command.sh::G1_smoke_fixture` | G1 | S1, S2, S5 | optional automated fixture check |

**Out of scope Sn:** S6–S9, S10–S12, S14, S16–S19, S18 (S1-6).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | User workspace is ADD-LLM-wiki repo, not their vault | Command tells agent to confirm vault root and refuse if only `test/` sample without `.obsidian/` |
| 2 | Template path when commands symlinked into vault | Document: resolve `templates/wiki/*` relative to ADD-LLM-wiki repo root (env or workspace multi-root) |
| 3 | Re-init appends duplicate init log lines | Acceptable; S2 prioritizes non-destructive behavior over log deduplication |

---

## Implementation Order

1. Add `templates/wiki/index.md` and `templates/wiki/log.md` starters (covers B1, B2).
2. Author `.cursor/commands/init-wiki.md` with vault detection, idempotent copy rules, immutability, log append (covers C1–F1, D1, E1).
3. Implement `scripts/verify-init-wiki-command.sh` matching Section 8a (red-first).
4. Add `test/vault/.obsidian/` placeholder (empty dir or minimal config) if needed for S3 smoke (covers G1).
5. Run `bash scripts/verify-init-wiki-command.sh` and `bash scripts/verify-wiki-schema-template.sh` (covers Y1, Y2, Z6 prep).
6. **Final verify** — Manual `/init-wiki` on `test/vault`; confirm `daily/` notes unchanged.

### `init-wiki.md` outline (implementer reference)

- Purpose and prerequisites (vault workspace, S1-1 template in repo)
- Step 1: Resolve vault root (walk-up algorithm)
- Step 2: Choose `wiki_dir` (default `wiki`)
- Step 3: Create directory; copy three templates if missing
- Step 4: Append init log entry; print summary table
- Explicit prohibitions: overwrite, touch sources, create `.ingested.json`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-01 |
| Completion ref | `59bd12b` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-init-wiki-command.sh` + `bash scripts/verify-wiki-schema-template.sh` |
| QA result | All criteria PASS (18/18); both verifiers exit 0 |
| Docs handoff | README backlog S1-2 → Done; Project Structure lists `init-wiki` command and init templates; Available Scripts lists init verifier |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-01 | Story: S1-2 | Epic: 1 — Stage 1 — Cursor daily driver*
