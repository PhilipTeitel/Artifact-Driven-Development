# design-application

This **directs the architect** to produce the technical design for the application from the approved purpose, domain model, and requirements you provide (workflow step (b): after init-project, define-purpose, refine-feature, and model-domain; or after `/assess-modernization` and slice recovery on a brownfield port). Before acting, resolve the workflow profile and use its configured purpose path, domain path, design doc, templates, requirements directory, features directory, backlog statuses, and scenario ID pattern.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

The architect will read the configured purpose artifact, configured domain model, and your requirements, analyze them, and fill the configured design doc (default `README.md`) with the design sections this command owns: Requirements (REQ and ADR logs), High-Level Architecture, Technical Stack, Key Design Decisions, Prerequisites, Getting Started, Available Scripts, and any of UI Components, API Contract, and Environment Variables that apply. Omit sections that do not apply. Omit `## Modernization` on greenfield. On a modernization repo, **preserve** an existing `## Modernization` section and Artifact index; do not rewrite those rows. Add missing design sections after the hub rather than replacing the file. The Requirements section's REQ list is append-only — the architect adds new entries but never removes prior ones. If the design doc does not exist, the architect will create it from the configured design doc template (default `~/.cursor/templates/readme-template.md`).

**Preserve completed and in-progress work.** When the configured design doc already has a Backlog Items section, do not modify existing epic or story rows whose Status is anything other than the configured open backlog status (default `Not Started`). Their IDs, titles, sizes, notes, and links to story documents in the configured features directory must remain exactly as they are. Changing them would orphan already-written story documents and create inconsistencies between the design and completed work. If the new design contradicts a completed or in-progress story, flag the conflict in the output rather than silently editing the row.

**You must point to the requirements** (e.g. a BA document, statement of work, or requirements doc). The architect does not assume a path—you provide it.

**Prefer purpose + refined requirements + domain model.** If you have not yet run `/define-purpose`, `/refine-feature`, and `/model-domain` against the raw source material, do that first — those artifacts provide intent, Gherkin scenario trace points, ubiquitous language, data dictionary fields, and consistency boundaries that later stories and model-fidelity reviews depend on. Raw requirement files are still accepted for legacy projects; the architect will warn when ambiguities force assumptions and recommend rerunning through the earlier steps.

Examples:
- `/design-application @{requirementsDir}/REQ-001-customer-search.md` — preferred (refined)
- `/design-application @{requirementsDir}/` — preferred (folder of refined REQ files)
- `/design-application @docs/sow.md` — accepted (raw); architect will flag ambiguities

After the design is written, you can run `/plan-project` to have the architect add epics and stories to the Backlog Items section, then `/plan-story <story-id>` for each story to produce the story documents.

**When to rerun this command:** If `/plan-project` reports that new requirements affect design sections (architecture, API contract, environment variables, etc.) and the changes are too broad for gated section patches to handle cleanly, rerun `/design-application` with the new requirements to reconcile the full design.

This command is available in chat with `/design-application`.
