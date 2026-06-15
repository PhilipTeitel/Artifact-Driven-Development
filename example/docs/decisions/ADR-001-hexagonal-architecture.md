# ADR-001: Hexagonal architecture and Python module layout

**Status:** Accepted
**Date:** 2026-05-30

---

## Context

REQ-001 requires Stage 2 as a Python CLI that shares a domain core with a future Obsidian plugin (S16, S17). Staged delivery must not force rework when adding new driving adapters. Domain use cases must not import CLI frameworks, HTTP clients, filesystem libraries, or read `os.environ` directly (S19).

---

## Decision

Adopt **hexagonal (ports and adapters) architecture** for Stage 2 with this module layout under `src/llm_wiki/`:

| Layer | Path | Responsibility |
|-------|------|----------------|
| **Domain** | `domain/models/`, `domain/use_cases/` | Entities, value objects, and use cases (`init`, `validate`, `ingest`, `query`, `lint`). No I/O imports. |
| **Ports** | `ports/` | Abstract interfaces (`typing.Protocol` or ABCs): driven ports consumed by use cases; application services invoked by driving adapters. |
| **Adapters** | `adapters/` | Technology-specific implementations grouped by concern (`cli/`, `llm/`, `storage/`, `schema/`, `interaction/`). |
| **Composition root** | `adapters/cli/main.py` (and `adapters/cli/wiring.py` if needed) | Instantiates adapters, injects ports into use cases, registers Typer commands. **Only** place that imports concrete adapters together. |

**Dependency rule:** `domain` → `ports` only. `adapters` → `domain` + `ports` + third-party libs. `domain` must never import from `adapters`.

**Stage 1** does not ship Python domain code. Cursor commands in `.cursor/commands/` follow the same behavioral contracts documented in ADR-003; they are a separate driving mechanism until Stage 2 implements the core.

**Testing layout:** `tests/unit/` (use cases + port fakes), `tests/contract/` (port contract tests runnable by any adapter), `tests/integration/` (real filesystem, hermetic LLM fixtures, or provider sandboxes).

---

## Consequences

**Positive**

- New driving surfaces (Obsidian plugin) add an adapter + composition wiring without changing use cases.
- New LLM providers add a driven adapter behind `LLMPort`.
- Unit tests run without network, real LLMs, or touching the user's vault.

**Negative / costs**

- More packages and indirection than a single-script CLI.
- Composition root must be maintained as ports grow.

---

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Monolithic CLI script with inline OpenAPI calls | Blocks plugin reuse; violates REQ-001 architectural constraints |
| Clean Architecture with separate `application`/`infrastructure` naming | Equivalent to hexagonal; ports/adapters naming matches REQ-001 vocabulary |
| Shared library extracted only at plugin time | Would require rewriting Stage 2; REQ-001 forbids Stage 1 shortcuts that Stage 2 must undo |

---

## Explicit non-decisions

- This ADR does not define individual port method signatures — see ADR-002.
- This ADR does not choose Typer vs Click — see ADR-005.
- Stage 1 Cursor command implementation details are out of scope here.

---

## Links

- Requirements: [docs/requirements/REQ-001-llm-wiki-cli.md](REQ-001-llm-wiki-cli.md) — S16, S17, S19
- Related README section: High-Level Architecture, Key Design Decisions — Project Structure
- Related stories: (assigned at `/plan-project`)
