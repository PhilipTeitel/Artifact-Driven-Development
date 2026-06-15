# S2-2: Port protocols and domain models

**Story**: Define the five driven port `typing.Protocol` interfaces and core domain models (`VaultContext`, `WikiSchema`, `InitResult`, `ValidationResult`, etc.) per ADR-002 so use cases and adapters share stable contracts.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Medium
**Status**: Complete

---

## 1. Summary

This story codifies the **integration boundaries** between domain use cases and the outside world. [ADR-002](ADR-002-port-interfaces.md) binds method names and semantics for `ConfigurationPort`, `LLMPort`, `WikiStoragePort`, `SchemaPort`, and `UserInteractionPort`. [REQ-001](REQ-001-llm-wiki-cli.md) scenarios **S16**, **S17**, and **S19** require configuration and I/O to flow through these ports — never through direct env/CLI/filesystem calls in use cases.

The Implementer adds one module per port under `src/llm_wiki/ports/` and domain models under `src/llm_wiki/domain/models/`. **No concrete adapters** ship in this story (those begin in S2-4–S2-7). Contract tests live in `tests/contract/` and exercise **in-memory reference fakes** that implement each port; those fakes prove the protocol shapes are usable and document expected behavior for future filesystem and LLM adapters (S2-4, S2-6, S2-12).

**Depends on:** [S2-1](S2-1-python-package-scaffold.md) (package layout and pytest harness).

**Out of scope:** Use case implementations (S2-3+), `CLIConfigurationAdapter` (S2-5), filesystem/LLM/terminal adapters, Typer wiring beyond S2-1 stub, parsing `wiki/SCHEMA.md` from disk (S2-4 `MarkdownSchemaAdapter`).

**Guiding constraint:** Port modules must not import from `adapters/` or third-party I/O libraries. Domain models are plain dataclasses or Pydantic models without side effects.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Ports live in `src/llm_wiki/ports/`; domain models in `domain/models/`; dependency rule domain → ports only |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | **Primary** — binding method/property names and semantics for all five ports |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | `InitResult`, wiki artifact names, `.ingested.json` shape reflected in models and `WikiStoragePort` |
| [`docs/decisions/ADR-004-configuration-and-llm-providers.md`](ADR-004-configuration-and-llm-providers.md) | `ConfigurationPort` fields and provider-related properties |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADR-002 agree on port names, key methods, and configuration fields
- [x] Section 4 (Binding constraints) is filled from ADR-002 and ADR-003
- [x] Section 4b lists all five ports (interfaces only — no adapters yet)
- [x] Section 8a includes **contract** test rows for every port in Section 4b
- [x] No adapters in Section 4b — integration tests against real backing services deferred to S2-4+; Phase Y uses contract tests + import-boundary checks
- [x] **S16**, **S17**, **S19** mapped in Section 8a; other Sn IDs explicitly out of scope or deferred to later stories
- [x] Phase Y includes **(binding)** criteria with non-mock evidence (contract tests + static import grep)

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Five port modules exist: `configuration.py`, `llm.py`, `storage.py`, `schema.py`, `interaction.py` under `src/llm_wiki/ports/` (ADR-002).
2. **Y2** — Ports are `typing.Protocol` (or ABC equivalent); method names match ADR-002 tables (`complete`, `is_available`, `ensure_wiki_layout`, etc.).
3. **Y3** — `ConfigurationPort` exposes all ADR-002 properties: `vault_root`, `wiki_dir`, `batch_mode`, `provider_override`, Ollama/OpenAI/Anthropic settings — **no** `os.environ` reads in port modules.
4. **Y4** — `WikiStoragePort` includes `ensure_wiki_layout() -> InitResult` and read/write methods for index, log, ingested sidecar per ADR-002/ADR-003; port docstring states non-wiki paths are not writable (S5 intent).
5. **Y5** — Domain models include at minimum: `InitResult` (created vs existing paths), `ValidationIssue` / `ValidationResult` (for S10), `WikiSchema` (excludes list + metadata from SCHEMA).
6. **Y6** — `src/llm_wiki/domain/` and `src/llm_wiki/ports/` contain **zero** imports from `llm_wiki.adapters` or HTTP/filesystem third-party libs.
7. **Y7** — Each port has a contract test module in `tests/contract/` runnable with an in-memory fake implementing that port.
8. **Y8** — `InitResult` and ingested sidecar typing align with ADR-003 JSON shape (`version`, `sources` map with ISO timestamps).

