# ADR-005: Python CLI packaging, tooling, and composition root

**Status:** Accepted
**Date:** 2026-05-30

---

## Context

Stage 2 delivers a terminal CLI invoked from within an Obsidian vault (REQ-001). The CLI is a **driving adapter** only; packaging and distribution choices affect CI, install docs, and future plugin bundling of the domain wheel.

---

## Decision

### Packaging

- **Build backend:** Hatchling (or setuptools) via `pyproject.toml` at repo root.
- **Package name:** `llm-wiki` (PyPI-style); import path `llm_wiki`.
- **Python version:** `>=3.11`.
- **Console script entry point:**

  ```toml
  [project.scripts]
  llm-wiki = "llm_wiki.adapters.cli.main:app"
  ```

- **Dependencies (runtime):** `typer[all]`, `httpx`, `openai`, `anthropic`, `pydantic` (config models optional), `rich` (terminal output via Typer).

### CLI framework

**Typer** for subcommands, `--help`, and type-hinted options. Subcommands:

| Command | Use case | REQ scenarios |
|---------|----------|---------------|
| `init` | `InitUseCase` | S1, S2 |
| `validate` | `ValidateUseCase` | S10 |
| `ingest [PATH]` | `IngestUseCase` | S6, S7, S12 |
| `query TEXT...` | `QueryUseCase` | S8 |
| `lint` | `LintUseCase` | S9 |

Global options on app callback: `--vault`, `--wiki-dir`, `--provider`, `--batch` (ingest only where applicable).

Exit codes: `0` success, `1` user/validation error, `2` usage error (Typer default).

### Composition root

`adapters/cli/main.py`:

1. Build `CLIConfigurationAdapter` from argv + env.
2. Construct `FilesystemWikiStorageAdapter`, `MarkdownSchemaAdapter`, `TerminalUserInteractionAdapter`.
3. Select `LLMPort` implementation via provider factory (ADR-004).
4. Inject ports into use cases; invoke from Typer commands.

No other module may wire concrete adapters together.

### Development tooling

| Tool | Purpose |
|------|---------|
| `uv` or `pip install -e ".[dev]"` | Editable install |
| `pytest` | Unit, contract, integration tests |
| `ruff` | Lint + format |
| `mypy` (optional strict on `domain/` + `ports/`) | Type-check ports and use cases |

### Logging

Use Python **stdlib `logging`** with module loggers (`llm_wiki.domain`, `llm_wiki.adapters...`). Default level `WARNING` for end users; `LLM_WIKI_LOG=DEBUG` env enables verbose adapter diagnostics. **Never log API keys or full prompt bodies** at INFO or below in shared logs.

### Future Obsidian plugin integration (binding clarification)

Obsidian plugins run as **TypeScript in Electron**. Python is the right language for Stage 2’s domain core and CLI; it does **not** imply the plugin will import or embed Python inside the Electron renderer/main process.

**Rejected for the plugin (do not pursue):**

- Embedding CPython, Pyodide, or similar inside the Obsidian/Electron bundle to call `llm_wiki` in-process
- Native Node↔Python bindings (e.g. `node-python-bridge`) inside the plugin process
- Any design that requires the plugin to load the Python wheel as a linked library in-process

Rationale: Electron’s process model, security sandboxes, packaging size, and platform matrix make in-process Python a high-cost, fragile path. Prior experience with Electron restrictions reinforces avoiding this entirely.

**Approved integration strategies (in priority order for a future plugin epic):**

1. **Subprocess to `llm-wiki` (preferred for S17)** — The plugin is a driving adapter in TypeScript: Obsidian UI, `ObsidianConfigurationAdapter` (maps plugin settings → env/flags), and `child_process` (or equivalent) invoking the installed `llm-wiki` binary with `--vault` pointed at the active vault. Business logic stays in the existing Python use cases; no duplication of ingest/query/lint orchestration. Stage 2 should keep the CLI stable, scriptable, and non-interactive where flags allow (e.g. `--batch`); machine-readable output (e.g. `--json`) may be added in a later plugin-focused ADR if the UI needs structured results.

2. **Out-of-process service (optional variant)** — A long-lived local Python process exposing a narrow API (HTTP or IPC) that wraps the same composition root as the CLI. Same reuse story as (1), with more operational complexity; only justified if subprocess-per-action is too slow or too awkward.

3. **TypeScript reimplementation (fallback)** — A second implementation of port contracts and use-case behavior in TypeScript, kept aligned via ADR-002 port shapes, vault layout (ADR-003), and shared scenario/contract tests. This mirrors **Stage 1** (Cursor agent, not Python): behavioral parity on wiki artifacts matters more than a shared runtime. Acceptable when subprocess is impractical (e.g. mobile, strict sandbox), at the cost of maintaining two cores.

**What Stage 2 must preserve for (1) and (2):**

- Thin Typer handlers; all orchestration in `domain/use_cases/`
- Documented exit codes and CLI flags (ADR-004)
- Vault/wiki contracts unchanged (ADR-003) so plugin and CLI produce identical artifacts

A dedicated **ADR-006** (or plugin epic story) may later specify subprocess argv conventions, JSON output, and install/discovery of `llm-wiki` on the user’s PATH. This ADR only rules out in-process Python and states the preferred direction.

---

## Consequences

**Positive**

- Standard `pip install` / `uv tool install` path for knowledge workers.
- A single Python domain implementation serves terminal users and a future plugin via **out-of-process** invocation (subprocess or service), satisfying S17 without Electron/Python coupling.
- Port and vault contracts (ADR-002, ADR-003) remain the portable spec if a TypeScript port is ever needed.

**Negative / costs**

- Typer/Rich dependency weight for a small CLI — acceptable for UX.
- Plugin users must have `llm-wiki` installed and on PATH (or plugin must resolve install location); document in plugin epic.
- Subprocess UX requires clear error propagation from CLI exit codes/stderr into Obsidian notices.

---

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| `click` without Typer | Typer reduces boilerplate; both acceptable — Typer chosen for type hints |
| Single-file `llm_wiki.py` | Conflicts with hexagonal layout |
| `poetry` | `pyproject.toml` + hatch/uv is sufficient; avoid locking tool unless team prefers |
| **TypeScript-only monorepo** (no Python) for CLI + plugin | REQ-001 binds Stage 2 to Python; TS-only would abandon accepted stack choice |
| **Embedded Python in Obsidian plugin** | Rejected — see “Future Obsidian plugin integration” above; Electron constraints and maintenance cost |
| **Plugin reimplements logic with no shared tests** | Violates S17 spirit; if TS port is used, contract/scenario tests must keep parity |

---

## Explicit non-decisions

- PyPI publication name availability — verify at release time.
- Subprocess argv, JSON schema, and `llm-wiki` discovery on user machines — future ADR or plugin epic (not blocking Stage 2 CLI).
- Docker image — not required for v1.
- **In-process Python inside Obsidian/Electron** — explicitly out of scope; do not prototype.

---

## Links

- Requirements: [docs/requirements/REQ-001-llm-wiki-cli.md](REQ-001-llm-wiki-cli.md) — S1, S3, S10, S14, S16, S17
- Related ADRs: [ADR-001](ADR-001-hexagonal-architecture.md), [ADR-004](ADR-004-configuration-and-llm-providers.md)
