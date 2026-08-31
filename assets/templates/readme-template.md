<!-- INSTRUCTIONS FOR THE AGENT (do not copy this block into README.md):

This file is the structure for the configured design doc (default `README.md`).
The README is a **hub**. It bundles several artifacts in one file. Ownership is per section,
not per file. An agent may write only the sections listed for its command.

## Who writes what

| Section | Owner | Created / updated by |
|---------|-------|----------------------|
| Title and one-paragraph description | Human at `/init-project`; Migration Strategist at `/assess-modernization` if the file does not exist yet | Later agents may not replace the port framing. Architect may append a product-thesis sentence after purpose exists. |
| Table of Contents | The agent that adds or omits a section | Update only the TOC entries for sections you just added or removed. |
| **Modernization** (optional) | See subsections | Include only on the `modernization-port` lane. Omit entirely for greenfield. |
| Modernization → What this is | Migration Strategist | `/assess-modernization` |
| Modernization → Lane status | Migration Strategist | `/assess-modernization`, `/record-decision`, `/plan-migration` |
| Modernization → Artifact index | The agent that owns the linked artifact | Each producing command updates **only its row**. Do not edit another agent's row. Do not copy table contents from the linked file. |
| Requirements (purpose/domain links + REQ log + ADR log) | Architect for REQ and ADR logs; Modeler may set the purpose/domain link bullets when `/recover-domain` first creates those files | Append-only for REQ and ADR lists. |
| High-Level Architecture through Environment Variables | Architect | `/design-application` (and gated `/plan-project` patches). Omit until design runs. |
| Backlog Items | Architect creates rows; Documenter updates Status from story specs | `/plan-project`, `/plan-skeleton`, `/plan-story`; `/document-story` for status only. |
| License | Human / init | Leave unless the project already has a license file to cite. |

## Optional sections

- **Include `## Modernization`** when this repo is a brownfield port. `/assess-modernization` creates the README from this template if it does not exist, and **must** include that section.
- **Omit `## Modernization` entirely** for greenfield. Do not leave an empty or "N/A" modernization block.
- **Omit High-Level Architecture, Technical Stack, Key Design Decisions, Prerequisites, Getting Started, Available Scripts, UI Components, API Contract, and Environment Variables** until `/design-application`. Keep the headings out of the file rather than filling them with TBD noise. `/design-application` adds them from this template and **must preserve** an existing Modernization section and Artifact index.
- **Omit UI Components** when the product has no UI. **Omit API Contract** when there is no HTTP/RPC/message API. **Omit Environment Variables** when the app has none.

## Hub rules (modernization)

- The hub is navigation: what this repo is, where the lane is, and links to artifacts that exist.
- The hub is not a second copy of analysis. One sentence or a link. If a fact lives in ASSESSMENT.md, the inventory, or the migration plan, point there.
- Artifact index Status is `missing` or a short pointer (`v1 Snapshot`, `present`, count of XP files). The linked file is canonical. If the hub row disagrees with the file, fix the row, not the file — unless you own that file and it is still Draft.
- Do not narrate history in the hub. Current state in the cell. Git is the log.
- Do not edit analysis snapshots from the README.

## Greenfield / init

During `/init-project`, a human may edit only the project title, short description, and optionally the Table of Contents. Leave design and backlog for the architect. Omit Modernization.

## Architect / design-application

(1) Read the workflow profile. (2) If the design doc does not exist, create it from this template. (3) Replace `{ ... }` placeholders in sections you own. (4) Omit sections that do not apply. (5) If a design section lacks evidence, keep the heading and write `TBD`. (6) Preserve an existing Modernization section, Artifact index rows, and completed/in-progress backlog rows. (7) Preserve copyright/license statements.
-->

# {Project Title}

{One paragraph. Greenfield: what the product is. Modernization: this repo is a port of {legacy name} from {source stack} to {target stack}, plus the assessment one-liner (verdict, oracle tier, first slice). Do not retell the inventories.}

## Table of Contents

{Linked list of the sections that are actually in this file. Omit entries for omitted sections.}

<!-- INCLUDE WHEN this repo is on the modernization-port lane.
     Created by /assess-modernization. OMIT ENTIRELY for greenfield. -->

