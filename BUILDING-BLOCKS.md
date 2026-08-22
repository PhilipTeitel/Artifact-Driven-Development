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
  - **[Modeler](assets/agents/modeler.md)** — captures purpose and domain meaning before architecture and judges unresolved modeling gaps.
  - **[Architect](assets/agents/architect.md)** — turns ambiguity into requirements, design, architecture decision records, and story specs.
  - **[Implementer](assets/agents/implementer.md)** — writes code and tests against an approved story spec.
  - **[Auditor](assets/agents/auditor.md)** — provides review gates for stories, diffs, and full-repo audits.
  - **[QA](assets/agents/qa.md)** — verifies acceptance criteria against executable evidence.
  - **[Documenter](assets/agents/documenter.md)** — keeps project documentation aligned with the story source of truth.
  - **[Archaeologist](assets/agents/archaeologist.md)** — recovers evidence-graded facts from legacy repositories, documentation, release notes, history, and executable behavior. Owns path inventory, dependency graph, path details, and the defect ledger.
  - **[Migration Strategist](assets/agents/migration-strategist.md)** — assesses modernization feasibility, classifies dependencies, analyzes impedance, records decisions, and plans staging. Owns the assessment, dependency inventory, impedance analysis, decision register, and migration plan.

An agent without a command is just a persona. It does nothing until a command tells it which step to perform.

---

## Command — the *control* dimension

A command is one workflow step under explicit control: the instructions the agent follows and the constraints it must respect.

- **Purpose.** Specify what step is happening, what context is in scope, what instructions guide the work, and what constraints bound it (for example, "do not modify acceptance criteria of a completed story" or "only update the post-complete follow-up ledger section").
- **Inputs.** Required source artifacts, the agent to invoke, the template that shapes the output, the sections of which artifact may be edited, and the step-specific instructions and constraints.
- **Output.** The invocation pattern that produces or updates a specific section of a specific artifact.
- **Examples (by lane).**
  - **Intent, modeling, and design.** [`/init-project`](assets/commands/init-project.md), [`/define-purpose`](assets/commands/define-purpose.md), [`/refine-feature`](assets/commands/refine-feature.md), [`/model-domain`](assets/commands/model-domain.md), [`/design-application`](assets/commands/design-application.md), [`/plan-skeleton`](assets/commands/plan-skeleton.md), [`/plan-project`](assets/commands/plan-project.md), [`/plan-story`](assets/commands/plan-story.md), [`/validate-story`](assets/commands/validate-story.md).
  - **Implementation and verification.** [`/implement-story`](assets/commands/implement-story.md), [`/review-story`](assets/commands/review-story.md), [`/qa-story`](assets/commands/qa-story.md), [`/fix-from-qa`](assets/commands/fix-from-qa.md), [`/document-story`](assets/commands/document-story.md), [`/complete-story`](assets/commands/complete-story.md).
  - **Post-story routing.** [`/patch-story`](assets/commands/patch-story.md), [`/reconcile-story`](assets/commands/reconcile-story.md), [`/review-diff`](assets/commands/review-diff.md).
  - **Audit.** [`/map-repo`](assets/commands/map-repo.md), [`/audit-all`](assets/commands/audit-all.md), [`/triage-audit-findings`](assets/commands/triage-audit-findings.md), plus the category audits [`/audit-tooling`](assets/commands/audit-tooling.md), [`/audit-reliability`](assets/commands/audit-reliability.md), [`/audit-db`](assets/commands/audit-db.md), [`/audit-api-contracts`](assets/commands/audit-api-contracts.md), [`/audit-security`](assets/commands/audit-security.md), [`/audit-performance`](assets/commands/audit-performance.md), [`/audit-test-coverage`](assets/commands/audit-test-coverage.md).
  - **Modernization.** [`/assess-modernization`](assets/commands/assess-modernization.md), [`/inventory-paths`](assets/commands/inventory-paths.md), [`/inventory-dependencies`](assets/commands/inventory-dependencies.md), [`/map-dependency-graph`](assets/commands/map-dependency-graph.md), [`/analyze-impedance`](assets/commands/analyze-impedance.md), [`/build-oracle`](assets/commands/build-oracle.md), [`/record-decision`](assets/commands/record-decision.md), [`/document-legacy`](assets/commands/document-legacy.md), [`/trace-path`](assets/commands/trace-path.md), [`/recover-domain`](assets/commands/recover-domain.md), [`/ledger-defects`](assets/commands/ledger-defects.md), [`/plan-migration`](assets/commands/plan-migration.md), [`/plan-path-tests`](assets/commands/plan-path-tests.md), [`/plan-port-story`](assets/commands/plan-port-story.md), [`/verify-parity`](assets/commands/verify-parity.md), [`/complete-port-story`](assets/commands/complete-port-story.md). Compatibility aliases: [`/map-legacy`](assets/commands/map-legacy.md), [`/mine-history`](assets/commands/mine-history.md), [`/catalog-behavior`](assets/commands/catalog-behavior.md), [`/trace-flow`](assets/commands/trace-flow.md), [`/analyze-translation-gap`](assets/commands/analyze-translation-gap.md).

