# S2-6: LLM port adapters and provider factory

**Story**: Implement `OllamaLLMAdapter`, `OpenAILLMAdapter`, and `AnthropicLLMAdapter` behind `LLMPort`, plus a provider factory that applies the ADR-004 selection algorithm (S11) using `ConfigurationPort` and `is_available()` checks.
**Epic**: 2 — Stage 2 — Hexagonal Python CLI
**Size**: Large
**Status**: Complete

---

## 1. Summary

Ingest, query, and lint use cases (S2-8–S2-10) require a single **`LLMPort`** for synchronous completions. This story adds three driven adapters and a **provider factory** that selects among them per ADR-004: Anthropic only when explicitly requested; otherwise Ollama if reachable; else OpenAI when a key is present; else a clear error (S11).

Each adapter reads model names and endpoints from **`ConfigurationPort`** (injected) — never from `os.environ` directly (S19). `OllamaLLMAdapter` uses **httpx** against the configured Ollama HTTP API. OpenAI and Anthropic adapters use their official SDKs as named in ADR-004/005.

**Integration tests** use a **hermetic HTTP fixture** (e.g. `pytest-httpx` or local `httpx` ASGI app) that speaks Ollama-shaped `/api/chat` responses — exercising real HTTP I/O without requiring a live Ollama daemon in CI. Optional `pytest.mark.live_ollama` tests may hit a real local Ollama when present. OpenAI/Anthropic integration tests use SDK **mock transports** or recorded fixtures at the SDK boundary only when no hermetic server is practical; prefer hermetic httpx for Ollama as the binding proof.

**Depends on:** [S2-1](S2-1-python-package-scaffold.md), [S2-2](S2-2-port-protocols-and-domain-models.md), [S2-5](S2-5-cli-configuration-adapter.md) (factory consumes `ConfigurationPort`).

**Out of scope:** Use case prompt templates (S2-8–S2-10), Typer wiring (S2-11), streaming responses, new providers beyond the three named in ADR-004.

**Guiding constraint:** Domain and use cases depend only on `LLMPort`; provider SDK imports exist solely under `adapters/llm/`.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | LLM adapters in `adapters/llm/`; factory wired at composition root later |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `LLMPort.complete`, `LLMPort.is_available` |
| [`docs/decisions/ADR-004-configuration-and-llm-providers.md`](ADR-004-configuration-and-llm-providers.md) | **Primary** — adapter modules, env defaults, provider selection algorithm (S11) |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](ADR-005-python-cli-packaging.md) | Runtime deps: `httpx`, `openai`, `anthropic` |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README stack lists httpx + OpenAI + Anthropic SDKs; matches ADR-004/005
- [x] Section 4 filled from ADR-004 selection algorithm and LLMPort contract
- [x] Section 4b lists `LLMPort` + three adapters + factory
- [x] Section 8a has contract row for `LLMPort` and integration rows per adapter + factory S11 tests
- [x] Phase Y cites integration tests with hermetic HTTP for Ollama (non-mock stack proof)
- [x] **S11** fully mapped; **S6–S9** deferred to use-case stories (adapter-level only here)

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Adapters live at `adapters/llm/ollama.py`, `openai.py`, `anthropic.py`; factory at `adapters/llm/factory.py`.
2. **Y2** — All adapters implement `LLMPort`; `complete()` is synchronous and returns `str`.
3. **Y3** — Ollama uses **httpx** HTTP client to `{ollama_base_url}/api/chat` (or `/api/generate` if chat unavailable) — not the OpenAI SDK.
4. **Y4** — OpenAI adapter uses official **`openai`** Python SDK; Anthropic uses official **`anthropic`** SDK (ADR-004).
5. **Y5** — Provider factory implements ADR-004 selection order exactly (S11); `provider_override == "ollama"` forces Ollama even when OpenAI key exists.
6. **Y6** — Anthropic is never auto-selected without `provider_override == "anthropic"`.
7. **Y7** — When no provider available, factory raises typed error listing Ollama start + API key guidance — does not silently fall back to a mock.
8. **Y8** — Adapters never log prompts, responses, or API keys at INFO or below (ADR-005).

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `LLMPort` | `src/llm_wiki/ports/llm.py` | `OllamaLLMAdapter` (`adapters/llm/ollama.py`) | Hermetic httpx server fixture mimicking Ollama `/api/chat` | httpx binding |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | `OpenAILLMAdapter` (`adapters/llm/openai.py`) | SDK with test HTTP transport / mock server returning OpenAI-shaped JSON | |
| `LLMPort` | `src/llm_wiki/ports/llm.py` | `AnthropicLLMAdapter` (`adapters/llm/anthropic.py`) | SDK with test HTTP transport / mock server returning Anthropic-shaped JSON | |
| — | — | `select_llm_provider(config) -> LLMPort` (`adapters/llm/factory.py`) | Combines real adapter instances + `is_available()` against hermetic Ollama | S11 |

