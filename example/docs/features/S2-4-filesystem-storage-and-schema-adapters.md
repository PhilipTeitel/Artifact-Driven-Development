# S2-4: Filesystem storage and schema adapters

**Story**: Implement `FilesystemWikiStorageAdapter` and `MarkdownSchemaAdapter` — real filesystem I/O for vault/wiki artifacts, idempotent init from repo templates, exclude-aware source listing, and `.ingested.json` sidecar handling per ADR-003.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

Stage 2 use cases ([S2-3](S2-3-init-and-validate-use-cases.md)) orchestrate init and validate through port interfaces; this story supplies the **first production driven adapters** that touch disk. `FilesystemWikiStorageAdapter` owns all vault/wiki filesystem effects: copying init templates from `templates/wiki/`, idempotent layout creation (S1, S2), append-only log writes (S13), wiki page read/write confined to the wiki subdirectory (S5), and `.ingested.json` persistence (S12). `MarkdownSchemaAdapter` parses `wiki/SCHEMA.md` — primarily the **Excludes** section — so `list_sources()` skips configured paths (S4, S7 intent).

Hermetic **integration tests** use `pytest` temporary directories seeded from `tests/fixtures/vault/` (minimal Obsidian stub + sample sources). **Contract tests** from [S2-2](S2-2-port-protocols-and-domain-models.md) must pass when run against these adapters (not only in-memory fakes).

**Depends on:** [S2-1](S2-1-python-package-scaffold.md), [S2-2](S2-2-port-protocols-and-domain-models.md), [S2-3](S2-3-init-and-validate-use-cases.md) (use cases consume these adapters in S2-11; optional smoke wiring not required here).

**Out of scope:** `CLIConfigurationAdapter` vault walk-up (S2-5 — tests pass explicit `ConfigurationPort` fake or test double with fixed paths), LLM adapters (S2-6), terminal interaction (S2-7), ingest/query/lint use cases (S2-8–S2-10), Typer CLI wiring (S2-11). Full end-to-end ingest batch skip (S7) is validated at use-case level in S2-8; this story proves storage + schema primitives.

**Guiding constraint:** Writes never occur outside `{wiki_dir}/`; source paths are read-only. Template copy is byte-identical from `templates/wiki/*` when creating missing init files.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Adapters under `adapters/storage/`, `adapters/schema/`; no domain imports |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `WikiStoragePort` and `SchemaPort` method contracts |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | **Primary** — init artifacts, idempotent init, `.ingested.json` format, immutability, log heading format |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs agree on wiki layout, excludes, sidecar format, and source immutability
- [x] Section 4 (Binding constraints) filled from ADR-002/003
- [x] Section 4b lists both adapters with real filesystem fixture paths
- [x] Section 8a includes **contract** rows per port and **integration** rows per adapter
- [x] Phase Y **(binding)** criteria cite integration tests for each adapter
- [x] **S1**, **S2**, **S4**, **S5**, **S12**, **S13** mapped in Section 8a; **S7** partial (exclude parsing only); **S3**, **S6–S11** out of scope
- [x] Phase Y includes non-mock filesystem evidence (no mocked `Path.write_text` in integration tests)

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `FilesystemWikiStorageAdapter` lives at `src/llm_wiki/adapters/storage/filesystem.py` and implements `WikiStoragePort`.
2. **Y2** — `MarkdownSchemaAdapter` lives at `src/llm_wiki/adapters/schema/markdown.py` and implements `SchemaPort`.
3. **Y3** — `ensure_wiki_layout()` copies from repo `templates/wiki/SCHEMA.md`, `index.md`, `log.md` only when each destination is **missing**; never overwrites existing content (S2).
4. **Y4** — No write/delete/rename methods target paths outside `{config.wiki_dir}/` (S5); attempts raise a clear domain or adapter error.
5. **Y5** — `.ingested.json` reads/writes ADR-003 shape (`version: 1`, `sources` map with vault-relative forward-slash keys and ISO 8601 UTC values) (S12).
6. **Y6** — `MarkdownSchemaAdapter.load()` parses **Excludes** bullets from `wiki/SCHEMA.md`; `default_excludes()` returns `.obsidian/`, `{wiki_dir_name}/`, `.*` when SCHEMA absent during init seed (S4, ADR-003).
7. **Y7** — `list_sources()` returns vault-relative `.md` paths excluding wiki subtree and schema excludes (uses injected `SchemaPort`).
8. **Y8** — `append_log()` appends to `log.md` without modifying prior lines (S13).

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | `FilesystemWikiStorageAdapter` (`src/llm_wiki/adapters/storage/filesystem.py`) | Hermetic temp vault under `pytest` `tmp_path` seeded from `tests/fixtures/vault/` | new in this story |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | `MarkdownSchemaAdapter` (`src/llm_wiki/adapters/schema/markdown.py`) | Real `wiki/SCHEMA.md` on disk in temp vault fixture | new in this story |

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI changes in this story.

