# S2-8: Ingest use case

**Story**: Implement `IngestUseCase` in the domain layer with unit tests using port fakes only, covering REQ-001 scenarios **S6**, **S7**, **S12**, and **S13** (ingest log heading) without real filesystem or LLM I/O.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Large
**Status**: Complete

---

## 1. Summary

This story delivers **`IngestUseCase`** — the domain orchestration that reads vault sources, invokes the LLM to propose wiki updates, optionally gates writes on user confirmation, and persists wiki pages, `index.md`, `log.md`, and `.ingested.json` through ports only ([ADR-001](ADR-001-hexagonal-architecture.md), [ADR-002](ADR-002-port-interfaces.md), [ADR-003](ADR-003-vault-wiki-layout.md)).

**Interactive ingest (S6):** For a single source file path, the use case reads content via `WikiStoragePort.read_source()`, calls `LLMPort.complete()` with an ingest-oriented prompt (templates in `domain/prompts/`), presents takeaways via `UserInteractionPort.present()`, and waits for `UserInteractionPort.confirm()` before writing wiki artifacts. If the user declines, no wiki writes occur (except none were started).

**Batch ingest (S7):** When `ConfigurationPort.batch_mode` is true and the path is a directory, the use case enumerates markdown files under that directory (via storage listing helpers or explicit directory walk delegated to a small domain helper that filters using `SchemaPort.load().excludes`), skips excluded paths and already-ingested sources (S12), processes each file sequentially without interactive prompts, and reports skipped vs processed counts.

**Sidecar tracking (S12):** After each successful ingest, the use case updates `.ingested.json` via `read_ingested()` / `write_ingested()` with vault-relative forward-slash keys and ISO 8601 UTC timestamps per ADR-003.

**Testing strategy:** Unit tests inject in-memory fakes from `tests/contract/fakes.py` with deterministic `InMemoryLLMFake.responses` keyed by prompt substrings. No real vault, no Typer CLI (S2-11), no filesystem adapter (S2-4) in unit tests.

**Depends on:** [S2-2](S2-2-port-protocols-and-domain-models.md), [S2-3](S2-3-init-and-validate-use-cases.md), [S2-4](S2-4-filesystem-storage-and-schema-adapters.md) (storage contract semantics), [S2-6](S2-6-llm-port-adapters.md), [S2-7](S2-7-terminal-interaction-adapter.md).

**Out of scope:** Typer `ingest` command wiring (S2-11), CLI integration tests (S2-12), real LLM prompt tuning beyond minimal parseable structure, `--force` re-ingest flag, non-markdown sources, modifying source files (S5 enforcement remains in storage adapter; use case must never call write on source paths).

**Guiding constraint:** Behavioral parity with [`.cursor/commands/wiki-ingest.md`](../../.cursor/commands/wiki-ingest.md) and Stage 1 ingest conventions (standard markdown links, log heading format). Use cases accept ports via constructor injection only; no imports from `adapters/` or reads of `os.environ`.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Use case in `domain/use_cases/`; depends on ports only |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `WikiStoragePort`, `LLMPort`, `SchemaPort`, `UserInteractionPort`, `ConfigurationPort` method usage |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | `.ingested.json` shape, log heading format, source immutability, exclude semantics |
| [`docs/decisions/ADR-004-configuration-and-llm-providers.md`](ADR-004-configuration-and-llm-providers.md) | `batch_mode` from configuration port (S7) |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs agree on ingest interactivity, batch mode, sidecar format, and source immutability (S6, S7, S12)
- [x] Section 4 (Binding constraints) filled from ADR-002/003 and REQ-001 S6, S7, S12, S13
- [x] Section 4b lists ports consumed (no new production adapters — fakes only in tests)
- [x] Section 8a maps **S6**, **S7**, **S12**, **S13** and every AC ID to unit test rows
- [x] No production adapters in Section 4b — Phase Y uses unit tests + import boundaries (real adapter proof deferred to S2-12)
- [x] **S5** enforced via use case never calling write methods for source paths; storage fake call log verifies
- [x] Phase Y **(binding)** criteria cite unit tests proving port-only orchestration

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `IngestUseCase` lives at `src/llm_wiki/domain/use_cases/ingest.py` with no adapter imports.
2. **Y2** — Constructor injection: receives `WikiStoragePort`, `LLMPort`, `SchemaPort`, `UserInteractionPort`, and `ConfigurationPort`.
3. **Y3** — Interactive single-file ingest (S6): presents LLM takeaways and requires `confirm()` before any `write_wiki_page`, `write_index`, `append_log`, or `write_ingested` when `batch_mode` is false.
4. **Y4** — Batch directory ingest (S7): when `batch_mode` is true, skips `confirm()` and processes eligible `.md` files sequentially; skips paths matching `SchemaPort.load().excludes`.
5. **Y5** — Already-ingested sources (S12): reads `.ingested.json`; skips sources whose vault-relative key exists; reports skipped paths in result summary.
6. **Y6** — After successful ingest, updates `.ingested.json` with ADR-003 shape (`version: 1`, `sources` map, ISO 8601 UTC timestamp for the source key).
7. **Y7** — Appends log entry with heading `## [YYYY-MM-DD] ingest | {title}` (S13); date uses UTC consistently (match `InitUseCase` convention).
8. **Y8** — Use case never invokes storage write/delete on source paths outside wiki (S5); only `read_source` for sources.
9. **Y9** — All runtime flags (`batch_mode`, paths) read from `ConfigurationPort` only (S19).

