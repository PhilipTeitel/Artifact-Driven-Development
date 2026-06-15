# S2-1: Python package scaffold

**Story**: Create the Stage 2 Python package layout (`pyproject.toml`, `src/llm_wiki/`, `tests/`, dev tooling) with an editable install and a stub `llm-wiki` Typer entrypoint so all subsequent Epic 2 stories have a binding home.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Small
**Status**: Complete

---

## 1. Summary

This story bootstraps the **Stage 2 Python codebase** described in [ADR-001](ADR-001-hexagonal-architecture.md) and [ADR-005](ADR-005-python-cli-packaging.md). Today the repository has Stage 1 Cursor commands and wiki templates but **no** `pyproject.toml`, no `src/llm_wiki/` tree, and no pytest/ruff configuration. Every Epic 2 story (ports, use cases, adapters, CLI wiring) depends on this scaffold.

The deliverable is a **minimal, installable package**: Hatchling build metadata, runtime dependencies declared (Typer, httpx, provider SDKs, Rich), dev extras (pytest, ruff, optional mypy), the hexagonal directory skeleton with empty `__init__.py` packages, and a **stub** Typer app at `llm_wiki.adapters.cli.main:app` that registers placeholder subcommands (`init`, `validate`, `ingest`, `query`, `lint`) returning “not implemented” until later stories wire use cases. No domain logic, port definitions, or real adapters belong in this story.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) — structural enabler for **S16** (hexagonal boundaries) and future CLI scenarios **S1–S3**, **S10**, **S14**; this story does **not** implement those behaviors.

**Out of scope:** Port protocols (S2-2), use cases (S2-3+), filesystem/LLM/config adapters (S2-4–S2-7), composition-root wiring beyond the stub CLI (S2-11), contract/integration tests against real boundaries (S2-12).

**Guiding constraint:** Directory layout and dependency choices must match accepted ADRs exactly so later stories add files without reorganizing the tree.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Module layout: `domain/`, `ports/`, `adapters/` (with `cli/`, `llm/`, `storage/`, `schema/`, `interaction/`), `tests/unit|contract|integration/` |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | `pyproject.toml`, Hatchling, Python ≥3.11, console script `llm-wiki`, Typer stub, pytest/ruff/mypy dev tooling, stdlib logging convention |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs agree on Python 3.11+, Typer CLI, Hatchling packaging, and module paths under `src/llm_wiki/`
- [x] Section 4 (Binding constraints) is filled from ADR-001 and ADR-005
- [x] Section 4b states no port/adapter integration boundaries are implemented in this story
- [x] Section 8a maps every AC ID to a planned test or verify row
- [x] No adapters in Section 4b — hexagonal pairing integration-test rule N/A
- [x] Phase Y includes **(binding)** criteria with non-mock evidence (`pyproject.toml`, directory grep, verify script)
- [x] Gherkin **S1–S19** are not behaviorally implemented here — only scaffold enablers; **S16** structure is partially satisfied by layout only

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Package import path is `llm_wiki` under `src/llm_wiki/` (src layout; ADR-005).
2. **Y2** — Console script entry point is exactly `llm-wiki = "llm_wiki.adapters.cli.main:app"` (ADR-005).
3. **Y3** — Python requirement is `>=3.11` in `pyproject.toml`.
4. **Y4** — Build backend is Hatchling (`[build-system]` with `hatchling.build`).
5. **Y5** — Hexagonal directories exist: `domain/models/`, `domain/use_cases/`, `ports/`, `adapters/cli/`, `adapters/llm/`, `adapters/storage/`, `adapters/schema/`, `adapters/interaction/` (ADR-001).
6. **Y6** — Test layout exists: `tests/unit/`, `tests/contract/`, `tests/integration/` with root `tests/conftest.py` (ADR-001).
7. **Y7** — Runtime dependencies include at minimum: `typer[all]`, `httpx`, `openai`, `anthropic`, `rich` (ADR-005); `pydantic` optional but recommended for config models in S2-5.
8. **Y8** — Dev dependency group `[project.optional-dependencies] dev` includes at minimum `pytest`, `ruff`; `mypy` optional but recommended for domain/ports in later stories.
9. **Y9** — Stub CLI lives only in `adapters/cli/`; **no** business logic in Typer handlers (ADR-005 composition-root rule — handlers may only print stub messages until S2-11).
10. **Y10** — `domain/` and `ports/` packages contain **no** imports from `adapters/` or third-party I/O libraries in this story (empty packages only).

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** It creates empty package directories and a stub Typer driving adapter shell with no port wiring. Port protocols are defined in **S2-2**; driven adapters begin in **S2-4** onward.

---

## 5. API Endpoints + Schemas

No HTTP API.

**CLI stub (binding shape only):** Typer app exposes subcommands aligned with [ADR-005](ADR-005-python-cli-packaging.md):

| Subcommand | Stub behavior (this story) |
|------------|----------------------------|
| `init` | Exit 0 with message “not implemented — see S2-11” |
| `validate` | Same stub pattern |
| `ingest [PATH]` | Same |
| `query TEXT...` | Same |
| `lint` | Same |

