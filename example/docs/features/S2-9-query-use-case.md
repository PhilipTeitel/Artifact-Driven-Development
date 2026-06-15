# S2-9: Query use case

**Story**: Implement `QueryUseCase` in the domain layer with unit tests using port fakes only, covering REQ-001 scenario **S8** and query log entries per **S13** without real filesystem or LLM I/O.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story delivers **`QueryUseCase`** — domain orchestration that answers natural-language questions using the wiki as the sole knowledge source ([ADR-001](ADR-001-hexagonal-architecture.md), [ADR-002](ADR-002-port-interfaces.md)).

**Index-first navigation (S8):** The use case **must** call `WikiStoragePort.read_index()` before reading any other wiki page. It selects candidate page paths from index content (and question text), reads those pages via `read_wiki_page()`, and passes index + page bodies to `LLMPort.complete()` for synthesis. No vector search, embeddings, or vault source reads (README non-goal; parity with [`.cursor/commands/wiki-query.md`](../../.cursor/commands/wiki-query.md)).

**Answer presentation:** The synthesized answer (with citations to wiki pages) is shown via `UserInteractionPort.present()`.

**Optional filing (S8):** After presenting the answer, the use case calls `UserInteractionPort.confirm()` asking whether to file the answer as a new wiki page. If confirmed, it writes a new page, updates `index.md`, and appends a query log entry (`## [YYYY-MM-DD] query | {title}`). If declined, **no** wiki writes occur after the answer was presented (read-only filing path).

**Testing strategy:** Unit tests use in-memory fakes with deterministic LLM responses. A fake storage pre-seeds `index.md` and wiki pages; tests assert read order (index before pages) via call log.

**Depends on:** [S2-2](S2-2-port-protocols-and-domain-models.md), [S2-3](S2-3-init-and-validate-use-cases.md), [S2-4](S2-4-filesystem-storage-and-schema-adapters.md), [S2-6](S2-6-llm-port-adapters.md), [S2-7](S2-7-terminal-interaction-adapter.md).

**Out of scope:** Typer `query` command wiring (S2-11), CLI integration tests (S2-12), reading vault sources outside wiki for answers (S5), vector RAG, batch/non-interactive query mode (not in REQ-001 v1).

**Guiding constraint:** Filing is opt-in via explicit confirmation; running query alone is not consent to file.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Use case in `domain/use_cases/`; ports only |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | Storage, LLM, interaction, configuration port usage |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Log heading format for query operations (S13) |

---

## 3. Definition of Ready (DoR)

- [ ] Linked ADRs exist and are **Accepted**
- [ ] README, requirements, and Stage 1 query command agree on index-first navigation and filing gate (S8)
- [ ] Section 4 filled from ADR-002/003 and REQ-001 S8, S13
- [ ] Section 4b lists ports consumed (fakes only in tests)
- [ ] Section 8a maps **S8**, **S13** and every AC ID to unit test rows
- [ ] **S5** — query path never reads sources via `read_source` (wiki-only reads)
- [ ] Phase Y **(binding)** criteria cite unit tests with fake call-order evidence

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `QueryUseCase` at `src/llm_wiki/domain/use_cases/query.py`; no adapter imports.
2. **Y2** — Constructor injection: `WikiStoragePort`, `LLMPort`, `UserInteractionPort`, `ConfigurationPort` (for wiki path display in prompts/results).
3. **Y3** — **Index-first:** `read_index()` is the first storage read in `execute()`; no `read_wiki_page` before index (S8).
4. **Y4** — Answer presented via `interaction.present()` before filing prompt (S8).
5. **Y5** — Filing requires `interaction.confirm()` returning true; otherwise no `write_wiki_page`, `write_index`, or `append_log` after answer (S8).
6. **Y6** — On confirm, creates new wiki page with standard markdown links, updates index, appends log with `## [YYYY-MM-DD] query | {title}` (S13).
7. **Y7** — Never calls `read_source()` — answers use wiki pages only (S5 intent for query workflow).
8. **Y8** — No vector/RAG dependencies or imports (README non-goal).

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | *(fake in tests)* | `InMemoryWikiStorageFake` | Real: S2-4 |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | *(fake in tests)* | `InMemoryLLMFake` | Real: S2-6 |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | *(fake in tests)* | interaction fake | Real: S2-7 |
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | *(fake in tests)* | `InMemoryConfigurationFake` | Real: S2-5 |

