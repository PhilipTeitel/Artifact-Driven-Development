# plan-story

This directs the Architect to plan and create a checklist for completing the given user story. Before acting, resolve the workflow profile and use its configured purpose path, domain path, features directory, story file pattern, templates, decisions directory, requirements directory, methodology settings, and design doc. The output will be a document in the configured features directory (default `docs/features`) following the configured story template (default `~/.cursor/templates/user-story-template.md`).

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

Before writing, read the configured story template and follow it exactly. Every section in the template is required. If a section does not apply, keep the heading and state why. **Acceptance Criteria Checklist:** each criterion must use markdown checkboxes (`- [ ] **A1** — ...`) so they can be checked off — not plain bullets.

**ADRs:** Read the configured ADR template. If the story touches a binding integration boundary (persistence, embeddings/vectors, auth, in-proc vs network, named dependencies) and no **Accepted** ADR exists, create an ADR in the configured decisions directory using the configured ADR naming pattern in the **target project**, then link it from the story and configured design doc summary. If the design doc, requirements, and ADRs disagree, **stop** and output a **Tensions / conflicts** list — do not write an implementation-ready story until the user resolves it (unless the story is explicitly a **spike** using only **Proposed** ADRs and the profile allows that).

**Definition of Ready:** The generated story must include completed sections **Domain model touchpoints**, **Linked architecture decisions (ADRs)**, **Definition of Ready (DoR)** (checkbox list ready for the human to verify), **Binding constraints (non-negotiable)**, **Ports & Adapters (Section 4b)**, **Test Plan (Section 8a)**, and **Phase Y: Binding & stack compliance** with at least one **(binding)** criterion backed by non-mock evidence where stack substitution is a risk. It must also include the configured model-fidelity Phase Z criterion (default `Z7`).

**Purpose/domain traceability (per configured methodology):** read the configured purpose document and domain model when they exist. The story's Section 1a must list every purpose section, domain term, entity, data dictionary field, invariant, lifecycle, or consistency boundary the story touches. If the story introduces or changes domain meaning that is absent from the domain model, stop and recommend `/model-domain` unless the story explicitly updates that artifact.

**Hexagonal pairing (per configured methodology):** if Section 4b lists any adapter, Section 8a must contain the configured port/adapter test rows (defaults: `contract` for the matching port and `integration` for the adapter against the real backing service), and Phase Y must contain a `(binding)` criterion citing the integration test.

**Scenario traceability (per configured methodology + `/refine-feature`):** if the story is linked to refined requirements in the configured requirements directory, every Gherkin scenario ID this story implements must appear in the **Covers Sn** column of at least one Section 8a row, and the test name should reference the scenario ID. If a particular scenario is intentionally out of scope for this story, the Summary section must state so and why.

**Modernization provenance (when linked REQ files include section 4b):** this is still `/plan-story` and still uses the user-story template. Do not switch to a port-story template.
- Copy the relevant 4b rows into Section 1b. REQ remains canonical.
- Copy the migration-plan prerequisite IDs that bind those `XP-NNN` into **Slice prerequisites**. Checkoff happens in the story. Do not edit analysis snapshots.
- Refuse to mark the story ready when a listed prerequisite is unresolved, a covered claim is `E4` / `E5` without a `DEC-NNN`, or an oracle-backed path has no comparison rule in the REQ.
- Add `parity` test rows covering those `Sn` / `XP-NNN` IDs. Use the REQ comparison rule. If oracle source is `none`, do not invent a parity row.
- If a cited `DEC-NNN` binds target design (persistence, named dependency, process boundary, integration, cutover) and no **Accepted** ADR exists, create or stop for that ADR. Cite both `DEC-NNN` and `ADR-NNN`.
- Do not silently improve legacy behavior; cite `DEF-NNN` from the REQ.
- Update the Artifact index row **Stories** when `## Modernization` exists (point at `docs/features/` or "see Backlog"). Do not edit Lane status or analysis index rows.

The result must have everything the Implementer needs to complete the story without asking clarifying questions.

Create a link to the generated file in the configured design doc's mention for the given user story in the appropriate epic's table. For instance, if the story is named `{STORY-ID}`:
- Each epic is in a subsection of the `Backlog Items` section.
- Each epic has a table listing all the stories.
- Update the given story's `ID` value for that row with a link to the generated user story document.

This command will be available in chat with /plan-story.
It expects one argument, the story name, like so: `/plan-story {STORY-ID}`.