Commands are also role-bound. The workflow profile maps each command to an agent definition, and a command must load that configured role contract before it runs. If the command and agent definition conflict, the workflow stops and reports the conflict instead of silently choosing one.

A command without an agent has no judgment behind it. A command without a template has no defined output. Commands are the connective tissue, not the whole engine.

---

## Template — the *output shape* dimension

A template is a contract for what an artifact must contain.

- **Purpose.** Make the shape of acceptable output explicit, so the agent cannot satisfy the command with prose alone.
- **Inputs.** Required sections, required fields, machine-readable markers (for example, the `REVIEW SUMMARY:` line on a review artifact), and explicit placeholders for traceability links.
- **Output.** A reusable artifact skeleton.
- **Examples.**
  - **[README / design hub template](assets/templates/readme-template.md)** — architecture, stack, key decisions, API contract, environment, setup, backlog; on the modernization-port lane, optional `## Modernization` (what this is, lane status, artifact index). Greenfield omits that section. Design headings stay out until `/design-application`.
  - **[Purpose template](assets/templates/purpose-template.md)** — thesis, job, north-star outcome, trade-off rule, anti-thesis, success signals.
  - **[Domain model template](assets/templates/domain-model-template.md)** — ubiquitous language, data dictionary, entities, relationships, invariants, lifecycles, and consistency boundaries.
  - **[Requirements template](assets/templates/requirements-template.md)** — goals, non-goals, personas, constraints, resolved and open questions, Gherkin scenarios.
  - **[architecture decision record template](assets/templates/adr-template.md)** — context, decision, alternatives considered, consequences.
  - **[Walking-skeleton template](assets/templates/walking-skeleton-template.md)** — one thin running end-to-end slice through the composition root and boundaries, with a reflection checkpoint.
  - **[User story template](assets/templates/user-story-template.md)** — linked architecture decision records, Definition of Ready, binding constraints, ports and adapters table (Section 4b), file touchpoints, acceptance criteria (including Phase Y binding and Phase Z quality gates), test plan with **Covers AC** and **Covers Sn** columns and test levels (`unit`, `contract`, `integration`, `e2e` / `ui`), implementation order, completion metadata, post-complete follow-up ledger with **Change ref** and **Review ref** columns.
  - **[Port-story template](assets/templates/port-story-template.md)** — a modernization story shape based on the user-story template, adding `### 1b. Legacy source touchpoints`, slice prerequisites, `Phase P`, `## 8b. Parity Plan`, a **Covers XP** test-plan column, and the `Z8` parity gate.
  - **[Story-review template](assets/templates/story-review-template.md)** — required actions, severity, machine-readable `REVIEW SUMMARY:` line.
  - **[Audit template](assets/templates/audit-template.md)** — findings by category with evidence citations.
  - **Modernization templates.** [Modernization assessment](assets/templates/modernization-assessment-template.md), [execution path inventory](assets/templates/execution-path-inventory-template.md), [dependency inventory](assets/templates/dependency-inventory-template.md), [dependency graph](assets/templates/dependency-graph-template.md), [technology and impedance analysis](assets/templates/impedance-analysis-template.md), [execution path detail](assets/templates/execution-path-detail-template.md), [path test plan](assets/templates/path-test-plan-template.md), [decision register](assets/templates/decision-register-template.md), [oracle strategy](assets/templates/oracle-template.md), [defect ledger](assets/templates/defect-ledger-template.md), [migration plan](assets/templates/migration-plan-template.md), and [parity report](assets/templates/parity-report-template.md).

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
| Purpose | Product thesis, job, north-star outcome, trade-off rule, anti-thesis, success signals | `/define-purpose` |
| Domain model | Ubiquitous language, data dictionary, entities, relationships, invariants, lifecycles, consistency boundaries | `/model-domain` |
| Refined requirements | Clarified intent, goals, non-goals, constraints, Gherkin scenarios | `/refine-feature` |
| Application design | Architecture, stack, API contract, environment, setup, UI structure | `/design-application` |
| architecture decision record | One binding technical decision, recorded durably | `/design-application` when a decision needs to be durable |
| Walking skeleton | A thin running slice proving purpose, domain model, architecture, composition root, and boundaries | `/plan-skeleton`, then the normal implementation/review/QA tail |
| Backlog | Epics and stories that organize delivery | `/plan-project`; status synced by `/document-story` |
| Story spec | Implementation-ready instructions: linked purpose/domain/requirements/design context, acceptance criteria, test plan, file touchpoints, implementation order | `/plan-story` |
| Code and tests | Production behavior and the tests that prove each acceptance criterion | `/implement-story`, `/fix-from-qa`, `/patch-story` |
| Story acceptance evidence | Status and criterion checkboxes flipped as evidence accumulates | `/implement-story`, `/fix-from-qa` |
| Story review | Review of the changed surface for reliability, security, contract risk, coverage gaps, and model fidelity | `/review-story`, `/review-diff` |
| QA evidence matrix | Per-criterion `PASS` / `FAIL` / `BLOCKED` with cited evidence | `/qa-story` |
| Documentation updates | Synchronized changes to project documentation surfaces | `/document-story` |
| Completion metadata | Final review summary, QA result, docs handoff, completion ref | `/document-story`, `/validate-story complete` |
| Post-complete follow-up ledger entry | One small follow-up tied to a completed story | `/patch-story` |
| Audit findings | System map, category findings, triage decisions from periodic audits | `/map-repo`, `/audit-all`, category audits, `/triage-audit-findings` |
| Modernization assessment | Feasibility verdict, first-slice conditions, oracle tier, walking-skeleton feasibility | `/assess-modernization` |
| Execution path inventory | Every executable path with trigger, description, and active/suspected-dead/unknown status | `/inventory-paths` |
| Dependency inventory | External dependencies with `available` / `reimplementable` / `undecided` / `no-route` dispositions | `/inventory-dependencies` |
| Dependency graph | Which paths use which internal modules and `DEP-NNN` IDs | `/map-dependency-graph` |
| Technology and impedance analysis | Source/target characteristics and `IMP-NNN` mismatches that change port/wrap/rewrite choices | `/analyze-impedance` |
| Oracle strategy | Oracle tier, execution environment, containment | `/build-oracle` |
| Execution path detail | Sequence, dependencies, data flow, and edge cases for one `XP-NNN` | `/trace-path` |
| Decision register | Port, retire, rewrite, substitute, and comparison-policy decisions as `DEC-NNN` | `/record-decision` |
| Defect ledger | `DEF-NNN` path-scoped decisions to reproduce faithfully, fix now, or fix later | `/ledger-defects` |
| Migration plan | Staging strategy, slice plan, per-slice prerequisites, cutover, forecast | `/plan-migration` |
| Path test plan | Per-path scenarios, oracle strategy, and comparison rules | `/plan-path-tests` |
| Parity report | Per-port-story comparison of legacy expectation to new behavior, including `PAR-#` and `PROV-#` blockers | `/verify-parity` |
| Modernization hub | What this repo is, where the lane is, and links to artifacts that exist — navigation, not a second analysis copy | `/assess-modernization` creates; each producing command updates only its index row |