---

## 5. API Endpoints + Schemas

No application HTTP API. External LLM APIs (adapter outbound):

| Provider | Endpoint / SDK | Config source |
|----------|----------------|---------------|
| Ollama | `POST {ollama_base_url}/api/chat` | `ConfigurationPort.ollama_*` |
| OpenAI | OpenAI SDK chat completions | `ConfigurationPort.openai_*` |
| Anthropic | Anthropic SDK messages | `ConfigurationPort.anthropic_*` |

**Factory signature:**

```python
def select_llm_provider(config: ConfigurationPort) -> LLMPort:
    """Apply ADR-004 / S11 selection; raise ProviderUnavailableError if none."""
```

---

## 6. Frontend Flow

Not applicable — LLM driven adapters only.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/adapters/llm/ollama.py` | `OllamaLLMAdapter` |
| 2 | `src/llm_wiki/adapters/llm/openai.py` | `OpenAILLMAdapter` |
| 3 | `src/llm_wiki/adapters/llm/anthropic.py` | `AnthropicLLMAdapter` |
| 4 | `src/llm_wiki/adapters/llm/factory.py` | Provider selection (S11) |
| 5 | `src/llm_wiki/adapters/llm/errors.py` | `ProviderUnavailableError` |
| 6 | `tests/integration/llm/conftest.py` | Hermetic Ollama HTTP fixture |
| 7 | `tests/integration/test_ollama_llm_adapter.py` | httpx integration against fixture |
| 8 | `tests/integration/test_openai_llm_adapter.py` | SDK integration with test transport |
| 9 | `tests/integration/test_anthropic_llm_adapter.py` | SDK integration with test transport |
| 10 | `tests/integration/test_llm_provider_factory.py` | S11 selection matrix |
| 11 | `scripts/verify-s2-6-llm-adapters.sh` | Binding: httpx + openai + anthropic in pyproject; no openai import in ollama.py |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `tests/contract/test_llm_port_contract.py` | Run contract suite against each adapter (with fixture-backed availability) |
| 2 | `README.md` | Link S2-6 row; add verifier if missing |

### Files UNCHANGED (confirm no modifications needed)

- `src/llm_wiki/domain/use_cases/*` — prompts in S2-8–S2-10
- `src/llm_wiki/adapters/cli/main.py` — factory wiring in S2-11

---

## 8. Acceptance Criteria Checklist

### Phase A: Ollama adapter

- [x] **A1** — `OllamaLLMAdapter.is_available()` returns `True` when hermetic server responds OK on tags or chat endpoint
  - Evidence: `tests/integration/test_ollama_llm_adapter.py::ollama_available_hermetic_A1(pytest)`

- [x] **A2** — `complete("hello")` returns assistant text from hermetic `/api/chat` JSON response
  - Evidence: `tests/integration/test_ollama_llm_adapter.py::ollama_complete_round_trip_A2(pytest)`

- [x] **A3** — Uses `config.ollama_base_url` and `config.ollama_model` — not hardcoded localhost except as config default
  - Evidence: `tests/integration/test_ollama_llm_adapter.py::ollama_respects_config_A3(pytest)`

### Phase B: OpenAI adapter

- [x] **B1** — With test transport returning chat completion JSON, `complete()` returns message content
  - Evidence: `tests/integration/test_openai_llm_adapter.py::openai_complete_round_trip_B1(pytest)`

- [x] **B2** — `is_available()` is `False` when `openai_api_key` is None
  - Evidence: `tests/integration/test_openai_llm_adapter.py::openai_unavailable_without_key_B2(pytest)`

### Phase C: Anthropic adapter

- [x] **C1** — With test transport returning messages JSON, `complete()` returns text block content
  - Evidence: `tests/integration/test_anthropic_llm_adapter.py::anthropic_complete_round_trip_C1(pytest)`

- [x] **C2** — `is_available()` is `False` when `anthropic_api_key` is None
  - Evidence: `tests/integration/test_anthropic_llm_adapter.py::anthropic_unavailable_without_key_C2(pytest)`

### Phase D: Provider factory (S11)

- [x] **D1** — Ollama reachable (hermetic) + no override → factory returns `OllamaLLMAdapter` instance
  - Evidence: `tests/integration/test_llm_provider_factory.py::selects_ollama_when_reachable_s11_D1(pytest)`

- [x] **D2** — Ollama unreachable + OpenAI key set → returns OpenAI adapter
  - Evidence: `tests/integration/test_llm_provider_factory.py::falls_back_openai_s11_D2(pytest)`

- [x] **D3** — `provider_override == "anthropic"` + key set → Anthropic adapter; fails if key missing
  - Evidence: `tests/integration/test_llm_provider_factory.py::explicit_anthropic_s11_D3(pytest)`

- [x] **D4** — `provider_override == "ollama"` forces Ollama even when OpenAI key present
  - Evidence: `tests/integration/test_llm_provider_factory.py::force_ollama_override_s11_D4(pytest)`

- [x] **D5** — No provider available → raises `ProviderUnavailableError` with actionable message
  - Evidence: `tests/integration/test_llm_provider_factory.py::error_when_none_available_s11_D5(pytest)`

- [x] **D6** — Anthropic key present but no override → **does not** auto-select Anthropic
  - Evidence: `tests/integration/test_llm_provider_factory.py::no_auto_anthropic_s11_D6(pytest)`

### Phase E: Contract compliance

- [x] **E1** — LLM port contract suite passes for Ollama adapter against hermetic server
  - Evidence: `tests/contract/test_llm_port_contract.py::ollama_passes_contract_E1(pytest)`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Ollama adapter imports and uses **httpx** (Section 4 Y3) — verified by integration test hitting hermetic HTTP server
  - Evidence: `tests/integration/test_ollama_llm_adapter.py::httpx_binding_Y1(pytest)`

- [x] **Y2** — **(binding)** OpenAI adapter uses **openai** SDK (Section 4 Y4)
  - Evidence: `scripts/verify-s2-6-llm-adapters.sh::openai_sdk_import_Y2(bash scripts/verify-s2-6-llm-adapters.sh)`

- [x] **Y3** — **(binding)** Anthropic adapter uses **anthropic** SDK (Section 4 Y4)
  - Evidence: `scripts/verify-s2-6-llm-adapters.sh::anthropic_sdk_import_Y3(bash scripts/verify-s2-6-llm-adapters.sh)`

- [x] **Y4** — **(binding)** Factory selection order matches ADR-004 (Section 4 Y5–Y7, S11)
  - Evidence: `tests/integration/test_llm_provider_factory.py::selection_order_binding_s11_Y4(pytest)`

### Phase Z: Quality Gates

- [x] **Z1** — `pytest tests/integration/test_ollama_llm_adapter.py tests/integration/test_openai_llm_adapter.py tests/integration/test_anthropic_llm_adapter.py tests/integration/test_llm_provider_factory.py tests/contract/test_llm_port_contract.py` passes
- [x] **Z2** — `ruff check .` passes on new/modified files
- [x] **Z3** — No untyped bare `Any` in new adapter modules
- [x] **Z4** — `@shared/types` — **N/A** (Python project)
- [x] **Z5** — LLM adapters log provider name + model at DEBUG only; never log prompts or keys
- [x] **Z6** — `/review-story S2-6` reports zero `high` or `critical` findings on changed surface

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `tests/integration/test_ollama_llm_adapter.py::ollama_available_hermetic_A1` | A1, Y1 | S11 | httpx server |
| 2 | integration | `tests/integration/test_ollama_llm_adapter.py::ollama_complete_round_trip_A2` | A2, Y1 | S6 | |
| 3 | integration | `tests/integration/test_ollama_llm_adapter.py::ollama_respects_config_A3` | A3 | S19 | config injection |
| 4 | integration | `tests/integration/test_openai_llm_adapter.py::openai_complete_round_trip_B1` | B1, Y2 | S6 | SDK transport |
| 5 | integration | `tests/integration/test_openai_llm_adapter.py::openai_unavailable_without_key_B2` | B2 | S11 | |
| 6 | integration | `tests/integration/test_anthropic_llm_adapter.py::anthropic_complete_round_trip_C1` | C1, Y3 | S6 | |
| 7 | integration | `tests/integration/test_anthropic_llm_adapter.py::anthropic_unavailable_without_key_C2` | C2 | S11 | |
| 8 | integration | `tests/integration/test_llm_provider_factory.py::selects_ollama_when_reachable_s11_D1` | D1, Y4 | S11 | |
| 9 | integration | `tests/integration/test_llm_provider_factory.py::falls_back_openai_s11_D2` | D2, Y4 | S11 | |
| 10 | integration | `tests/integration/test_llm_provider_factory.py::explicit_anthropic_s11_D3` | D3, Y4 | S11 | |
| 11 | integration | `tests/integration/test_llm_provider_factory.py::force_ollama_override_s11_D4` | D4, Y4 | S11 | |
| 12 | integration | `tests/integration/test_llm_provider_factory.py::error_when_none_available_s11_D5` | D5, Y4 | S11 | |
| 13 | integration | `tests/integration/test_llm_provider_factory.py::no_auto_anthropic_s11_D6` | D6, Y4 | S11 | |
| 14 | contract | `tests/contract/test_llm_port_contract.py::ollama_passes_contract_E1` | E1 | S16 | |
| 15 | integration | `scripts/verify-s2-6-llm-adapters.sh::openai_sdk_import_Y2` | Y2 | — | manifest |

**Out of scope Sn:** **S6–S9** end-to-end ingest/query/lint behavior — use cases S2-8–S2-10. **S8** filing prompt — S2-7. **S13** — log append in storage adapter.

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | CI flakiness if tests require live Ollama | Default CI uses hermetic httpx fixture; live tests opt-in via marker |
| 2 | SDK version drift changes request shape | Pin minimum versions in `pyproject.toml`; integration tests catch breakage |
| 3 | Accidental logging of secrets | Code review + test asserting log records exclude key substrings |

---

## Implementation Order

1. `tests/integration/llm/conftest.py` — hermetic Ollama HTTP fixture
2. `src/llm_wiki/adapters/llm/errors.py` + `ollama.py` + tests (covers A1–A3, Y1)
3. `openai.py`, `anthropic.py` + respective integration tests (covers B1–C2, Y2–Y3)
4. `factory.py` + `test_llm_provider_factory.py` (covers D1–D6, Y4)
5. Extend LLM contract tests (covers E1)
6. `scripts/verify-s2-6-llm-adapters.sh`
7. **Verify** — full pytest integration + contract + verify script
8. `README.md` — backlog link

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `2026-06-06` |
| Completion ref | `1f7816f` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `pytest tests/integration/test_ollama_llm_adapter.py tests/integration/test_openai_llm_adapter.py tests/integration/test_anthropic_llm_adapter.py tests/integration/test_llm_provider_factory.py tests/contract/test_llm_port_contract.py && ruff check src/llm_wiki/adapters/llm tests/integration/*llm* tests/contract/test_llm_port_contract.py && bash scripts/verify-s2-6-llm-adapters.sh` |
| QA result | `24/24 criteria PASS (A1–Z6); 19 pytest collected, all passed` |
| Docs handoff | `README.md` backlog row S2-6 → Complete with verify script link; verifier table already listed `verify-s2-6-llm-adapters.sh` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Change ref | Review ref | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|------------|------------|-------------|-----------|
| F1 | 2026-06-07 | story-followup | Resolve Ollama chat model against `/api/tags`: prefix match, fallback to first installed model when default is missing, actionable `ValueError` on 404 | `src/llm_wiki/adapters/llm/ollama.py` | Covered by F2 hermetic integration tests | `44d61e1` | none | none | none — existing A1–A3 unchanged |
| F2 | 2026-06-07 | story-followup | Hermetic integration tests for Ollama model resolution (tag prefix, default fallback, chat 404 error message) | `tests/integration/test_ollama_llm_adapter.py`, `tests/integration/llm/conftest.py`, `pyproject.toml` | `pytest tests/integration/test_ollama_llm_adapter.py tests/integration/test_openai_llm_adapter.py tests/integration/test_anthropic_llm_adapter.py tests/integration/test_llm_provider_factory.py tests/contract/test_llm_port_contract.py` — 24/24 passed | `44d61e1` | none | none | none |

---

*Created: 2026-06-04 | Story: S2-6 | Epic: 2 — Stage 2 — Hexagonal Python CLI*
