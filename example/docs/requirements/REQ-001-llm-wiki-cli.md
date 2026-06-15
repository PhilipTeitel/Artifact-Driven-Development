# REQ-001: LLM Wiki CLI

**Source material:**
- `docs/requirements/llm-wiki.md` — Karpathy LLM-wiki pattern (raw sources, wiki layer, schema; ingest/query/lint operations; index.md and log.md conventions)
- User clarifications (2026-05-30): Obsidian vault (already populated); wiki as configurable subdirectory (default `wiki/`); full operations as **project scope** across epics/stories; terminal CLI run from within vault; staged delivery Cursor-first then standalone Python CLI; LLM via Ollama (local-first) or API (OpenAI, Anthropic); full ADD lifecycle as showcase
- User clarification (2026-05-30): **hexagonal architecture (ports and adapters)** required — proper abstraction across staged delivery so Stage 2 CLI and future Obsidian plugin share a core without rework
- User clarification (2026-05-30): **Stage 1 must be a fully usable end-to-end tool** on a real vault (init, ingest, query, lint) — not a schema-only prototype; user can iterate via SCHEMA.md and Cursor commands before Stage 2
- User clarification (2026-05-30): **configuration (env vars, CLI parameters, etc.) must be a driven port** (`ConfigurationPort`); Stage 2 implements a CLI configuration adapter; future Obsidian plugin uses a native settings adapter on the same port (not implemented until later stage)
- `docs/features/README.md` — project intent to implement the pattern via ADD refinement → design → plan → implement

**Date:** 2026-05-30
**Status:** Draft

---

## 1. Goals

- Enable an **LLM-maintained persistent wiki** inside an **existing Obsidian vault**: the vault's markdown content (excluding the wiki layer and configured excludes) serves as **raw source material**; the CLI builds and maintains a structured, interlinked wiki in a **subdirectory of the vault** (default `wiki/`).
- Deliver **full operations** — init, ingest, query, and lint — as the complete project scope, sliced into **ADD epics and stories** (not a single story).
- Use a **staged delivery path**:
  - **Stage 1 (Cursor-first):** A **fully usable daily driver** — `wiki/SCHEMA.md`, Cursor `/init-wiki`, and slash commands for ingest, query, and lint shipped in `.cursor/commands/`. The user can operate on a real populated vault immediately and evolve behavior by editing SCHEMA.md or commands without waiting for Stage 2.
  - **Stage 2 (standalone CLI):** Python terminal CLI invoked from within the vault (CWD detection or `--vault`), calling **Ollama** (preferred when reachable), **OpenAI**, or **Anthropic** via environment variables.
- Preserve the pattern's core property: the wiki is a **persistent, compounding artifact** — not ephemeral chat output or query-time RAG alone. Good query answers can be **filed back into the wiki** with user confirmation.
- Keep raw sources **immutable**: the tool reads vault content for ingestion but never modifies source files.
- Apply **hexagonal architecture (ports and adapters)** so domain logic (init, ingest, query, lint) is isolated from delivery mechanisms (terminal CLI, Cursor agent, future Obsidian plugin), external systems (LLM providers, filesystem, user prompts), and **runtime configuration** (environment variables, CLI flags, future Obsidian plugin settings).
- **Design for a future Obsidian plugin** (chat window) as a new **driving adapter** on the same domain core; the terminal CLI is the near-term delivery target.
- Deliver through the **full ADD lifecycle**, producing traceable artifacts at each gate so this repo demonstrates that quality software can be built with AI by focusing on **artifacts**, not code alone.

## 2. Non-goals

