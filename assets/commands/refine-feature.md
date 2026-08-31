# refine-feature

This **directs the architect** in **Discovery / Refinement Mode** to take raw, ambiguous, or partial feature input and produce a refined requirements document with Gherkin acceptance scenarios. Before acting, resolve the workflow profile and use its configured purpose path, domain path, requirements template, requirements directory, naming pattern, scenario ID pattern, and status vocabulary.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition and follow it as binding role context.

This is workflow step (a-prime): it runs **after** `/define-purpose` when purpose is available and **before** `/model-domain`, `/design-application`, or `/plan-project` so those steps consume a clean, unambiguous specification instead of raw notes.

## Why this exists

When raw requirements go straight into design, the architect often has to guess. Those guesses become silent assumptions in the design, then in stories, then in code — and the final product is "what I asked for but not what I really wanted." This command forces the ambiguity to surface and get resolved upfront.

## What the architect will do

1. Read every source the user points to (notes, tickets, transcripts, slide decks, pasted text, or modernization path details). The user must point to them — the architect does not assume a path. If the configured purpose artifact exists, read it as intent context. In a port, prefer `docs/modernization/paths/XP-NNN-*.md` over retelling global inventories.
2. Read the configured requirements template (default `~/.cursor/templates/requirements-template.md`) for output structure.
3. Extract goals, non-goals, personas, constraints, and candidate user scenarios from the source.
4. Use `AskQuestion` to resolve every meaningful ambiguity. Acceptable resolution targets include:
   - Who triggers the behavior and from what context.
   - Exact preconditions, inputs, and outputs (data shapes, units, ranges).
   - Failure modes the user expects to be handled visibly.
   - Integration boundaries (what services/data sources are in/out of scope).
   - Non-functional bounds (latency, volume, security, audit).
5. Translate the resolved scenarios into **Gherkin** (`Given/When/Then`), one block per scenario, each tagged with an ID matching the configured scenario ID pattern (default `S1`, `S2`, …). These IDs are what later stories' Test Plans must trace to.
6. Identify terms, entities, fields, invariants, lifecycles, or boundaries that should be modeled in the configured domain artifact and call them out for `/model-domain`.
7. Identify constraints that imply long-lived binding decisions and list them under **Suggested ADR triggers** so `/design-application` or `/plan-project` knows to create the ADRs.
8. Write the result using the configured requirements directory and naming pattern (default `docs/requirements/REQ-NNN-short-slug.md`) using the next sequential `NNN`. Do not renumber existing REQ files.
9. **Modernization handoff.** When any source is a path detail (`docs/modernization/paths/XP-NNN-*.md`), also fill **4b. Legacy provenance**:
   - One row per `Sn`, naming the `XP-NNN`, exactly one evidence grade, any binding `DEC-NNN` / `DEF-NNN`, the comparison rule, and the oracle source (`FIX-NNN`, acceptance data, or `none`).
   - Restate each comparison rule under **Constraints**. Do not use a workflow-profile numeric hint as the rule.
   - Leave unresolved `E4` / `E5` claims in **Open questions** unless a `DEC-NNN` accepts them. Do not mark the REQ ready for design while those questions remain.
   - Cite the path detail, decision register, defect ledger, and oracle in **Links**. Do not copy inventory tables.
   - If a cited `DEC-NNN` chooses a named target dependency, persistence, process boundary, integration model, or cutover mechanism, list it under **Suggested ADR triggers**. Binding target design still needs an ADR.

## Hard rules

- **Do not invent answers.** If the user does not answer a clarifying question, the question stays in **Open questions**. Open questions block downstream design for the affected scope.
- **Do not produce design.** This command produces requirements only. Architecture, technical stack, and stories come from `/design-application` and `/plan-story`.
- **Source provenance.** Every goal, non-goal, persona, constraint, and scenario must be traceable to a piece of the source material or to an answered clarifying question (logged under **Resolved questions**).
- **Do not write path test plans, port stories, or parity reports.** Recovered behavior becomes `Sn` scenarios. Comparison rules live in this REQ. Delivery uses `/plan-story` and `/complete-story`.
- Status starts at the configured draft requirements status if one is present; otherwise use `Draft`. The user marks it `Ready for Design` after a final review.

## Outputs

- A new requirements file at the configured requirements path
- A short summary in chat listing: REQ ID, count of scenarios, count of resolved questions, count of open questions, suggested ADR triggers, and when section 4b is present the covered `XP-NNN` IDs plus any unresolved `E4` / `E5` blockers. Suggested next command is `/design-application` or `/plan-project`, not a port-story command.

## Examples

- `/refine-feature @notes/customer-call-2026-04-12.md` — refine from a single source file
- `/refine-feature @docs/intake/feature-x/` — refine from a folder of source material
- `/refine-feature @docs/intake/feature-x/ @{decisionsDir}/ADR-002-auth.md` — refine with an existing ADR as constraint context
- `/refine-feature @docs/modernization/paths/XP-001-linspace.md` — refine a port slice from a path detail

This command is available in chat with `/refine-feature`.
It expects at least one argument pointing to source material.
