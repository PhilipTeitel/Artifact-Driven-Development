# define-purpose

This directs the **Modeler** agent in **Purpose mode** to turn raw product intent into the configured purpose artifact (default `docs/PURPOSE.md`). Before acting, resolve the workflow profile and use its configured purpose template, purpose path, requirements directory, domain path, and status vocabulary.

**Command-agent binding:** This command is role-bound to `agents.modeler`. Before executing any step, load the configured Modeler agent definition and follow it as binding role context.

This is workflow step (0): it runs before `/refine-feature`, `/model-domain`, `/design-application`, or `/plan-story` so every downstream artifact has a clear center of gravity.

## Why this exists

Requirements can describe the desired attributes of a system without saying what the system fundamentally is. That leaves models and humans to choose trade-offs locally. `/define-purpose` captures the product thesis, job, north-star outcome, trade-off rule, anti-thesis, and success signals so later agents can judge whether work remains true to intent.

## Inputs

- Raw idea, notes, transcripts, tickets, product briefs, existing requirements, or pasted conversation.
- Optional: existing configured purpose document to update.

The user must point to source material. The Modeler does not assume a path.

## What the Modeler will do

1. Resolve the workflow profile and read the configured purpose template (default `~/.cursor/templates/purpose-template.md`).
2. Read every source the user points to.
3. Extract only purpose-level content:
   - Thesis
   - Job-to-be-done
   - North-star outcome
   - Trade-off rule
   - Anti-thesis
   - Success signals
4. Ask the user to resolve contradictions or purpose-level gaps that would change downstream design.
5. Write or update the configured purpose artifact (default `docs/PURPOSE.md`).
6. Leave unresolved purpose questions under **Open purpose questions**. Those questions block downstream work for the affected scope.
7. **README hub.** If `## Modernization` exists, update only the Artifact index row **Purpose**. Do not create a Modernization section from this command; `/assess-modernization` does that. Do not edit Lane status.

## Hard rules

- Do not produce requirements, architecture, backlog, stories, API contracts, file touchpoints, or code.
- Do not invent intent. Every statement must trace to source material or a resolved user answer.
- Keep the artifact concise. It is a decision lens, not a feature list.
- If the existing purpose and new source material disagree, stop with a **Tensions / conflicts** list instead of silently rewriting the thesis.
- Status starts as `Draft` unless the user explicitly approves it.

## Outputs

- Configured purpose artifact (default `docs/PURPOSE.md`).
- A short chat summary listing: source material consumed, thesis, trade-off rule, open purpose questions, and suggested next command.

## Examples

- `/define-purpose @notes/product-idea.md`
- `/define-purpose @docs/requirements/REQ-001-customer-search.md`
- `/define-purpose @transcripts/customer-discovery/`

This command is available in chat with `/define-purpose`.
It expects at least one argument pointing to source material.
