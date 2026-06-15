# S2-5: CLI configuration adapter and vault walk-up

**Story**: Implement `CLIConfigurationAdapter` that resolves vault root via walk-up, reads environment variables and Typer CLI flags (flags override env), and exposes an immutable object implementing `ConfigurationPort` per ADR-004 and S19.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

Every Stage 2 use case and adapter needs resolved runtime settings — vault path, wiki subdirectory, provider credentials, batch mode — through **`ConfigurationPort`**, never via direct `os.environ` or argparse in domain code (S19). This story delivers the **CLI configuration adapter** at `src/llm_wiki/adapters/cli/configuration.py` plus a small **vault walk-up** helper that implements ADR-003 detection rules (`.obsidian/` or `{wiki_dir}/SCHEMA.md`).

When walk-up fails and no valid `--vault` is supplied, the adapter raises a typed configuration error with guidance (S3). CLI flags (`--vault`, `--wiki-dir`, `--provider`, `--batch`) override environment variables when both are set for the same setting (ADR-004). Provider **selection algorithm** (S11) is implemented in `src/llm_wiki/adapters/llm/factory.py` in **S2-6**; this story exposes all config fields the factory consumes.

**Depends on:** [S2-1](S2-1-python-package-scaffold.md), [S2-2](S2-2-port-protocols-and-domain-models.md).

**Out of scope:** Typer app wiring beyond what is needed to test flag parsing (full composition root S2-11), LLM HTTP adapters (S2-6), filesystem adapters (S2-4 — tests may use temp dirs for walk-up), Obsidian settings adapter (future epic).

**Guiding constraint:** `ConfigurationPort` implementation is immutable after construction; vault walk-up uses real filesystem paths in integration tests (no mock of directory existence).

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Adapter in `adapters/cli/`; domain never reads env |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `ConfigurationPort` property surface |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Vault walk-up algorithm (`.obsidian/` or `wiki/SCHEMA.md`) |
| [`docs/decisions/ADR-004-configuration-and-llm-providers.md`](ADR-004-configuration-and-llm-providers.md) | **Primary** — env var names, defaults, CLI override rule |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | Typer global options; adapter colocated with CLI package |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README Environment Variables table matches ADR-004 field names and defaults
- [x] Section 4 filled from ADR-003/004 and REQ-001 S3, S19
- [x] Section 4b lists `ConfigurationPort` + `CLIConfigurationAdapter`
- [x] Section 8a has contract + integration rows; Phase Y cites integration tests
- [x] **S3**, **S19** fully mapped; **S11** config fields only (selection algorithm deferred to S2-6 with note in Summary)
- [x] Phase Y uses real temp-dir walk-up integration tests

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `CLIConfigurationAdapter` (or factory function `build_cli_configuration(...)`) lives at `src/llm_wiki/adapters/cli/configuration.py`.
2. **Y2** — Implements all ADR-002 `ConfigurationPort` properties with ADR-004 defaults when env/flags unset.
3. **Y3** — Vault walk-up from CWD: stop at first ancestor containing `.obsidian/` **or** `{wiki_dir}/SCHEMA.md` (ADR-003).
4. **Y4** — Explicit `--vault PATH` validates the same rules; invalid path raises clear error without creating wiki files (S3).
5. **Y5** — CLI flags override env for: `LLM_WIKI_DIR` ↔ `--wiki-dir`, `LLM_WIKI_PROVIDER` ↔ `--provider`, and `--batch` for batch mode (S19).
6. **Y6** — `wiki_dir` property is absolute `{vault_root}/{wiki_subdir_name}`.
7. **Y7** — No domain or use-case module imports `CLIConfigurationAdapter`; only composition root / tests do.
8. **Y8** — Never log API keys; adapter may log resolved provider name and vault path at DEBUG only.

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | `CLIConfigurationAdapter` (`src/llm_wiki/adapters/cli/configuration.py`) | Real temp directory tree under `pytest` `tmp_path` with `.obsidian/` or `wiki/SCHEMA.md` markers | new in this story |

Supporting module: `src/llm_wiki/adapters/cli/vault_walk.py` — walk-up helper (tested via integration through adapter).

---

## 5. API Endpoints + Schemas

No HTTP API. Typer option shapes (consumed in S2-11; declared here for binding):

| Flag | Env var | Maps to `ConfigurationPort` |
|------|---------|----------------------------|
| `--vault PATH` | — | `vault_root` |
| `--wiki-dir NAME` | `LLM_WIKI_DIR` | wiki subdirectory name → absolute `wiki_dir` |
| `--provider {ollama,openai,anthropic}` | `LLM_WIKI_PROVIDER` | `provider_override` |
| `--batch` | — | `batch_mode` |
| — | `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OPENAI_*`, `ANTHROPIC_*` | respective properties |