### Implementation note: artifacts and files

The methodology defines artifacts as concepts. The current implementation bundles related artifacts into a small number of files for trace co-location, not because the artifacts are one thing.

Three examples of bundling:

- The **story spec file** (`docs/features/{STORY-ID}-*.md`) carries the story spec, the implementer's status and acceptance-criteria evidence, the QA evidence matrix, the completion metadata, and the post-complete follow-up ledger entries — every artifact tied to one story in one document so the trace stays in one place. A walking-skeleton story uses the same file pattern with a thinner scope.
- The **project README** carries the application design and the backlog because both describe the same project. On a brownfield port it also carries the **modernization hub** (`## Modernization`): what the port is, lane status, and an index of links. Those cells have separate owners listed in the README template. The linked files remain canonical.
- The **purpose and domain files** (`docs/PURPOSE.md` and `docs/DOMAIN.md`) stay separate because they are small, global source-of-truth artifacts that every later step reads.
- The **story review file** carries one story review artifact; a diff review of the same shape lives under `docs/reviews/`.

This bundling is a convenience. The artifacts are still distinct: each has one producer, one purpose, and one place in the trace. A project that wanted to keep them in separate files could; this methodology happens to keep them together because related context is easier to follow when it is co-located.

Templates in this methodology — purpose, domain model, README, architecture decision record, requirements, walking skeleton, user story, story review, audit — define the shape of those files, including which artifacts each file is expected to carry. The templates are an implementation choice. The artifacts are the design.

