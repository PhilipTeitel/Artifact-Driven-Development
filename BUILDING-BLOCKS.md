# Building Blocks

This document is the deep dive on the small set of pieces the methodology is built from. The [README](README.md) introduces them; here they get definitions, the dimension of context they manage, and a composition matrix that shows how they wire together to produce every artifact.

---

## Modularity is the mechanism

The pieces of this methodology are deliberately kept independent. Each one manages context along a different dimension:

- **Agents** manage the *concern* dimension. Who is acting, and what judgment do they apply?
- **Commands** manage the *control* dimension. What step is being performed, what instructions does the agent follow, what constraints must it respect, what sections of which artifact may it touch?
- **Templates** manage the *output shape* dimension. What must the artifact contain to be acceptable?

Keeping these dimensions independent is what allows context to be managed precisely. The same agent can be reused across many commands without their concerns leaking into each other. The same command can be expressed through different templates when the artifact needs to change shape. The same template can be filled by different agents when responsibility shifts.

If those three dimensions were collapsed into one prompt or one "skill," every change to one dimension would force a rewrite of the others. Separation is what makes the workflow composable.

The remaining pieces — **artifacts**, **evidence**, and **gates** — are not dimensions of context; they are the *outputs* and *checkpoints* produced when agents, commands, and templates compose.

---

## Agent — the *concern* dimension

An agent is a durable role definition. It says what the model is allowed to think about, what it is responsible for, and what it must not do.

- **Purpose.** Constrain the model's role across many commands so it brings consistent judgment to each one.
- **Inputs.** A persona, responsibilities, and behavioral rules (for example, "do not invent requirements," "do not silently substitute named dependencies").
- **Output.** A reusable role that any command can invoke.
- **Examples.**
  - **Architect** — turns ambiguity into requirements, design, ADRs, and story specs.
  - **Implementer** — writes code and tests against an approved story spec.
  - **Auditor** — provides review gates for stories, diffs, and full-repo audits.
  - **QA** — verifies acceptance criteria against executable evidence.
  - **Documenter** — keeps project documentation aligned with the story source of truth.

An agent without a command is just a persona. It does nothing until a command tells it which step to perform.

---

## Command — the *control* dimension

A command is one workflow step under explicit control: the instructions the agent follows and the constraints it must respect.

- **Purpose.** Specify what step is happening, what context is in scope, what instructions guide the work, and what constraints bound it (for example, "do not modify acceptance criteria of a completed story" or "only update the post-complete follow-up ledger section").
- **Inputs.** Required source artifacts, the agent to invoke, the template that shapes the output, the sections of which artifact may be edited, and the step-specific instructions and constraints.
- **Output.** The invocation pattern that produces or updates a specific section of a specific artifact.
- **Examples (by lane).**
  - **Refinement and design.** `/init-project`, `/refine-feature`, `/design-application`, `/plan-project`, `/plan-story`, `/validate-story`.
  - **Implementation and verification.** `/implement-story`, `/review-story`, `/qa-story`, `/fix-from-qa`, `/document-story`, `/complete-story`.
  - **Post-story routing.** `/patch-story`, `/reconcile-story`, `/review-diff`.
  - **Audit.** `/map-repo`, `/audit-all`, `/triage-audit-findings`, plus the category audits `/audit-tooling`, `/audit-reliability`, `/audit-db`, `/audit-api-contracts`, `/audit-security`, `/audit-performance`, `/audit-test-coverage`.

A command without an agent has no judgment behind it. A command without a template has no defined output. Commands are the connective tissue, not the whole engine.

---

## Template — the *output shape* dimension

A template is a contract for what an artifact must contain.

