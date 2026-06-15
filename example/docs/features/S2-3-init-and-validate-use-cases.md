# S2-3: Init and Validate use cases

**Story**: Implement `InitUseCase` and `ValidateUseCase` in the domain layer with unit tests using port fakes only, covering REQ-001 scenarios **S1**, **S2**, and **S10** without real filesystem or LLM I/O.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story delivers the first **domain use cases** for Stage 2: wiki initialization and vault/wiki layout validation. Stage 1 already implements init behavior via the `/init-wiki` Cursor command; Stage 2 must encode the same contracts in testable Python orchestration behind ports ([ADR-001](ADR-001-hexagonal-architecture.md), [ADR-002](ADR-002-port-interfaces.md)).

**`InitUseCase`** (S1, S2): Delegates idempotent layout creation to `WikiStoragePort.ensure_wiki_layout()`, appends an init log entry via `WikiStoragePort.append_log()` using the ADR-003 heading format, and reports created vs already-present artifacts through `UserInteractionPort.present()`. It must not write outside the wiki subdirectory (enforced by port contract; real enforcement ships in S2-4 adapter).

**`ValidateUseCase`** (S10): Inspects wiki layout via `WikiStoragePort` and `SchemaPort`, aggregates `ValidationIssue` entries into a `ValidationResult`, and exposes whether the vault conforms (for CLI exit code wiring in S2-11). Validation names each missing or malformed required piece.

**Testing strategy:** Unit tests inject **in-memory port fakes** from S2-2 (`tests/contract/fakes.py` or dedicated `tests/unit/fakes/`). No real vault, no Typer CLI wiring, no `CLIConfigurationAdapter` (S2-5), no filesystem adapter (S2-4).

**Depends on:** [S2-1](S2-1-python-package-scaffold.md), [S2-2](S2-2-port-protocols-and-domain-models.md).

**Out of scope:** Vault walk-up / invalid vault errors (S3 → S2-5), real template copy from `templates/wiki/*` (S2-4), LLM calls, ingest/query/lint use cases, Typer command wiring (S2-11), CLI integration tests (S2-12).

**Guiding constraint:** Use cases accept ports via constructor injection only; no imports from `adapters/` or reads of `os.environ`.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Use cases live in `domain/use_cases/`; depend on ports only |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `InitUseCase` / `ValidateUseCase` call `WikiStoragePort`, `SchemaPort`, `UserInteractionPort`, `ConfigurationPort` as needed |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Required init artifacts (`SCHEMA.md`, `index.md`, `log.md`), idempotent rules (S2), log heading format (S13 for init log line) |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs agree on init artifacts, idempotent init, and validate behavior (S1, S2, S10)
- [x] Section 4 (Binding constraints) filled from ADR-002/003 and REQ-001 S1, S2, S10
- [x] Section 4b lists ports consumed (no new adapters — fakes only in tests)
- [x] Section 8a maps **S1**, **S2**, **S10** and every AC ID to unit test rows
- [x] No production adapters in Section 4b — integration tests deferred to S2-4/S2-12; Phase Y uses unit tests + import boundaries
- [x] **S3**, **S5**, **S13** partially touched (log format in init append); vault detection and real immutability explicitly deferred
- [x] Phase Y **(binding)** criteria cite unit tests proving port-only orchestration

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `InitUseCase` and `ValidateUseCase` live under `src/llm_wiki/domain/use_cases/` with no adapter imports.
2. **Y2** — Constructor injection: use cases receive port instances (`WikiStoragePort`, `SchemaPort`, `UserInteractionPort`, and `ConfigurationPort` if needed for `wiki_dir` display paths).
3. **Y3** — Init invokes `WikiStoragePort.ensure_wiki_layout()` exactly once per run; interprets `InitResult.created` vs `InitResult.already_present` for user report (S1, S2).
4. **Y4** — Init appends log entry with heading matching `## [YYYY-MM-DD] init | {title}` (ADR-003 / S13) via `append_log`; date is UTC or local consistently documented in use case docstring.
5. **Y5** — Init does **not** create `.ingested.json` (ADR-003 — first ingest only).
6. **Y6** — Validate returns `ValidationResult` with `valid=False` when any required artifact missing (`SCHEMA.md`, `index.md`, `log.md` under wiki root) or `wiki_exists()` is false (S10).
7. **Y7** — Validate lists **each** issue with stable `code` and human `message` naming what is wrong (S10).
8. **Y8** — Use cases never call `os.environ`, Typer, or filesystem libraries directly (S19).