**Hexagonal note:** Phase Y evidence is unit tests with fakes; real adapter integration deferred to S2-12.

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI wiring in this story.

```python
# src/llm_wiki/domain/models/query_result.py
@dataclass(frozen=True)
class QueryResult:
    answer: str
    citations: tuple[str, ...]   # wiki-relative paths cited
    filed: bool
    filed_page: str | None

# src/llm_wiki/domain/use_cases/query.py
class QueryUseCase:
    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        llm: LLMPort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None: ...

    def execute(self, question: str) -> QueryResult:
        """Answer question from wiki; optional filing on confirm."""
```

Prompt templates in `src/llm_wiki/domain/prompts/query.py` include index + selected pages and require citation paths in the LLM response (parsed by domain helper).

---

## 6. Frontend Flow

Not applicable — domain use case only.

### 6a. Use case orchestration (reference)

```
QueryUseCase.execute(question)
├── storage.read_index()          # MUST be first storage read
├── select pages from index + question
├── storage.read_wiki_page(each)
├── llm.complete(query_prompt)
├── interaction.present(answer)
├── if interaction.confirm("File answer?"):
│   ├── write_wiki_page, write_index, append_log
│   └── return QueryResult(filed=True, ...)
└── else return QueryResult(filed=False, ...)
```

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/domain/use_cases/query.py` | `QueryUseCase` |
| 2 | `src/llm_wiki/domain/prompts/query.py` | Query prompt + citation parser |
| 3 | `src/llm_wiki/domain/models/query_result.py` | `QueryResult` |
| 4 | `tests/unit/test_query_use_case.py` | S8, S13 unit tests |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `src/llm_wiki/domain/use_cases/__init__.py` | Export `QueryUseCase` |
| 2 | `src/llm_wiki/domain/models/__init__.py` | Export `QueryResult` |
| 3 | `README.md` | Link S2-9 backlog row |

### Files UNCHANGED

- `src/llm_wiki/adapters/**` — no adapter changes
- `src/llm_wiki/adapters/cli/main.py` — S2-11

---

## 8. Acceptance Criteria Checklist

### Phase A: Index-first answer (S8)

- [x] **A1** — Storage call log shows `read_index` before any `read_wiki_page` call
  - Evidence: `tests/unit/test_query_use_case.py::index_read_first_s8_A1(pytest)`

- [x] **A2** — Answer includes citations to at least one wiki page path used in synthesis
  - Evidence: `tests/unit/test_query_use_case.py::answer_has_citations_s8_A2(pytest)`

- [x] **A3** — `UserInteractionPort.present()` receives the full answer text before any confirm prompt
  - Evidence: `tests/unit/test_query_use_case.py::presents_before_confirm_s8_A3(pytest)`

### Phase B: Filing gate (S8)

- [x] **B1** — When user confirms filing, use case writes new wiki page, updates index, appends query log entry; `QueryResult.filed is True`
  - Evidence: `tests/unit/test_query_use_case.py::confirm_files_answer_s8_B1(pytest)`

- [x] **B2** — When user declines filing, no wiki writes after present; `QueryResult.filed is False`
  - Evidence: `tests/unit/test_query_use_case.py::decline_no_writes_s8_B2(pytest)`

### Phase C: Log format (S13)

- [x] **C1** — Filed query appends log heading matching `## [YYYY-MM-DD] query |`
  - Evidence: `tests/unit/test_query_use_case.py::query_log_heading_s13_C1(pytest)`

### Phase D: Wiki-only reads (S5)

- [x] **D1** — Execute never calls `read_source` on storage fake
  - Evidence: `tests/unit/test_query_use_case.py::no_source_reads_s5_D1(pytest)`

### Phase E: Domain isolation (S16, S19)

- [x] **E1** — `query.py` has no adapter or `os.environ` imports
  - Evidence: `tests/unit/test_import_boundaries.py::query_use_case_no_adapters_E1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Index-first order enforced — call log assertion fails if reordered
  - Evidence: `tests/unit/test_query_use_case.py::index_first_binding_s8_Y1(pytest)`

- [x] **Y2** — **(binding)** Filing gate — writes only after confirm true
  - Evidence: `tests/unit/test_query_use_case.py::filing_gate_binding_s8_Y2(pytest)`

- [x] **Y3** — **(binding)** No RAG/vector imports in query use case or prompts module
  - Evidence: `tests/unit/test_import_boundaries.py::query_no_rag_imports_Y3(pytest)` or grep in verify script

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/unit/test_query_use_case.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Logs query start, pages read count, filing outcome at info/debug; no full answer body at INFO
- [x] **Z6** — `/review-story S2-9` reports zero `high` or `critical` findings

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | unit | `tests/unit/test_query_use_case.py::index_read_first_s8_A1` | A1 | S8 | call order |
| 2 | unit | `tests/unit/test_query_use_case.py::answer_has_citations_s8_A2` | A2 | S8 | citations |
| 3 | unit | `tests/unit/test_query_use_case.py::presents_before_confirm_s8_A3` | A3 | S8 | present first |
| 4 | unit | `tests/unit/test_query_use_case.py::confirm_files_answer_s8_B1` | B1 | S8, S13 | filing yes |
| 5 | unit | `tests/unit/test_query_use_case.py::decline_no_writes_s8_B2` | B2 | S8 | filing no |
| 6 | unit | `tests/unit/test_query_use_case.py::query_log_heading_s13_C1` | C1 | S13 | log format |
| 7 | unit | `tests/unit/test_query_use_case.py::no_source_reads_s5_D1` | D1 | S5 | wiki only |
| 8 | unit | `tests/unit/test_import_boundaries.py::query_use_case_no_adapters_E1` | E1 | S16 | boundary |
| 9 | unit | `tests/unit/test_query_use_case.py::index_first_binding_s8_Y1` | Y1 | S8 | binding |
| 10 | unit | `tests/unit/test_query_use_case.py::filing_gate_binding_s8_Y2` | Y2 | S8 | binding |
| 11 | unit | `tests/unit/test_import_boundaries.py::query_no_rag_imports_Y3` | Y3 | — | no RAG |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Index-only navigation misses relevant pages not linked | Allow reading additional wiki pages after index if index lists none relevant — document in prompt; empty wiki returns clear message (Stage 1 parity) |
| 2 | LLM citation paths unreliable | Parser validates paths against pages actually read; unit tests use deterministic fake LLM output |

---

## Implementation Order

1. `domain/models/query_result.py` — result type
2. `domain/prompts/query.py` — prompt + page selection helper
3. `tests/unit/test_query_use_case.py` — red-first (S8, S13)
4. `domain/use_cases/query.py` — implement
5. Extend import boundary tests
6. **Verify** — `pytest tests/unit/test_query_use_case.py && ruff check src/llm_wiki/domain/use_cases/query.py`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-06 |
| Completion ref | `86b372d` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `pytest tests/unit/test_query_use_case.py tests/unit/test_import_boundaries.py::query_use_case_no_adapters_E1 tests/unit/test_import_boundaries.py::query_no_rag_imports_Y3 && ruff check src/llm_wiki/domain/use_cases/query.py src/llm_wiki/domain/prompts/query.py src/llm_wiki/domain/models/query_result.py` |
| QA result | All 19 acceptance criteria PASS (11 unit tests + Z1–Z6 quality gates) |
| Docs handoff | README Epic 2 backlog row S2-9 → Complete with verify command |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-06 | Story: S2-9 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
