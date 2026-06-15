# S2-7: Terminal user interaction adapter

**Story**: Implement `TerminalUserInteractionAdapter` behind `UserInteractionPort` using Rich for `present`, `confirm`, and `prompt`, with integration tests exercising real stdin/stdout paths.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Small
**Status**: Complete

---

## 1. Summary

Interactive ingest (S6) and query filing (S8) require user prompts and confirmations through **`UserInteractionPort`**. Batch ingest (S7) skips interactive checkpoints at the **use-case** layer when `ConfigurationPort.batch_mode` is true — this adapter still implements the port faithfully; use cases in S2-8/S2-9 decide whether to call `confirm()`.

`TerminalUserInteractionAdapter` uses **Rich** (already a Typer dependency per ADR-005) for readable terminal output. Integration tests drive the adapter with **`pytest`** `monkeypatch` on `builtins.input` and **`capsys`** / Rich `Console(file=...)` to capture output — exercising the real adapter code without mocking the port interface itself.

**Depends on:** [S2-1](S2-1-python-package-scaffold.md), [S2-2](S2-2-port-protocols-and-domain-models.md).

**Out of scope:** Use-case orchestration of batch bypass (S2-8, S2-9), Typer CLI wiring (S2-11), Obsidian plugin UI adapter (future epic), non-terminal `UserInteractionPort` variants.

**Guiding constraint:** Adapter lives in `adapters/interaction/`; no business logic about ingest or query filing decisions.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Adapter in `adapters/interaction/` |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | **Primary** — `confirm`, `present`, `prompt` methods |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | Rich for terminal UX |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README stack lists Rich; matches ADR-005
- [x] Section 4 filled from ADR-002 UserInteractionPort
- [x] Section 4b lists adapter with stdin/stdout integration fixture
- [x] Section 8a has contract + integration rows; Phase Y cites integration tests
- [x] **S6**, **S8** mapped at adapter level; **S7** batch skip documented as use-case responsibility
- [x] Phase Y uses integration tests with real adapter + patched stdin

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — `TerminalUserInteractionAdapter` at `src/llm_wiki/adapters/interaction/terminal.py` implements `UserInteractionPort`.
2. **Y2** — `present(text)` writes user-visible output to stdout (via Rich Console).
3. **Y3** — `confirm(message)` reads y/n (or default Rich confirm UX); returns `True`/`False` without raising on decline.
4. **Y4** — `prompt(message)` reads a line of text input and returns stripped string.
5. **Y5** — Adapter accepts injectable `Console` (default stdout) for testability — production uses stderr/stdout per Rich Typer conventions.
6. **Y6** — No ingest/query/lint logic in adapter module.

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `UserInteractionPort` | `src/llm_wiki/ports/interaction.py` | `TerminalUserInteractionAdapter` (`src/llm_wiki/adapters/interaction/terminal.py`) | Real adapter with `Rich.Console(file=StringIO)` + `monkeypatch` on `input()` | new in this story |

---

## 5. API Endpoints + Schemas

No HTTP API. No CLI changes in this story.

**Adapter constructor:**

```python
class TerminalUserInteractionAdapter:
    def __init__(self, *, console: Console | None = None) -> None: ...
```

---

## 6. Frontend Flow

Not applicable — terminal adapter only (no web UI).

### 6a. Interaction flow (reference for use cases)

```
present(takeaways)     → user reads stdout
confirm("File answer?") → user enters y/n → bool
prompt("Optional note") → user enters text → str
```