- **Purpose.** Make the shape of acceptable output explicit, so the agent cannot satisfy the command with prose alone.
- **Inputs.** Required sections, required fields, machine-readable markers (for example, the `REVIEW SUMMARY:` line on a review artifact), and explicit placeholders for traceability links.
- **Output.** A reusable artifact skeleton.
- **Examples.**
  - **README / design hub template** — architecture, stack, key decisions, API contract, environment, setup, backlog.
  - **Requirements template** — goals, non-goals, personas, constraints, resolved and open questions, Gherkin scenarios.
  - **ADR template** — context, decision, alternatives considered, consequences.
  - **User story template** — linked ADRs, binding constraints, ports and adapters, file touchpoints, acceptance criteria, test plan, implementation order, completion metadata, follow-up ledger.
  - **Story-review template** — required actions, severity, machine-readable `REVIEW SUMMARY:` line.
  - **Audit template** — findings by category with evidence citations.

A template is what prevents an artifact from drifting into a different shape every time it is produced.

---

## Artifact — the durable output

An artifact is a durable, reviewable output of the workflow. It is defined by **what it carries** — intent, a decision, design context, evidence — not by the file it happens to live in.

- **Purpose.** Carry intent, decisions, design, or evidence forward in a form humans can review.
- **Defined by.** The role the artifact plays in the trace from intent to delivery.
- **Recorded in.** A file, or a section of a file shared with related artifacts to keep the trace co-located.

### The artifact set

| Artifact | Carries | Produced or updated by |
|---|---|---|
| Refined requirements | Clarified intent, goals, non-goals, constraints, Gherkin scenarios | `/refine-feature` |
| Application design | Architecture, stack, API contract, environment, setup, UI structure | `/design-application` |
| ADR | One binding technical decision, recorded durably | `/design-application` when a decision needs to be durable |
| Backlog | Epics and stories that organize delivery | `/plan-project`; status synced by `/document-story` |
| Story spec | Implementation-ready instructions: linked context, acceptance criteria, test plan, file touchpoints, implementation order | `/plan-story` |
| Code and tests | Production behavior and the tests that prove each acceptance criterion | `/implement-story`, `/fix-from-qa`, `/patch-story` |
| Story acceptance evidence | Status and criterion checkboxes flipped as evidence accumulates | `/implement-story`, `/fix-from-qa` |
| Story review | Review of the changed surface for reliability, security, contract risk, coverage gaps | `/review-story`, `/review-diff` |
| QA evidence matrix | Per-criterion `PASS` / `FAIL` / `BLOCKED` with cited evidence | `/qa-story` |
| Documentation updates | Synchronized changes to project documentation surfaces | `/document-story` |
| Completion metadata | Final review summary, QA result, docs handoff, completion ref | `/document-story`, `/validate-story complete` |
| Post-complete follow-up ledger entry | One small follow-up tied to a completed story | `/patch-story` |
| Audit findings | System map, category findings, triage decisions from periodic audits | `/map-repo`, `/audit-all`, category audits, `/triage-audit-findings` |

### Implementation note: artifacts and files

The methodology defines artifacts as concepts. The current implementation bundles related artifacts into a small number of files for trace co-location, not because the artifacts are one thing.

Three examples of bundling:

- The **story spec file** (`docs/features/{STORY-ID}-*.md`) carries the story spec, the implementer's status and acceptance-criteria evidence, the QA evidence matrix, the completion metadata, and the post-complete follow-up ledger entries — every artifact tied to one story in one document so the trace stays in one place.
- The **project README** carries the application design and the backlog because both describe the same project.
- The **story review file** carries one story review artifact; a diff review of the same shape lives under `docs/reviews/`.

This bundling is a convenience. The artifacts are still distinct: each has one producer, one purpose, and one place in the trace. A project that wanted to keep them in separate files could; this methodology happens to keep them together because related context is easier to follow when it is co-located.

Templates in this methodology — README, ADR, requirements, user story, story review, audit — define the shape of those files, including which artifacts each file is expected to carry. The templates are an implementation choice. The artifacts are the design.

### Project documentation surfaces

Some documentation surfaces — OpenAPI specs, runbooks, environment docs, project-specific setup instructions — are not artifacts the methodology itself produces. They are **project documentation** that the Documenter syncs as part of `/document-story` when a story changes them. They are downstream surfaces kept in agreement with the artifacts above, not new artifacts in their own right.

Artifacts are what distinguish this methodology from "ask the model nicely." Prompts are ephemeral. Artifacts are durable.

