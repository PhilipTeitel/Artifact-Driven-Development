# S2-10: Lint use case

**Story**: Implement `LintUseCase` in the domain layer with unit tests using port fakes only, covering REQ-001 scenarios **S9** and lint log entries per **S13** without auto-applying fixes or real filesystem/LLM I/O.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story delivers **`LintUseCase`** — domain orchestration that health-checks the wiki, prints a human-readable report with suggested fixes, and appends a lint log entry without modifying wiki page bodies or `index.md` ([ADR-001](ADR-001-hexagonal-architecture.md), [ADR-002](ADR-002-port-interfaces.md)).

**Lint workflow (S9):** The use case reads `index.md`, enumerates wiki pages (via new `WikiStoragePort.list_wiki_pages()` — backward-compatible method addition per ADR-002), loads page contents, and sends them to `LLMPort.complete()` with a lint-oriented prompt covering the five Stage 1 categories: contradictions, stale claims, orphan pages, missing concept pages, and broken/missing cross-references (parity with [`.cursor/commands/wiki-lint.md`](../../.cursor/commands/wiki-lint.md)).

**Report-only (S9):** Findings and **Suggestion:** lines are presented via `UserInteractionPort.present()`. The use case must **not** call `write_wiki_page` or `write_index` during lint — only `append_log` after the report.

**Port extension:** Add `list_wiki_pages() -> list[str]` to `WikiStoragePort`, implement in `FilesystemWikiStorageAdapter` (S2-4), `InMemoryWikiStorageFake`, and extend storage contract tests. Paths are wiki-relative, excluding `SCHEMA.md`, `log.md`, and `.ingested.json` from the lint scan set (configurable constant in domain).

**Testing strategy:** Unit tests with fakes and deterministic LLM lint reports. No Typer wiring (S2-11), no CLI integration (S2-12).

**Depends on:** [S2-2](S2-2-port-protocols-and-domain-models.md), [S2-3](S2-3-init-and-validate-use-cases.md), [S2-4](S2-4-filesystem-storage-and-schema-adapters.md) (adapter update for `list_wiki_pages`), [S2-6](S2-6-llm-port-adapters.md).

**Out of scope:** Auto-fixing wiki pages, Typer `lint` command (S2-11), terminal interaction beyond present (S2-7 already ships adapter), lint focus filter CLI flag (optional future; v1 full lint only).

**Guiding constraint:** Lint is suggest-only — the only wiki mutation is append-only `log.md` entry.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Use case + port extension in domain/ports |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `list_wiki_pages()` addition; LLM + storage usage |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Log heading `lint` operation (S13) |

---

## 3. Definition of Ready (DoR)

- [ ] Linked ADRs exist and are **Accepted**
- [ ] README and REQ-001 S9 agree: report + suggest only, log append allowed, no page rewrites
- [ ] Section 4 filled; Section 4b includes `list_wiki_pages` port extension + filesystem adapter update
- [ ] Section 8a maps **S9**, **S13** and every AC ID; storage contract + integration rows for new port method
- [ ] Phase Y cites storage integration test for `list_wiki_pages` on real filesystem adapter
- [ ] **S5** — lint never reads or writes vault sources outside wiki

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `LintUseCase` at `src/llm_wiki/domain/use_cases/lint.py`; no adapter imports in use case.
2. **Y2** — Constructor injection: `WikiStoragePort`, `LLMPort`, `UserInteractionPort`, `ConfigurationPort`.
3. **Y3** — Produces report via `present()` covering S9 categories (structured in LLM prompt; parsed into `LintFinding` list).
4. **Y4** — Does **not** call `write_wiki_page` or `write_index` (S9 no auto-fix).
5. **Y5** — Appends log entry `## [YYYY-MM-DD] lint | {title}` after report (S13).
6. **Y6** — `WikiStoragePort.list_wiki_pages()` returns wiki-relative `.md` paths excluding schema/log sidecar artifacts.
7. **Y7** — `FilesystemWikiStorageAdapter.list_wiki_pages()` walks wiki directory on disk (real listing — no mock in integration test).
8. **Y8** — Never calls `read_source()` (wiki-only scan).

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | `FilesystemWikiStorageAdapter` — **modify** | Hermetic temp vault (`tests/integration/conftest.py` `vault_tmp`) | add `list_wiki_pages` |
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | *(fake in unit tests)* | `InMemoryWikiStorageFake` | extend fake |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | *(fake in unit tests)* | `InMemoryLLMFake` | Real: S2-6 |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | *(fake in unit tests)* | interaction fake | Real: S2-7 |
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | *(fake in unit tests)* | `InMemoryConfigurationFake` | Real: S2-5 |

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI wiring in this story.