**Error type (Python):**

```python
class VaultNotFoundError(Exception):
    """Raised when walk-up and --vault both fail (S3)."""
```

---

## 6. Frontend Flow

Not applicable — configuration adapter only; no terminal UX beyond error messages raised to CLI layer.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/adapters/cli/configuration.py` | `CLIConfigurationAdapter` / builder |
| 2 | `src/llm_wiki/adapters/cli/vault_walk.py` | Walk-up from `Path.cwd()` or given start |
| 3 | `src/llm_wiki/adapters/cli/errors.py` | `VaultNotFoundError`, optional `ConfigurationError` |
| 4 | `tests/integration/test_cli_configuration.py` | Walk-up, flags, env override integration |
| 5 | `tests/unit/test_vault_walk.py` | Unit tests for walk-up edge cases on temp dirs |
| 6 | `scripts/verify-s2-5-configuration.sh` | Binding: env var names match ADR-004 / README |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/test_configuration_port_contract.py` | Add run against `CLIConfigurationAdapter` with env + temp vault |
| 2 | `README.md` | Link S2-5 row; add verifier if missing |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/adapters/llm/*` — provider factory in S2-6
- `src/llm_wiki/domain/*` — no domain changes
- `src/llm_wiki/adapters/cli/main.py` — full wiring in S2-11

---

## 8. Acceptance Criteria Checklist

### Phase A: Vault walk-up (ADR-003)

- [x] **A1** — Starting inside nested folder, walk-up finds vault root at ancestor with `.obsidian/`
  - Evidence: `tests/integration/test_cli_configuration.py::walkup_finds_obsidian_A1(pytest)`

- [x] **A2** — Walk-up finds vault when `{wiki_dir}/SCHEMA.md` exists without `.obsidian/` (edge case)
  - Evidence: `tests/integration/test_cli_configuration.py::walkup_finds_schema_A2(pytest)`

- [x] **A3** — `--vault` explicit path used when provided and valid
  - Evidence: `tests/integration/test_cli_configuration.py::explicit_vault_flag_A3(pytest)`

### Phase B: Invalid vault (S3)

- [x] **B1** — No marker in ancestor chain and no `--vault`: raises `VaultNotFoundError` with message mentioning `--vault` and opening vault in workspace
  - Evidence: `tests/integration/test_cli_configuration.py::rejects_invalid_vault_s3_B1(pytest)`

- [x] **B2** — Invalid `--vault` path: raises without creating any wiki files in cwd or tmp
  - Evidence: `tests/integration/test_cli_configuration.py::no_partial_wiki_on_error_s3_B2(pytest)`

### Phase C: Environment defaults (ADR-004)

- [x] **C1** — Unset env: `ollama_base_url` defaults to `http://localhost:11434`, `ollama_model` to `llama3.2`, OpenAI/Anthropic models to ADR-004 defaults
  - Evidence: `tests/integration/test_cli_configuration.py::default_models_adr004_C1(pytest)`

- [x] **C2** — `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` read into respective properties when set
  - Evidence: `tests/integration/test_cli_configuration.py::reads_api_keys_C2(pytest)`

### Phase D: CLI overrides (S19)

- [x] **D1** — When both `LLM_WIKI_DIR=notes` env and `--wiki-dir wiki` flag set, `wiki_dir` resolves to `{vault}/wiki`
  - Evidence: `tests/integration/test_cli_configuration.py::flag_overrides_wiki_dir_s19_D1(pytest)`

- [x] **D2** — When both `LLM_WIKI_PROVIDER=openai` env and `--provider ollama` flag set, `provider_override == "ollama"`
  - Evidence: `tests/integration/test_cli_configuration.py::flag_overrides_provider_s19_D2(pytest)`

- [x] **D3** — `--batch` sets `batch_mode is True`
  - Evidence: `tests/integration/test_cli_configuration.py::batch_flag_sets_mode_D3(pytest)`

### Phase E: Contract compliance

- [x] **E1** — S2-2 configuration port contract suite passes against `CLIConfigurationAdapter`
  - Evidence: `tests/contract/test_configuration_port_contract.py::cli_adapter_passes_contract_E1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Walk-up uses real filesystem markers on temp dirs (Section 4 Y3) — not mocked `Path.exists`
  - Evidence: `tests/integration/test_cli_configuration.py::real_walkup_binding_Y1(pytest)`

- [x] **Y2** — **(binding)** CLI flag override rule verified for wiki dir and provider (Section 4 Y5, S19)
  - Evidence: `tests/integration/test_cli_configuration.py::override_rule_binding_s19_Y2(pytest)`

- [x] **Y3** — **(binding)** Env var names match ADR-004 / README table
  - Evidence: `scripts/verify-s2-5-configuration.sh::env_names_match_adr004_Y3(bash scripts/verify-s2-5-configuration.sh)`

- [x] **Y4** — **(binding)** Configuration contract test passes against CLI adapter (Section 4 Y1–Y2)
  - Evidence: `tests/contract/test_configuration_port_contract.py::cli_adapter_passes_contract_Y4(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/integration/test_cli_configuration.py tests/unit/test_vault_walk.py tests/contract/test_configuration_port_contract.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Configuration adapter logs at DEBUG only; never logs key values
- [x] **Z6** — `/review-story S2-5` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `tests/integration/test_cli_configuration.py::walkup_finds_obsidian_A1` | A1, Y1 | S3 | real tmp dirs |
| 2 | integration | `tests/integration/test_cli_configuration.py::walkup_finds_schema_A2` | A2, Y1 | — | edge case |
| 3 | integration | `tests/integration/test_cli_configuration.py::explicit_vault_flag_A3` | A3 | S1 | --vault |
| 4 | integration | `tests/integration/test_cli_configuration.py::rejects_invalid_vault_s3_B1` | B1 | S3 | error message |
| 5 | integration | `tests/integration/test_cli_configuration.py::no_partial_wiki_on_error_s3_B2` | B2 | S3 | no writes |
| 6 | integration | `tests/integration/test_cli_configuration.py::default_models_adr004_C1` | C1, Y3 | S11 | defaults only |
| 7 | integration | `tests/integration/test_cli_configuration.py::reads_api_keys_C2` | C2 | S19 | monkeypatch env |
| 8 | integration | `tests/integration/test_cli_configuration.py::flag_overrides_wiki_dir_s19_D1` | D1, Y2 | S19 | |
| 9 | integration | `tests/integration/test_cli_configuration.py::flag_overrides_provider_s19_D2` | D2, Y2 | S19 | |
| 10 | integration | `tests/integration/test_cli_configuration.py::batch_flag_sets_mode_D3` | D3 | S7 | batch flag |
| 11 | unit | `tests/unit/test_vault_walk.py::stops_at_filesystem_root` | A1 | — | edge case |
| 12 | contract | `tests/contract/test_configuration_port_contract.py::cli_adapter_passes_contract_E1` | E1, Y4 | S19 | |
| 13 | integration | `scripts/verify-s2-5-configuration.sh::env_names_match_adr004_Y3` | Y3 | S11 | static |

**Out of scope Sn:** **S11** provider **selection algorithm** (Ollama-first routing) — **S2-6** `adapters/llm/factory.py`. **S1**, **S2**, **S5–S10**, **S12–S18** — not configuration adapter concerns.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Typer context not available in unit tests | Builder accepts explicit namespace/dataclass of flag values for testability |
| 2 | Symlinked vault roots | Follow ADR-003 literally; document symlink limitation if encountered |
| 3 | Secrets in process env during tests | Use monkeypatch; never assert log output contains key material |

---

## Implementation Order

1. `src/llm_wiki/adapters/cli/errors.py` — typed errors (covers B1)
2. `src/llm_wiki/adapters/cli/vault_walk.py` + `tests/unit/test_vault_walk.py` (covers A1–A2)
3. `src/llm_wiki/adapters/cli/configuration.py` — env + flag resolution (covers C1–D3)
4. `tests/integration/test_cli_configuration.py` — red-first (covers Phase A–D, Y1–Y2)
5. Extend configuration contract tests for CLI adapter (covers E1, Y4)
6. `scripts/verify-s2-5-configuration.sh` (covers Y3)
7. **Verify** — `bash scripts/verify-s2-5-configuration.sh && pytest tests/integration/test_cli_configuration.py tests/unit/test_vault_walk.py tests/contract/test_configuration_port_contract.py`
8. `README.md` — backlog link

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `1074629` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-5-configuration.sh && pytest tests/integration/test_cli_configuration.py tests/unit/test_vault_walk.py tests/contract/test_configuration_port_contract.py` |
| QA result | `19/19 criteria PASS (A1–Z6)` |
| Docs handoff | `README.md` backlog row S2-5 → Complete; verify script already listed in Available Scripts |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-5 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