- **Obsidian plugin with chat UI** in the initial release — documented as a future epic; architecture should not foreclose it.
- Replacing the human as curator — the human sources material, directs analysis, and confirms filing; the LLM writes and maintains wiki pages.
- Embedding-based RAG, vector search, or LLM re-ranking in early releases (`index.md` navigation suffices at moderate scale per source pattern).
- Non-markdown source formats in v1 (PDF, images, audio) — markdown (`.md`) only for first CLI release.
- Auto-applying lint fixes without human/LLM review — lint **suggests** fixes; it does not silently rewrite wiki pages.
- Obsidian `[[wikilinks]]` as the link format — wiki pages use **standard markdown links** `[text](path)`.
- Image download, Obsidian plugin configuration (Dataview, Marp, Web Clipper), or attachment management — user responsibilities per source pattern tips.
- Team/multi-user auth, Slack ingestion, or external service integrations.
- Dedicated vault config files for LLM keys — provider credentials and endpoints use **environment variables** only.
- **Monolithic or tightly coupled architecture** where CLI, LLM clients, or filesystem access are embedded in use-case logic — domain core must not import adapter implementations directly.
- Rewriting domain logic when adding the Obsidian plugin or a new LLM provider — new surfaces and providers must plug in via ports.
- **Stage 1 as schema-only or non-functional prototype** — Stage 1 must deliver working init, ingest, query, and lint via Cursor on a real vault before Stage 2 begins.
- **Obsidian plugin configuration adapter** in Stage 2 — the `ConfigurationPort` interface is defined and the CLI adapter is implemented; the Obsidian-native settings adapter is a future stage only.
- **Direct configuration access in domain code** — use cases must not read `os.environ`, parse CLI arguments, or read Obsidian settings; all runtime config flows through `ConfigurationPort`.

## 3. Personas / actors

- **Knowledge worker** — Has a populated Obsidian vault. Runs Cursor commands (Stage 1) or the terminal CLI (Stage 2) from within the vault. Browses the wiki in Obsidian (graph view, links) while the LLM ingests sources, answers questions, and lints the wiki. Prefers interactive ingest with the option to batch-process a directory unattended.

- **ADD practitioner** — Uses this repository as a reference walkthrough of Artifact-Driven Development: requirements → design → ADRs → epics/stories → implementation → review → QA → documentation, with evidence at each gate.

## 4. Delivery phases (project scope)

These phases guide epic slicing in `/plan-project`; they are not implementation design.

| Phase | Deliverable | Primary actor |
|-------|-------------|---------------|
| **Stage 1** | **Fully usable Cursor-based tool:** `wiki/SCHEMA.md` template; `/init-wiki`; ingest, query, lint commands in `.cursor/commands/` — operable on a real vault immediately; user iterates via SCHEMA.md and commands | Cursor agent + human |
| **Stage 2** | Python CLI as a **driving adapter** over a hexagonal domain core; init, validate, ingest, query, lint with Ollama/OpenAI/Anthropic via **driven adapters** | Standalone terminal |
| **Future** | Obsidian plugin as driving adapter + **Obsidian `ConfigurationPort` adapter** (native plugin settings UI) on the same domain core | Out of scope for Stage 2 |

Stage 1 (Cursor commands) defines behavioral contracts and wiki artifacts **and must be shippable as a complete, usable tool**; Stage 2 implements those same contracts in a hexagonal Python core. Stage 1 wiki artifacts and SCHEMA.md carry forward — Stage 2 adds a standalone terminal interface, not a replacement wiki. Stage 1 must not force architectural shortcuts that Stage 2 would have to undo.

## 5. User scenarios (Gherkin)

### S1 — Initialize wiki in a populated Obsidian vault

```gherkin
Given an existing Obsidian vault with markdown content outside the wiki subdirectory
And   the user is in the vault directory or passes --vault /path/to/vault
When  the user runs init (Cursor /init-wiki in Stage 1, or CLI init in Stage 2)
Then  the tool creates the wiki subdirectory (default wiki/, overridable via --wiki-dir)
And   the tool creates wiki/SCHEMA.md describing layers, workflows, and exclude paths
And   the tool creates wiki/index.md with an initial empty catalog structure
And   the tool creates wiki/log.md as an append-only chronological record
And   existing vault files outside the wiki subdirectory are not modified or moved
And   the tool exits successfully and reports what was created
```

### S2 — Idempotent init on an existing wiki