---

## 4b. Ports & Adapters

Use cases **consume** ports defined in S2-2; this story adds **no production adapters**. Unit tests use in-memory fakes.

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | *(fake in tests only)* | `tests/contract/fakes.py` or `tests/unit/fakes/storage.py` | Real adapter: S2-4 |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | *(fake in tests only)* | in-memory fake | Real adapter: S2-4 |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | *(fake in tests only)* | in-memory fake capturing `present()` calls | Real adapter: S2-7 |
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | *(fake in tests only)* | in-memory fake with fixed `vault_root` / `wiki_dir` | Real adapter: S2-5 |

**Hexagonal note:** No integration tests against real filesystem in this story. Phase Y **(binding)** evidence is unit tests proving use cases honor port contracts and S1/S2/S10 semantics via fakes.

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI wiring in this story.

**Use case public API (Python):**

```python
# src/llm_wiki/domain/use_cases/init.py
class InitUseCase:
    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None: ...

    def execute(self) -> InitResult:
        """Initialize wiki layout idempotently; append init log; present summary."""

# src/llm_wiki/domain/use_cases/validate.py
class ValidateUseCase:
    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        schema: SchemaPort,
        config: ConfigurationPort,
    ) -> None: ...

    def execute(self) -> ValidationResult:
        """Check vault/wiki layout; return issues for S10."""
```

Return types reuse `InitResult` and `ValidationResult` from S2-2 domain models.

---

## 6. Frontend Flow

Not applicable — domain use cases only; CLI presentation in S2-11.

### 6a. Use case orchestration (reference)

