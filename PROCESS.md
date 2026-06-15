# The Process

This document walks through the full story lifecycle from a raw idea to a shipped story. It expands the swimlane diagram in the [README](README.md) and names every human gate.

The lifecycle separates **agent actions** (commands run by an agent) from **artifacts** (durable outputs that become context for the next step). The human owns the decisions that bind work between steps.

For everything that happens *after* a story is complete — small follow-ups, hotfixes, audits, drift reconciliation — see [POST-STORY.md](POST-STORY.md).

---

## The full lifecycle

```mermaid
flowchart TD
    subgraph Human [Human]
        rawIdea["Raw idea or notes"]
        approveReqs{"Approve refined requirements"}
        approveDesign{"Approve design and architecture decision records"}
        approveBacklog{"Approve backlog"}
        approveStory{"Approve story spec"}
        acceptQa{"Accept QA evidence"}
        approveDocs{"Approve documentation"}
        done["Story shipped"]
    end

    subgraph Architect [Architect agent]
        refine["/refine-feature"]
        design["/design-application"]
        planProj["/plan-project"]
        planStory["/plan-story"]
        validateReady["/validate-story ready"]
        reqsDoc[/"requirements"/]
        designDoc[/"Design and architecture decision records"/]
        backlog[/"Backlog epics and stories"/]
        storyDoc[/"Implementation-ready story spec"/]
    end

    subgraph Implementer [Implementer agent]
        implement["/implement-story"]
        fixQa["/fix-from-qa"]
        code[/"Code, tests, checked criteria"/]
    end

    subgraph Auditor [Auditor agent]
        review["/review-story"]
        reviewArtifact[/"Review artifact"/]
    end

    subgraph QAlane [QA agent]
        qa["/qa-story"]
        qaMatrix[/"Criterion evidence matrix"/]
    end

    subgraph Documenter [Documenter agent]
        docStory["/document-story"]
        validateComplete["/validate-story complete"]
        docsUpdate[/"README, API, runbook updates"/]
        completionMeta[/"Completion metadata"/]
    end

    rawIdea --> refine --> reqsDoc --> approveReqs
    approveReqs --> design --> designDoc --> approveDesign
    approveDesign --> planProj --> backlog --> approveBacklog
    approveBacklog --> planStory --> storyDoc --> validateReady --> approveStory
    approveStory --> implement --> code --> review --> reviewArtifact
    reviewArtifact -->|Block| implement
    reviewArtifact -->|Pass| qa --> qaMatrix
    qaMatrix -->|FAIL or BLOCKED| fixQa --> qa
    qaMatrix -->|All PASS| acceptQa
    acceptQa --> docStory --> docsUpdate --> approveDocs
    approveDocs --> validateComplete --> completionMeta --> done
```

The happy path can be run one command at a time. The tail — implement, review, QA, document, validate — can also be orchestrated with `/complete-story` after `/plan-story` has produced an approved story document.

---

## The six human gates

The agents do the work. The human makes the decisions that bind it.

| Gate | What is being decided | What the human is looking for |
|---|---|---|
| 1. Approve refined requirements | Is this the right problem, stated clearly enough to design against? | Goals, non-goals, personas, constraints, and Gherkin scenarios that match real intent. Open questions resolved or explicitly deferred. |
| 2. Approve design and architecture decision records | Is this the right shape, with the binding decisions captured? | Architecture, stack, API contract, environment, and any architecture decision records needed for persistence, transport, auth, named dependencies, or integration model. |
| 3. Approve backlog | Are the epics and stories the right slices, in the right order? | Epics that map to the design, stories sized for one implementer pass, and no orphaned or duplicated work. |
| 4. Approve story spec | Is this story implementation-ready? | Linked requirements and architecture decision records, file touchpoints, acceptance criteria, test plan rows, implementation order, binding constraints. |
| 5. Accept QA evidence | Did the implementation actually satisfy the story? | Every acceptance criterion marked PASS in the QA matrix with executable evidence. Any FAIL or BLOCKED resolved. |
| 6. Approve documentation | Do the project's documentation surfaces match what was shipped? | README, API docs, OpenAPI specs, runbooks, setup, and environment docs updated for any surface the story changed. |

A gate that is rubber-stamped is a gate that has stopped doing its job. Each one exists because skipping it has been observed to cost more later.

---

## Stage by stage

Each stage names its primary inputs, the agent action, the artifact produced, the human gate that follows, and the exit condition.

### 0. `/init-project` (optional)