---

## 4b. Ports & Adapters

Use cases **consume** ports defined in S2-2; this story adds **no production adapters**. Unit tests use in-memory fakes.

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | *(fake in tests only)* | `tests/contract/fakes.py` `InMemoryWikiStorageFake` | Real adapter: S2-4 |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | *(fake in tests only)* | `InMemoryLLMFake` with keyed responses | Real adapters: S2-6 |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | *(fake in tests only)* | `InMemorySchemaFake` | Real adapter: S2-4 |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | *(fake in tests only)* | fake capturing present/confirm | Real adapter: S2-7 |
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | *(fake in tests only)* | `InMemoryConfigurationFake` with `batch_mode` | Real adapter: S2-5 |

**Hexagonal note:** No integration tests against real filesystem or LLM in this story. Phase Y **(binding)** evidence is unit tests proving use cases honor port contracts and S6/S7/S12 semantics via fakes.

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI wiring in this story.

**Use case public API (Python):**

```python
# src/llm_wiki/domain/models/ingest_result.py
@dataclass(frozen=True)
class IngestResult:
    processed: tuple[str, ...]      # vault-relative source paths ingested
    skipped: tuple[str, ...]       # excluded or already-ingested
    pages_written: tuple[str, ...]  # wiki-relative page paths
    log_appended: bool

# src/llm_wiki/domain/use_cases/ingest.py
class IngestUseCase:
    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        llm: LLMPort,
        schema: SchemaPort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None: ...

    def execute(self, path: str) -> IngestResult:
        """Ingest one source file or directory per S6/S7."""
```

**LLM response convention (v1):** Prompt templates in `src/llm_wiki/domain/prompts/ingest.py` instruct the model to return markdown with labeled sections (`## TAKEAWAYS`, `## WIKI_PAGES`, `## INDEX_UPDATE`) that the use case parses deterministically. Parsing logic lives in the domain layer (unit-tested without LLM).

---

## 6. Frontend Flow

Not applicable — domain use case only; CLI presentation in S2-11.

### 6a. Use case orchestration (reference)

```
IngestUseCase.execute(path)
├── schema.load() -> excludes
├── if path is file:
│   ├── read_source(path)
│   ├── llm.complete(ingest_prompt)
│   ├── if not batch_mode: interaction.present + confirm (abort if false)
│   ├── write_wiki_page(s), write_index, append_log, write_ingested
│   └── return IngestResult
└── if path is directory and batch_mode:
    ├── enumerate *.md under path (respect excludes)
    ├── skip if path in read_ingested().sources
    └── loop single-file flow without confirm
```

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/domain/use_cases/ingest.py` | `IngestUseCase` |
| 2 | `src/llm_wiki/domain/prompts/ingest.py` | Ingest prompt templates + response parser |
| 3 | `src/llm_wiki/domain/models/ingest_result.py` | `IngestResult` dataclass |
| 4 | `tests/unit/test_ingest_use_case.py` | S6, S7, S12, S13 unit tests with fakes |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `src/llm_wiki/domain/use_cases/__init__.py` | Export `IngestUseCase` |
| 2 | `src/llm_wiki/domain/models/__init__.py` | Export `IngestResult` |
| 3 | `tests/contract/fakes.py` | Extend fakes if ingest tests need call tracking (e.g. `source_writes` guard) |
| 4 | `README.md` | Link S2-8 backlog row to this story |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/adapters/**` — no adapter work
- `src/llm_wiki/adapters/cli/main.py` — Typer wiring in S2-11
- `.cursor/commands/wiki-ingest.md` — Stage 1 reference behavior only

