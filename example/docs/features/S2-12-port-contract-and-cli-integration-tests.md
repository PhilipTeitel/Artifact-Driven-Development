# S2-12: Port contract tests and CLI integration tests

**Story**: Complete Stage 2 QA harness — parametrized port contract suites against all real adapters, hermetic vault CLI end-to-end tests, scenario traceability matrix for REQ-001, and binding verify script proving hexagonal boundaries (S16).
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

Individual adapter stories (S2-4–S2-7, S2-6) introduced contract and integration tests incrementally. This story ** consolidates and completes** the Stage 2 test pyramid so QA can trace REQ-001 scenarios **S1–S13**, **S16**, and **S19** to executable evidence without live LLM or network in CI ([ADR-001](ADR-001-hexagonal-architecture.md)).

**Contract test harness:** Refactor `tests/contract/` so shared behavioral suites run against **both** in-memory fakes and production adapters (filesystem, schema, configuration, LLM, interaction) via pytest parametrization. Any adapter regression fails the same contract row as the fake.

**CLI integration / E2E:** Extend `tests/integration/test_cli_commands.py` (from S2-11) into a full **Stage 2 E2E** flow on a hermetic vault copy (`tests/fixtures/vault/`): `init` → `ingest --batch` → `query` (decline filing) → `lint` → `validate`, asserting ADR-003 artifacts and S5 source immutability (checksum manifest). Uses injectable fake LLM with canned responses — real filesystem and configuration adapters only.

**Scenario traceability:** Publish `docs/features/S2-12-scenario-traceability.md` mapping each implemented REQ-001 `Sn` to test file::name and verify script rows (S15 ADD traceability for Stage 2).

**Verify script:** `scripts/verify-s2-12-integration.sh` runs contract parametrization smoke + CLI E2E pytest marker + import-boundary grep.

**Depends on:** [S2-11](S2-11-typer-cli-composition-root.md) (wired CLI), all S2-4–S2-10 stories **Complete**.

**Out of scope:** Live Ollama/OpenAI/Anthropic in CI (optional `pytest -m live_llm` markers only), Obsidian plugin tests (S17), Stage 1 command re-verification (S1-6 already Done), performance/load testing.

**Guiding constraint:** Binding CI evidence uses hermetic fixtures — no mocked filesystem inside integration tests that claim adapter coverage.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Contract + import boundary proof (S16) |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Contract suites per port |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | E2E artifact checklist |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | CLI E2E subcommand sequence |

---

## 3. Definition of Ready (DoR)

- [x] S2-11 CLI composition root **Complete** with injectable LLM hook
- [x] All five ports have at least one production adapter in repo
- [x] Section 4b lists every adapter exercised by parametrized contract or integration rows
- [x] Section 8a maps **S1–S13**, **S16**, **S19** (Stage 2 subset) — **S14**, **S17**, **S18** explicitly out of scope (Stage 1 / future)
- [x] Phase Y cites CLI E2E integration test and import-boundary test with non-mock filesystem evidence
- [x] Traceability doc planned with one row per in-scope Sn

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Each port in ADR-002 has contract tests runnable against **≥1 real adapter** (not fake-only) in CI.
2. **Y2** — CLI E2E test uses real `FilesystemWikiStorageAdapter` + `CLIConfigurationAdapter` on temp vault copy.
3. **Y3** — E2E asserts: `SCHEMA.md`, `index.md`, `log.md`, ≥1 wiki page, `.ingested.json` with ≥1 source, log lines for `init`, `ingest`, `query`, `lint` (ADR-003 / S13).
4. **Y4** — E2E verifies `tests/fixtures/vault/daily/` sources unchanged via SHA256 manifest (`scripts/fixtures/test-vault-daily.sha256` or equivalent) (S5).
5. **Y5** — `tests/unit/test_import_boundaries.py` confirms `domain/` and `ports/` never import `adapters/` (S16).
6. **Y6** — Scenario traceability doc links every in-scope Sn to ≥1 test or verify script check (S15).
7. **Y7** — No live LLM required for binding CI (`verify-s2-12-integration.sh` must pass offline).

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | `CLIConfigurationAdapter` | Temp dirs + Typer context | contract + integration |
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | `FilesystemWikiStorageAdapter` | `vault_tmp` fixture | contract parametrized |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | `MarkdownSchemaAdapter` | Real SCHEMA on disk | contract parametrized |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | Ollama/OpenAI/Anthropic adapters | Hermetic httpx/SDK fixtures from S2-6 | contract parametrized |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | `TerminalUserInteractionAdapter` | StringIO console + patched stdin | contract parametrized |
| — | — | Typer CLI (`main.py`) | `CliRunner` full E2E | driving adapter |