Use cases in S2-8/S2-9 gate `confirm`/`prompt` on `not config.batch_mode`.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/adapters/interaction/terminal.py` | `TerminalUserInteractionAdapter` |
| 2 | `tests/integration/test_terminal_interaction.py` | stdin/stdout integration tests |
| 3 | `scripts/verify-s2-7-interaction.sh` | Binding: adapter module exists; uses Rich |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/test_interaction_port_contract.py` | Run contract suite against `TerminalUserInteractionAdapter` with StringIO console |
| 2 | `README.md` | Link S2-7 row |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/domain/use_cases/*` — batch gating in S2-8/S2-9
- `src/llm_wiki/adapters/cli/main.py` — wiring in S2-11

---

## 8. Acceptance Criteria Checklist

### Phase A: Present output (S6, S8)

- [x] **A1** — `present("hello")` writes `hello` (or Rich-rendered equivalent) to configured console output
  - Evidence: `tests/integration/test_terminal_interaction.py::present_writes_output_A1(pytest)`

### Phase B: Confirm (S8 filing, S6 checkpoints)

- [x] **B1** — `confirm()` returns `True` when stdin provides affirmative (`y`, `yes`, case-insensitive per adapter docstring)
  - Evidence: `tests/integration/test_terminal_interaction.py::confirm_yes_s8_B1(pytest)`

- [x] **B2** — `confirm()` returns `False` on negative input without exception
  - Evidence: `tests/integration/test_terminal_interaction.py::confirm_no_s8_B2(pytest)`

### Phase C: Prompt

- [x] **C1** — `prompt()` returns stripped user input from stdin
  - Evidence: `tests/integration/test_terminal_interaction.py::prompt_returns_input_C1(pytest)`

### Phase D: Contract compliance

- [x] **D1** — S2-2 interaction port contract suite passes against terminal adapter
  - Evidence: `tests/contract/test_interaction_port_contract.py::terminal_passes_contract_D1(pytest)`

### Phase E: Batch mode note (S7)

- [x] **E1** — Document in adapter module docstring: batch bypass is **use-case** responsibility (`ConfigurationPort.batch_mode`); adapter methods remain callable
  - Evidence: `scripts/verify-s2-7-interaction.sh::documents_batch_delegation_s7_E1(bash scripts/verify-s2-7-interaction.sh)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Adapter uses Rich `Console` (Section 4 Y2–Y4) — integration test captures StringIO output from real adapter instance
  - Evidence: `tests/integration/test_terminal_interaction.py::rich_console_binding_Y1(pytest)`

- [x] **Y2** — **(binding)** Interaction contract suite passes against terminal adapter (Section 4 Y1)
  - Evidence: `tests/contract/test_interaction_port_contract.py::terminal_passes_contract_Y2(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/integration/test_terminal_interaction.py tests/contract/test_interaction_port_contract.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — Adapter does not log user input at INFO (privacy); DEBUG may note prompt invoked without content
- [x] **Z6** — `/review-story S2-7` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `tests/integration/test_terminal_interaction.py::present_writes_output_A1` | A1, Y1 | S6, S8 | StringIO console |
| 2 | integration | `tests/integration/test_terminal_interaction.py::confirm_yes_s8_B1` | B1 | S8 | monkeypatch input |
| 3 | integration | `tests/integration/test_terminal_interaction.py::confirm_no_s8_B2` | B2 | S8 | decline path |
| 4 | integration | `tests/integration/test_terminal_interaction.py::prompt_returns_input_C1` | C1 | S6 | |
| 5 | contract | `tests/contract/test_interaction_port_contract.py::terminal_passes_contract_D1` | D1, Y2 | S16 | |
| 6 | integration | `scripts/verify-s2-7-interaction.sh::documents_batch_delegation_s7_E1` | E1 | S7 | docstring grep |

**Out of scope Sn:** **S7** unattended batch **behavior** — implemented in `IngestUseCase` (S2-8), not in this adapter. **S9**, **S10+** — not interaction concerns.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Rich confirm UX differs from plain input | Document accepted affirmative tokens; keep contract tests aligned with S2-2 fake semantics |
| 2 | Non-interactive CI stdin | Always inject stdin via monkeypatch in tests; never block on TTY |
| 3 | Plugin future needs GUI prompts | Separate `UserInteractionPort` adapter in plugin epic; port shape unchanged |

---

## Implementation Order

1. `src/llm_wiki/adapters/interaction/terminal.py` (covers A1–C1)
2. `tests/integration/test_terminal_interaction.py` — red-first
3. Extend interaction contract tests for terminal adapter (covers D1, Y2)
4. `scripts/verify-s2-7-interaction.sh` (covers E1)
5. **Verify** — `bash scripts/verify-s2-7-interaction.sh && pytest tests/integration/test_terminal_interaction.py tests/contract/test_interaction_port_contract.py`
6. `README.md` — backlog link

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `61975c5` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-s2-7-interaction.sh && pytest tests/integration/test_terminal_interaction.py tests/contract/test_interaction_port_contract.py && ruff check src/llm_wiki/adapters/interaction/terminal.py tests/integration/test_terminal_interaction.py tests/contract/test_interaction_port_contract.py` |
| QA result | `15/15 criteria PASS (A1–Z6); 10 pytest collected, all passed` |
| Docs handoff | `README.md` backlog row S2-7 → Complete with verify script link; verifier table already listed `verify-s2-7-interaction.sh` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-06-04 | Story: S2-7 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