---

## Evidence — the proof

Evidence is what makes "done" mean something specific.

- **Purpose.** Tie each acceptance criterion to something executable or verifiable.
- **Examples.** Unit, contract, and integration tests cited by path; changed files; the QA matrix rows that mark each criterion `PASS`; the review summary line; the documentation diff that closes the loop.

Evidence answers the question "how do we know?" An artifact without evidence is a claim. Evidence turns the claim into a check.

---

## Gate — the decision point

A gate is where work stops until someone — human or agent — decides whether it moves forward.

- **Purpose.** Make completion explicit instead of implicit.
- **Examples.**
  - **Agent gates.** Review `Pass` or `Block`. QA `PASS`, `FAIL`, or `BLOCKED` per criterion. `validate-story ready` and `validate-story complete`.
  - **Human gates.** The six approvals in the [README](README.md) swimlane: refined requirements, design and ADRs, backlog, story spec, QA evidence, documentation.

Gates exist because skipping them has been observed to cost more later. A gate that becomes a formality has stopped doing its job.

---

## Composition matrix

The composition matrix shows which command produces or updates which artifact, with which agent, and where the artifact is currently recorded.

| Command | Agent | Artifact produced or updated | Recorded in |
|---|---|---|---|
| `/init-project` | Architect or human | Project scaffold | `README.md`, `docs/` layout |
| `/refine-feature` | Architect | Refined requirements | `docs/requirements/REQ-NNN-*.md` |
| `/design-application` | Architect | Application design; ADRs (as needed) | Project README design sections; `docs/decisions/ADR-NNN-*.md` |
| `/plan-project` | Architect | Backlog | Project README backlog section |
| `/plan-story` | Architect | Story spec | `docs/features/{STORY-ID}-*.md` |
| `/validate-story ready` | Architect | Readiness validation | Assertion against the story spec; corrects readiness defects only |
| `/implement-story` | Implementer | Code, tests; story acceptance evidence | Codebase; story spec status field and criteria checkboxes |
| `/review-story` | Auditor | Story review | `docs/features/{STORY-ID}-review.md` |
| `/qa-story` | QA | QA evidence matrix | Story spec QA section |
| `/fix-from-qa` | Implementer | Code, tests; updated story acceptance evidence | Codebase; story spec checkboxes for failed or blocked rows only |
| `/document-story` | Documenter | Documentation updates; completion metadata | Project README and project documentation surfaces (OpenAPI, runbooks, environment docs); story spec completion metadata |
| `/validate-story complete` | Documenter | Completion validation | Assertion against story spec; corrects metadata if needed |
| `/patch-story` | Implementer | Post-complete follow-up ledger entry; targeted code, test, or doc changes | Story spec follow-up ledger; codebase or documentation surfaces |
| `/reconcile-story` | Auditor | Drift classification and recommended lane | Recommendation only; no edits |
| `/review-diff` | Auditor | Story review (diff scope) | `docs/reviews/*.md` |
| `/map-repo` | Auditor | System map | Audit findings |
| `/audit-all` | Auditor | Audit findings across all categories | Audit findings |
| `/audit-{category}` | Auditor | Category findings (`tooling`, `reliability`, `db`, `api-contracts`, `security`, `performance`, `test-coverage`) | Audit findings |
| `/triage-audit-findings` | Auditor | Audit triage decisions | Audit findings |

Read this matrix as: *the agent brings concern; the command brings control (instructions and constraints); the template shapes the file the artifact lands in; the artifact itself is the durable conceptual output.* Each axis moves independently. Change the template and the file layout changes; the artifacts do not. Change the command and where the artifact lands may change; the artifact does not. Change the agent and the judgment behind the artifact changes; everything else stays.

---

## Read next

- [ROLES.md](ROLES.md) — the agents in depth: what each one owns and how work hands off.
- [PROCESS.md](PROCESS.md) — how these blocks chain together across the story lifecycle.
- [TRACEABILITY.md](TRACEABILITY.md) — how the artifacts in this matrix link into a single trace from intent to evidence.
