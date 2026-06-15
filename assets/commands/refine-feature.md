# refine-feature

This **directs the architect** in **Discovery / Refinement Mode** to take raw, ambiguous, or partial feature input and produce a refined requirements document with Gherkin acceptance scenarios.

This is workflow step (a-prime): it runs **before** `/design-application` or `/plan-project` so that those steps consume a clean, unambiguous specification instead of raw notes.

## Why this exists

When raw requirements go straight into design, the architect often has to guess. Those guesses become silent assumptions in the design, then in stories, then in code — and the final product is "what I asked for but not what I really wanted." This command forces the ambiguity to surface and get resolved upfront.

## What the architect will do

1. Read every source the user points to (notes, tickets, transcripts, slide decks, pasted text). The user must point to them — the architect does not assume a path.
2. Read `~/.cursor/templates/requirements-template.md` for output structure.
3. Extract goals, non-goals, personas, constraints, and candidate user scenarios from the source.
4. Use `AskQuestion` to resolve every meaningful ambiguity. Acceptable resolution targets include:
   - Who triggers the behavior and from what context.
   - Exact preconditions, inputs, and outputs (data shapes, units, ranges).
   - Failure modes the user expects to be handled visibly.
   - Integration boundaries (what services/data sources are in/out of scope).
   - Non-functional bounds (latency, volume, security, audit).
5. Translate the resolved scenarios into **Gherkin** (`Given/When/Then`), one block per scenario, each tagged with an ID `S1`, `S2`, … . These IDs are what later stories' Test Plans must trace to.
6. Identify constraints that imply long-lived binding decisions and list them under **Suggested ADR triggers** so `/design-application` or `/plan-project` knows to create the ADRs.
7. Write the result to `docs/requirements/REQ-NNN-short-slug.md` using the next sequential `NNN`. Do not renumber existing REQ files.

## Hard rules

- **Do not invent answers.** If the user does not answer a clarifying question, the question stays in **Open questions**. Open questions block downstream design for the affected scope.
- **Do not produce design.** This command produces requirements only. Architecture, technical stack, and stories come from `/design-application` and `/plan-story`.
- **Source provenance.** Every goal, non-goal, persona, constraint, and scenario must be traceable to a piece of the source material or to an answered clarifying question (logged under **Resolved questions**).
- Status starts at `Draft`. The user marks it `Ready for Design` after a final review.

## Outputs

- `docs/requirements/REQ-NNN-short-slug.md` (new file)
- A short summary in chat listing: REQ ID, count of scenarios, count of resolved questions, count of open questions, and any suggested ADR triggers.

## Examples

- `/refine-feature @notes/customer-call-2026-04-12.md` — refine from a single source file
- `/refine-feature @docs/intake/feature-x/` — refine from a folder of source material
- `/refine-feature @docs/intake/feature-x/ @docs/decisions/ADR-002-auth.md` — refine with an existing ADR as constraint context

This command is available in chat with `/refine-feature`.
It expects at least one argument pointing to source material.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
