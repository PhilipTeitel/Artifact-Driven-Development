# Why This Works

This document is for readers who have skimmed the rest of the repository and want to know whether the methodology actually addresses the problems it claims to. It also names what the methodology does *not* do, so expectations stay calibrated.

---

## Problem to remedy

Each problem from the [README](README.md) is addressed by a specific artifact or gate. The methodology does not solve any of them through cleverness; it solves them by giving the model bounded context and giving humans something concrete to inspect.

| Problem | What addresses it | How |
|---|---|---|
| Vibe coding produces inconsistent and messy code | Templates and agent roles | Templates make output shape explicit; agent roles keep concerns from blurring. The same request, asked twice, returns the same artifact shape because the contract is in the template, not the prompt. |
| Any code written requires a line-by-line review | Review, model-fidelity, and QA gates | The auditor reviews the changed surface for reliability, security, contract risk, coverage, and fidelity to the purpose/domain model before QA. QA verifies each acceptance criterion against executable evidence. Review remains essential, but it is reviewing claims tied to evidence rather than unaccompanied output. |
| Getting a satisfactory result can require more effort than writing the code | Purpose, domain model, walking skeleton, and story specs | The purpose and domain model capture intent and meaning before design. The walking skeleton exposes tacit "not what I meant" feedback early. The story spec captures linked context, binding constraints, file touchpoints, acceptance criteria, and a test plan before implementation begins. |
| Where is the productivity gain? | Artifact reuse | The expensive work — refining requirements, recording binding decisions, designing the system — is captured once and reused across every story that touches it. The model's speed compounds because it does not relitigate the same context. |
| The purpose is to build applications, not write code | Artifact-driven workflow | Purpose, domain model, requirements, design, architecture decision records, and story specs sit upstream of code. Code is one output among several: tests, review artifacts, QA matrices, documentation diffs, and completion metadata are equally first-class. |
| Aim higher: build applications with AI | The full lifecycle | Purpose definition, refinement, domain modeling, design, skeleton proof, planning, implementation, review, QA, documentation, and validation are each a distinct step with a distinct artifact. The methodology operates at the level of an application, not a function. |

---

## Recurring themes

A few ideas show up in every part of the methodology, and they are worth naming directly.

### Prompts are ephemeral. Artifacts are durable.

A prompt explains what someone wanted in a moment. An artifact survives the moment. Artifacts are how intent travels between sessions, between people, and between tools. The methodology preserves prompts when useful as history, but the artifact is what proves the intent was captured and verified.

### Context is managed along independent dimensions.

Agents manage the concern dimension. Commands manage the control dimension — instructions and constraints, including which sections of which artifact may be touched. Templates manage the output-shape dimension. Keeping the dimensions independent is what allows the workflow to compose: change a template without rewriting the agent, change a command without rewriting the template, add a new agent without rewriting the commands. The opposite — collapsing all three into one prompt or one "skill" — is what destroys modularity.

### Single source of truth per concern.

Purpose lives in `docs/PURPOSE.md`. Domain language and data meaning live in `docs/DOMAIN.md`. Requirements live in one file each. architecture decision records live in one file each. Design lives in one section of the README. Story scope lives in the story document. Documentation lives in the surfaces it describes. The workflow refuses to silently reconcile conflicts between sources; it surfaces them.

### Evidence is what makes "done" mean something.

Tests, changed files, the QA matrix, the review summary, the documentation diff — these are not paperwork. They are what turn "the model says it's done" into "here is the executable proof, per criterion." Without evidence, completion is a claim. With evidence, completion is a check.

### Evidence has a grade.

Brownfield modernization fails when inferred facts are laundered into requirements, and it also fails when global analysis is treated as a gate on every slice. Evidence grades make provenance inspectable: `E1 verified`, `E2 documented`, `E3 code-derived`, `E4 inferred`, and `E5 unknown` do not carry the same authority, and each claim carries exactly one of them. The model can recover and organize weak evidence, but it cannot silently promote weak evidence into implementation-ready truth. Analysis snapshots stay frozen; decisions live in the register, the defect ledger, the slice prerequisite table, and the story spec.

### Humans own the decisions that bind work.

The agents do the work. The human approves the purpose, refined requirements, domain model, design and architecture decision records, walking skeleton, backlog, story spec, QA evidence, and documentation. Nine gates is more than zero gates. It is also fewer than the number of places where ad-hoc AI-assisted work usually requires backtracking.

---

## What this methodology does not do

It is worth being explicit about the limits.

- **It does not eliminate review.** The auditor reduces the surface area a human reviewer must examine, but a human still owns the QA-acceptance and documentation-approval gates.
- **It does not eliminate QA.** The QA matrix records evidence; a human still decides whether the evidence is good enough.
- **It does not make purpose, domain, or architectural decisions.** The modeler and architect agents record and structure decisions; the human still owns whether those decisions are correct.
- **It does not manufacture an oracle.** If the legacy system cannot be executed and only `T3 documented-only` evidence exists, parity is not independently provable. The methodology records that limit instead of hiding it behind confident language.
- **It does not make AI "autonomous."** It makes AI more reviewable. The two are different, and the methodology takes the second goal seriously and treats the first with skepticism.
- **It does not work without discipline.** A skipped gate, a silently substituted decision, or a story marked complete with unchecked criteria breaks the trace. The methodology gives the discipline somewhere to live; it does not replace the discipline itself.

---

## What good looks like

A team using this methodology well should be able to answer, for any shipped story:

- Which purpose and domain model did it preserve?
- Where is the requirement that caused it?
- Which architecture decision records constrained how it was built?
- What were the acceptance criteria?
- What evidence proves each criterion was met?
- Which review and QA gates passed, with what summary?
- Which documentation surfaces were updated?
- Who approved each gate?
- What post-complete follow-ups happened, with what **Change ref** and **Review ref**?
- For a port story, which legacy citation, evidence grade, oracle tier, fixture, tolerance, and defect decision justified the parity claim?

If those answers are all in the story document and its linked artifacts, the methodology is doing its job. If any of them requires reading the model's chat transcript, something earlier broke and the trace needs to be repaired — often via `/reconcile-story` — before more work is layered on top.

---

## Read next

- [README.md](README.md) — start here if you arrived from outside.
- [WORKFLOW-EXAMPLE.md](WORKFLOW-EXAMPLE.md) — a concrete artifact trace through the sample application.
- [PROCESS.md](PROCESS.md) — the full lifecycle, stage by stage.
- [MODERNIZATION.md](MODERNIZATION.md) — how the workflow handles legacy assessment, recovery, parity, and migration planning.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — the composable pieces and how they wire together.
- [TRACEABILITY.md](TRACEABILITY.md) — how intent flows through artifacts to evidence.