**Adapter constructors (Python):**

```python
class FilesystemWikiStorageAdapter:
    def __init__(
        self,
        *,
        config: ConfigurationPort,
        schema: SchemaPort,
        templates_dir: Path | None = None,  # default: repo templates/wiki/
    ) -> None: ...

class MarkdownSchemaAdapter:
    def __init__(self, *, config: ConfigurationPort) -> None: ...
```

**`.ingested.json` on disk (ADR-003, unchanged):**

```json
{
  "version": 1,
  "sources": {
    "daily/2026-05-01.md": "2026-06-01T12:00:00Z"
  }
}
```

Reference fixture: [`test/fixtures/ingested-v1.json`](ingested-v1.json).

---

## 6. Frontend Flow

Not applicable — driven adapters only; terminal presentation is S2-7.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/adapters/storage/filesystem.py` | `FilesystemWikiStorageAdapter` |
| 2 | `src/llm_wiki/adapters/schema/markdown.py` | `MarkdownSchemaAdapter` |
| 3 | `src/llm_wiki/adapters/schema/excludes_parser.py` | Parse **Excludes** section (optional split if parser > ~80 lines) |
| 4 | `tests/fixtures/vault/.obsidian/` | Obsidian vault stub for hermetic tests |
| 5 | `tests/fixtures/vault/daily/sample.md` | Read-only source sample (S5 checks) |
| 6 | `tests/integration/test_filesystem_wiki_storage.py` | Integration tests — real temp filesystem |
| 7 | `tests/integration/test_markdown_schema_adapter.py` | Integration tests — real SCHEMA.md on disk |
| 8 | `tests/integration/conftest.py` | Shared `vault_tmp` fixture (copy seed → tmp_path) |
| 9 | `scripts/verify-s2-4-adapters.sh` | Binding grep: adapter modules exist, no writes outside wiki in adapter source |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/test_storage_port_contract.py` | Parametrize or add class to run contract suite against `FilesystemWikiStorageAdapter` |
| 2 | `tests/contract/test_schema_port_contract.py` | Run contract suite against `MarkdownSchemaAdapter` |
| 3 | `README.md` | Link S2-4 row; add verifier to Available Scripts if missing |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/domain/use_cases/*` — no use case changes required
- `templates/wiki/*` — consumed as copy source; content owned by Stage 1 stories
- `src/llm_wiki/adapters/cli/*` — composition root wiring in S2-11

---

## 8. Acceptance Criteria Checklist

### Phase A: Init layout on filesystem (S1)

- [x] **A1** — Fresh temp vault: `ensure_wiki_layout()` creates `SCHEMA.md`, `index.md`, `log.md` under wiki dir; `InitResult.created` lists all three
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::creates_wiki_layout_s1_A1(pytest)`

- [x] **A2** — Created files match repo templates byte-for-byte (hash or diff against `templates/wiki/*`)
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::templates_match_repo_s1_A2(pytest)`

- [x] **A3** — Pre-existing vault source (e.g. `daily/sample.md`) mtime and content unchanged after init (S5)
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::sources_unmodified_s5_A3(pytest)`

### Phase B: Idempotent init (S2)

- [x] **B1** — Second `ensure_wiki_layout()` call: `InitResult.already_present` contains all three artifacts; `created` empty
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::idempotent_init_s2_B1(pytest)`

- [x] **B2** — Pre-existing custom wiki page (e.g. `wiki/existing-page.md`) content unchanged after re-init
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::preserves_wiki_pages_s2_B2(pytest)`

- [x] **B3** — Partial layout (only `SCHEMA.md` present): creates only missing `index.md` and `log.md`
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::creates_missing_only_s2_B3(pytest)`

### Phase C: Schema parsing (S4)

- [x] **C1** — `MarkdownSchemaAdapter.load()` on initialized vault returns `WikiSchema.excludes` including `.obsidian/`, wiki dir name, and `.*`
  - Evidence: `tests/integration/test_markdown_schema_adapter.py::parses_default_excludes_s4_C1(pytest)`

- [x] **C2** — User-added exclude bullet in SCHEMA is included in parsed excludes
  - Evidence: `tests/integration/test_markdown_schema_adapter.py::parses_custom_exclude_s4_C2(pytest)`

### Phase D: Source listing and immutability (S5, S7 partial)

- [x] **D1** — `list_sources()` returns `daily/sample.md` but not paths under `.obsidian/` or `wiki/`
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::list_sources_respects_excludes_s7_D1(pytest)`

- [x] **D2** — Calling write methods with a vault-relative path outside wiki dir raises error; file on disk unchanged
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::rejects_outside_wiki_write_s5_D2(pytest)`

### Phase E: Ingested sidecar (S12)

- [x] **E1** — `write_ingested` / `read_ingested` round-trip ADR-003 JSON; keys normalized to forward slashes
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::ingested_sidecar_round_trip_s12_E1(pytest)`

- [x] **E2** — Sidecar write does not modify the source file referenced in `sources` key
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::sidecar_does_not_touch_source_s12_E2(pytest)`

### Phase F: Log append (S13)

- [x] **F1** — `append_log()` adds content at EOF; prior `log.md` bytes unchanged
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::append_only_log_s13_F1(pytest)`

### Phase G: Contract compliance

- [x] **G1** — S2-2 storage port contract suite passes against `FilesystemWikiStorageAdapter`
  - Evidence: `tests/contract/test_storage_port_contract.py::filesystem_adapter_passes_contract_G1(pytest)`

- [x] **G2** — S2-2 schema port contract suite passes against `MarkdownSchemaAdapter`
  - Evidence: `tests/contract/test_schema_port_contract.py::markdown_adapter_passes_contract_G2(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Filesystem adapter uses stdlib `pathlib` only (no ORM/alternate storage); integration test proves real disk writes under wiki dir
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::real_disk_layout_Y1(pytest)`

- [x] **Y2** — **(binding)** Source immutability enforced — integration test proves source file unchanged after init + sidecar write (Section 4 Y4, Y5)
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::sources_immutable_binding_s5_Y2(pytest)`

- [x] **Y3** — **(binding)** `.ingested.json` on disk matches ADR-003 schema (Section 4 Y5)
  - Evidence: `tests/integration/test_filesystem_wiki_storage.py::ingested_adr003_shape_Y3(pytest)`

- [x] **Y4** — **(binding)** Schema adapter parses real `SCHEMA.md` file (Section 4 Y6) — not an in-memory string mock of the port
  - Evidence: `tests/integration/test_markdown_schema_adapter.py::loads_from_disk_Y4(pytest)`

- [x] **Y5** — **(binding)** Storage contract suite passes against filesystem adapter (Section 4 Y1)
  - Evidence: `tests/contract/test_storage_port_contract.py::filesystem_adapter_passes_contract_Y5(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/integration/test_filesystem_wiki_storage.py tests/integration/test_markdown_schema_adapter.py tests/contract/test_storage_port_contract.py tests/contract/test_schema_port_contract.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new adapter modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Adapters log errors at `warning`/`error` via `llm_wiki.adapters.storage` / `llm_wiki.adapters.schema` loggers; never log full file contents at INFO
- [x] **Z6** — `/review-story S2-4` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `tests/integration/test_filesystem_wiki_storage.py::creates_wiki_layout_s1_A1` | A1, Y1 | S1 | tmp_path vault |
| 2 | integration | `tests/integration/test_filesystem_wiki_storage.py::templates_match_repo_s1_A2` | A2 | S1 | byte compare |
| 3 | integration | `tests/integration/test_filesystem_wiki_storage.py::sources_unmodified_s5_A3` | A3, Y2 | S5 | mtime/content |
| 4 | integration | `tests/integration/test_filesystem_wiki_storage.py::idempotent_init_s2_B1` | B1 | S2 | |
| 5 | integration | `tests/integration/test_filesystem_wiki_storage.py::preserves_wiki_pages_s2_B2` | B2 | S2 | |
| 6 | integration | `tests/integration/test_filesystem_wiki_storage.py::creates_missing_only_s2_B3` | B3 | S2 | partial layout |
| 7 | integration | `tests/integration/test_markdown_schema_adapter.py::parses_default_excludes_s4_C1` | C1, Y4 | S4 | real SCHEMA.md |
| 8 | integration | `tests/integration/test_markdown_schema_adapter.py::parses_custom_exclude_s4_C2` | C2 | S4 | user exclude |
| 9 | integration | `tests/integration/test_filesystem_wiki_storage.py::list_sources_respects_excludes_s7_D1` | D1 | S7 | excludes only |
| 10 | integration | `tests/integration/test_filesystem_wiki_storage.py::rejects_outside_wiki_write_s5_D2` | D2, Y2 | S5 | raise on bad path |
| 11 | integration | `tests/integration/test_filesystem_wiki_storage.py::ingested_sidecar_round_trip_s12_E1` | E1, Y3 | S12 | |
| 12 | integration | `tests/integration/test_filesystem_wiki_storage.py::sidecar_does_not_touch_source_s12_E2` | E2 | S12 | |
| 13 | integration | `tests/integration/test_filesystem_wiki_storage.py::append_only_log_s13_F1` | F1 | S13 | |
| 14 | contract | `tests/contract/test_storage_port_contract.py::filesystem_adapter_passes_contract_G1` | G1, Y5 | S16 | real adapter |
| 15 | contract | `tests/contract/test_schema_port_contract.py::markdown_adapter_passes_contract_G2` | G2 | S4, S16 | real adapter |
| 16 | integration | `scripts/verify-s2-4-adapters.sh::adapter_modules_exist` | Y1 | — | static grep |

**Out of scope Sn:** **S3** (S2-5), **S6**, **S8**, **S9**, **S10** (validate use case wiring S2-11), **S11**, **S14**, **S16–S19** (full hexagonal proof S2-12).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Resolving `templates_dir` when installed as wheel vs editable | Default: walk from package to repo root in dev; allow explicit `templates_dir` injection in adapter constructor |
| 2 | User-edited SCHEMA breaks exclude parser | Tolerant parser; log warning and fall back to `default_excludes()` for malformed sections |
| 3 | Windows path separators in sidecar keys | Normalize to forward slashes on write per ADR-003 |

---

## Implementation Order

1. `tests/fixtures/vault/**` — seed vault with `.obsidian/`, source note, optional pre-init wiki partial
2. `tests/integration/conftest.py` — `vault_tmp` fixture + test `ConfigurationPort` with paths into tmp
3. `src/llm_wiki/adapters/schema/excludes_parser.py` + `markdown.py` (covers C1–C2)
4. `tests/integration/test_markdown_schema_adapter.py` — red-first (covers C1–C2, Y4)
5. `src/llm_wiki/adapters/storage/filesystem.py` (covers A1–F1, D1–D2, E1–E2)
6. `tests/integration/test_filesystem_wiki_storage.py` — red-first (covers Phase A–F, Y1–Y3)
7. Extend contract test modules to run against filesystem/markdown adapters (covers G1–G2, Y5)
8. `scripts/verify-s2-4-adapters.sh` (covers static binding)
9. **Verify** — `bash scripts/verify-s2-4-adapters.sh && pytest tests/integration/test_filesystem_wiki_storage.py tests/integration/test_markdown_schema_adapter.py tests/contract/`
10. `README.md` — backlog link + verifier script

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `5425ece` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-4-adapters.sh && pytest tests/integration/test_filesystem_wiki_storage.py tests/integration/test_markdown_schema_adapter.py tests/contract/test_storage_port_contract.py tests/contract/test_schema_port_contract.py && ruff check .` |
| QA result | `31/31 criteria PASS (27 pytest + verify script + ruff + review gate Z6)` |
| Docs handoff | `README backlog S2-4 → Complete; verify-s2-4-adapters.sh already listed in Available Scripts` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-4 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