Global options on app callback (declared but not resolved): `--vault`, `--wiki-dir`, `--provider`. Ingest adds `--batch` in stub signature only.

No shared TypeScript types. No Pydantic models required in this story.

---

## 6. Frontend Flow

Not applicable — terminal CLI stub only; no web UI.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `pyproject.toml` | Hatchling metadata, dependencies, console script, ruff/pytest tool config |
| 2 | `src/llm_wiki/__init__.py` | Package marker; expose `__version__` string |
| 3 | `src/llm_wiki/domain/__init__.py` | Domain package |
| 4 | `src/llm_wiki/domain/models/__init__.py` | Models package (empty until S2-2) |
| 5 | `src/llm_wiki/domain/use_cases/__init__.py` | Use cases package (empty until S2-3) |
| 6 | `src/llm_wiki/ports/__init__.py` | Ports package (empty until S2-2) |
| 7 | `src/llm_wiki/adapters/__init__.py` | Adapters package |
| 8 | `src/llm_wiki/adapters/cli/__init__.py` | CLI adapter package |
| 9 | `src/llm_wiki/adapters/cli/main.py` | Typer `app` + stub subcommands |
| 10 | `src/llm_wiki/adapters/llm/__init__.py` | Placeholder for S2-6 |
| 11 | `src/llm_wiki/adapters/storage/__init__.py` | Placeholder for S2-4 |
| 12 | `src/llm_wiki/adapters/schema/__init__.py` | Placeholder for S2-4 |
| 13 | `src/llm_wiki/adapters/interaction/__init__.py` | Placeholder for S2-7 |
| 14 | `tests/conftest.py` | Shared pytest fixtures (may be minimal) |
| 15 | `tests/unit/__init__.py` | Unit test package |
| 16 | `tests/contract/__init__.py` | Contract test package |
| 17 | `tests/integration/__init__.py` | Integration test package |
| 18 | `tests/unit/test_scaffold.py` | Smoke tests for import and CLI stub |
| 19 | `scripts/verify-s2-1-scaffold.sh` | Binding verifier for layout, pyproject, entry point |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Link S2-1 row to this story; add `scripts/verify-s2-1-scaffold.sh` to Available Scripts if missing |

### Files UNCHANGED (confirm no modifications needed)

- `templates/wiki/*` — Stage 1 artifacts
- `.cursor/commands/*` — Stage 1 driving adapter
- `docs/decisions/*` — ADRs already Accepted
- `test/vault/*` — fixture for Stage 1; Stage 2 integration tests expand in S2-12

---

## 8. Acceptance Criteria Checklist

### Phase A: Package metadata and install

- [x] **A1** — `pyproject.toml` exists with project name `llm-wiki`, import package `llm_wiki`, Python `>=3.11`, and Hatchling build backend
  - Evidence: `scripts/verify-s2-1-scaffold.sh::pyproject_metadata_A1`

- [x] **A2** — `pip install -e ".[dev]"` (or `uv pip install -e ".[dev]"`) from repo root succeeds and `python -c "import llm_wiki"` succeeds
  - Evidence: `tests/unit/test_scaffold.py::editable_install_imports_A2(pytest)`

### Phase B: Directory layout (ADR-001)

- [x] **B1** — All hexagonal directories from Section 4 constraint Y5 exist with `__init__.py` files
  - Evidence: `scripts/verify-s2-1-scaffold.sh::hexagonal_layout_B1`

- [x] **B2** — Test directories `tests/unit/`, `tests/contract/`, `tests/integration/` exist
  - Evidence: `scripts/verify-s2-1-scaffold.sh::test_layout_B2`

### Phase C: CLI entrypoint stub (ADR-005)

- [x] **C1** — Console script `llm-wiki` is declared and resolves to `llm_wiki.adapters.cli.main:app`
  - Evidence: `scripts/verify-s2-1-scaffold.sh::console_script_C1`

- [x] **C2** — `llm-wiki --help` lists subcommands `init`, `validate`, `ingest`, `query`, `lint`
  - Evidence: `tests/unit/test_scaffold.py::help_lists_subcommands_C2(pytest)`

- [x] **C3** — Stub subcommands exit without importing domain use cases or concrete adapters (handlers contain no business logic)
  - Evidence: `tests/unit/test_scaffold.py::stub_handlers_no_domain_imports_C3(pytest)`

### Phase D: Dev tooling

- [x] **D1** — `pytest` discovers and runs `tests/unit/test_scaffold.py` with zero failures
  - Evidence: `tests/unit/test_scaffold.py::pytest_runs_D1(pytest)`

- [x] **D2** — `ruff check .` passes on `src/` and `tests/`
  - Evidence: `tests/unit/test_scaffold.py::ruff_clean_D2(pytest)` or CI-equivalent subprocess in test

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Import path, Python version, and Hatchling backend match Section 4 Y1, Y3, Y4
  - Evidence: `scripts/verify-s2-1-scaffold.sh::package_metadata_Y1(bash scripts/verify-s2-1-scaffold.sh)`

