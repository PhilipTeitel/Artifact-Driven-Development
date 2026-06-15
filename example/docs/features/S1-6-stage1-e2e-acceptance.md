# S1-6: Stage 1 end-to-end acceptance on a real vault

**Story**: Prove Stage 1 is a usable daily driver (S18) by running `/init-wiki`, `/wiki-ingest`, `/wiki-query`, and `/wiki-lint` on a populated vault fixture, capturing QA evidence, and confirming wiki artifacts match CLI-bound contracts without Stage 2.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Small
**Status**: Complete

---

## 1. Summary

This story is the **Epic 1 completion gate**. It does not add new user-facing commands; it validates that [S1-2](S1-2-init-wiki-command.md) through [S1-5](S1-5-wiki-lint-command.md) work together on a **realistic vault** and documents objective evidence for QA and ADD traceability (S15, S18).

**Primary fixture:** `test/vault/` in this repo — populated markdown under `daily/` (existing sample notes). The implementer adds minimal Obsidian markers (e.g. `test/vault/.obsidian/`) if required for vault detection (S3). QA may also record a second run on the implementer's personal vault as optional supplemental evidence; the **binding** automated checks use the repo fixture only.

**Scenarios exercised:** **S5** (sources unchanged), **S14** (Cursor commands produce CLI-parity artifacts), **S18** (init → ingest → query → lint without Python CLI). **S1–S4**, **S6–S9**, **S12**, **S13** are verified indirectly via command verifiers plus this E2E script.

**Depends on:** S1-2, S1-3, S1-4, S1-5 **Complete**. **Blocks:** Epic 2 start (per README).

**Out of scope:** Stage 2 CLI (S10–S11, S16), Obsidian plugin (S17), provider port tests (S19).

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Artifact checklist for E2E validation |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Stage 1 must match contracts Stage 2 will implement |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Filesystem layout expected by ports |

---

## 3. Definition of Ready (DoR)

- [x] S1-2 through S1-5 are **Complete** with verifiers passing
- [x] All four commands exist under `.cursor/commands/`
- [x] Section 8a maps **S5**, **S14**, **S18** (and cross-cutting **S13** via log grep)
- [x] Phase Y cites `scripts/verify-stage1-e2e.sh`
- [x] Epic 1 README row may move to **Done** only after this story is **Complete**

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Evidence artifact path: `docs/features/S1-6-acceptance-evidence.md` (created by this story).
2. **Y2** — Automated checker `scripts/verify-stage1-e2e.sh` validates post-run filesystem state under `test/vault/wiki/` (or configurable `VAULT_FIXTURE`).
3. **Y3** — E2E proof includes: `SCHEMA.md`, `index.md`, `log.md`, at least one wiki page, `.ingested.json` with ≥1 source, log lines for `init`, `ingest`, `query`, and `lint` operations.
4. **Y4** — Checker verifies no modification to tracked source files under `test/vault/daily/` (checksum or git status clean for that subtree).
5. **Y5** — Stage 2 / `llm-wiki` CLI is not invoked in binding evidence.
6. **Y6** — All upstream command verifiers (`verify-init-wiki`, `verify-wiki-ingest`, `verify-wiki-query`, `verify-wiki-lint`, `verify-wiki-schema-template`) must pass in the E2E pipeline.

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** It aggregates QA evidence for Stage 1 commands.

---

## 5. API Endpoints + Schemas

No HTTP API. E2E validates on-disk artifacts per ADR-003.

---

## 6. Frontend Flow

Not applicable. **Human/agent procedure** documented in `docs/features/S1-6-acceptance-evidence.md`:

1. Open `test/vault` as Cursor workspace (or multi-root with commands repo).
2. Run `/init-wiki`.
3. Run `/wiki-ingest` on one `daily/*.md` (interactive).
4. Run `/wiki-query` with a question answerable from new wiki content; decline filing for first run (optional second run with filing).
5. Run `/wiki-lint`.
6. Run `bash scripts/verify-stage1-e2e.sh`.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `scripts/verify-stage1-e2e.sh` | Post-conditions on fixture vault wiki |
| 2 | `docs/features/S1-6-acceptance-evidence.md` | QA evidence template (commands run, dates, PASS/FAIL) |
| 3 | `test/vault/.obsidian/.gitkeep` or minimal config | Vault root marker for S3 (if not present) |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Epic 1 status note; S1-6 link; document E2E verifier in Available Scripts |
| 2 | `docs/features/S1-6-stage1-e2e-acceptance.md` | Fill Completion Metadata when done |

### Files UNCHANGED

- Command markdown files — owned by S1-2–S1-5 unless E2E reveals gaps (then patch via follow-up ledger on those stories)

---

## 8. Acceptance Criteria Checklist

### Phase A: Evidence document

- [x] **A1** — `docs/features/S1-6-acceptance-evidence.md` exists with sections: Environment, Commands executed, Observations, Verifier output, Sign-off
  - Evidence: `scripts/verify-stage1-e2e.sh::A1_evidence_doc_exists`

### Phase B: Automated post-conditions (S18, S14)