```gherkin
Given a vault that already has a valid LLM-wiki layout from a prior init
When  the user runs init again
Then  the tool does not overwrite or destroy existing wiki pages, index entries, or log history
And   the tool creates only missing required pieces
And   the tool reports what already existed vs what was added
And   the tool exits successfully
```

### S3 — Reject invalid vault context

```gherkin
Given a working directory that is not inside an Obsidian vault and no valid --vault path is provided
When  the user runs any wiki command
Then  the tool exits with a non-zero status
And   the tool prints a clear error explaining how to specify the vault
And   no partial wiki structure is left in an inconsistent state
```

### S4 — Schema defines workflows and excludes

```gherkin
Given a vault initialized with wiki/SCHEMA.md
When  the user or agent reads SCHEMA.md
Then  it describes the three layers: vault sources (read-only), wiki (LLM-owned), and schema (configuration)
And   it documents ingest, query, and lint workflows
And   it lists user-configured exclude paths that are not treated as ingest sources
And   it references index.md and log.md update conventions including log entry prefix format
```

### S5 — Raw sources remain immutable

```gherkin
Given a populated vault with markdown files outside the wiki subdirectory
When  the user runs ingest, query, lint, or init
Then  the tool never modifies, deletes, or renames any file outside the wiki subdirectory
```

### S6 — Ingest source interactively

```gherkin
Given a vault with at least one markdown file outside the wiki subdirectory and excludes
And   an LLM provider is available (Ollama reachable, or API key in environment)
When  the user runs ingest without --batch for a specific source file
Then  the LLM reads the source and presents key takeaways for user review
And   the LLM writes or updates wiki pages (summary, entity/concept pages, cross-references)
And   the LLM updates wiki/index.md and appends an entry to wiki/log.md
And   the source file itself is not modified
```

### S7 — Ingest directory in batch mode

```gherkin
Given a vault with multiple markdown files outside the wiki subdirectory and excludes
And   an LLM provider is available
When  the user runs ingest --batch on a directory path
Then  the tool processes all markdown files in that directory sequentially without interactive prompts
And   each processed file produces wiki updates, index updates, and a log entry
And   files matching exclude paths in SCHEMA.md are skipped
And   already-ingested sources are skipped or reported (tracked via wiki/.ingested.json sidecar)
```

### S8 — Query wiki and optionally file answer

```gherkin
Given a vault with an initialized wiki containing indexed pages
And   an LLM provider is available
When  the user runs query with a natural-language question
Then  the LLM reads wiki/index.md to locate relevant pages, then reads those pages
And   the LLM synthesizes an answer with citations to wiki pages
And   the answer is printed to the terminal
And   the tool prompts the user whether to file the answer as a new wiki page
And   if the user confirms, the LLM creates the page, updates index.md, and appends to log.md
And   if the user declines, no wiki files are changed by the filing step
```

### S9 — Lint wiki and suggest fixes

```gherkin
Given a vault with an initialized wiki
And   an LLM provider is available
When  the user runs lint
Then  the LLM checks for contradictions, stale claims, orphan pages, missing concept pages, and missing cross-references
And   the tool prints a report of findings with suggested fixes
And   the tool appends a lint entry to wiki/log.md
And   the tool does not automatically apply fixes to wiki pages
```

### S10 — Validate vault structure

```gherkin
Given an Obsidian vault path
When  the user runs validate (Stage 2 CLI)
Then  the tool reports whether the vault conforms to the LLM-wiki layout
And   for each missing or malformed required piece, the tool names what is wrong
And   the tool exits non-zero if validation fails, zero if valid
```

### S11 — Select LLM provider with local-first default

```gherkin
Given resolved configuration from ConfigurationPort
When  Ollama is reachable per configuration
And   the user has not specified --provider anthropic
Then  the tool uses Ollama
When  Ollama is not reachable but OpenAI credentials are present in configuration
Then  the tool uses OpenAI
When  the user specifies --provider anthropic and Anthropic credentials are present in configuration
Then  the tool uses Anthropic
When  no provider is available per configuration
Then  the tool exits with a non-zero status and a clear error
```

### S12 — Track ingested sources via sidecar file