## Modernization

### What this is

{Migration Strategist. Two to four sentences: legacy system, source → target, that legacy behavior is evidence not automatic requirement, and a link to the assessment. Do not paste inventory tables.}

- Legacy repo: `{path or URL}`
- Source stack: `{language / version / framework}`
- Target stack: `{language / version / framework}`
- Assessment: [`docs/modernization/ASSESSMENT.md`](docs/modernization/ASSESSMENT.md)

### Lane status

{Migration Strategist only. Current state, not a changelog. Canonical evidence is the assessment, migration plan, and decision register. If this table disagrees with those files, those files win.}

| Field | Value |
|-------|-------|
| Phase | `{Assessment \| Planning}` |
| Verdict | `{go \| go-with-conditions \| no-go \| pending}` |
| Oracle tier | `{T1 executable \| T2 recorded \| T3 documented-only \| pending}` |
| Gate | `{M1 pending \| M1 accepted \| M4 pending \| M4 accepted}` |
| First / current slice | `{XP-NNN IDs or migration-plan row, or none yet}` |
| Next command | `{command}` |

Phase stays `Assessment` or `Planning` here. Recovery and delivery progress show up in the Artifact index (path details, requirements) and in **Backlog Items**. Do not add a third progress narrative.

### Artifact index

{Each producing command updates **only its row**. Link the file; do not copy its tables. Status: `missing`, or the artifact's own Version/Status (for example `v1 Snapshot`), or a count (for example `3 path details`).}

| Artifact | Owner | Status | Link |
|----------|-------|--------|------|
| Execution path inventory | Archaeologist | `{missing \| vN Snapshot}` | [`docs/modernization/execution-path-inventory.md`](docs/modernization/execution-path-inventory.md) |
| Dependency inventory | Migration Strategist | `{missing \| vN Snapshot}` | [`docs/modernization/dependency-inventory.md`](docs/modernization/dependency-inventory.md) |
| Dependency graph | Archaeologist | `{missing \| vN Snapshot}` | [`docs/modernization/dependency-graph.md`](docs/modernization/dependency-graph.md) |
| Impedance analysis | Migration Strategist | `{missing \| vN Snapshot}` | [`docs/modernization/impedance-analysis.md`](docs/modernization/impedance-analysis.md) |
| Oracle | Implementer | `{missing \| vN Snapshot}` | [`docs/modernization/oracle.md`](docs/modernization/oracle.md) |
| Assessment | Migration Strategist | `{missing \| present}` | [`docs/modernization/ASSESSMENT.md`](docs/modernization/ASSESSMENT.md) |
| Decision register | Migration Strategist | `{missing \| present}` | [`docs/modernization/decision-register.md`](docs/modernization/decision-register.md) |
| Path details | Archaeologist | `{missing \| N files}` | [`docs/modernization/paths/`](docs/modernization/paths/) |
| Purpose | Modeler | `{missing \| present}` | [`docs/PURPOSE.md`](docs/PURPOSE.md) |
| Domain model | Modeler | `{missing \| present}` | [`docs/DOMAIN.md`](docs/DOMAIN.md) |
| Defect ledger | Archaeologist | `{missing \| present}` | [`docs/modernization/defect-ledger.md`](docs/modernization/defect-ledger.md) |
| Migration plan | Migration Strategist | `{missing \| present}` | [`docs/modernization/migration-plan.md`](docs/modernization/migration-plan.md) |
| Requirements | Architect | `{missing \| see Requirements section}` | [`docs/requirements/`](docs/requirements/) |
| Stories | Architect | `{missing \| see Backlog}` | [`docs/features/`](docs/features/) |

---

## Requirements

**Purpose and domain model**
{ Link the configured purpose and domain artifacts. Default examples:
- [docs/PURPOSE.md](docs/PURPOSE.md) — product thesis, job, north-star outcome, trade-off rule, anti-thesis
- [docs/DOMAIN.md](docs/DOMAIN.md) — ubiquitous language, data dictionary, entities, invariants, lifecycles, consistency boundaries
If either artifact is not available yet, write `TBD` and explain the risk. Modeler may set these two bullets when `/recover-domain` first writes the files. Architect maintains them after `/design-application`. }

<!-- Append-only log of requirement files consumed to produce or update this design. Architect only. When new requirements are added via /design-application or /plan-project, append them — do not remove or reorder prior entries. -->

{ Bullet list of every requirements file used to generate or update this design. Each item is a markdown link (default example: `- [docs/requirements/01-initial.md](docs/requirements/01-initial.md)`). }

**Architecture decisions included for traceability for backlog alignment**
{ Architect. Append-only ADR links (default example: `- [docs/decisions/ADR-001-short-slug.md](docs/decisions/ADR-001-short-slug.md) — Accepted; constraint context`). }

<!-- INCLUDE WHEN /design-application has run. OMIT ENTIRELY until then on a modernization repo that is still in assessment or recovery. -->

## High-Level Architecture

{ Architect. High-level architecture, mermaid diagram, how the architecture preserves the purpose thesis and the domain model's consistency boundaries. }

## Technical Stack

{Architect. Table with at least: Layer, Technology, Rationale.}

## Key Design Decisions
{Architect. Binding choices summarized here; full records in ADRs. }

### 1. Use mock data for development

- Create mock data using expected schema
- use `{example of data from requirements}` for guidance
- ...

### Project Structure
```
{ascii diagram of the project structure}
```

### Logging and Observability

{ Architect. Logging strategy for the Implementer. }

- **Logger** — which library (e.g. Pino, Winston) and why. If none is chosen yet, write "TBD" so it is resolved before implementation begins.
- **Format** — structured JSON, plaintext, or other. Note whether `pino-pretty` or similar is used in development only.
- **Request/correlation IDs** — how they are generated and propagated.
- **Log levels** — standard levels (`debug`, `info`, `warn`, `error`) and any project-specific conventions.
- **Sensitive data** — what must never appear in logs and any explicit exceptions.

### { ... }

## Prerequisites
{ Architect. What is needed to run or build. }

## 1. Getting Started

{ Architect. Install, configure, run. Substitute commands from the workflow profile `stack` section where available. Documenter may later sync these if a story changes setup. }
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
{Architect creates; Documenter may add verify scripts a story introduced.}

| Command | Description |
|---------|-------------|
| `{stack.buildCommand}` | Build / type-check |
| `{stack.lintCommand}` | Lint |
| `{stack.testCommand}` | Test |
| `{dev command}` | Run locally |

<!-- INCLUDE WHEN the product has a UI. OMIT ENTIRELY otherwise. -->

## UI Components

{ Architect. Project-specific paths. }
Reusable primitives in `{ui components path}`:

| Component     | Description                                        |
|---------------|----------------------------------------------------|
| `{Component}` | `{What it renders and when to use it}`             |

Utility: `{utilityName}` in `{utilityPath}` — `{what it does}`.

<!-- INCLUDE WHEN the product exposes an HTTP, RPC, or message API. OMIT ENTIRELY otherwise. -->

## API Contract

{ Architect. }
| Path | Method | Purpose |
|------|--------|---------|
| `{route path}` | `{GET/POST/...}` | `{observable behavior}` |

<!-- INCLUDE WHEN the application requires environment variables. OMIT ENTIRELY otherwise. -->

## Environment Variables
{ Architect creates; Documenter syncs when a story changes them. }
See [`{env example path}`]({env example path}) for all available variables, if one exists. Key settings:

| Variable            | Default              | Description                          |
|---------------------|----------------------|--------------------------------------|
| `{VAR_NAME}`        | `{default}`          | `{description}`                      |

## Backlog Items
{ Architect creates epic/story rows (`/plan-project`, `/plan-skeleton`, `/plan-story`). Documenter updates **Status** from the story spec. Do not edit IDs, titles, or links of in-progress or completed rows. }

### Epic 1: {Epic Name}

{Epic description.}

| ID | Status | Story | Size | Notes |
|----|--------|-------|------|-------|
| [`{STORY-ID}`]({featuresDir}/{STORY-ID}-{slug}.md) | `{status.backlog.open}` | {Story title} | {S/M/L} | {one-line note} |

## License
MIT © Philip Teitel