### Project documentation surfaces

Some documentation surfaces — OpenAPI specs, runbooks, environment docs, project-specific setup instructions — are not artifacts the methodology itself produces. They are **project documentation** that the Documenter syncs as part of `/document-story` when a story changes them. They are downstream surfaces kept in agreement with the artifacts above, not new artifacts in their own right.

Artifacts are what distinguish this methodology from "ask the model nicely." Prompts are ephemeral. Artifacts are durable.

---

## Evidence — the proof

Evidence is what makes "done" mean something specific.

- **Purpose.** Tie each acceptance criterion to something executable or verifiable.
- **Examples.** Unit, contract, and integration tests cited by path; changed files; the QA matrix rows that mark each criterion `PASS`; the review summary line; the documentation diff that closes the loop.

Evidence answers the question "how do we know?" An artifact without evidence is a claim. Evidence turns the claim into a check.

Modernization adds a second evidence axis: **provenance**. Greenfield evidence proves an acceptance criterion passed. Brownfield provenance proves where a recovered fact came from and how much confidence it deserves. The default grades are `E1 verified`, `E2 documented`, `E3 code-derived`, `E4 inferred`, and `E5 unknown`. Each claim carries exactly one grade — the weakest grade that applies to the actionable part. `E4` and `E5` do not become implementation-ready facts unless a human resolves or explicitly accepts the uncertainty for the scope those claims bind.

---

## Gate — the decision point

A gate is where work stops until someone — human or agent — decides whether it moves forward.

- **Purpose.** Make completion explicit instead of implicit.
- **Examples.**
  - **Agent gates.** Review `Pass` or `Block`, including model-fidelity `MODEL-#` findings. QA `PASS`, `FAIL`, or `BLOCKED` per criterion. `validate-story ready`, `validate-story complete`, and `validate-story followups`.
  - **Human gates.** The nine approvals in the [README](README.md) swimlane: purpose, refined requirements, domain model, design and architecture decision records, walking skeleton, backlog, story spec, QA evidence, documentation.
  - **Modernization gates.** M1 assessment verdict, M2 recovered path documentation for the current slice, M3 defect decisions for that slice, M4 migration plan, and M5 parity evidence. Parity adds `PAR-#` and `PROV-#` review findings, `PASS` / `FAIL` / `BLOCKED` verification rows, and the port-story `Z8` quality gate.

Gates exist because skipping them has been observed to cost more later. A gate that becomes a formality has stopped doing its job.

---

## Composition matrix

The composition matrix shows which command produces or updates which artifact, with which agent, and where the artifact is currently recorded.