- [x] **B1** — `wiki/SCHEMA.md`, `wiki/index.md`, `wiki/log.md` exist under fixture vault
  - Evidence: `scripts/verify-stage1-e2e.sh::B1_core_artifacts_s18`

- [x] **B2** — At least one `wiki/**/*.md` page exists besides SCHEMA, index, and log
  - Evidence: `scripts/verify-stage1-e2e.sh::B2_wiki_page_s18`

- [x] **B3** — `wiki/.ingested.json` exists with `"version": 1` and ≥1 entry in `sources`
  - Evidence: `scripts/verify-stage1-e2e.sh::B3_ingested_json_s12`

- [x] **B4** — `wiki/log.md` contains grep matches for operations `init`, `ingest`, `query`, and `lint`
  - Evidence: `scripts/verify-stage1-e2e.sh::B4_log_operations_s13_s18`

### Phase C: Source immutability (S5)

- [x] **C1** — No diff under `test/vault/daily/` after E2E (git clean or checksum match pre/post)
  - Evidence: `scripts/verify-stage1-e2e.sh::C1_sources_unchanged_s5`

### Phase D: Command suite (S14)

- [x] **D1** — All five Stage 1 verifiers exit 0 when run from repo root
  - Evidence: `scripts/verify-stage1-e2e.sh::D1_all_command_verifiers`

### Phase E: Stage 2 independence (S18)

- [x] **E1** — Evidence doc states Stage 2 CLI was not used; no `pyproject.toml` install required for PASS
  - Evidence: `docs/features/S1-6-acceptance-evidence.md` + `scripts/verify-stage1-e2e.sh::E1_no_stage2`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Full E2E verifier exit 0 after agent workflow
  - Evidence: `scripts/verify-stage1-e2e.sh::Y1_full(bash scripts/verify-stage1-e2e.sh)`

- [x] **Y2** — **(binding)** Evidence doc completed with date and `QA result: PASS`
  - Evidence: `docs/features/S1-6-acceptance-evidence.md` contains `QA result: PASS`

### Phase Z: Quality Gates

- [x] **Z1**–**Z5** — **N/A**
- [x] **Z6** — `/review-story S1-6` zero high/critical on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-stage1-e2e.sh::A1_evidence_doc_exists` | A1 | S15 | doc present |
| 2 | integration | `scripts/verify-stage1-e2e.sh::B1_core_artifacts_s18` | B1, Y1 | S18, S14 | SCHEMA/index/log |
| 3 | integration | `scripts/verify-stage1-e2e.sh::B2_wiki_page_s18` | B2 | S18 | content page |
| 4 | integration | `scripts/verify-stage1-e2e.sh::B3_ingested_json_s12` | B3 | S12, S18 | sidecar |
| 5 | integration | `scripts/verify-stage1-e2e.sh::B4_log_operations_s13_s18` | B4 | S13, S18 | four ops |
| 6 | integration | `scripts/verify-stage1-e2e.sh::C1_sources_unchanged_s5` | C1 | S5 | daily/ clean |
| 7 | integration | `scripts/verify-stage1-e2e.sh::D1_all_command_verifiers` | D1, Y2 | S14 | upstream scripts |
| 8 | integration | `scripts/verify-stage1-e2e.sh::E1_no_stage2` | E1 | S18 | no Python CLI |
| 9 | e2e | `docs/features/S1-6-acceptance-evidence.md` | Y2, A1 | S18 | human sign-off |
| 10 | integration | `scripts/verify-stage1-e2e.sh::Y1_full` | Y1 | S18 | aggregate |

**Note:** Rows 2–8 assume the agent workflow has already been executed once against the fixture; the script validates resulting tree. CI may skip agent steps and only run structural checks on committed fixture wiki if the project chooses to commit a golden `test/vault/wiki/` — document choice in evidence file.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Agent workflow not reproducible in CI | Binding checks are filesystem-based; agent run is manual once per release |
| 2 | Committed wiki pollutes fixture | Prefer gitignored `test/vault/wiki/` with documented regen, or committed golden tree + script |
| 3 | Personal vault differs from fixture | Repo fixture is source of truth for PASS |

---

## Implementation Order

1. Ensure S1-2–S1-5 complete; all command verifiers green.
2. Add `test/vault/.obsidian/` if needed.
3. Run full agent workflow; capture transcript snippets in evidence doc.
4. Implement `scripts/verify-stage1-e2e.sh` (may run in CI after wiki committed or post-local run).
5. Complete `docs/features/S1-6-acceptance-evidence.md` with PASS.
6. Update README Epic 1 narrative: Stage 1 gate met when S1-6 Complete.
7. **Final verify** — `bash scripts/verify-stage1-e2e.sh` from repo root.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-05 |
| Completion ref | `c7dc11c` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-stage1-e2e.sh` |
| QA result | All criteria PASS (29/29 verifier checks, exit 0) |
| Docs handoff | README Epic 1 → Done; S1-1–S1-6 backlog rows Done; Getting Started cites E2E verifier; evidence: `docs/features/S1-6-acceptance-evidence.md` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-01 | Story: S1-6 | Epic: 1 — Stage 1 — Cursor daily driver*