- **Inputs.** A new repository.
- **Agent.** Architect (or run by the human directly).
- **Artifact.** Scaffolded `README.md`, `docs/features/`, and `docs/requirements/` directories using the README template.
- **Human gate.** None — this is mechanical setup.
- **Exit.** A repository ready to accept refined requirements.

Skip this stage when working in an existing project that already has a README and `docs/` layout.

### 1. `/refine-feature`

- **Inputs.** Raw notes, tickets, transcripts, pasted requirements, or a conversation.
- **Agent.** Architect.
- **Artifact.** `docs/requirements/REQ-NNN-*.md`. The architect asks clarifying questions, records resolved and open questions, and writes Gherkin scenarios (`S1`, `S2`, `S3`...) that later stages use as trace points.
- **Human gate.** **Gate 1: Approve refined requirements.**
- **Exit.** Approved requirements that the design step can consume without guessing.

### 2. `/design-application`

- **Inputs.** Approved refined requirements.
- **Agent.** Architect.
- **Artifact.** Updated project `README` design section (architecture, stack, API contract, environment variables, setup, UI structure) plus any architecture decision records needed for binding technical decisions.
- **Human gate.** **Gate 2: Approve design and architecture decision records.**
- **Exit.** An approved design that backlog planning can slice into stories.

If the design would silently commit to a persistence choice, transport, auth model, embedding stack, or named dependency, the architect writes an architecture decision record before later steps depend on it.

### 3. `/plan-project`

- **Inputs.** Approved design and requirements.
- **Agent.** Architect.
- **Artifact.** Backlog epics and story rows in the project README. Updates the requirements log and backlog only; preserves completed or in-progress work so existing story documents do not become orphaned.
- **Human gate.** **Gate 3: Approve backlog.**
- **Exit.** A backlog whose stories can each be planned individually.

### 4. `/plan-story`

- **Inputs.** Approved backlog, refined requirements, design, architecture decision records.
- **Agent.** Architect.
- **Artifact.** `docs/features/{STORY-ID}-*.md` — the implementer's spec. Includes linked architecture decision records, Definition of Ready, binding constraints, ports and adapters (Section 4b), API and frontend flow notes, file touchpoints, acceptance criteria (including Phase Y binding and Phase Z quality gates), test plan rows with **Covers AC** and **Covers Sn** columns, implementation order, completion metadata, and a post-complete follow-up ledger.
- **Validation.** `/validate-story ready` confirms the story spec matches the user-story template contract: required sections present, every acceptance criterion has an `Evidence:` line, every AC ID appears in the test plan, Gherkin `Sn` IDs are mapped (or explicitly out of scope), and when Section 4b lists ports or adapters, each port has a `contract` test row, each adapter has an `integration` test row, and Phase Y contains `(binding)` criteria citing non-mock evidence.
- **Human gate.** **Gate 4: Approve story spec.**
- **Exit.** An approved, validated story document.

When a story touches an integration boundary, Section 4b must list every port and adapter, Section 8a must plan a `contract` test row per port and an `integration` test row per adapter (against the real backing service or fixture — no mock of the boundary the adapter owns), and Phase Y must contain `(binding)` criteria citing the integration tests. Every Gherkin `Sn` ID from the linked requirements that this story implements must appear in the test plan's **Covers Sn** column.

### 5. `/implement-story`

- **Inputs.** Approved story spec and linked architecture decision records.
- **Agent.** Implementer.
- **Artifact.** Code changes, tests, and an updated story document with criteria checked off as they pass. Status moves `Open` → `In Progress` → `Complete`.
- **Human gate.** None at this step. The next gate is QA evidence; the auditor and QA agents run before the human is asked to accept anything.
- **Exit.** All acceptance criteria checked off, ready for review.

The implementer follows the planned implementation order, uses red-first tests by default for each acceptance criterion, and does not silently reinterpret requirements or substitute binding decisions. If the plan turns out to be wrong, the workflow escalates back to architect rather than hiding the change in code.

### 6. `/review-story`

- **Inputs.** Story document and the changed surface.
- **Agent.** Auditor.
- **Artifact.** `docs/features/{STORY-ID}-review.md`, with a machine-readable `REVIEW SUMMARY:` line and a `Pass` or `Block` gate result.
- **Human gate.** None directly. A `Block` returns to the implementer with required actions. A `Pass` allows the story to move to QA.
- **Exit.** Review artifact with a `Pass` result.