---

## 4b. Ports & Adapters

This story **defines ports only** — no production adapters. Contract tests use **test-local reference fakes** (not shipped adapters).

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | *(none in this story)* | In-memory fake in `tests/contract/fakes.py` | S2-5 adds `CLIConfigurationAdapter` |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | *(none in this story)* | In-memory fake | S2-6 adds Ollama/OpenAI/Anthropic |
| `WikiStoragePort` | `src/llm_wiki/ports/storage.py` | *(none in this story)* | In-memory fake | S2-4 adds `FilesystemWikiStorageAdapter` |
| `SchemaPort` | `src/llm_wiki/ports/schema.py` | *(none in this story)* | In-memory fake | S2-4 adds `MarkdownSchemaAdapter` |
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | *(none in this story)* | In-memory fake | S2-7 adds `TerminalUserInteractionAdapter` |

**Hexagonal note:** Integration tests against real filesystem/LLM/terminal are **out of scope** until adapter stories land. Phase Y **(binding)** evidence for each port is the **contract test** against the reference fake (proves protocol is implementable and behavior is specified).

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI changes beyond what S2-1 stub provides.

**Domain types (Python — add to `src/llm_wiki/domain/models/`):**

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

WikiOperation = Literal["init", "ingest", "query", "lint"]

@dataclass(frozen=True)
class InitResult:
    """Outcome of idempotent wiki layout initialization (S1, S2)."""
    created: tuple[str, ...]      # paths relative to wiki root, newly created
    already_present: tuple[str, ...]  # required artifacts that existed
    wiki_dir: Path                # absolute wiki directory

@dataclass(frozen=True)
class ValidationIssue:
    """Single validation finding (S10)."""
    code: str                     # stable machine id, e.g. "missing_schema"
    message: str                  # human-readable description
    path: Path | None = None      # related path when applicable

@dataclass(frozen=True)
class ValidationResult:
    """Aggregate validate outcome (S10)."""
    valid: bool
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class WikiSchema:
    """Parsed SCHEMA.md subset (S4) — full parse in S2-4 adapter."""
    excludes: tuple[str, ...]     # glob patterns relative to vault root
    raw_sections: dict[str, str] = field(default_factory=dict)  # optional capture

@dataclass(frozen=True)
class IngestedSidecar:
    """wiki/.ingested.json document (ADR-003)."""
    version: int
    sources: dict[str, str]       # vault-relative path -> ISO 8601 UTC timestamp