---

## 8. Acceptance Criteria Checklist

### Phase A: Interactive single-file ingest (S6)

- [x] **A1** — For a single `.md` source with `batch_mode=False`, use case reads source via `read_source`, calls `LLMPort.complete`, and presents takeaways before any wiki write
  - Evidence: `tests/unit/test_ingest_use_case.py::interactive_presents_before_write_s6_A1(pytest)`

- [x] **A2** — When user confirms, use case writes at least one wiki page, updates `index.md`, appends ingest log entry, and updates `.ingested.json` for the source path
  - Evidence: `tests/unit/test_ingest_use_case.py::confirm_writes_wiki_artifacts_s6_A2(pytest)`

- [x] **A3** — When user declines `confirm()`, no `write_wiki_page`, `write_index`, `append_log`, or `write_ingested` calls occur
  - Evidence: `tests/unit/test_ingest_use_case.py::decline_skips_writes_s6_A3(pytest)`

### Phase B: Batch directory ingest (S7)

- [x] **B1** — With `batch_mode=True` and directory path, processes all eligible `.md` files without calling `confirm()`
  - Evidence: `tests/unit/test_ingest_use_case.py::batch_no_confirm_s7_B1(pytest)`

- [x] **B2** — Skips files matching schema excludes; skipped paths appear in `IngestResult.skipped`
  - Evidence: `tests/unit/test_ingest_use_case.py::batch_skips_excludes_s7_B2(pytest)`

- [x] **B3** — Each processed file produces wiki updates and a log append (count matches processed sources)
  - Evidence: `tests/unit/test_ingest_use_case.py::batch_each_file_logged_s7_B3(pytest)`

### Phase C: Ingested sidecar (S12)

- [x] **C1** — After successful ingest, `.ingested.json` contains source key with ISO 8601 UTC timestamp
  - Evidence: `tests/unit/test_ingest_use_case.py::ingested_sidecar_updated_s12_C1(pytest)`

- [x] **C2** — Batch re-run skips already-ingested source; reports in `IngestResult.skipped` without duplicate wiki writes for that source
  - Evidence: `tests/unit/test_ingest_use_case.py::batch_skips_ingested_s12_C2(pytest)`

### Phase D: Log format and immutability (S13, S5)

- [x] **D1** — Appended log entry first line matches `## [YYYY-MM-DD] ingest |` pattern
  - Evidence: `tests/unit/test_ingest_use_case.py::ingest_log_heading_s13_D1(pytest)`

- [x] **D2** — Storage fake call log shows `read_source` for source path but never `write_wiki_page` or equivalent for a source path outside wiki
  - Evidence: `tests/unit/test_ingest_use_case.py::no_source_writes_s5_D2(pytest)`

### Phase E: Domain isolation (S16, S19)

- [x] **E1** — `ingest.py` contains no imports from `llm_wiki.adapters` or `os.environ`
  - Evidence: `tests/unit/test_import_boundaries.py::ingest_use_case_no_adapters_E1(pytest)`

