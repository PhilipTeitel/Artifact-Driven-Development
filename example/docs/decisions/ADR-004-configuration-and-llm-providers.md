# ADR-004: Configuration resolution and LLM providers

**Status:** Accepted
**Date:** 2026-05-30

---

## Context

REQ-001 requires Ollama (local-first), OpenAI, and Anthropic in Stage 2, with credentials via environment variables and explicit `--provider` (S11). Runtime configuration must flow through `ConfigurationPort` (S19). Default model names were deferred from requirements to design.

---

## Decision

### Provider selection algorithm (S11)

At CLI startup, after `CLIConfigurationAdapter` builds `ConfigurationPort`:

1. If `provider_override == "anthropic"` → use Anthropic adapter; fail if no API key.
2. Else if Ollama adapter `is_available()` → use Ollama.
3. Else if `openai_api_key` set → use OpenAI.
4. Else if `provider_override == "openai"` → use OpenAI; fail if no key.
5. Else → exit non-zero with message listing how to start Ollama or set API keys.

`provider_override == "ollama"` forces Ollama even if OpenAI key exists (for testing).

Anthropic is **not** auto-selected without explicit `--provider anthropic` (local-first + OpenAI fallback before paid Anthropic default).

### Environment variables and CLI flags

| Setting | Environment variable | CLI flag | Default |
|---------|---------------------|----------|---------|
| Vault root | — | `--vault PATH` | Detect from CWD |
| Wiki subdirectory | `LLM_WIKI_DIR` | `--wiki-dir NAME` | `wiki` |
| Provider | `LLM_WIKI_PROVIDER` | `--provider {ollama,openai,anthropic}` | (auto per algorithm) |
| Batch ingest | — | `--batch` | `false` |
| Ollama base URL | `OLLAMA_BASE_URL` | — | `http://localhost:11434` |
| Ollama model | `OLLAMA_MODEL` | — | `llama3.2` |
| OpenAI API key | `OPENAI_API_KEY` | — | — |
| OpenAI model | `OPENAI_MODEL` | — | `gpt-4o-mini` |
| Anthropic API key | `ANTHROPIC_API_KEY` | — | — |
| Anthropic model | `ANTHROPIC_MODEL` | — | `claude-3-5-sonnet-20241022` |

**Override rule:** When a CLI flag exists for a setting also available via env, **CLI wins**.

No vault-local `.env` file is loaded automatically; users export vars or use shell direnv. Optional `LLM_WIKI_*` prefix keeps wiki vars distinct from generic `OPENAI_*` only where noted — OpenAI/Anthropic keys use conventional names for tooling compatibility.

### LLM adapters (driven)

| Adapter | Module | Notes |
|---------|--------|-------|
| `OllamaLLMAdapter` | `adapters/llm/ollama.py` | HTTP to `{ollama_base_url}/api/chat` or `/api/generate` |
| `OpenAILLMAdapter` | `adapters/llm/openai.py` | Official OpenAI Python SDK |
| `AnthropicLLMAdapter` | `adapters/llm/anthropic.py` | Official Anthropic SDK |

A small **provider factory** in the composition root selects the adapter instance from `ConfigurationPort` + availability checks. Use cases depend only on `LLMPort`.

### `CLIConfigurationAdapter`

Located at `adapters/cli/configuration.py`. Responsibilities:

- Parse Typer/Click context for flags
- Read env vars
- Resolve `vault_root` via walk-up algorithm (ADR-003)
- Compute absolute `wiki_dir` path
- Expose immutable config object implementing `ConfigurationPort`

---

## Consequences

**Positive**

- Predictable local-first behavior for knowledge workers.
- Obsidian plugin can map native settings to the same port fields without env vars.

**Negative / costs**

- Anthropic requires explicit flag — slightly more typing for Anthropic-only users.
- Model defaults may drift; document in README Environment Variables.

---

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Auto-pick Anthropic when only Anthropic key set | Conflicts with Ollama-first priority in REQ-001 |
| Vault-local config file for API keys | REQ-001 non-goal |
| Single `LLM_API_KEY` | Cannot support three providers cleanly |

---

## Explicit non-decisions

- Prompt content and token limits — use case / adapter tuning in implementation stories.
- Streaming responses — v1 synchronous `LLMPort.complete`.
- Azure OpenAI / other providers — out of v1 scope.

---

## Links

- Requirements: [docs/requirements/REQ-001-llm-wiki-cli.md](REQ-001-llm-wiki-cli.md) — S6–S9, S11, S19
- Related ADRs: [ADR-002](ADR-002-port-interfaces.md), [ADR-005](ADR-005-python-cli-packaging.md)
