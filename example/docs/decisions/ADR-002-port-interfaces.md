# ADR-002: Port interface contracts

**Status:** Accepted
**Date:** 2026-05-30

---

## Context

REQ-001 lists five driven ports plus driving adapters (CLI, future Obsidian plugin). Adapter interchangeability and unit testing depend on stable port contracts (S16). `ConfigurationPort` must remain stable for a future Obsidian settings adapter without domain changes (S19).

---

## Decision

Define five driven ports in `src/llm_wiki/ports/`. Use `typing.Protocol` (preferred) or ABCs. Method names below are binding; signatures may add optional parameters only in backward-compatible ways.

### `ConfigurationPort`

Resolved runtime settings. **Domain and other adapters read only through this port** — never `os.environ` or argparse in use cases.

| Property / method | Type | Notes |
|-----------------|------|-------|
| `vault_root` | `Path` | Absolute vault directory |
| `wiki_dir` | `Path` | Absolute path to wiki subdirectory (default `{vault_root}/wiki`) |
| `batch_mode` | `bool` | `True` when `--batch` (ingest) |
| `provider_override` | `str \| None` | Explicit provider: `ollama`, `openai`, `anthropic` |
| `ollama_base_url` | `str` | Default `http://localhost:11434` |
| `ollama_model` | `str` | See ADR-004 defaults |
| `openai_api_key` | `str \| None` | |
| `openai_model` | `str` | |
| `anthropic_api_key` | `str \| None` | |
| `anthropic_model` | `str` | |

Resolution rules for **CLI adapter** (ADR-004): CLI flags override environment variables when both are set for the same key.

### `LLMPort`

Single interface for all LLM operations (ingest, query, lint). Provider selection uses values from `ConfigurationPort`; adapters implement provider-specific HTTP/local calls.

| Method | Purpose |
|--------|---------|
| `complete(prompt: str, *, system: str \| None = None) -> str` | Synchronous completion for v1; streaming deferred |
| `is_available() -> bool` | Health check for provider selection (Ollama reachability) |

Structured JSON responses are **not** required in v1; use cases parse markdown-oriented text. A future revision may add `complete_structured` without breaking v1 adapters.

### `WikiStoragePort`

All filesystem effects on vault and wiki. Enforces immutability of non-wiki paths (S5).

| Method | Purpose |
|--------|---------|
| `read_source(relative_path: str) -> str` | Read-only vault markdown outside wiki |
| `list_sources() -> list[str]` | Markdown paths respecting excludes (via `SchemaPort`) |
| `read_wiki_page(relative_path: str) -> str` | Path relative to wiki root |
| `write_wiki_page(relative_path: str, content: str) -> None` | Create/update wiki pages |
| `read_index() / write_index(content: str)` | `index.md` |
| `append_log(entry: str) -> None` | Append-only `log.md` |
| `read_ingested() / write_ingested(data: dict) -> None` | `.ingested.json` sidecar (ADR-003) |
| `wiki_exists() -> bool` | Init/idempotency checks |
| `ensure_wiki_layout() -> InitResult` | Create missing init artifacts (idempotent) |

### `SchemaPort`

Parse `wiki/SCHEMA.md` for excludes and documented conventions (S4).

| Method | Purpose |
|--------|---------|
| `load() -> WikiSchema` | Parsed excludes, workflow docs (domain model) |
| `default_excludes() -> list[str]` | Used when SCHEMA missing during init template seed |

### `UserInteractionPort`

Terminal or future UI prompts (S6, S8).

| Method | Purpose |
|--------|---------|
| `confirm(message: str) -> bool` | Query filing, interactive ingest checkpoints |
| `present(text: str) -> None` | Show takeaways / reports to user |
| `prompt(message: str) -> str` | Optional text input |

In `batch_mode`, use cases skip interactive prompts and proceed unattended (S7).

### Application services (driving side)

Use cases are plain classes or functions in `domain/use_cases/` accepting port instances via constructor injection:

- `InitUseCase`, `ValidateUseCase`, `IngestUseCase`, `QueryUseCase`, `LintUseCase`

The **Typer CLI adapter** maps subcommands to these use cases only — no business logic in CLI handlers.

**Contract tests:** For each port, `tests/contract/test_<port>_contract.py` defines behavior expected of every adapter (e.g. fake + filesystem adapter both pass).

---

## Consequences

**Positive**

- Obsidian plugin implements `ConfigurationPort` + `UserInteractionPort` (and optionally a non-terminal `UserInteractionPort`) without touching use cases.
- LLM provider swaps are isolated to `adapters/llm/`.

**Negative / costs**

- Port churn requires updating all adapters and contract tests.

---

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Separate ports per operation (`IngestLLMPort`, `QueryLLMPort`) | Duplicates provider wiring; REQ-001 specifies single `LLMPort` |
| Use cases read env directly for secrets | Violates S19 and Obsidian reuse |
| Rich domain events / CQRS | Over-engineered for v1 scope |

---

## Explicit non-decisions

- Exact prompt templates and wiki page templates — owned by use cases + SCHEMA.md, not ports.
- Obsidian `ConfigurationPort` adapter implementation — future epic.
- Async/`asyncio` LLM calls — v1 synchronous only unless a later ADR adopts async.

---

## Links

- Requirements: [docs/requirements/REQ-001-llm-wiki-cli.md](REQ-001-llm-wiki-cli.md) — S6–S9, S16–S19
- Related ADRs: [ADR-001](ADR-001-hexagonal-architecture.md), [ADR-004](ADR-004-configuration-and-llm-providers.md)
- Related README section: API Contract (CLI ↔ use cases)