---

## 5. API Endpoints + Schemas

No HTTP API. Validates CLI + on-disk artifacts per ADR-003.

**Traceability artifact schema (`S2-12-scenario-traceability.md`):**

| Sn | Stage 2 evidence (test or script) | Notes |
|----|-----------------------------------|-------|
| S1 | `test_cli_e2e.py::...` | init artifacts |
| … | … | … |

---

## 6. Frontend Flow

Not applicable — test/QA story only.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `tests/contract/conftest.py` | Parametrize `adapter_impl` fixture per port |
| 2 | `tests/integration/test_cli_e2e.py` | Full Stage 2 E2E sequence |
| 3 | `tests/integration/fake_llm.py` | Canned LLM responses for CLI tests |
| 4 | `scripts/verify-s2-12-integration.sh` | Binding verify script |
| 5 | `docs/features/S2-12-scenario-traceability.md` | Sn → evidence matrix (S15) |
| 6 | `scripts/fixtures/test-vault-daily.sha256` | Extend if E2E uses different fixture path |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/test_*_port_contract.py` | Parametrize against fake + real adapters |
| 2 | `tests/integration/test_cli_commands.py` | Align with shared E2E fixtures if duplicated |
| 3 | `tests/unit/test_import_boundaries.py` | Expand S16 checks if gaps |
| 4 | `pyproject.toml` | Optional `live_llm` pytest marker registration |
| 5 | `README.md` | Link S2-12; add verify script to Available Scripts |

### Files UNCHANGED

- `src/llm_wiki/domain/use_cases/**` — unless contract failures expose bugs (fix in place with story note)
- `.cursor/commands/**` — Stage 1 scope

---

## 8. Acceptance Criteria Checklist

### Phase A: Contract parametrization (S16)

- [x] **A1** — Each `tests/contract/test_*_port_contract.py` runs core suite against fake **and** real adapter via shared parametrization
  - Evidence: `tests/contract/conftest.py::parametrize_adapters_A1(pytest -k contract)`

- [x] **A2** — All five ports represented in parametrized contract runs
  - Evidence: `scripts/verify-s2-12-integration.sh::five_ports_contract_A2(bash)`

### Phase B: CLI E2E flow (S1, S6–S9, S12, S13)

- [x] **B1** — E2E runs `init`, `ingest --batch`, `query`, `lint`, `validate` in sequence; final `validate` exits 0
  - Evidence: `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1(pytest)`

- [x] **B2** — Post-run wiki contains log headings for init, ingest, query, lint operations (grep parseable S13)
  - Evidence: `tests/integration/test_cli_e2e.py::log_operations_s13_B2(pytest)`

- [x] **B3** — `.ingested.json` contains ≥1 ingested source key after batch ingest (S12)
  - Evidence: `tests/integration/test_cli_e2e.py::ingested_sidecar_s12_B3(pytest)`

### Phase C: Source immutability (S5)

- [x] **C1** — Daily source manifest checksums unchanged after E2E
  - Evidence: `tests/integration/test_cli_e2e.py::sources_unchanged_s5_C1(pytest)`

### Phase D: Configuration port (S19, S3)

- [x] **D1** — E2E uses `--vault` flag resolution through CLI (explicit vault path)
  - Evidence: `tests/integration/test_cli_e2e.py::explicit_vault_flag_s19_D1(pytest)`

### Phase E: Traceability (S15)

- [x] **E1** — `docs/features/S2-12-scenario-traceability.md` lists S1–S13, S16, S19 with evidence links
  - Evidence: `scripts/verify-s2-12-integration.sh::traceability_doc_E1(bash)`

### Phase F: Import boundaries (S16)

- [x] **F1** — `domain/` and `ports/` packages have zero imports from `llm_wiki.adapters`
  - Evidence: `tests/unit/test_import_boundaries.py::domain_ports_no_adapters_F1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** CLI E2E uses real filesystem adapter on temp vault (not InMemoryWikiStorageFake)
  - Evidence: `tests/integration/test_cli_e2e.py::real_filesystem_binding_Y1(pytest)`

- [x] **Y2** — **(binding)** Storage contract parametrized run passes for `FilesystemWikiStorageAdapter`
  - Evidence: `tests/contract/test_storage_port_contract.py::filesystem_parametrize_Y2(pytest)`

- [x] **Y3** — **(binding)** `verify-s2-12-integration.sh` passes offline in CI
  - Evidence: `scripts/verify-s2-12-integration.sh(bash scripts/verify-s2-12-integration.sh)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/contract/ tests/integration/test_cli_e2e.py tests/unit/test_import_boundaries.py` passes
- [x] **Z2** — `ruff check .` passes
- [x] **Z3** — No untyped bare `Any` in new test modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Test modules use structured logging or pytest caplog where asserting error paths
- [x] **Z6** — `/review-story S2-12` reports zero `high` or `critical` findings

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | contract | `tests/contract/test_storage_port_contract.py` (parametrize) | A1, Y2 | S16 | fake + FS |
| 2 | contract | `tests/contract/test_schema_port_contract.py` (parametrize) | A1 | S16, S4 | fake + markdown |
| 3 | contract | `tests/contract/test_configuration_port_contract.py` (parametrize) | A1 | S19 | fake + CLI adapter |
| 4 | contract | `tests/contract/test_llm_port_contract.py` (parametrize) | A1 | S11, S16 | fake + ollama httpx |
| 5 | contract | `tests/contract/test_interaction_port_contract.py` (parametrize) | A1 | S6, S8 | fake + terminal |
| 6 | e2e | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | B1 | S1, S6–S9, S10 | full CLI |
| 7 | e2e | `tests/integration/test_cli_e2e.py::log_operations_s13_B2` | B2 | S13 | log grep |
| 8 | e2e | `tests/integration/test_cli_e2e.py::ingested_sidecar_s12_B3` | B3 | S12 | sidecar |
| 9 | e2e | `tests/integration/test_cli_e2e.py::sources_unchanged_s5_C1` | C1 | S5 | checksum |
| 10 | e2e | `tests/integration/test_cli_e2e.py::explicit_vault_flag_s19_D1` | D1 | S3, S19 | --vault |
| 11 | unit | `tests/unit/test_import_boundaries.py::domain_ports_no_adapters_F1` | F1 | S16 | static |
| 12 | e2e | `tests/integration/test_cli_e2e.py::real_filesystem_binding_Y1` | Y1 | S16 | binding |
| 13 | script | `scripts/verify-s2-12-integration.sh` | Y3, E1 | S15 | offline CI |

**Out of scope Sn (documented in traceability doc):**

| Sn | Reason |
|----|--------|
| S14 | Stage 1 Cursor commands — covered by S1-6 |
| S17 | Future Obsidian plugin |
| S18 | Stage 1 daily driver gate — Stage 2 E2E is parallel evidence, not S18 replacement |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Contract parametrization refactor breaks existing tests | Migrate one port at a time; keep existing test names as wrappers |
| 2 | E2E brittle to LLM output format | Canned fake LLM at wiring boundary; assert filesystem artifacts not answer quality |
| 3 | Duplicate coverage with S2-11 smoke tests | S2-11 keeps per-command smoke; S2-12 owns full pipeline + traceability |

---

## Implementation Order

1. `tests/integration/fake_llm.py` — shared canned responses
2. `tests/contract/conftest.py` — parametrization fixtures
3. Refactor contract tests port-by-port (A1, A2)
4. `tests/integration/test_cli_e2e.py` — red-first E2E (Phase B–D)
5. `docs/features/S2-12-scenario-traceability.md`
6. `scripts/verify-s2-12-integration.sh`
7. **Verify** — `bash scripts/verify-s2-12-integration.sh`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `10bedfa` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-12-integration.sh && pytest tests/contract/ tests/integration/test_cli_e2e.py tests/unit/test_import_boundaries.py && ruff check .` |
| QA result | All criteria PASS (50 pytest + verify script + ruff) |
| Docs handoff | README: S2-12 → Complete; added `verify-s2-12-integration.sh`; traceability doc at `docs/features/S2-12-scenario-traceability.md` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-06 | Story: S2-12 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
