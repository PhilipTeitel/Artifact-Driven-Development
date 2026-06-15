<!-- INSTRUCTIONS FOR THE AGENT (do not copy this block into README.md):
This file is the structure for the project's README.

**Who fills what:** Only the **architect** agent fills sections from "High-Level Architecture" through "Backlog Items" (design and plan). During project init, a human may edit only the project title, short description, and optionally the Table of Contents; all other placeholders and sections are left for the architect. Do not infer or fill design/plan sections from the codebase during init.

**When the architect uses this template:** (1) Replace every `{ ... }` placeholder with project-specific content from the requirements the user provided. (2) If no README.md exists, create it from this template. (3) Omit or adapt sections that don't apply. (4) Write the result to README.md in the project root. (5) If the requirements don't provide enough for a section, keep the section and use "TBD" or a short placeholder so the structure stays complete.
-->

# {Project Title}

{ Description of project.  Include major features.  The architect will specify where the requirements are located with links. }

{ Any additional sections that may be needed are marked with `{...}` }

## Table of Contents

{ A list with of the sections below.  Each item should be linked to the corresponding section }

## Requirements

<!-- Append-only log of requirement files that have been consumed to produce or update this design. Each entry is a linked file path. When new requirements are added via /design-application or /plan-project, append them here — do not remove or reorder prior entries. -->

{ A bullet list of every requirements file used to generate or update this README. Each item should be a markdown link to the file path (e.g. `- [docs/requirements/01-initial.md](docs/requirements/01-initial.md)`). Append new entries when additional requirement files are consumed — do not remove prior entries. }

**Architecture decisions included for traceability for backlog alignment**
{ A bullet list of the ADRs used to generate or update this README.  Each item should be a markdown link to the filepath (e.g. `- [docs/decisions/ADR-001-wasm-sqlite-vec-shipped-plugin.md](docs/decisions/ADR-001-wasm-sqlite-vec-shipped-plugin.md) — Superseded by ADR-006; documents iteration 1 constraint context`).  Append new entries when additional requirement files are consumed - do not remove prior entries. }

## High-Level Architecture

{ Describe the high-level architecture.  Provide a mermaid diagram.  Give any additional clarifying information to help describe components, processes, flows, etc. }

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

{ Give steps needed to install dependencies, configure the environment, run in dev.  An example is below. There may be additional subsections needed. }
```bash
# From the repo root — install client, server, and shared packages
cd client  && npm install && cd ..
cd server  && npm install && cd ..
cd shared  && npm install && cd ..
```
### 2. Configure environment

```bash
cp server/.env.example server/.env
# Edit server/.env if needed; defaults use mock data (USE_MOCK_DATA=true)
```

### 3. Run the dev servers

```bash
# Terminal 1 — API server (port 3000)
cd server && npm run dev

# Terminal 2 — Client dev server (port 5173)
cd client && npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### { ... }

## Available Scripts
{Scripts used within the project.  This would be scripts that might appear in the equivalent to the `scripts` section of a `package.json` file.}

### Client (`client/`)

| Command          | Description                        |
|------------------|------------------------------------|
| `npm run dev`    | Start Vite dev server with HMR     |
| `npm run build`  | Type-check and build for production|
| `npm run lint`   | Run ESLint                         |
| `npm run preview`| Preview production build locally   |

### Server (`server/`)

| Command              | Description                           |
|----------------------|---------------------------------------|
| `npm run dev`        | Start with nodemon (auto-reload)      |
| `npm run dev:api`    | Start without file watching           |
| `npm run build`      | Compile TypeScript                    |
| `npm run typecheck`  | Type-check without emitting           |

## UI Components

{ If there are any UI components, they would described below similar to this: }
Reusable primitives in `client/src/components/` (added in OTO-1):

| Component     | Description                                        |
|---------------|----------------------------------------------------|
| `KPI`         | Icon + label + value card for key metrics          |
| `Card`        | Rounded container with shadow                      |
| `Section`     | Layout block with title, subtitle, and right slot  |
| `FilterBar`   | Dropdowns for portfolio/PM/client/practice filters |
| `Breadcrumb`  | Clickable navigation path with Home button         |

Utility: `downloadCSV` in `client/src/lib/download-csv.ts` — triggers browser CSV download from row data.

## API Contract

{ Give a table of the api routes similar to below. }
| -------------------------- | ------ | ----------------------------------------------- |
| `/api/customers`            | GET    | List customers and their info                  |
| `/api/customers/:id`        | GET    | Single project detail                          |
| `/api/invoices  `           | GET    | List invoices and their info                   |

## Environment Variables
{ List and describe any environment variables the application requires.  An example is below:}
See [`server/.env.example`](server/.env.example) for all available variables. Key settings:

| Variable            | Default              | Description                          |
|---------------------|----------------------|--------------------------------------|
| `PORT`              | `3000`               | API server port                      |
| `CORS_ORIGIN`       | `http://localhost:5173` | Allowed CORS origin               |
| `USE_MOCK_DATA`     | `true`               | Use mock data instead of live API    |
| `AUTH_ENABLED`      | `false`              | Enable JWT auth (off for MVP)        |
| `CACHE_TTL_MS`      | `300000`             | In-memory cache TTL (5 min default)  |

## { ... }

## Backlog Items
{ The project backlog will go here. Each epic will have a description and a table showing the stories within it. An example is below.  Note how defined stories have links to the story document in the ID column. }

### Epic 1: Project Foundation

Core infrastructure and scaffolding.

| ID    | Status   | Story                                                                 | Size | Notes                                                                                       |
| ----- | -------- | --------------------------------------------------------------------- | ---- | ------------------------------------------------------------------------------------------- |
| [FND-1](docs/features/FND-1-initialize-frontend) | **DONE**     | ~~Initialize React frontend with Vite + Tailwind + TypeScript~~       | S    | Vite 7 + React 19 + Tailwind v4 + TS                                                        |
| FND-2 | **DONE**     | ~~Create shared types package for client/server~~                     | S    | shared/types.ts + @shared/* alias                                                           |
| FND-3 | **DONE**     | ~~Implement Fastify server structure (routes, middleware, services)~~ | M    | 6 route plugins, error handler, auth middleware, DataProvider abstraction, JSON schemas     |
| FND-4 | **DONE**     | ~~Create mock data service mirroring Planview schema~~                | M    | mock-data.ts + MockProvider with filtering (built as part of FND-3)                         |
| FND-5 | **DONE**     | ~~Implement JWT auth middleware (stub for now)~~                      | S    | auth.ts with stubbed JWT, gated by AUTH_ENABLED flag (built as part of FND-3)               |
| FND-6 | **DONE**     | ~~Setup Pino logging with request IDs~~                               | S    | genReqId via crypto.randomUUID(), Pino with pino-pretty in debug (built as part of FND-3)   |
| FND-7 | Not Started     | ~~Create env config service (dotenv + validation)~~                   | S    | config.ts with 13 env vars, validation for live mode, .env.example (built as part of FND-3) |

## License
MIT © Philip Teitel

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
