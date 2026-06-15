# S2-11: Typer CLI composition root

**Story**: Replace stub Typer handlers in `adapters/cli/main.py` with the composition root that wires all driven adapters and domain use cases for `init`, `validate`, `ingest`, `query`, and `lint` per ADR-005.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

Stage 2's **driving adapter** is the Typer CLI. Stories S2-3 through S2-10 implemented use cases and driven adapters; this story is the **only** place concrete adapters are assembled and injected into use cases ([ADR-001](ADR-001-hexagonal-architecture.md), [ADR-005](ADR-005-python-cli-packaging.md)).

**Composition root responsibilities:**

1. Parse global options (`--vault`, `--wiki-dir`, `--provider`) and subcommand flags via Typer.
2. Build `CLIConfigurationAdapter` from argv + environment (S3, S19).
3. Construct `FilesystemWikiStorageAdapter`, `MarkdownSchemaAdapter`, `TerminalUserInteractionAdapter`, and `LLMPort` via `select_llm_provider()` (S11).
4. Invoke the matching use case; map outcomes to exit codes (`validate` → non-zero on failure per S10; provider unavailable → non-zero per S11).
5. Contain **no** ingest/query/lint business logic — handlers are thin delegates.

**Depends on:** [S2-3](S2-3-init-and-validate-use-cases.md) through [S2-10](S2-10-lint-use-case.md), [S2-5](S2-5-cli-configuration-adapter.md), [S2-6](S2-6-llm-port-adapters.md), [S2-7](S2-7-terminal-interaction-adapter.md).

**Out of scope:** Full CLI integration test suite (S2-12), Obsidian plugin, JSON output flag, new subcommands beyond ADR-005 table.

**Guiding constraint:** No module other than `adapters/cli/main.py` (and a small `adapters/cli/wiring.py` helper if needed) may wire concrete adapters together.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Single composition root; dependency direction |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Use cases invoked via port-injected instances |
| [`docs/decisions/ADR-004-configuration-and-llm-providers.md`](ADR-004-configuration-and-llm-providers.md) | Provider factory wiring (S11) |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | **Primary** — Typer subcommands, exit codes, entry point |

---

## 3. Definition of Ready (DoR)

- [ ] Linked ADRs exist and are **Accepted**
- [ ] S2-3–S2-10 use cases and S2-4–S2-7 adapters are **Complete**
- [ ] Section 4 filled from ADR-005 subcommand table and exit code rules
- [ ] Section 4b lists all wired adapters at composition root
- [ ] Section 8a includes integration tests via Typer `CliRunner` with hermetic vault + fake LLM
- [ ] Phase Y cites integration tests exercising real filesystem + config adapters (LLM fake acceptable at boundary)
- [ ] **S3**, **S10**, **S11**, **S16**, **S19** mapped in Section 8a

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Entry point remains `llm_wiki.adapters.cli.main:app` per `pyproject.toml` (ADR-005).
2. **Y2** — Subcommands: `init`, `validate`, `ingest`, `query`, `lint` — each delegates to exactly one use case class.
3. **Y3** — `CLIConfigurationAdapter` is the sole configuration source for use cases (S19); handlers do not read `os.environ` directly except via adapter construction.
4. **Y4** — Invalid vault context raises/returns error with guidance; exit code `1`; no partial wiki writes (S3).
5. **Y5** — `validate` exits `0` when `ValidationResult.valid`, `1` otherwise (S10).
6. **Y6** — `ingest` passes `--batch` into configuration resolution before constructing use case (S7).
7. **Y7** — Provider selection uses `select_llm_provider(config)`; no provider → exit `1` with message (S11).
8. **Y8** — CLI handlers contain no LLM prompt strings or wiki write logic — only wiring and error translation.
9. **Y9** — Logging uses `llm_wiki.adapters.cli` logger; never logs API keys (ADR-005).

---

## 4b. Ports & Adapters

All adapters wired at composition root (this story):

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | `CLIConfigurationAdapter` | Typer `CliRunner` + temp vault dirs | S2-5 |
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | `FilesystemWikiStorageAdapter` | Hermetic vault copy | S2-4 |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | `MarkdownSchemaAdapter` | Real SCHEMA on disk | S2-4 |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | `select_llm_provider()` → provider adapters | **`RecordingLLMFake` or injectable test double** in CLI integration tests; real httpx in S2-6 tests | S2-6 |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | `TerminalUserInteractionAdapter` | `CliRunner` with `--batch` bypasses confirm paths | S2-7 |

