<!-- INSTRUCTIONS FOR THE AGENT (do not copy this block into README.md):
This file is the structure for the configured design doc (default `README.md`).

**Who fills what:** Only the **architect** agent fills sections from "High-Level Architecture" through "Backlog Items" (design and plan). During project init, a human may edit only the project title, short description, and optionally the Table of Contents; all other placeholders and sections are left for the architect. Do not infer or fill design/plan sections from the codebase during init.

**When the architect uses this template:** (1) Read the workflow profile and replace every `{ ... }` placeholder with project-specific content from the requirements the user provided. (2) If the configured design doc does not exist, create it from this template. (3) Omit or adapt sections that don't apply. (4) Write the result to the configured design doc in the project root. (5) If the requirements don't provide enough for a section, keep the section and use "TBD" or a short placeholder so the structure stays complete. (6) Preserve copyright/license statements when adapting examples.
-->

# {Project Title}

{ Description of project.  Include major features.  The architect will specify where the requirements are located with links. }

{ Any additional sections that may be needed are marked with `{...}` }

## Table of Contents

{ A list with of the sections below.  Each item should be linked to the corresponding section }

## Requirements

**Purpose and domain model**
{ Link the configured purpose and domain artifacts used to generate this design. Default examples:
- [docs/PURPOSE.md](docs/PURPOSE.md) — product thesis, job, north-star outcome, trade-off rule, anti-thesis
- [docs/DOMAIN.md](docs/DOMAIN.md) — ubiquitous language, data dictionary, entities, invariants, lifecycles, consistency boundaries
If either artifact is not available yet, write `TBD` and explain the risk. }

<!-- Append-only log of requirement files that have been consumed to produce or update this design. Each entry is a linked file path. When new requirements are added via /design-application or /plan-project, append them here — do not remove or reorder prior entries. -->

{ A bullet list of every requirements file used to generate or update this design doc. Each item should be a markdown link to the configured requirements path (default example: `- [docs/requirements/01-initial.md](docs/requirements/01-initial.md)`). Append new entries when additional requirement files are consumed — do not remove prior entries. }

**Architecture decisions included for traceability for backlog alignment**
{ A bullet list of the ADRs used to generate or update this design doc. Each item should be a markdown link to the configured decisions path (default example: `- [docs/decisions/ADR-001-short-slug.md](docs/decisions/ADR-001-short-slug.md) — Accepted; documents constraint context`). Append new entries when additional requirement files are consumed - do not remove prior entries. }

## High-Level Architecture

{ Describe the high-level architecture.  Provide a mermaid diagram.  Give any additional clarifying information to help describe components, processes, flows, etc. Explain how the architecture preserves the purpose thesis and the domain model's consistency boundaries. }

## Technical Stack

{A table describing the technologies used in the project.  Include at a minimum these columns: Layer, Technology, Rationale.}

## Key Design Decisions
{Give key design decisions that answer key design questions and clarify ambiguities.  Some examples are below.  There may be additional subsections needed. }

### 1. Use mock data for development

- Create mock data using expected schema
- use `{example of data from requirements}` for guidance
- ...

### Project Structure
```
{ascii diagram of the project structure}
```

### Logging and Observability

{ Specify the project's logging strategy so the Implementer has a concrete standard to follow. Cover: }

- **Logger** — which library (e.g. Pino, Winston) and why. If none is chosen yet, write "TBD" so it is resolved before implementation begins.
- **Format** — structured JSON, plaintext, or other. Note whether `pino-pretty` or similar is used in development only.
- **Request/correlation IDs** — how they are generated (e.g. `crypto.randomUUID()` in middleware) and propagated (e.g. Fastify `request.id`, async context, header forwarding).
- **Log levels** — confirm the project uses standard levels (`debug`, `info`, `warn`, `error`) and note any project-specific conventions (e.g. `info` for all request completion, `debug` for cache hits).
- **Sensitive data** — state what must never appear in logs (e.g. tokens, PII, full request bodies) and any exceptions the project explicitly allows.

### { ... }

## Prerequisites
{ Give any prerequisites in order to run or build the application }

## 1. Getting Started

{ Give steps needed to install dependencies, configure the environment, run in dev. Substitute commands from the workflow profile's `stack` section where available. An example is below. There may be additional subsections needed. }
```bash
# From the repo root
{stack.installCommand}
```
### 2. Configure environment

```bash
{copy env example command, if the project uses one}
# Edit the environment file if needed.
```

### 3. Run the dev servers

```bash
{configured dev command or per-service commands}
```

Open `{configured local URL}` in your browser, if this project exposes a browser UI.

### { ... }

## Available Scripts
{Scripts used within the project. Use the workflow profile's package manager and stack commands as defaults, then replace or expand with project-specific commands.}

| Command | Description |
|---------|-------------|
| `{stack.buildCommand}` | Build / type-check |
| `{stack.lintCommand}` | Lint |
| `{stack.testCommand}` | Test |
| `{dev command}` | Run locally |

## UI Components

{ If there are any UI components, describe them below using project-specific paths. Example structure: }
Reusable primitives in `{ui components path}`:

| Component     | Description                                        |
|---------------|----------------------------------------------------|
| `{Component}` | `{What it renders and when to use it}`             |

Utility: `{utilityName}` in `{utilityPath}` — `{what it does}`.

## API Contract

{ Give a table of the API routes similar to below. }
| Path | Method | Purpose |
|------|--------|---------|
| `{route path}` | `{GET/POST/...}` | `{observable behavior}` |

## Environment Variables
{ List and describe any environment variables the application requires. Example structure below:}
See [`{env example path}`]({env example path}) for all available variables, if one exists. Key settings:

| Variable            | Default              | Description                          |
|---------------------|----------------------|--------------------------------------|
| `{VAR_NAME}`        | `{default}`          | `{description}`                      |

## { ... }

## Backlog Items
{ The project backlog will go here. Each epic will have a description and a table showing the stories within it. Use configured backlog statuses and story paths. Example structure below. Note how defined stories have links to the story document in the ID column. }

### Epic 1: {Epic Name}

{Epic description.}

| ID | Status | Story | Size | Notes |
|----|--------|-------|------|-------|
| [`{STORY-ID}`]({featuresDir}/{STORY-ID}-{slug}.md) | `{status.backlog.open}` | {Story title} | {S/M/L} | {one-line note} |

## License
MIT © Philip Teitel