```gherkin
Given a vault where a source file has been successfully ingested
When  the ingest completes
Then  the tool records the source path and ingest timestamp in wiki/.ingested.json
And   the source file itself is not modified
When  the user runs ingest --batch on a directory containing that source
Then  the tool skips the already-ingested source and reports it as skipped
```

### S13 — Log entry format supports unix tooling

```gherkin
Given a vault with wiki/log.md
When  an ingest, query, or lint operation completes
Then  the appended log entry uses the heading prefix "## [YYYY-MM-DD] {operation} | {title}"
And   entries are grep-parseable by simple unix tools
```

### S14 — Cursor commands operate on vault layout (Stage 1)

```gherkin
Given Cursor with commands from this repo's .cursor/commands/ available
And   the user opens a populated vault as a workspace
When  the user runs /init-wiki, then ingest, query, or lint commands
Then  the Cursor agent follows wiki/SCHEMA.md conventions
And   the agent produces the same observable wiki artifacts as the standalone CLI (index, log, pages, .ingested.json)
And   raw source files outside the wiki subdirectory remain unmodified
```

### S18 — Stage 1 is a usable daily driver on a real vault

```gherkin
Given Stage 1 Cursor commands and SCHEMA.md template are shipped
And   the user has a populated Obsidian vault with markdown sources
When  the user completes the Stage 1 epic (no Stage 2 CLI required)
Then  the user can init a wiki, ingest at least one source, query the wiki, and lint the wiki entirely within Cursor
And   the resulting wiki is browsable in Obsidian with persistent pages, index, and log
And   the user can change future behavior by editing wiki/SCHEMA.md or .cursor/commands/ without code changes
And   Stage 1 acceptance does not depend on Stage 2 being started or complete
```

### S15 — ADD traceability for delivery

```gherkin
Given this repository follows the ADD workflow
When  a reader inspects docs/requirements/, docs/decisions/, and docs/features/
Then  they can trace from REQ-001 scenarios (S1–S19) through design, epics, stories, and QA evidence
And   the README backlog reflects Stage 1, Stage 2, and future plugin work
```

### S16 — Hexagonal boundaries enable staged delivery

```gherkin
Given the Stage 2 Python implementation
When  a developer inspects the codebase structure
Then  domain use cases (init, ingest, query, lint) depend only on port interfaces, not on concrete adapters
And   LLM providers (Ollama, OpenAI, Anthropic) are driven adapters behind a single LLM port
And   vault/wiki filesystem access is behind a storage port
And   user interaction (prompts, confirmations) is behind a user-interface port
And   runtime configuration (vault path, wiki dir, provider, credentials, batch mode) is behind a configuration port
And   the CLI entrypoint is a driving adapter that orchestrates use cases via ports
And   domain logic is unit-testable with port fakes without calling real LLMs, touching the filesystem, or reading environment variables
```

### S17 — New delivery surface reuses domain core

```gherkin
Given a working Stage 2 CLI backed by the hexagonal domain core
When  a future Obsidian plugin driving adapter is added
Then  it invokes the same domain use cases via the same ports
And   no ingest, query, or lint business logic is duplicated in the plugin layer
And   the plugin supplies configuration via a ConfigurationPort adapter backed by Obsidian native settings
And   adding the plugin does not require changes to domain use cases, LLM adapters, or storage adapters
```

### S19 — Configuration flows through a port

```gherkin
Given the Stage 2 Python implementation
When  a use case needs runtime configuration (vault path, wiki subdirectory, LLM provider, credentials, batch mode, model names)
Then  it reads values from ConfigurationPort, not from os.environ or CLI argument parsers directly
Given the CLI is the active delivery mechanism
When  the user passes CLI flags and/or has environment variables set
Then  the CLI configuration adapter resolves values (CLI flags override environment variables where both apply)
And   the resolved configuration is exposed to use cases through ConfigurationPort
Given only the ConfigurationPort interface exists (Obsidian adapter not yet built)
When  a future Obsidian plugin is implemented
Then  it provides an Obsidian-native ConfigurationPort adapter without changing domain use cases or other ports
```