```
InitUseCase.execute()
├── storage.ensure_wiki_layout() -> InitResult
├── storage.append_log("## [date] init | …")
└── interaction.present(summary of created vs already_present)

ValidateUseCase.execute()
├── if not storage.wiki_exists(): issue missing_wiki
├── check SCHEMA.md, index.md, log.md readable via storage/schema
└── return ValidationResult(valid=len(issues)==0, issues=…)
```

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/domain/use_cases/init.py` | `InitUseCase` |
| 2 | `src/llm_wiki/domain/use_cases/validate.py` | `ValidateUseCase` |
| 3 | `src/llm_wiki/domain/use_cases/__init__.py` | Re-export use case classes |
| 4 | `tests/unit/test_init_use_case.py` | S1, S2 unit tests with fakes |
| 5 | `tests/unit/test_validate_use_case.py` | S10 unit tests with fakes |
| 6 | `tests/unit/fakes/__init__.py` | Optional dedicated fakes if not reusing contract fakes |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/fakes.py` | Extend storage fake if init/validate need behaviors not yet in S2-2 fakes |
| 2 | `README.md` | Link S2-3 backlog row to this story |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/adapters/**` — no adapter work
- `templates/wiki/*` — copied by filesystem adapter in S2-4
- `.cursor/commands/init-wiki.md` — Stage 1 reference behavior only

---

## 8. Acceptance Criteria Checklist

### Phase A: InitUseCase — fresh layout (S1)

- [x] **A1** — On empty wiki (fake reports all artifacts missing), `InitUseCase.execute()` returns `InitResult` with `created` containing `SCHEMA.md`, `index.md`, `log.md` (or equivalent relative paths) and empty `already_present`
  - Evidence: `tests/unit/test_init_use_case.py::fresh_init_creates_layout_s1_A1(pytest)`

- [x] **A2** — After execute, fake storage records an appended log entry whose first line matches `## [YYYY-MM-DD] init |` pattern
  - Evidence: `tests/unit/test_init_use_case.py::appends_init_log_s13_A2(pytest)`

- [x] **A3** — `UserInteractionPort.present()` receives a summary mentioning created paths (S1 “reports what was created”)
  - Evidence: `tests/unit/test_init_use_case.py::presents_created_summary_s1_A3(pytest)`

### Phase B: InitUseCase — idempotent init (S2)

- [x] **B1** — When fake reports all required artifacts already present, `InitResult.already_present` lists them and `created` is empty; no overwrite calls on fake
  - Evidence: `tests/unit/test_init_use_case.py::idempotent_skips_existing_s2_B1(pytest)`

- [x] **B2** — Partial layout (only `SCHEMA.md` exists): `created` lists only missing files (`index.md`, `log.md`); existing `SCHEMA.md` appears in `already_present`
  - Evidence: `tests/unit/test_init_use_case.py::partial_init_creates_missing_s2_B2(pytest)`

- [x] **B3** — Idempotent re-run does not duplicate wiki page content in fake (no extra writes to pre-existing page paths)
  - Evidence: `tests/unit/test_init_use_case.py::no_overwrite_wiki_pages_s2_B3(pytest)`

### Phase C: InitUseCase — constraints

- [x] **C1** — Init does not invoke ingested sidecar write methods (no `.ingested.json` at init)
  - Evidence: `tests/unit/test_init_use_case.py::no_ingested_sidecar_at_init_C1(pytest)`

### Phase D: ValidateUseCase (S10)

- [x] **D1** — Valid complete layout: `ValidationResult.valid is True` and `issues` empty
  - Evidence: `tests/unit/test_validate_use_case.py::valid_layout_s10_D1(pytest)`

- [x] **D2** — Missing `SCHEMA.md`: `valid is False`, issue code/message names missing schema
  - Evidence: `tests/unit/test_validate_use_case.py::missing_schema_s10_D2(pytest)`

- [x] **D3** — Missing `index.md` and `log.md`: separate issues for each missing piece (S10 “names what is wrong”)
  - Evidence: `tests/unit/test_validate_use_case.py::multiple_issues_named_s10_D3(pytest)`

- [x] **D4** — Wiki directory absent (`wiki_exists()` false): validation fails with issue describing missing wiki layout
  - Evidence: `tests/unit/test_validate_use_case.py::no_wiki_dir_s10_D4(pytest)`

### Phase E: Domain isolation (S16, S19)

- [x] **E1** — Use case modules contain no imports from `llm_wiki.adapters` or `os.environ`
  - Evidence: `tests/unit/test_import_boundaries.py::use_cases_no_adapters_E1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** `InitUseCase` uses only port methods — unit test spy fake confirms no direct filesystem/HTTP imports in use case module
  - Evidence: `tests/unit/test_init_use_case.py::init_port_only_s16_Y1(pytest)`

- [x] **Y2** — **(binding)** Idempotent init behavior matches ADR-003 S2 rules via fake storage call log
  - Evidence: `tests/unit/test_init_use_case.py::idempotent_binding_s2_Y2(pytest)`

- [x] **Y3** — **(binding)** Init log heading format matches ADR-003 / S13 pattern
  - Evidence: `tests/unit/test_init_use_case.py::log_format_binding_s13_Y3(pytest)`

- [x] **Y4** — **(binding)** `ValidateUseCase` failure paths produce named issues suitable for CLI non-zero exit in S2-11
  - Evidence: `tests/unit/test_validate_use_case.py::validate_binding_s10_Y4(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/unit/test_init_use_case.py tests/unit/test_validate_use_case.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new use case modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Use cases log significant failures at `warning`/`error` via `llm_wiki.domain` logger (e.g. validation failure summary at debug/info — no vault paths with secrets)
- [x] **Z6** — `/review-story S2-3` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | unit | `tests/unit/test_init_use_case.py::fresh_init_creates_layout_s1_A1` | A1, Y1 | S1 | port fakes |
| 2 | unit | `tests/unit/test_init_use_case.py::appends_init_log_s13_A2` | A2, Y3 | S13 | log heading |
| 3 | unit | `tests/unit/test_init_use_case.py::presents_created_summary_s1_A3` | A3 | S1 | interaction fake |
| 4 | unit | `tests/unit/test_init_use_case.py::idempotent_skips_existing_s2_B1` | B1, Y2 | S2 | |
| 5 | unit | `tests/unit/test_init_use_case.py::partial_init_creates_missing_s2_B2` | B2, Y2 | S2 | |
| 6 | unit | `tests/unit/test_init_use_case.py::no_overwrite_wiki_pages_s2_B3` | B3 | S2, S5 | fake enforces no overwrite |
| 7 | unit | `tests/unit/test_init_use_case.py::no_ingested_sidecar_at_init_C1` | C1 | S1 | ADR-003 |
| 8 | unit | `tests/unit/test_validate_use_case.py::valid_layout_s10_D1` | D1, Y4 | S10 | |
| 9 | unit | `tests/unit/test_validate_use_case.py::missing_schema_s10_D2` | D2, Y4 | S10 | |
| 10 | unit | `tests/unit/test_validate_use_case.py::multiple_issues_named_s10_D3` | D3, Y4 | S10 | |
| 11 | unit | `tests/unit/test_validate_use_case.py::no_wiki_dir_s10_D4` | D4, Y4 | S10 | |
| 12 | unit | `tests/unit/test_import_boundaries.py::use_cases_no_adapters_E1` | E1, Y1 | S16, S19 | extend S2-2 test |

**Out of scope Sn (explicit):** **S3** (invalid vault — S2-5), **S4** (schema content — S2-4 parser + templates), **S5** (real filesystem immutability — S2-4; fake simulates only), **S6–S9**, **S11–S12**, **S14–S19**, **S18**.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Init logic split between use case and `ensure_wiki_layout` adapter | Keep template copy/idempotency in storage adapter (S2-4); use case orchestrates log + user report only |
| 2 | Validate rules diverge from Stage 1 `/init-wiki` | Cross-check required file list against ADR-003 and S1-2 command table |
| 3 | Log date timezone ambiguity | Document and test one convention (UTC ISO date in heading) |

---

## Implementation Order

1. Extend `tests/contract/fakes.py` (or `tests/unit/fakes/`) for init/validate scenarios (covers fake prerequisites)
2. `src/llm_wiki/domain/use_cases/init.py` — `InitUseCase` (covers A1–C1, Y1–Y3)
3. `tests/unit/test_init_use_case.py` — red-first tests for S1, S2, S13 log (covers Phase A–C)
4. `src/llm_wiki/domain/use_cases/validate.py` — `ValidateUseCase` (covers D1–D4, Y4)
5. `tests/unit/test_validate_use_case.py` — red-first S10 tests
6. Extend `tests/unit/test_import_boundaries.py` for use_cases package (covers E1)
7. **Verify** — `pytest tests/unit/test_init_use_case.py tests/unit/test_validate_use_case.py tests/unit/test_import_boundaries.py && ruff check .`
8. `README.md` — backlog link

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-05` |
| Completion ref | `7efa2e3` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `pytest tests/unit/test_init_use_case.py tests/unit/test_validate_use_case.py tests/unit/test_import_boundaries.py::use_cases_no_adapters_E1 && ruff check .` |
| QA result | `16/16 criteria PASS (A1–E1, Y1–Y4, Z1–Z6)` |
| Docs handoff | `README.md` Epic 2 backlog row S2-3 marked **Done** with verify command; no setup/env/runbook changes required |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-3 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
