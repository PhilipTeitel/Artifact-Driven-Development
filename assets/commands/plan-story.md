# plan-story

This directs the Architect to plan and create a checklist for completing the given user story. The output will be a document in the `docs/features` folder following the structure defined in `~/.cursor/templates/user-story-template.md`.

Before writing, read `~/.cursor/templates/user-story-template.md` and follow it exactly. Every section in the template is required. If a section does not apply, keep the heading and state why. **Acceptance Criteria Checklist:** each criterion must use markdown checkboxes (`- [ ] **A1** — ...`) so they can be checked off — not plain bullets.

**ADRs:** Read `~/.cursor/templates/adr-template.md`. If the story touches a binding integration boundary (persistence, embeddings/vectors, auth, in-proc vs network, named dependencies) and no **Accepted** ADR exists, create `docs/decisions/ADR-NNN-*.md` in the **target project** following that template, then link it from the story and README summary. If README, requirements, and ADRs disagree, **stop** and output a **Tensions / conflicts** list — do not write an implementation-ready story until the user resolves it (unless the story is explicitly a **spike** using only **Proposed** ADRs).

**Definition of Ready:** The generated story must include completed sections **Linked architecture decisions (ADRs)**, **Definition of Ready (DoR)** (checkbox list ready for the human to verify), **Binding constraints (non-negotiable)**, **Ports & Adapters (Section 4b)**, **Test Plan (Section 8a)**, and **Phase Y: Binding & stack compliance** with at least one **(binding)** criterion backed by non-mock evidence where stack substitution is a risk.

**Hexagonal pairing (per `~/.cursor/AGENTS.md` rule 2):** if Section 4b lists any adapter, Section 8a must contain a `contract` test row for the matching port and an `integration` test row for the adapter against the real backing service, and Phase Y must contain a `(binding)` criterion citing the integration test.

**Scenario traceability (per `~/.cursor/AGENTS.md` rule 3 + `/refine-feature`):** if the story is linked to refined requirements at `docs/requirements/REQ-NNN-*.md`, every Gherkin `Sn` ID this story implements must appear in the **Covers Sn** column of at least one Section 8a row, and the test name should reference the `Sn`. If a particular `Sn` is intentionally out of scope for this story, the Summary section must state so and why.

The result must have everything the Implementer needs to complete the story without asking clarifying questions.

Create a link to the generated file in the `README.md`'s mention for the given user story in the appropriate epic's table.  For instance, if the story is named `FND-1`:
- Each epic is in a subsection of the `Backlog Items` section.
- Each epic has a table listing all the stories.
- Update the given story's `ID` value for that row with a link to the generated user story document.

This command will be available in chat with /plan-story.
It expects one argument, the story name, like so: `/plan-story OTO-1`.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