```python
# src/llm_wiki/domain/models/lint_result.py
@dataclass(frozen=True)
class LintFinding:
    category: str          # contradiction | stale | orphan | missing_concept | broken_link
    location: str          # wiki-relative path
    description: str
    suggestion: str

@dataclass(frozen=True)
class LintResult:
    findings: tuple[LintFinding, ...]
    report: str            # full text presented to user
    log_appended: bool

# src/llm_wiki/ports/storage.py — ADD method:
def list_wiki_pages(self) -> list[str]: ...

# src/llm_wiki/domain/use_cases/lint.py
class LintUseCase:
    def execute(self) -> LintResult: ...
```

---

## 6. Frontend Flow

Not applicable — domain use case only.

### 6a. Use case orchestration (reference)

```
LintUseCase.execute()
├── read_index()
├── list_wiki_pages() -> read each page
├── llm.complete(lint_prompt)
├── interaction.present(report)
└── append_log(lint heading)   # no write_wiki_page / write_index
```

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/domain/use_cases/lint.py` | `LintUseCase` |
| 2 | `src/llm_wiki/domain/prompts/lint.py` | Lint prompt + findings parser |
| 3 | `src/llm_wiki/domain/models/lint_result.py` | `LintFinding`, `LintResult` |
| 4 | `tests/unit/test_lint_use_case.py` | S9, S13 unit tests |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `src/llm_wiki/ports/storage.py` | Add `list_wiki_pages()` to protocol |
| 2 | `src/llm_wiki/adapters/storage/filesystem.py` | Implement `list_wiki_pages()` |
| 3 | `tests/contract/fakes.py` | Fake `list_wiki_pages()` from `wiki_pages` keys |
| 4 | `tests/contract/test_storage_port_contract.py` | Assert method exists; fake + filesystem coverage |
| 5 | `tests/integration/test_filesystem_wiki_storage.py` | Integration test for `list_wiki_pages` |
| 6 | `src/llm_wiki/domain/use_cases/__init__.py` | Export `LintUseCase` |
| 7 | `src/llm_wiki/domain/models/__init__.py` | Export lint models |
| 8 | `README.md` | Link S2-10 backlog row |

### Files UNCHANGED

- `src/llm_wiki/adapters/cli/main.py` — S2-11
- `.cursor/commands/wiki-lint.md` — Stage 1 reference

---

## 8. Acceptance Criteria Checklist

### Phase A: Report generation (S9)

- [x] **A1** — Use case reads index and all listable wiki pages before LLM call
  - Evidence: `tests/unit/test_lint_use_case.py::reads_index_and_pages_s9_A1(pytest)`

- [x] **A2** — Report text includes at least one **Suggestion:** line per finding from fake LLM output
  - Evidence: `tests/unit/test_lint_use_case.py::report_has_suggestions_s9_A2(pytest)`

- [x] **A3** — Clean wiki (no findings) still produces success report and log append
  - Evidence: `tests/unit/test_lint_use_case.py::clean_wiki_report_s9_A3(pytest)`

### Phase B: No auto-fix (S9)

- [x] **B1** — After execute, storage fake shows no `write_wiki_page` or `write_index` calls
  - Evidence: `tests/unit/test_lint_use_case.py::no_page_writes_s9_B1(pytest)`

- [x] **B2** — Only `append_log` mutates wiki state besides reads
  - Evidence: `tests/unit/test_lint_use_case.py::only_log_append_s9_B2(pytest)`

### Phase C: Log format (S13)

- [x] **C1** — Appended log heading matches `## [YYYY-MM-DD] lint |`
  - Evidence: `tests/unit/test_lint_use_case.py::lint_log_heading_s13_C1(pytest)`

### Phase D: Port extension

- [x] **D1** — `WikiStoragePort` defines `list_wiki_pages` per ADR-002
  - Evidence: `tests/contract/test_storage_port_contract.py::list_wiki_pages_method_D1(pytest)`

