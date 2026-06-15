# plan-project

This **directs the architect** to create the epics and stories needed to build the project (workflow step (c): after the architect has designed the app).

**Sources of truth:** `README.md` (the accumulated design state) and the new requirements document(s) the user points you to. The architect reads the current `README.md` as the baseline — it already encodes all prior design decisions. Only the new requirement files the user provides need to be read. Old requirement files are an audit trail and do not need to be re-read unless the user explicitly includes them.

**Prefer refined requirements (`docs/requirements/REQ-NNN-*.md`) produced by `/refine-feature`.** Their Gherkin `Sn` scenarios become the basis of the Test Plan in each story document, so test names trace back to user-stated behavior. Raw requirements are accepted but will produce backlog rows with weaker traceability.

## Default behavior (backlog only)

- **Only** create or update the **Backlog Items** section and the **Requirements** section in `README.md`. Append new requirement file entries to the Requirements section — do not remove prior entries.
- Do not add or change High-Level Architecture, Technical Stack, Key Design Decisions, Prerequisites, Getting Started, Available Scripts, UI Components, API Contract, or Environment Variables.
- If the new requirements imply changes to any of those design sections, emit a **"Design sections affected"** note listing the sections and recommending either a gated rerun (see below) or `/design-application`.
- **Preserve completed and in-progress work.** Do not modify existing epic or story rows whose Status is anything other than `Not Started` (e.g. `In Progress`, `Done`). Their IDs, titles, sizes, notes, and links to story documents in `docs/features/` must remain exactly as they are. Changing them would create inconsistencies with already-written story documents. New epics and stories are appended; they do not rewrite or renumber existing items. If new requirements contradict a completed or in-progress story, flag the conflict in the output rather than silently editing the row.
- Put epics and stories in Backlog Items. Use `~/.cursor/templates/readme-template.md` for the expected table format and examples.
- Create only the epic titles and story rows (IDs, titles, size, notes) — do not fully write out story content; that is done later with `/plan-story` for each story.
- Produce enough structure that stories can be planned without further questions.

## Gated design-section updates

When the user explicitly opts in — by including phrasing like "update design sections" or naming specific sections (e.g. "update API Contract and Environment Variables") — the architect may also edit those named sections. When doing so:

- Only edit the sections the user authorized. All other design sections remain unchanged.
- Output an **impact summary** listing what changed, which sections were touched, and why.
- If the changes are broad enough that isolated section patches risk inconsistency (e.g. a service moves from embedded to external API, affecting architecture, routes, and env vars simultaneously), recommend running `/design-application` instead for a full design reconciliation.

## Requirement file ordering

When multiple requirement files are provided:

- **Individual files listed as arguments:** argument order wins — the last file takes precedence on conflicts.
- **Folder path (e.g. `@docs/requirements/`):** files are resolved in lexical filename order.
- **Recommended naming convention:** use numbered prefixes for predictable ordering: `01-initial.md`, `02-feature-x.md`, `03-api-changes.md`.

This command will be available in chat with /plan-project.
It expects at least one argument. Examples are below:
- `/plan-project @docs/requirements/03-api-changes.md` — reads README + new file, updates backlog only
- `/plan-project @docs/requirements/03-api-changes.md update design sections for API Contract and Environment Variables` — gated: also patches those two sections
- `/plan-project @docs/requirements/` — reads README + all files in folder (lexical order), backlog only
- `/plan-project @docs/requirements/03-api-changes.md update design sections` — gated: architect decides which sections are affected
- `/plan-project @docs/requirements ... overwrite current plans` — replaces existing backlog items
- `/plan-project @docs/requirements ... overwrite the Epic 1 section of the backlog items` — replaces a specific epic

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