**Note:** CLI integration tests in this story use dependency injection hook (e.g. `main.build_context(overrides=...)`) to substitute a fake `LLMPort` while keeping real filesystem and configuration adapters — proving wiring without live LLM.

---

## 5. API Endpoints + Schemas

No HTTP API. **CLI surface (binding per ADR-005):**

| Subcommand | Arguments / options | Use case | Exit codes |
|------------|---------------------|----------|------------|
| `init` | global opts | `InitUseCase.execute()` | 0 success |
| `validate` | global opts | `ValidateUseCase.execute()` | 0 valid, 1 invalid |
| `ingest PATH` | `--batch`, global opts | `IngestUseCase.execute(path)` | 0 success, 1 error |
| `query TEXT...` | global opts | `QueryUseCase.execute(question)` | 0 success |
| `lint` | global opts | `LintUseCase.execute()` | 0 success |

Global callback options: `--vault`, `--wiki-dir`, `--provider`.

---

## 6. Frontend Flow

Not applicable — terminal CLI only.

### 6a. Composition root flow

```
Typer subcommand handler
├── CLIConfigurationAdapter.from_context(ctx)
├── schema = MarkdownSchemaAdapter(config)
├── storage = FilesystemWikiStorageAdapter(config, schema)
├── interaction = TerminalUserInteractionAdapter()
├── llm = select_llm_provider(config)   # or injected fake in tests
├── use_case = *UseCase(storage=..., llm=..., ...)
└── use_case.execute(...) → map to exit code / typer.Exit
```

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/adapters/cli/wiring.py` | `AppContext` dataclass + `build_context()` factory |
| 2 | `tests/integration/test_cli_commands.py` | CliRunner smoke tests for each subcommand |
| 3 | `scripts/verify-s2-11-cli.sh` | Static binding checks (no stub message, use case imports) |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `src/llm_wiki/adapters/cli/main.py` | Replace stubs with wired handlers |
| 2 | `README.md` | Link S2-11; add verify script to Available Scripts |
| 3 | `pyproject.toml` | Only if dev dependency needed for CliRunner (Typer includes it) |

### Files UNCHANGED

- `src/llm_wiki/domain/use_cases/**` — no business logic changes unless blocking bug found (escalate to new story)
- `src/llm_wiki/adapters/storage/**` — no storage changes unless S2-10 port extension landed separately

---

## 8. Acceptance Criteria Checklist

### Phase A: Wiring structure (S16, ADR-005)

- [x] **A1** — `main.py` imports use cases and adapters only for construction; handlers call `execute()` on use case instances
  - Evidence: `scripts/verify-s2-11-cli.sh::handlers_delegate_to_use_cases_A1(bash)`

- [x] **A2** — Stub message `_STUB_MESSAGE` removed; all five subcommands invoke real use cases
  - Evidence: `scripts/verify-s2-11-cli.sh::no_stub_message_A2(bash)`

- [x] **A3** — `build_context()` (or equivalent) is the single adapter assembly point
  - Evidence: `scripts/verify-s2-11-cli.sh::single_wiring_point_A3(bash)`

### Phase B: Vault errors (S3)

- [x] **B1** — Running any subcommand outside vault without `--vault` exits non-zero with guidance text
  - Evidence: `tests/integration/test_cli_commands.py::invalid_vault_exits_s3_B1(pytest)`

- [x] **B2** — Invalid vault attempt does not create `wiki/` artifacts in temp cwd
  - Evidence: `tests/integration/test_cli_commands.py::no_partial_wiki_s3_B2(pytest)`

### Phase C: Validate exit code (S10)

- [x] **C1** — `llm-wiki validate` on initialized hermetic vault exits 0
  - Evidence: `tests/integration/test_cli_commands.py::validate_success_s10_C1(pytest)`

- [x] **C2** — `llm-wiki validate` on vault without wiki exits 1
  - Evidence: `tests/integration/test_cli_commands.py::validate_failure_s10_C2(pytest)`

### Phase D: Init smoke (S1, S2)

- [x] **D1** — `llm-wiki init` creates SCHEMA, index, log in temp vault
  - Evidence: `tests/integration/test_cli_commands.py::init_creates_layout_s1_D1(pytest)`

- [x] **D2** — Second `init` is idempotent (exit 0; no destructive overwrite — inspect file content hash or mtime)
  - Evidence: `tests/integration/test_cli_commands.py::init_idempotent_s2_D2(pytest)`

### Phase E: Ingest / query / lint smoke (S6–S9)

- [x] **E1** — `llm-wiki ingest --batch daily/` with fake LLM exits 0 and writes `.ingested.json` entry
  - Evidence: `tests/integration/test_cli_commands.py::ingest_batch_smoke_s7_E1(pytest)`

- [x] **E2** — `llm-wiki query "question"` with fake LLM presents answer (stdout contains answer substring)
  - Evidence: `tests/integration/test_cli_commands.py::query_smoke_s8_E2(pytest)`

- [x] **E3** — `llm-wiki lint` appends lint log line without modifying wiki pages (page content unchanged)
  - Evidence: `tests/integration/test_cli_commands.py::lint_smoke_s9_E3(pytest)`

### Phase F: Provider wiring (S11, S19)

- [x] **F1** — When no LLM provider available, ingest exits 1 with clear error (monkeypatch config/factory)
  - Evidence: `tests/integration/test_cli_commands.py::no_provider_error_s11_F1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Composition root uses `CLIConfigurationAdapter` — grep confirms no direct `os.environ` in handlers except adapter module
  - Evidence: `scripts/verify-s2-11-cli.sh::config_via_adapter_s19_Y1(bash)`

- [x] **Y2** — **(binding)** Real filesystem + schema adapters used in CLI integration tests (not mocked storage)
  - Evidence: `tests/integration/test_cli_commands.py::real_storage_binding_Y2(pytest)`

- [x] **Y3** — **(binding)** Provider factory invoked from wiring module
  - Evidence: `scripts/verify-s2-11-cli.sh::uses_provider_factory_s11_Y3(bash)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/integration/test_cli_commands.py` passes
- [x] **Z2** — `ruff check .` passes on modified files
- [x] **Z3** — No untyped bare `Any` in new wiring modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — CLI logs subcommand name and exit outcome at info/debug
- [x] **Z6** — `/review-story S2-11` reports zero `high` or `critical` findings

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-s2-11-cli.sh` (static) | A1–A3, Y1, Y3 | S16, S19 | binding script |
| 2 | integration | `tests/integration/test_cli_commands.py::invalid_vault_exits_s3_B1` | B1 | S3 | CliRunner |
| 3 | integration | `tests/integration/test_cli_commands.py::no_partial_wiki_s3_B2` | B2 | S3 | no writes |
| 4 | integration | `tests/integration/test_cli_commands.py::validate_success_s10_C1` | C1 | S10 | exit 0 |
| 5 | integration | `tests/integration/test_cli_commands.py::validate_failure_s10_C2` | C2 | S10 | exit 1 |
| 6 | integration | `tests/integration/test_cli_commands.py::init_creates_layout_s1_D1` | D1 | S1 | init |
| 7 | integration | `tests/integration/test_cli_commands.py::init_idempotent_s2_D2` | D2 | S2 | idempotent |
| 8 | integration | `tests/integration/test_cli_commands.py::ingest_batch_smoke_s7_E1` | E1 | S6, S7, S12 | fake LLM |
| 9 | integration | `tests/integration/test_cli_commands.py::query_smoke_s8_E2` | E2 | S8 | fake LLM |
| 10 | integration | `tests/integration/test_cli_commands.py::lint_smoke_s9_E3` | E3 | S9 | fake LLM |
| 11 | integration | `tests/integration/test_cli_commands.py::no_provider_error_s11_F1` | F1 | S11 | error path |
| 12 | integration | `tests/integration/test_cli_commands.py::real_storage_binding_Y2` | Y2 | S16 | real FS |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Testing CLI with live LLM flaky | Injectable fake LLM at wiring boundary; S2-12 expands coverage |
| 2 | Global Typer callback vs subcommand option timing | Follow S2-5 `CLIConfigurationAdapter` patterns; reuse integration conftest |
| 3 | Circular imports if wiring in main.py grows | Extract `wiring.py` with lazy imports |

---

## Implementation Order

1. `adapters/cli/wiring.py` — `AppContext`, `build_context(overrides=...)`
2. `tests/integration/test_cli_commands.py` — red-first smoke tests
3. `adapters/cli/main.py` — replace stubs, map exit codes
4. `scripts/verify-s2-11-cli.sh`
5. **Verify** — `bash scripts/verify-s2-11-cli.sh && pytest tests/integration/test_cli_commands.py`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `d3fd55a` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-11-cli.sh && pytest tests/integration/test_cli_commands.py && ruff check src/llm_wiki/adapters/cli/` |
| QA result | All 22 criteria PASS (12 pytest + static binding checks) |
| Docs handoff | README: Added `verify-s2-11-cli.sh` to Available Scripts; S2-11 backlog row → Complete |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-06 | Story: S2-11 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