- [x] **Y2** — **(binding)** Console script entry point matches Section 4 Y2 exactly
  - Evidence: `scripts/verify-s2-1-scaffold.sh::entry_point_Y2(bash scripts/verify-s2-1-scaffold.sh)`

- [x] **Y3** — **(binding)** Hexagonal directory tree matches ADR-001 layout (Section 4 Y5, Y6)
  - Evidence: `scripts/verify-s2-1-scaffold.sh::directory_tree_Y3(bash scripts/verify-s2-1-scaffold.sh)`

- [x] **Y4** — **(binding)** Runtime dependencies in `pyproject.toml` include Typer, httpx, OpenAI SDK, Anthropic SDK, Rich (Section 4 Y7)
  - Evidence: `scripts/verify-s2-1-scaffold.sh::runtime_deps_Y4(bash scripts/verify-s2-1-scaffold.sh)`

### Phase Z: Quality Gates

- [x] **Z1** — Editable install succeeds; `python -c "import llm_wiki; import llm_wiki.adapters.cli.main"` exits 0
- [x] **Z2** — `ruff check .` passes (or only pre-existing warnings outside `src/` / `tests/`)
- [x] **Z3** — No untyped bare `Any` in new Python files under `src/` and `tests/`
- [x] **Z4** — `@shared/types` alias — **N/A** (Python project; no TypeScript client)
- [x] **Z5** — Stub CLI module configures module logger `llm_wiki.adapters.cli` per ADR-005 (may log at DEBUG when `LLM_WIKI_LOG=DEBUG`)
- [x] **Z6** — `/review-story S2-1` reports zero `high` or `critical` `TEST-#`, `SEC-#`, `REL-#`, or `API-#` findings on the changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-s2-1-scaffold.sh::pyproject_metadata_A1` | A1, Y1 | — | static manifest |
| 2 | integration | `scripts/verify-s2-1-scaffold.sh::hexagonal_layout_B1` | B1, Y3 | S16 | layout only |
| 3 | integration | `scripts/verify-s2-1-scaffold.sh::test_layout_B2` | B2, Y3 | S16 | test dirs |
| 4 | integration | `scripts/verify-s2-1-scaffold.sh::console_script_C1` | C1, Y2 | — | entry point |
| 5 | integration | `scripts/verify-s2-1-scaffold.sh::runtime_deps_Y4` | Y4 | — | dependency manifest |
| 6 | unit | `tests/unit/test_scaffold.py::editable_install_imports_A2` | A2 | S16 | import smoke |
| 7 | unit | `tests/unit/test_scaffold.py::help_lists_subcommands_C2` | C2 | — | Typer help |
| 8 | unit | `tests/unit/test_scaffold.py::stub_handlers_no_domain_imports_C3` | C3 | S16 | no premature wiring |
| 9 | unit | `tests/unit/test_scaffold.py::pytest_runs_D1` | D1 | — | harness |
| 10 | unit | `tests/unit/test_scaffold.py::ruff_clean_D2` | D2, Z2 | — | lint gate |

**Out of scope Sn:** S1–S15, S17–S19 behavioral scenarios — not implemented until later Epic 2 stories. **S16** is partially covered by directory layout evidence only.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Stub CLI misleads users into thinking Stage 2 is ready | Help text and stub output explicitly reference upcoming stories (S2-11) |
| 2 | Tool config drift (ruff vs mypy paths) | Centralize `[tool.ruff]` and `[tool.pytest.ini_options]` in `pyproject.toml` now |
| 3 | `src/` layout breaks naive `PYTHONPATH` | Document editable install in README Getting Started (Stage 2 section) |

---

## Implementation Order

1. `pyproject.toml` — metadata, dependencies, console script, tool sections (covers A1, Y1–Y2, Y4)
2. `src/llm_wiki/**/__init__.py` — create full hexagonal skeleton (covers B1)
3. `tests/**` — conftest, package inits, empty integration/contract dirs (covers B2)
4. `src/llm_wiki/adapters/cli/main.py` — Typer stub with subcommand names (covers C1–C3)
5. `tests/unit/test_scaffold.py` — import, help, ruff subprocess tests (covers A2, C2–C3, D1–D2)
6. `scripts/verify-s2-1-scaffold.sh` — binding layout/manifest checks (covers Y1–Y4)
7. **Verify** — `bash scripts/verify-s2-1-scaffold.sh && pip install -e ".[dev]" && pytest tests/unit/test_scaffold.py && ruff check .`
8. `README.md` — link story + verifier script (backlog row)

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-05` |
| Completion ref | `a83bf68` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-1-scaffold.sh && pytest tests/unit/test_scaffold.py -v && ruff check .` |
| QA result | All 19 criteria PASS (A1–Z6) |
| Docs handoff | README backlog S2-1 → Complete; project structure `pyproject.toml` note updated; `verify-s2-1-scaffold.sh` listed under Available Scripts |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-1 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