Review focuses on the changed surface: reliability, security, API contracts, test coverage. It is not a substitute for QA, and it is not a substitute for the human's QA-evidence gate.

### 7. `/qa-story`

- **Inputs.** Story acceptance criteria and executable evidence.
- **Agent.** QA.
- **Artifact.** A criterion evidence matrix with `PASS`, `FAIL`, or `BLOCKED` for every criterion, citing the test path or other evidence that proves the result.
- **Human gate.** **Gate 5: Accept QA evidence** — only after the matrix is all PASS.
- **Exit.** Accepted QA matrix.

Any `FAIL` or `BLOCKED` loops through `/fix-from-qa`, where the implementer fixes only the failed or blocked criteria and returns to QA. QA does not infer completion from code alone.

### 8. `/document-story`

- **Inputs.** Completed story, accepted QA matrix, completion metadata, follow-up ledger.
- **Agent.** Documenter.
- **Artifact.** Updated README, API docs, OpenAPI specs, runbooks, setup instructions, or environment docs — only where the story changed those surfaces.
- **Validation.** `/validate-story complete` checks that completion metadata, evidence, and follow-up consistency match the story.
- **Human gate.** **Gate 6: Approve documentation.**
- **Exit.** Approved documentation updates and recorded completion metadata.

Documentation updates are driven by the story source of truth. The documenter does not update unrelated documentation just because it is nearby.

### `/validate-story` (cross-cutting)

`/validate-story` checks that a story document is structurally consistent with the user-story template and that its evidence, completion metadata, and follow-up ledger are coherent. Run it as a lightweight quality gate after planning, before implementation, after completion, or after post-story commands append ledger rows.

| Mode | When to run | What it checks |
|---|---|---|
| `ready` | After `/plan-story`, before Gate 4 approval | Required sections, AC `Evidence:` lines, test plan coverage of every AC ID, port/adapter contract and integration test rows, Phase Y `(binding)` criteria |
| `complete` | After `/document-story`, before Gate 6 approval | All criteria checked, Completion Metadata filled, review summary starts with `REVIEW SUMMARY:`, QA result shows all PASS |
| `followups` | After `/patch-story` or `/reconcile-story` appends ledger rows | Each follow-up row has sequential ID, date, allowed change class, files touched, verification (or justified `TBD`), **Change ref**, **Review ref**, and AC impact |
| *(default)* | Any time | All checks applicable to the story's current status |

Output is a Story Validation Matrix with `PASS` / `FAIL` / `BLOCKED` per check.

---

## What each stage produces

| Stage | Primary input | Primary output | Human gate |
|---|---|---|---|
| `/init-project` | Empty repo | Scaffolded README and `docs/` layout | — |
| `/refine-feature` | Raw notes | `docs/requirements/REQ-NNN-*.md` | Gate 1 |
| `/design-application` | Refined requirements | Design section and architecture decision records | Gate 2 |
| `/plan-project` | Design and requirements | Backlog epics and story rows | Gate 3 |
| `/plan-story` | Requirements, design, architecture decision records, backlog | `docs/features/{STORY-ID}-*.md` | Gate 4 |
| `/validate-story ready` | Story document | Readiness validation (sections, AC evidence, test plan, ports/adapters) | (supports Gate 4) |
| `/validate-story followups` | Completed story with ledger rows | Follow-up ledger validation (`Change ref`, `Review ref`, change class) | (supports post-story lanes) |
| `/implement-story` | Story spec and architecture decision records | Code, tests, updated story status | — |
| `/review-story` | Story and changed surface | Review artifact (`Pass`/`Block`) | — |
| `/qa-story` | Story criteria and evidence | Criterion evidence matrix | Gate 5 |
| `/fix-from-qa` | Failed or blocked criteria | Targeted fix | — |
| `/document-story` | Completed story, metadata, ledger | Documentation updates | Gate 6 |
| `/validate-story complete` | Completed story | Completion validation | (supports Gate 6) |

---

## Read next

- [WORKFLOW-EXAMPLE.md](WORKFLOW-EXAMPLE.md) — the same lifecycle shown through one completed story in the sample application.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — what agents, commands, templates, artifacts, evidence, and gates each do, and how they compose.
- [ROLES.md](ROLES.md) — what each agent owns and how work hands off between them.
- [TRACEABILITY.md](TRACEABILITY.md) — how requirements, architecture decision records, and design flow through the story spec into evidence.
- [POST-STORY.md](POST-STORY.md) — small follow-ups, hotfixes, audits, drift reconciliation, escalation.