## 6. Constraints

- **Vault model:** An existing, populated Obsidian vault. Vault root supplied via `ConfigurationPort` (CLI adapter: walk up from CWD until `.obsidian/` or `wiki/SCHEMA.md`, or `--vault` flag).
- **Wiki location:** Supplied via `ConfigurationPort` (CLI adapter: `--wiki-dir` flag, default `wiki/`). No persistent vault config file for wiki name.
- **Source scope:** All markdown in the vault **except** the wiki subdirectory and paths listed as excludes in `wiki/SCHEMA.md`. Markdown (`.md`) only in v1.
- **Schema location:** `wiki/SCHEMA.md` — the configuration document for both Cursor agents and the standalone CLI.
- **Link format:** Standard markdown links, not Obsidian wikilinks.
- **LLM providers:** Ollama (local-first default), OpenAI, Anthropic — credentials and provider selection supplied via `ConfigurationPort` (CLI adapter: environment variables with `--provider` and related flags overriding where applicable).
- **Immutability:** Files outside the wiki subdirectory are read-only from the tool's perspective.
- **Interactivity:** Ingest is interactive by default; batch mode supplied via `ConfigurationPort` (CLI adapter: `--batch` flag).
- **Query filing:** Answers print to terminal; user is prompted before filing into wiki.
- **Lint:** Suggest fixes only; no silent auto-fix.
- **Language (Stage 2):** Python.
- **Cursor commands (Stage 1):** Shipped in this repo under `.cursor/commands/`. Stage 1 epic is **not complete** until init, ingest, query, and lint all work end-to-end on a real vault via those commands.
- **Stage 1 usability:** Stage 1 is a shippable product increment — the user can maintain a compounding wiki daily in Cursor + Obsidian before Stage 2 exists. Iteration path: edit `wiki/SCHEMA.md` and `.cursor/commands/`.
- **ADD delivery:** Full lifecycle with human gates; work sliced into epics and stories.
- **Future plugin:** Stage 2 architecture must separate core logic from CLI shell so an Obsidian plugin can reuse it.
- **Ingested tracking:** `wiki/.ingested.json` sidecar maps source paths to ingest timestamps; source files are never modified.
- **Wiki layout at init:** Flat `wiki/` directory; SCHEMA.md documents that the LLM may create subfolders as the wiki grows.
- **Default excludes (SCHEMA.md template):** `.obsidian/`, wiki subdirectory, and dotfiles (`.*`).

### Architectural constraints (hexagonal)

- **Domain core:** Contains use cases and domain models only — vault context, wiki operations, ingest/query/lint orchestration. No imports of CLI frameworks, HTTP clients, or filesystem libraries in domain logic.
- **Driving ports (inbound):** Application services invoked by delivery mechanisms — CLI commands (Stage 2), future Obsidian plugin UI. Stage 1 Cursor commands follow the same behavioral contracts but are not Python code.
- **Driven ports (outbound):**
  - `ConfigurationPort` — runtime settings: vault path, wiki subdirectory, LLM provider and credentials, model names, batch/interactive mode, and other operational flags. **Stage 2:** `CLIConfigurationAdapter` (environment variables + CLI flags; flags override env). **Future:** `ObsidianConfigurationAdapter` (native plugin settings UI) — port defined in Stage 2, Obsidian adapter not implemented until a later stage.
  - `LLMPort` — complete prompts, return structured responses (shared by ingest, query, lint); provider selection and credentials come from `ConfigurationPort`, not env vars directly
  - `WikiStoragePort` — read/write wiki pages, index, log, `.ingested.json`; read-only access to vault sources
  - `SchemaPort` — parse `wiki/SCHEMA.md` (excludes, conventions)
  - `UserInteractionPort` — interactive prompts, batch/bypass, query filing confirmation