```

Port `Protocol` definitions follow ADR-002 method tables exactly; use `pathlib.Path` for path-typed configuration fields.

---

## 6. Frontend Flow

Not applicable — library interfaces only.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/ports/configuration.py` | `ConfigurationPort` Protocol |
| 2 | `src/llm_wiki/ports/llm.py` | `LLMPort` Protocol |
| 3 | `src/llm_wiki/ports/storage.py` | `WikiStoragePort` Protocol |
| 4 | `src/llm_wiki/ports/schema.py` | `SchemaPort` Protocol |
| 5 | `src/llm_wiki/ports/interaction.py` | `UserInteractionPort` Protocol |
| 6 | `src/llm_wiki/ports/__init__.py` | Re-export port names |
| 7 | `src/llm_wiki/domain/models/init_result.py` | `InitResult` |
| 8 | `src/llm_wiki/domain/models/validation.py` | `ValidationIssue`, `ValidationResult` |
| 9 | `src/llm_wiki/domain/models/wiki_schema.py` | `WikiSchema`, `IngestedSidecar`, `WikiOperation` |
| 10 | `src/llm_wiki/domain/models/__init__.py` | Re-export models |
| 11 | `tests/contract/fakes.py` | In-memory fakes implementing all five ports for contract tests |
| 12 | `tests/contract/test_configuration_port_contract.py` | Contract suite |
| 13 | `tests/contract/test_llm_port_contract.py` | Contract suite |
| 14 | `tests/contract/test_storage_port_contract.py` | Contract suite |
| 15 | `tests/contract/test_schema_port_contract.py` | Contract suite |
| 16 | `tests/contract/test_interaction_port_contract.py` | Contract suite |
| 17 | `tests/unit/test_import_boundaries.py` | Static test: domain/ports do not import adapters |
| 18 | `scripts/verify-s2-2-ports.sh` | Grep-based binding verifier for port files and ADR-002 method names |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S2-2 backlog row to this story |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/adapters/cli/main.py` — stub only until S2-11
- `templates/wiki/*` — schema content unchanged; parser comes in S2-4
- `docs/decisions/*` — ADRs already Accepted

---

## 8. Acceptance Criteria Checklist

### Phase A: Port modules (ADR-002)

- [x] **A1** — `ConfigurationPort` defines all ADR-002 properties with correct types (`Path`, `bool`, `str | None`, etc.)
  - Evidence: `tests/contract/test_configuration_port_contract.py::configuration_properties_A1(pytest)`

- [x] **A2** — `LLMPort` defines `complete(prompt, *, system=None) -> str` and `is_available() -> bool`
  - Evidence: `tests/contract/test_llm_port_contract.py::llm_methods_A2(pytest)`

- [x] **A3** — `WikiStoragePort` defines all ADR-002 methods including `ensure_wiki_layout() -> InitResult`, index/log/ingested accessors, `read_source`, `list_sources`, `wiki_exists`
  - Evidence: `tests/contract/test_storage_port_contract.py::storage_methods_A3(pytest)`

- [x] **A4** — `SchemaPort` defines `load() -> WikiSchema` and `default_excludes() -> list[str]`
  - Evidence: `tests/contract/test_schema_port_contract.py::schema_methods_A4(pytest)`

- [x] **A5** — `UserInteractionPort` defines `confirm`, `present`, `prompt`
  - Evidence: `tests/contract/test_interaction_port_contract.py::interaction_methods_A5(pytest)`

### Phase B: Domain models

- [x] **B1** — `InitResult` captures `created`, `already_present`, and `wiki_dir` for idempotent init reporting (S1, S2)
  - Evidence: `tests/contract/test_storage_port_contract.py::init_result_shape_B1(pytest)`

- [x] **B2** — `ValidationResult` / `ValidationIssue` support S10-style named failures
  - Evidence: `tests/unit/test_domain_models.py::validation_models_B2(pytest)`

- [x] **B3** — `WikiSchema` and `IngestedSidecar` align with ADR-003 excludes and `.ingested.json` version 1 shape
  - Evidence: `tests/unit/test_domain_models.py::wiki_schema_and_sidecar_B3(pytest)`

### Phase C: Contract tests (reference fakes)

- [x] **C1** — In-memory `WikiStoragePort` fake: `ensure_wiki_layout` is idempotent (second call reports `already_present`, does not duplicate creates)
  - Evidence: `tests/contract/test_storage_port_contract.py::idempotent_layout_s2_C1(pytest)`

- [x] **C2** — In-memory `LLMPort` fake: `complete` returns deterministic text; `is_available` toggles
  - Evidence: `tests/contract/test_llm_port_contract.py::llm_fake_round_trip_C2(pytest)`

- [x] **C3** — In-memory `SchemaPort` fake: `default_excludes` includes `.obsidian/`, `wiki/`, `.*` (ADR-003 defaults)
  - Evidence: `tests/contract/test_schema_port_contract.py::default_excludes_s4_C3(pytest)`

### Phase D: Import boundaries (S16, S19)

- [x] **D1** — No module under `domain/` or `ports/` imports `llm_wiki.adapters` or `httpx`/`openai`/`anthropic`/`typer`
  - Evidence: `tests/unit/test_import_boundaries.py::no_adapter_imports_in_core_D1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** All five port modules exist with ADR-002 method names verifiable by script
  - Evidence: `scripts/verify-s2-2-ports.sh::port_modules_Y1(bash scripts/verify-s2-2-ports.sh)`

- [x] **Y2** — **(binding)** `ConfigurationPort` contract test passes against reference fake (no env reads in port definition)
  - Evidence: `tests/contract/test_configuration_port_contract.py::configuration_contract_Y2(pytest)`

- [x] **Y3** — **(binding)** `WikiStoragePort` contract test passes including idempotent `ensure_wiki_layout` (S2)
  - Evidence: `tests/contract/test_storage_port_contract.py::storage_contract_s2_Y3(pytest)`

- [x] **Y4** — **(binding)** `SchemaPort` contract test passes with ADR-003 default excludes (S4)
  - Evidence: `tests/contract/test_schema_port_contract.py::schema_contract_s4_Y4(pytest)`

- [x] **Y5** — **(binding)** `LLMPort` and `UserInteractionPort` contract tests pass against reference fakes
  - Evidence: `tests/contract/test_llm_port_contract.py::llm_contract_Y5(pytest)` and `tests/contract/test_interaction_port_contract.py::interaction_contract_Y5(pytest)`

- [x] **Y6** — **(binding)** Domain/ports import boundary check passes (Section 4 Y6)
  - Evidence: `tests/unit/test_import_boundaries.py::core_isolation_Y6(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — Editable install + `pytest tests/contract tests/unit/test_domain_models.py tests/unit/test_import_boundaries.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new port/model modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Port modules use module loggers only if they log; prefer no logging in pure Protocol modules
- [x] **Z6** — `/review-story S2-2` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | contract | `tests/contract/test_configuration_port_contract.py::configuration_properties_A1` | A1, Y2 | S19 | fake implements port |
| 2 | contract | `tests/contract/test_llm_port_contract.py::llm_methods_A2` | A2, Y5 | S16 | |
| 3 | contract | `tests/contract/test_storage_port_contract.py::storage_methods_A3` | A3 | S16, S5 | docstring immutability |
| 4 | contract | `tests/contract/test_schema_port_contract.py::schema_methods_A4` | A4, Y4 | S4, S16 | |
| 5 | contract | `tests/contract/test_interaction_port_contract.py::interaction_methods_A5` | A5, Y5 | S16 | |
| 6 | contract | `tests/contract/test_storage_port_contract.py::init_result_shape_B1` | B1 | S1, S2 | |
| 7 | contract | `tests/contract/test_storage_port_contract.py::idempotent_layout_s2_C1` | C1, Y3 | S2 | idempotent fake |
| 8 | contract | `tests/contract/test_llm_port_contract.py::llm_fake_round_trip_C2` | C2, Y5 | S16 | |
| 9 | contract | `tests/contract/test_schema_port_contract.py::default_excludes_s4_C3` | C3, Y4 | S4 | ADR-003 defaults |
| 10 | unit | `tests/unit/test_domain_models.py::validation_models_B2` | B2 | S10 | models only |
| 11 | unit | `tests/unit/test_domain_models.py::wiki_schema_and_sidecar_B3` | B3 | S12 | sidecar typing |
| 12 | unit | `tests/unit/test_import_boundaries.py::no_adapter_imports_in_core_D1` | D1, Y6 | S16, S19 | static |
| 13 | integration | `scripts/verify-s2-2-ports.sh::port_modules_Y1` | Y1 | S16 | manifest grep |

**Out of scope Sn (explicit):** **S1**, **S2**, **S3**, **S5**, **S6–S11**, **S13–S15**, **S18** — behavioral implementation deferred to S2-3+ and adapter stories. **S17** — port stability only; Obsidian adapter not built. **S10** — `ValidationResult` model only; `ValidateUseCase` in S2-3.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | ADR-002 signatures too vague for implementers | Contract tests encode minimal behavioral expectations beyond signatures |
| 2 | Pydantic vs dataclass for models | Prefer stdlib `dataclass` for domain; Pydantic reserved for adapter config if needed in S2-5 |
| 3 | Contract fakes diverge from real adapters | S2-12 re-runs contract suites against filesystem/LLM adapters |

---

## Implementation Order

1. `src/llm_wiki/domain/models/*` — dataclasses (covers B1–B3)
2. `src/llm_wiki/ports/*.py` — five Protocol modules (covers A1–A5)
3. `tests/contract/fakes.py` — reference in-memory implementations
4. `tests/contract/test_*_port_contract.py` — one file per port (covers C1–C3, Y2–Y5)
5. `tests/unit/test_domain_models.py` — model construction tests
6. `tests/unit/test_import_boundaries.py` — adapter import guard (covers D1, Y6)
7. `scripts/verify-s2-2-ports.sh` — binding grep script (covers Y1)
8. **Verify** — `bash scripts/verify-s2-2-ports.sh && pytest tests/contract tests/unit/test_domain_models.py tests/unit/test_import_boundaries.py`
9. `README.md` — backlog link

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-05` |
| Completion ref | `640aa99` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-2-ports.sh && pytest tests/contract tests/unit/test_domain_models.py tests/unit/test_import_boundaries.py && ruff check .` |
| QA result | `24/24 criteria PASS` (A1–A5, B1–B3, C1–C3, D1, Y1–Y6, Z1–Z6) |
| Docs handoff | `README.md` Epic 2 backlog row updated to **Complete** with verify script; no API/runbook changes (ports-only story) |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-2 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
