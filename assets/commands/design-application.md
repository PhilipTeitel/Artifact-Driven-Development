# design-application

This **directs the architect** to produce the technical design for the application from the requirements you provide (workflow step (b): after init-project, or as the first step if you skipped init).

The architect will read your requirements, analyze them, and fill the project's `README.md` with the full design: Requirements, High-Level Architecture, Technical Stack, Key Design Decisions, Prerequisites, Getting Started, Available Scripts, UI Components, API Contract, Environment Variables, and any TBD placeholders where the requirements don't specify enough. The Requirements section is an append-only log of every requirement file consumed — the architect adds new entries but never removes prior ones. If no `README.md` exists, the architect will create it from `~/.cursor/templates/readme-template.md`.

**Preserve completed and in-progress work.** When `README.md` already has a Backlog Items section, do not modify existing epic or story rows whose Status is anything other than `Not Started`. Their IDs, titles, sizes, notes, and links to story documents in `docs/features/` must remain exactly as they are. Changing them would orphan already-written story documents and create inconsistencies between the design and completed work. If the new design contradicts a completed or in-progress story, flag the conflict in the output rather than silently editing the row.

**You must point to the requirements** (e.g. a BA document, statement of work, or requirements doc). The architect does not assume a path—you provide it.

**Prefer refined requirements.** If you have not yet run `/refine-feature` against the raw source material, do that first — refined `docs/requirements/REQ-NNN-*.md` files are unambiguous, contain Gherkin scenarios with `Sn` IDs that later stories will trace tests to, and surface open questions that would otherwise become silent assumptions in the design. Raw requirement files are still accepted; the architect will warn when ambiguities force assumptions and recommend rerunning through `/refine-feature`.

Examples:
- `/design-application @docs/requirements/REQ-001-customer-search.md` — preferred (refined)
- `/design-application @docs/requirements/` — preferred (folder of refined REQ files)
- `/design-application @docs/sow.md` — accepted (raw); architect will flag ambiguities

After the design is written, you can run `/plan-project` to have the architect add epics and stories to the Backlog Items section, then `/plan-story <story-id>` for each story to produce the story documents.

**When to rerun this command:** If `/plan-project` reports that new requirements affect design sections (architecture, API contract, environment variables, etc.) and the changes are too broad for gated section patches to handle cleanly, rerun `/design-application` with the new requirements to reconcile the full design.

This command is available in chat with `/design-application`.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