- [x] **D2** — `FilesystemWikiStorageAdapter.list_wiki_pages()` returns seeded pages in integration fixture
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::list_wiki_pages_D2(pytest)`

### Phase E: Domain isolation (S16)

- [x] **E1** — `lint.py` has no adapter imports
  - Evidence: `tests/unit/test_import_boundaries.py::lint_use_case_no_adapters_E1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** No auto-fix — unit test call log proves zero page/index writes
  - Evidence: `tests/unit/test_lint_use_case.py::no_autofix_binding_s9_Y1(pytest)`

- [x] **Y2** — **(binding)** Real filesystem adapter implements `list_wiki_pages` against temp vault
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::list_wiki_pages_binding_Y2(pytest)`

- [x] **Y3** — **(binding)** Storage contract passes for fake and filesystem adapter with new method
  - Evidence: `tests/contract/test_storage_port_contract.py::list_wiki_pages_contract_Y3(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/unit/test_lint_use_case.py tests/contract/test_storage_port_contract.py tests/integration/test_filesystem_wiki_storage.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Logs lint start, page count, finding count at info/debug
- [x] **Z6** — `/review-story S2-10` reports zero `high` or `critical` findings

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | unit | `tests/unit/test_lint_use_case.py::reads_index_and_pages_s9_A1` | A1 | S9 | read set |
| 2 | unit | `tests/unit/test_lint_use_case.py::report_has_suggestions_s9_A2` | A2 | S9 | suggestions |
| 3 | unit | `tests/unit/test_lint_use_case.py::clean_wiki_report_s9_A3` | A3 | S9 | empty ok |
| 4 | unit | `tests/unit/test_lint_use_case.py::no_page_writes_s9_B1` | B1 | S9 | no fix |
| 5 | unit | `tests/unit/test_lint_use_case.py::only_log_append_s9_B2` | B2 | S9 | log only |
| 6 | unit | `tests/unit/test_lint_use_case.py::lint_log_heading_s13_C1` | C1 | S13 | log format |
| 7 | contract | `tests/contract/test_storage_port_contract.py::list_wiki_pages_method_D1` | D1 | S16 | port shape |
| 8 | integration | `tests/integration/test_filesystem_wiki_storage.py::list_wiki_pages_D2` | D2, Y2 | S9 | real FS |
| 9 | unit | `tests/unit/test_import_boundaries.py::lint_use_case_no_adapters_E1` | E1 | S16 | boundary |
| 10 | unit | `tests/unit/test_lint_use_case.py::no_autofix_binding_s9_Y1` | Y1 | S9 | binding |
| 11 | contract | `tests/contract/test_storage_port_contract.py::list_wiki_pages_contract_Y3` | Y3 | S16 | binding |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Port method addition touches S2-4 adapter | Keep change minimal; extend contract + integration tests in same story |
| 2 | LLM lint quality variable | v1 focuses on orchestration + report structure; deterministic fakes for unit proof |
| 3 | Large wikis exceed context | Document truncation strategy in prompt (e.g. cap pages in v1); optional follow-up story |

---

## Implementation Order

1. Add `list_wiki_pages()` to port, fake, filesystem adapter + contract/integration tests (D1, D2, Y2, Y3)
2. `domain/models/lint_result.py`
3. `domain/prompts/lint.py`
4. `tests/unit/test_lint_use_case.py` — red-first
5. `domain/use_cases/lint.py`
6. **Verify** — `pytest tests/unit/test_lint_use_case.py tests/integration/test_filesystem_wiki_storage.py tests/contract/test_storage_port_contract.py`

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-06-06 |
| Completion ref | `e451cad` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `pytest tests/unit/test_lint_use_case.py tests/contract/test_storage_port_contract.py::list_wiki_pages_method_D1 tests/contract/test_storage_port_contract.py::list_wiki_pages_contract_Y3 tests/integration/test_filesystem_wiki_storage.py::list_wiki_pages_D2 tests/integration/test_filesystem_wiki_storage.py::list_wiki_pages_binding_Y2 tests/unit/test_import_boundaries.py::lint_use_case_no_adapters_E1 && ruff check src/llm_wiki/domain/use_cases/lint.py src/llm_wiki/domain/prompts/lint.py src/llm_wiki/domain/models/lint_result.py` |
| QA result | All 19 acceptance criteria PASS (12 tests + Z1–Z6 quality gates) |
| Docs handoff | README Epic 2 backlog row S2-10 → Complete with verify command |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-06 | Story: S2-10 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