| Command | Agent | Artifact produced or updated | Recorded in |
|---|---|---|---|
| `/init-project` | Architect or human | Project scaffold | `README.md`, `docs/` layout |
| `/define-purpose` | Modeler | Purpose | `docs/PURPOSE.md` |
| `/refine-feature` | Architect | Refined requirements | `docs/requirements/REQ-NNN-*.md` |
| `/model-domain` | Modeler | Domain model and data dictionary | `docs/DOMAIN.md` |
| `/design-application` | Architect | Application design; architecture decision records (as needed) | Project README design sections; `docs/decisions/ADR-NNN-*.md` |
| `/plan-skeleton` | Architect | Walking-skeleton story | `docs/features/SK-1-*.md` or configured story path |
| `/plan-project` | Architect | Backlog | Project README backlog section |
| `/plan-story` | Architect | Story spec | `docs/features/{STORY-ID}-*.md` |
| `/validate-story ready` | Architect | Readiness validation | Story Validation Matrix against the story spec; corrects readiness defects only |
| `/validate-story followups` | Implementer or Auditor | Follow-up ledger validation | Story Validation Matrix; corrects ledger drift only |
| `/implement-story` | Implementer | Code, tests; story acceptance evidence | Codebase; story spec status field and criteria checkboxes |
| `/review-story` | Auditor | Story review | `docs/features/{STORY-ID}-review.md` |
| `/qa-story` | QA | QA evidence matrix | Story spec QA section |
| `/fix-from-qa` | Implementer | Code, tests; updated story acceptance evidence | Codebase; story spec checkboxes for failed or blocked rows only |
| `/document-story` | Documenter | Documentation updates; completion metadata | Project README and project documentation surfaces (OpenAPI, runbooks, environment docs); story spec completion metadata |
| `/validate-story complete` | Documenter | Completion validation | Assertion against story spec; corrects metadata if needed |
| `/patch-story` | Implementer | Post-complete follow-up ledger entry; targeted code, test, or doc changes | Story spec follow-up ledger; codebase or documentation surfaces |
| `/reconcile-story` | Auditor | Drift classification; follow-up ledger entries when safe | Story spec follow-up ledger (when drift is reconcilable); Drift Reconciliation Summary |
| `/review-diff` | Auditor | Story review (diff scope) | `docs/reviews/diff-{base}--{target}-{YYYYMMDD}.md` |
| `/map-repo` | Auditor | System map | Audit findings |
| `/audit-all` | Auditor | Audit findings across all categories | Audit findings |
| `/audit-{category}` | Auditor | Category findings (`tooling`, `reliability`, `db`, `api-contracts`, `security`, `performance`, `test-coverage`) | Audit findings |
| `/triage-audit-findings` | Auditor | Audit triage decisions | Audit findings |
| `/inventory-paths` | Archaeologist | Execution path inventory | `docs/modernization/execution-path-inventory.md` |
| `/inventory-dependencies` | Migration Strategist | Dependency inventory | `docs/modernization/dependency-inventory.md` |
| `/map-dependency-graph` | Archaeologist | Dependency graph | `docs/modernization/dependency-graph.md` |
| `/analyze-impedance` | Migration Strategist | Technology and impedance analysis | `docs/modernization/impedance-analysis.md` |
| `/build-oracle` | Implementer | Oracle strategy and harness/fixture files | `docs/modernization/oracle.md`; fixture or harness files when built |
| `/assess-modernization` | Migration Strategist | Modernization assessment; README hub created or updated | `docs/modernization/ASSESSMENT.md`; project README `## Modernization` |
| `/record-decision` | Migration Strategist (records); human (decides) | Decision register | `docs/modernization/decision-register.md` |
| `/trace-path` | Archaeologist | Execution path detail | `docs/modernization/paths/XP-NNN-*.md` |
| `/recover-domain` | Modeler | Recovered purpose and domain model | `docs/PURPOSE.md`; `docs/DOMAIN.md` |
| `/ledger-defects` | Archaeologist (records); human (decides) | Defect ledger | `docs/modernization/defect-ledger.md` |
| `/document-legacy` | Archaeologist and Modeler | Coordinates slice-scoped recovery | Path details, purpose, domain model, defect ledger |
| `/plan-migration` | Migration Strategist | Migration plan; recommended ADRs | `docs/modernization/migration-plan.md` |
| `/plan-path-tests` | Architect | Path test plan | `docs/modernization/test-plans/XP-NNN-tests.md` |
| `/plan-port-story` | Architect | Port story spec | `docs/features/{STORY-ID}-*.md` |
| `/verify-parity` | QA | Parity report | `docs/modernization/parity/{STORY-ID}-parity.md` |
| `/complete-port-story` | Implementer, Auditor, QA, Docs-PM | Code, tests, review, parity report, QA evidence, documentation, validation | Codebase; story spec; story review; parity report; project docs |

Each producing modernization command also updates **only its README Artifact index row** when `## Modernization` exists. `/assess-modernization`, `/record-decision`, and `/plan-migration` also update **What this is** / **Lane status**. The hub is navigation; the linked file is canonical.

Read this matrix as: *the agent brings concern; the command brings control (instructions and constraints); the template shapes the file the artifact lands in; the artifact itself is the durable conceptual output.* Each axis moves independently. Change the template and the file layout changes; the artifacts do not. Change the command and where the artifact lands may change; the artifact does not. Change the agent and the judgment behind the artifact changes; everything else stays.

---

## Read next

- [WORKFLOW-EXAMPLE.md](WORKFLOW-EXAMPLE.md) — a concrete walkthrough showing agents, commands, templates, artifacts, evidence, and gates in one completed story.
- [MODERNIZATION.md](MODERNIZATION.md) — the brownfield modernization lane and its additional artifacts.
- [ROLES.md](ROLES.md) — the agents in depth: what each one owns and how work hands off.
- [PROCESS.md](PROCESS.md) — how these blocks chain together across the story lifecycle.
- [TRACEABILITY.md](TRACEABILITY.md) — how the artifacts in this matrix link into a single trace from intent to evidence.
