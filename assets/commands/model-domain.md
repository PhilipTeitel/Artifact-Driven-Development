# model-domain

This directs the **Modeler** agent in **Domain mode** to create or update the configured domain model and data dictionary artifact (default `docs/DOMAIN.md`). Before acting, resolve the workflow profile and use its configured purpose path, domain template, domain path, requirements directory, decisions directory, and scenario ID pattern.

**Command-agent binding:** This command is role-bound to `agents.modeler`. Before executing any step, load the configured Modeler agent definition and follow it as binding role context.

This is workflow step (a-plus): it runs after `/define-purpose` and `/refine-feature`, before `/design-application`, `/plan-skeleton`, `/plan-project`, or `/plan-story`.

## Why this exists

Many requirements describe behavior and constraints without making the underlying domain explicit. Human teams often rely on shared background knowledge ("everyone knows what a pricing system is"). AI agents do not have that shared local context. `/model-domain` turns the product's nouns, fields, relationships, invariants, lifecycles, and consistency boundaries into a durable artifact that later code and reviews can judge against.

## Inputs

- Configured purpose document (default `docs/PURPOSE.md`).
- Refined requirements in the configured requirements directory, or other source material the user points to.
- Optional existing configured domain model to update.
- Optional ADRs when they constrain domain boundaries.

The user must point to the requirements or source material to model. The Modeler does not assume a path beyond the configured purpose/domain artifacts.

## What the Modeler will do

1. Resolve the workflow profile and read the configured domain model template (default `~/.cursor/templates/domain-model-template.md`).
2. Read the configured purpose document if it exists. If missing, warn that `/define-purpose` should run first unless the user explicitly chooses to proceed.
3. Read every source the user points to.
4. Extract and normalize:
   - Ubiquitous language terms
   - Data dictionary fields
   - Core entities and identity rules
   - Relationships and cardinality
   - Invariants
   - Aggregates / consistency boundaries
   - Lifecycles and state transitions
   - Domain events
5. Ask the user to resolve modeling gaps that would affect design or test design.
6. Write or update the configured domain model artifact.
7. Leave unresolved modeling questions under **Open modeling questions**. Those questions block downstream work for the affected scope.

## Hard rules

- Do not invent entities, fields, invariants, lifecycle states, or relationships. Use `TBD` plus an open modeling question when source material is incomplete.
- Do not silently rename existing terms. If a rename is needed, mark the old term as deprecated and ask for approval.
- Do not turn technical implementation mechanisms into domain concepts unless the product domain itself uses those terms.
- Every data dictionary row must have a field name, owner entity, type/format, requiredness, constraints or allowed values, source of value, and source citation.
- Every entity must have either an invariant list or an explicit `TBD` note linked to an open modeling question.
- Do not write architecture, stack choices, API contracts, story acceptance criteria, or code.

## Outputs

- Configured domain model artifact (default `docs/DOMAIN.md`).
- A short chat summary listing: terms/entities added or changed, open modeling questions, likely consistency boundaries, and suggested next command.

## Examples

- `/model-domain @docs/requirements/REQ-001-customer-search.md`
- `/model-domain @docs/requirements/`
- `/model-domain @docs/requirements/REQ-001.md @docs/decisions/ADR-002-pricing-boundary.md`

This command is available in chat with `/model-domain`.
It expects at least one argument pointing to requirements or other source material.