- **Adapters:** One adapter per port per technology — e.g. `CLIConfigurationAdapter`, `OllamaLLMAdapter`, `OpenAILLMAdapter`, `FilesystemWikiStorageAdapter`, `TerminalUserInteractionAdapter`, `TyperCLIAdapter`. Adapters are wired at the composition root (CLI entrypoint), not inside use cases.
- **Staged delivery rule:** Stage 2 stories implement domain core and ports first; adapters and CLI shell are thin. No Stage 2 story may embed LLM or I/O calls directly in use-case code.
- **Testability:** Every domain use case must be verifiable with port fakes/mocks — no live LLM or filesystem required for unit tests.
- **Design artifact:** `/design-application` must produce an ADR for hexagonal structure and document port interfaces before implementation stories begin.

## 7. Resolved questions

| # | Question | Resolution | Source |
|---|----------|------------|--------|
| 1 | What is a "vault"? | An existing, populated Obsidian vault directory. | user (2026-05-30) |
| 2 | Where does the wiki live? | A subdirectory within the vault; default `wiki/`, configurable via `--wiki-dir` (no persistent config file). | user (2026-05-30) |
| 3 | What counts as raw source material? | All vault markdown except the wiki subdirectory and user-configured excludes (listed in `wiki/SCHEMA.md`). | user (2026-05-30) |
| 4 | Project scope vs first story? | Full operations (init, ingest, query, lint) across multiple ADD epics/stories — not one story. | user (2026-05-30) |
| 5 | Staging approach? | Stage 1: Cursor-first (schema + slash commands including `/init-wiki`); Stage 2: standalone Python CLI with direct LLM calls. | user (2026-05-30) |
| 6 | LLM integration? | Direct API/local calls in Stage 2 CLI; Stage 1 uses Cursor agent following SCHEMA.md. Providers: Ollama, OpenAI, Anthropic. | user (2026-05-30) |
| 7 | LLM configuration? | Environment variables for keys and endpoints; `--provider` flag for explicit selection. | user (2026-05-30) |
| 8 | Default provider priority? | Ollama if reachable → OpenAI if key set → Anthropic only when explicitly selected. | user (2026-05-30) |
| 9 | Ingest interactivity? | Interactive by default; `--batch` for unattended directory ingest. | user (2026-05-30) |
| 10 | Batch ingest scope? | All markdown in the specified directory, respecting excludes; skip already-ingested (via log). | user (2026-05-30) |
| 11 | Query output? | Print to terminal; prompt user before filing answer into wiki. | user (2026-05-30) |
| 12 | Lint behavior? | Report findings and suggest fixes; do not auto-apply. | user (2026-05-30) |
| 13 | Schema file location? | `wiki/SCHEMA.md`. | user (2026-05-30) |
| 14 | Exclude path storage? | Listed in `wiki/SCHEMA.md`, parsed by CLI and agents. | user (2026-05-30) |
| 15 | Link format? | Standard markdown links. | user (2026-05-30) |
| 16 | Source file types v1? | Markdown (`.md`) only. | user (2026-05-30) |
| 17 | CLI invocation? | Detect vault from CWD or accept `--vault /path`. | user (2026-05-30) |
| 18 | Stage 2 language? | Python. | user (2026-05-30) |
| 19 | Cursor commands location? | Shipped in this repo under `.cursor/commands/`. | user (2026-05-30) |
| 20 | Stage 1 includes init? | Yes — Cursor `/init-wiki` creates wiki layout and SCHEMA.md. | user (2026-05-30) |
| 21 | Future Obsidian plugin? | Out of scope for v1; design Stage 2 core for reuse by a future plugin. | user (2026-05-30) |
| 22 | ADD demo purpose? | Full lifecycle showcase — artifacts over code as the narrative. | user (2026-05-30) |
| 23 | Anthropic in v1? | Yes — all three providers (Ollama, OpenAI, Anthropic) from Stage 2 start. | user (2026-05-30) |
| 24 | Already-ingested detection? | Sidecar file `wiki/.ingested.json`; source files never modified. | user (2026-05-30) |
| 25 | Wiki internal layout at init? | Flat `wiki/`; LLM may create subfolders as wiki grows (documented in SCHEMA.md). | user (2026-05-30) |
| 26 | Default exclude paths? | Template seeds: `.obsidian/`, wiki subdirectory, dotfiles (`.*`); user adds more in SCHEMA.md. | user (2026-05-30) |
| 27 | Vault root detection? | Walk up from CWD until `.obsidian/` or `wiki/SCHEMA.md` found. | user (2026-05-30) |
| 28 | Default model names? | Defer to design phase / LLM provider ADR. | user (2026-05-30) |
| 29 | Architecture style? | Hexagonal (ports and adapters) — domain core isolated from CLI, LLM providers, filesystem, and user I/O; supports staged delivery and future Obsidian plugin. | user (2026-05-30) |
| 30 | Is Stage 1 usable without Stage 2? | Yes — Stage 1 must be a fully usable end-to-end tool (init, ingest, query, lint) on a real vault; user iterates via SCHEMA.md and commands; not a prototype. | user (2026-05-30) |
| 31 | Where does runtime configuration live? | `ConfigurationPort` driven port; Stage 2 implements `CLIConfigurationAdapter` (env vars + CLI flags); future Obsidian plugin implements native settings adapter on same port. Domain code never reads env/CLI/Obsidian settings directly. | user (2026-05-30) |