- [x] **E2** — Batch vs interactive behavior driven solely by `config.batch_mode`, not hard-coded flags
  - Evidence: `tests/unit/test_ingest_use_case.py::batch_mode_from_config_s19_E2(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** `IngestUseCase` orchestrates only through port methods — fake call log proves no direct I/O imports in use case module
  - Evidence: `tests/unit/test_ingest_use_case.py::ingest_port_only_s16_Y1(pytest)`

- [x] **Y2** — **(binding)** `.ingested.json` updates match ADR-003 shape via fake storage
  - Evidence: `tests/unit/test_ingest_use_case.py::ingested_shape_binding_s12_Y2(pytest)`

- [x] **Y3** — **(binding)** Interactive gate matches S6 — writes occur only after confirm when not batch
  - Evidence: `tests/unit/test_ingest_use_case.py::interactive_gate_binding_s6_Y3(pytest)`

- [x] **Y4** — **(binding)** Batch skip of ingested sources matches S12
  - Evidence: `tests/unit/test_ingest_use_case.py::skip_ingested_binding_s12_Y4(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/unit/test_ingest_use_case.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new use case modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Use case logs ingest start/complete and skip reasons at `info`/`debug` via `llm_wiki.domain` logger; never logs full LLM prompts at INFO
- [x] **Z6** — `/review-story S2-8` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | unit | `tests/unit/test_ingest_use_case.py::interactive_presents_before_write_s6_A1` | A1 | S6 | happy path gate |
| 2 | unit | `tests/unit/test_ingest_use_case.py::confirm_writes_wiki_artifacts_s6_A2` | A2 | S6 | writes all artifacts |
| 3 | unit | `tests/unit/test_ingest_use_case.py::decline_skips_writes_s6_A3` | A3 | S6 | no writes on decline |
| 4 | unit | `tests/unit/test_ingest_use_case.py::batch_no_confirm_s7_B1` | B1 | S7 | batch mode |
| 5 | unit | `tests/unit/test_ingest_use_case.py::batch_skips_excludes_s7_B2` | B2 | S7 | schema excludes |
| 6 | unit | `tests/unit/test_ingest_use_case.py::batch_each_file_logged_s7_B3` | B3 | S7, S13 | per-file log |
| 7 | unit | `tests/unit/test_ingest_use_case.py::ingested_sidecar_updated_s12_C1` | C1 | S12 | sidecar write |
| 8 | unit | `tests/unit/test_ingest_use_case.py::batch_skips_ingested_s12_C2` | C2 | S12 | idempotent batch |
| 9 | unit | `tests/unit/test_ingest_use_case.py::ingest_log_heading_s13_D1` | D1 | S13 | log prefix |
| 10 | unit | `tests/unit/test_ingest_use_case.py::no_source_writes_s5_D2` | D2 | S5 | immutability |
| 11 | unit | `tests/unit/test_import_boundaries.py::ingest_use_case_no_adapters_E1` | E1 | S16 | static boundary |
| 12 | unit | `tests/unit/test_ingest_use_case.py::batch_mode_from_config_s19_E2` | E2 | S19 | config port |
| 13 | unit | `tests/unit/test_ingest_use_case.py::ingest_port_only_s16_Y1` | Y1 | S16 | binding |
| 14 | unit | `tests/unit/test_ingest_use_case.py::ingested_shape_binding_s12_Y2` | Y2 | S12 | binding |
| 15 | unit | `tests/unit/test_ingest_use_case.py::interactive_gate_binding_s6_Y3` | Y3 | S6 | binding |
| 16 | unit | `tests/unit/test_ingest_use_case.py::skip_ingested_binding_s12_Y4` | Y4 | S12 | binding |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | LLM free-text responses hard to parse reliably | Constrain v1 with labeled markdown sections; unit tests use fixed fake responses; parser tested independently |
| 2 | Directory enumeration without `list_sources()` filter | Domain helper filters paths under requested directory using schema excludes; document assumption that storage `list_sources()` is vault-wide (filter locally) |
| 3 | Prompt templates drift from Stage 1 command behavior | Cross-reference `.cursor/commands/wiki-ingest.md`; S2-12 CLI integration validates parity |

---

## Implementation Order

1. `src/llm_wiki/domain/models/ingest_result.py` — result type (covers A2, C1)
2. `src/llm_wiki/domain/prompts/ingest.py` — prompt + parser with unit tests inline or separate (covers A1)
3. `tests/unit/test_ingest_use_case.py` — red-first tests for S6, S7, S12 (covers Phase A–C)
4. `src/llm_wiki/domain/use_cases/ingest.py` — implement to green (covers all phases)
5. Extend `tests/unit/test_import_boundaries.py` for E1
6. **Verify** — `pytest tests/unit/test_ingest_use_case.py tests/unit/test_import_boundaries.py && ruff check src/llm_wiki/domain/use_cases/ingest.py`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-06 |
| Completion ref | `dbcbed7` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `pytest tests/unit/test_ingest_use_case.py tests/unit/test_import_boundaries.py::ingest_use_case_no_adapters_E1 && ruff check src/llm_wiki/domain/use_cases/ingest.py src/llm_wiki/domain/prompts/ src/llm_wiki/domain/models/ingest_result.py` |
| QA result | All 22 acceptance criteria PASS (16 unit tests + Z1–Z6 quality gates) |
| Docs handoff | README Epic 2 backlog row S2-8 → Complete with verify command |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-06 | Story: S2-8 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