## 8. Open questions

Remaining items are suitable for `/design-application` (ADR-level detail, not requirement ambiguity):

- [ ] **Default model names and env var names** per provider — deferred to design; exposed via `ConfigurationPort`, not read directly by use cases.
- [ ] **Stage 1 Cursor command names** — propose during `/plan-project` (e.g. `/init-wiki`, `/wiki-ingest`, `/wiki-query`, `/wiki-lint`).

## 9. Suggested ADR triggers

| Trigger | Why it likely needs an ADR | Related Sn |
|---------|----------------------------|------------|
| **Stage 1 epic completion criteria** | Stage 1 must gate on S18 — usable tool, not templates alone; affects QA evidence for first epic | S14, S18 |
| Hexagonal architecture and module layout | Binding structural decision for all Stage 2 stories; defines domain vs ports vs adapters vs composition root | S16, S17 |
| **Port interface definitions** (`ConfigurationPort`, `LLMPort`, `WikiStoragePort`, `SchemaPort`, `UserInteractionPort`) | Contract between domain and adapters; `ConfigurationPort` must be stable before Obsidian plugin | S16, S17, S19, S6–S9 |
| **`ConfigurationPort` and CLI adapter** | Env vars + CLI flags with override rules; Obsidian adapter deferred but port shape is binding now | S11, S19 |
| Python CLI packaging and distribution | Long-lived tooling choice; affects CI, install, plugin reuse; CLI is a driving adapter only | S1, S14, S16 |
| LLM provider adapters (Ollama/OpenAI/Anthropic) | Driven adapters behind `LLMPort`; must not leak provider SDKs into domain | S6–S9, S11, S16 |
| Composition root and dependency wiring | Where adapters are assembled (CLI entrypoint); affects testability and plugin reuse | S16, S17 |
| Vault layout, SCHEMA.md format, and exclude parsing | Hard to migrate; shared by Cursor commands and CLI; `SchemaPort` contract | S1, S4, S5, S7 |
| Ingested-source tracking (`wiki/.ingested.json`) | Sidecar format is binding for batch idempotency; `WikiStoragePort` concern | S7, S12 |
| Provider selection and configuration contract | Local-first default, credentials, model names — owned by `ConfigurationPort`, consumed by LLM adapters | S11, S19 |
| Wiki page organization conventions | Flat init layout; LLM-created subfolders over time | S1, S6 |
| Vault root detection algorithm | Walk-up to `.obsidian/` or `wiki/SCHEMA.md`; vault context in domain | S3, S10 |

## 10. Links

- Source material: see header
- Pattern reference: [Karpathy LLM-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- ADD process: [Artifact-Driven-Development](file:///Users/philipteitel/code/Artifact-Driven-Development)
- Related REQ files: (none — REQ-001 is first)
- Related ADRs: (none yet)

---

*Created: 2026-05-30 | Refined by: architect in Discovery Mode*
