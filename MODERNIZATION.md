# Modernization Lane

Artifact-Driven Development can start from a raw idea, or it can start from an existing application that needs to be ported to a new language, framework, architecture, or operating model.

The main delivery workflow does not change. Purpose, domain, requirements, design, stories, implementation, review, QA, documentation, and validation still provide the trace from intent to evidence. Modernization adds an upstream lane that examines the legacy system first, recovers what is knowable, grades the evidence, and decides how much parity can honestly be proved.

The rule is simple: the legacy application is evidence, not automatically the requirement. User documentation, release notes, executable behavior, source code, and commit history can disagree. The modernization lane preserves those disagreements until a human decision resolves them.

Two further rules keep the lane usable:

1. **Global analysis informs. Slice prerequisites gate.** Inventories describe the whole legacy system. They do not decide whether a given slice may start.
2. **Analysis is a snapshot. Decisions are living.** Later work cites an analysis artifact; it does not rewrite it.

---

## Design Principles

These rules bind every modernization command, template, and agent.

**A. One owner, one writer.** Each artifact has one owning agent. Only that agent may write it. Other agents consume it. If a later phase needs to override a finding, the override goes in the later phase's own artifact with a citation.

**B. Analysis is immutable after snapshot.** Execution-path inventory, dependency inventory, path details, dependency graph, and impedance analysis describe *what is*. After `Status: Snapshot`, the owner may append `## Errata` or produce a new version. Nobody edits table cells in place to record a later decision.

**C. Decisions are mutable and live in one place.** The decision register, defect ledger, migration plan, ADRs, and story specs describe *what we will do*. Current state belongs in the cell. History belongs in version control. Do not add prose preambles that narrate how a cell used to read.

**D. Slice prerequisites gate delivery.** Each slice (and its port story) carries a short prerequisite table naming the specific `DEP-NNN`, `DEC-NNN`, and `DEF-NNN` IDs that bind it. A global count such as "16 of 33 dependency routes are unresolved" never blocks a slice that does not use those routes.

**E. Templates are conditional.** Omit sections that do not apply to the discovered source or target stack. Do not fill them with "not applicable" rows. Reserve, retired, and suspected-dead items belong in an appendix, not interleaved with active work.

**F. Evidence grades are singular.** Each claim gets exactly one grade — the weakest grade that applies to the actionable part of the claim. If sub-claims differ, split them into separate rows.

**G. Cross-references do not duplicate state.** A tension, conflict, or finding is recorded once, in the artifact that owns that concern. Other documents link by ID.

**H. Every document opens with one paragraph.** The summary says what the document covers, the key findings, and where to look next. No document should require reading four others to answer a basic question.

**I. Brevity is a feature.** An artifact earns its keep if it helps a human decide what to port, retire, rewrite, substitute, or sequence. Traceability does not require restating the same fact in four taxonomies.

---

## High-Level Flow

```mermaid
flowchart TD
    subgraph Human [Human]
        legacyApp["Legacy application and docs"]
        acceptAssessment{"M1 accept assessment"}
        acceptRecovery{"M2 accept recovered path docs"}
        decideDefects{"M3 record defect decisions"}
        approveMigration{"M4 approve migration plan"}
        acceptParity{"M5 accept parity evidence"}
    end

    subgraph AssessmentPhase [Assessment — global, once]
        inventoryPaths["/inventory-paths"]
        inventoryDeps["/inventory-dependencies"]
        mapGraph["/map-dependency-graph"]
        analyzeImp["/analyze-impedance"]
        buildOracle["/build-oracle probe"]
        assess["/assess-modernization"]
        pathInv[/"Execution path inventory"/]
        depInv[/"Dependency inventory"/]
        depGraph[/"Dependency graph"/]
        impDoc[/"Impedance analysis"/]
        oracleDoc[/"Oracle strategy"/]
        assessDoc[/"Assessment"/]
    end

    subgraph RecoverySlice [Recovery — per slice]
        tracePath["/trace-path"]
        recoverDomain["/recover-domain"]
        ledgerDefects["/ledger-defects"]
        pathDetail[/"Execution path detail"/]
        purposeDoc[/"Purpose"/]
        domainDoc[/"Domain model"/]
        defectLedger[/"Defect ledger"/]
    end

    subgraph Planning [Planning]
        recordDec["/record-decision"]
        planMig["/plan-migration"]
        planTests["/plan-path-tests"]
        planPort["/plan-port-story"]
        decReg[/"Decision register"/]
        migPlan[/"Migration plan"/]
        testPlan[/"Path test plan"/]
        portStory[/"Port story"/]
    end

    subgraph Delivery [Standard lifecycle tail]
        completePort["/complete-port-story"]
        parityReport[/"Parity report"/]
    end

    legacyApp --> inventoryPaths --> pathInv --> assess
    legacyApp --> inventoryDeps --> depInv --> assess
    pathInv --> mapGraph
    depInv --> mapGraph --> depGraph --> assess
    pathInv --> analyzeImp
    depInv --> analyzeImp --> impDoc --> assess
    legacyApp --> buildOracle --> oracleDoc --> assess
    assess --> assessDoc --> acceptAssessment
    acceptAssessment --> recordDec --> decReg
    acceptAssessment --> planMig
    decReg --> planMig --> migPlan --> approveMigration
    approveMigration --> tracePath --> pathDetail --> acceptRecovery
    pathDetail --> recoverDomain --> purposeDoc
    recoverDomain --> domainDoc
    pathDetail --> ledgerDefects --> defectLedger --> decideDefects
    pathDetail --> planTests --> testPlan
    decideDefects --> planPort
    testPlan --> planPort
    migPlan --> planPort --> portStory --> completePort --> parityReport --> acceptParity
```

The modernization lane has three phases:

1. **Assessment** decides whether the port is feasible and what conditions must be true before *any* slice starts. Its artifacts are global and short.
2. **Recovery** is slice-scoped. It traces only the execution paths in the next slice, recovers purpose/domain terms those paths require, and ledgers defects that bind those paths.
3. **Migration planning and port delivery** stages the work, records decisions, plans per-path tests, implements parity-first, and verifies the new system against the legacy oracle.

The per-slice ADD loop is: **recover → refine → design → implement → UAT**. Global analysis feeds that loop. It does not replace it.

The configured design doc (default `README.md`) is the repo hub. `/assess-modernization` creates it if it is missing, including a `## Modernization` section: what this port is, lane status, and an index of links. That section is omitted on greenfield projects. Design sections (architecture, stack, getting started, and so on) stay out of the file until `/design-application`. Each modernization command updates only the hub cells it owns — see [the README template](assets/templates/readme-template.md).

---

## Artifact Ownership

| Artifact | Owner (writer) | Command | Recorded in | Kind |
|---|---|---|---|---|
| Execution path inventory | Archaeologist | `/inventory-paths` | `docs/modernization/execution-path-inventory.md` | Analysis snapshot |
| Dependency inventory | Migration Strategist | `/inventory-dependencies` | `docs/modernization/dependency-inventory.md` | Analysis snapshot |
| Dependency graph | Archaeologist | `/map-dependency-graph` | `docs/modernization/dependency-graph.md` | Analysis snapshot |
| Technology and impedance analysis | Migration Strategist | `/analyze-impedance` | `docs/modernization/impedance-analysis.md` | Analysis snapshot |
| Oracle strategy | Implementer | `/build-oracle` | `docs/modernization/oracle.md` | Analysis snapshot (tier); harness files may grow |
| Modernization assessment | Migration Strategist | `/assess-modernization` | `docs/modernization/ASSESSMENT.md` | Decision (M1) |
| Execution path detail | Archaeologist | `/trace-path` | `docs/modernization/paths/XP-NNN-*.md` | Analysis snapshot |
| Defect ledger | Archaeologist records; human decides | `/ledger-defects` | `docs/modernization/defect-ledger.md` | Decision (M3) |
| Decision register | Migration Strategist records; human decides | `/record-decision` | `docs/modernization/decision-register.md` | Decision |
| Migration plan | Migration Strategist | `/plan-migration` | `docs/modernization/migration-plan.md` | Decision (M4) |
| Path test plan | Architect plans; QA verifies via parity | `/plan-path-tests` | `docs/modernization/test-plans/XP-NNN-tests.md` | Decision |
| Port story spec | Architect | `/plan-port-story` | `docs/features/{STORY-ID}-*.md` | Decision |
| Parity report | QA | `/verify-parity` | `docs/modernization/parity/{STORY-ID}-parity.md` | Evidence (M5) |
| Modernization hub (bundled in README) | Split by section — see the README template | `/assess-modernization` creates; each producing command updates its index row | Configured design doc `## Modernization` | Navigation |

The Archaeologist builds the dependency *graph* (which paths use which modules and dependencies). The Migration Strategist *uses* that graph in the assessment and migration plan. Sequencing analysis does not get written back into the graph.

Path test plans are written by the Architect. QA does not edit them; `/verify-parity` checks the story's Phase P criteria against the plan's oracle and comparison rules.

---

## Snapshot, Errata, And Versions

Analysis artifacts use this header contract:

- `**Status:** Draft` — the owning command may still rewrite rows.
- `**Status:** Snapshot` — the phase that produced it has completed. Table cells are frozen.
- `**Version:** vN` — increment when the owner replaces the snapshot with a new one.

After Snapshot:

- **Do not** edit a cell to record a later decision, status, or "we decided this is fine."
- **Do** record the decision in the decision register, defect ledger, migration-plan slice row, or story spec, citing the analysis ID.
- **Do** append `## Errata` when a factual error is found (wrong path, wrong citation). An erratum names the row ID, the correction, the evidence, and the date.
- **Do** produce `vN+1` when new evidence changes the snapshot's substance. Git is the history of vN.

Decision artifacts stay mutable. Their tables show current state. Do not keep a prose changelog in the file.

---

## Modernization Gates

The greenfield workflow has nine human gates. Modernization adds five more. M1 and M4 are project-level. M2 and M3 are re-entered for each slice. M5 is per port story.

| Gate | What is being decided | What the human is looking for |
|---|---|---|
| M1. Accept assessment verdict | Is this modernization feasible enough to start the first slice? | `go`, `go-with-conditions`, or `no-go`; a one-page `ASSESSMENT.md`; oracle tier; first-slice conditions only; walking-skeleton feasibility. Global unresolved dependencies that do not bind the first slice are not M1 blockers. |
| M2. Accept recovered documentation | Is the *current slice's* path-detail evidence strong enough to plan against? | In-scope `XP-NNN` details at `Ready for Requirements`; singular evidence grades; no unaccepted `E4 inferred` or `E5 unknown` claims in that slice. Other slices may still be inventory-only. |
| M3. Record defect decisions | Should suspicious legacy behavior in *this slice* be reproduced, fixed now, or fixed later? | Each in-scope `DEF-NNN` names one or more `XP-NNN` IDs and has one decision: `reproduce-faithfully`, `fix-now`, or `fix-later`. A defect that asks a system-wide question the methodology says has no system-wide answer is mis-posed: decompose it or close it. |
| M4. Approve migration plan | Is this the right staging, cutover, and structure-fidelity strategy? | Chosen strategy (`strangler`, `phased-rewrite`, or `big-bang-parallel-run`); slice order; each slice's prerequisite table; covered `XP-NNN` / `Sn`; oracle evidence; ADR implications; rollback; forecast confidence. Later slices may be inventory IDs until their recovery runs. |
| M5. Accept parity evidence | Did this port story match the accepted legacy expectation? | A parity report with `PARITY SUMMARY:`; no blocking `PAR-#` or `PROV-#` findings; mismatches reconciled through the defect ledger; comparison rules taken from the path test plan, not a global default. |

These gates do not replace the greenfield gates. They add the decisions that only brownfield work needs.

---

## Phase 1: Assessment

Assessment answers: *Can this legacy application be migrated with credible evidence, and what would make the first slice unsafe?*

The five-minute picture lives in `docs/modernization/ASSESSMENT.md`. Inventories behind it are reference, not a second narrative.

`/assess-modernization` is the orchestrator. It runs or consumes:

1. `/inventory-paths`
2. `/inventory-dependencies`
3. `/map-dependency-graph`
4. `/analyze-impedance`
5. `/build-oracle probe`
6. `/assess-modernization` (synthesis)

`/record-decision` runs whenever an owner choice is needed. It is not a required step in the sequence; open `DEC-NNN` rows that bind the first slice become M1 conditions.

### `/inventory-paths`

- **Inputs.** Legacy repository path, optional scope.
- **Agent.** Archaeologist.
- **Artifact.** `docs/modernization/execution-path-inventory.md`.
- **Exit.** Every executable path — CLI, library API entry point, batch job, service endpoint, scheduled task, event handler — has an `XP-NNN` ID, trigger, one-line description, and status (`active`, `suspected-dead`, or `unknown`). Active paths are the main table. Suspected-dead, unknown, and retired paths go in an appendix. History is used only to classify status, not to produce a separate intent ledger.

### `/inventory-dependencies`

- **Inputs.** Legacy repository, source stack, target stack when known.
- **Agent.** Migration Strategist.
- **Artifact.** `docs/modernization/dependency-inventory.md`.
- **Exit.** Each external dependency has a `DEP-NNN` ID, version (known or unknown), license, support status, and exactly one disposition:

| Disposition | Meaning |
|---|---|
| `available` | A credible target-stack equivalent exists. |
| `reimplementable` | No direct equivalent, but the needed behavior is bounded enough to rewrite. |
| `undecided` | An owner decision is needed. Name the question; do not call this blocked. |
| `no-route` | No known replacement. This disposition blocks *paths that use it*, not the whole program. |

Do not use `blocked`. Fourteen owner-pending rows and two dead ends must not look identical.

Dispositions are snapshot classifications. A later substitution choice is a `DEC-NNN` (and an ADR when it binds the target design). The inventory row stays as classified.

### `/map-dependency-graph`

- **Inputs.** Path inventory, dependency inventory, legacy repository.
- **Agent.** Archaeologist.
- **Artifact.** `docs/modernization/dependency-graph.md`.
- **Exit.** A join table answering: if I port path X, which internal modules and `DEP-NNN` IDs come with it? If dependency Y is `no-route`, which paths are affected? If a used dependency is missing from the inventory, stop and return to `/inventory-dependencies`. Do not add `DEP-NNN` rows from this command.

### `/analyze-impedance`

- **Inputs.** Source stack, target stack, path inventory, dependency inventory, dependency graph.
- **Agent.** Migration Strategist.
- **Artifact.** `docs/modernization/impedance-analysis.md`.
- **Exit.** Source and target characteristics that actually affect porting, plus `IMP-NNN` mismatches with severity, affected `XP-NNN` IDs, and a candidate pattern (`preserve`, `wrap`, `rewrite`, `adapter`). Include a seeded language-family section only when that family is the discovered source stack. Omit the rest entirely.

### `/build-oracle probe`

- **Inputs.** Legacy repository, setup docs.
- **Agent.** Implementer, with oracle-tier constraints from the Migration Strategist.
- **Artifact.** `docs/modernization/oracle.md`.
- **Exit.** The legacy oracle is classified as `T1 executable`, `T2 recorded`, or `T3 documented-only`. Containment, determinism, and environment facts that affect the *tier* are recorded. Per-path fixtures and comparison rules do not live here; they live in path test plans.

### `/assess-modernization`

- **Inputs.** The five assessment artifacts, target stack, and source docs.
- **Agent.** Migration Strategist.
- **Artifact.** `docs/modernization/ASSESSMENT.md`.
- **Human gate.** **M1: Accept assessment verdict.**
- **Exit.** A `go`, `go-with-conditions`, or `no-go` verdict that a reader can understand in under five minutes: what exists, oracle tier, first-slice candidate, conditions that actually bind that slice, and where to look next.

---

## Phase 2: Recovery

Recovery answers: *What does this slice's execution paths do, how do we know, and what remains uncertain?*

Do not catalog the entire legacy system before the first slice. The path inventory already says what exists. `/document-legacy` takes a scope — typically the next slice's `XP-NNN` IDs — and runs:

1. `/trace-path` for each in-scope path (or logical group)
2. `/recover-domain` from those details plus user docs
3. `/ledger-defects` for mismatches those paths surface

### `/trace-path`

- **Inputs.** One `XP-NNN` (or a named group), the path inventory, and the legacy repository.
- **Agent.** Archaeologist.
- **Artifact.** `docs/modernization/paths/XP-NNN-*.md`.
- **Human gate.** Supports **M2** for the current slice.
- **Exit.** Sequence of operations, internal and external dependencies, data flow, edge cases and error handling as the code actually behaves, and one evidence grade per claim. This document feeds the port story's `§1b Legacy source touchpoints` and the path test plan. It does not include target design, slice status, or decision preambles.

Related paths may share one detail document when they are the same operation with different triggers. Unrelated paths do not.

### `/recover-domain`

- **Inputs.** In-scope path details, user docs, release notes, defect ledger, existing purpose/domain artifacts.
- **Agent.** Modeler in legacy recovery mode.
- **Artifacts.** `docs/PURPOSE.md` and `docs/DOMAIN.md`.
- **Human gate.** Supports the standard purpose/domain approvals and **M2**.
- **Exit.** Purpose and domain model recovered from evidence only. `E4 inferred` and `E5 unknown` claims remain open questions when they affect design or story planning. Implementation names are candidate terms, not domain truth.

### `/ledger-defects`

- **Inputs.** Bug reports, support notes, path details, oracle mismatches, suspicious legacy behavior.
- **Agent.** Archaeologist.
- **Artifact.** `docs/modernization/defect-ledger.md`.
- **Human gate.** **M3: Record defect decisions** for defects that bind the current slice.
- **Exit.** Each `DEF-NNN` names the affected `XP-NNN` ID(s) and a decision: `reproduce-faithfully`, `fix-now`, or `fix-later`. Refuse a defect that asks a system-wide question (for example a single numeric tolerance for every path) when the methodology requires a per-path answer. Split it, or record a `DEC-NNN` that says comparison is per path, and close the mis-posed defect.

Open defect decisions for *other* slices do not block this slice.

### `/document-legacy`

- **Inputs.** Accepted or conditionally accepted assessment, a slice or `XP-NNN` scope, user documentation.
- **Agent.** Orchestrates Archaeologist and Modeler.
- **Artifacts.** Path details, purpose, domain model, defect ledger rows for that scope.
- **Human gate.** **M2** and **M3** for the scoped slice.
- **Exit.** Recovered artifacts are ready to feed `/refine-feature`, `/plan-path-tests`, and `/plan-port-story` for that slice.

---

## Phase 3: Migration Planning And Port Delivery

Planning answers: *How should the migration be sliced, what must stay faithful, what can be changed, and how will parity be proved for this path?*

### `/record-decision`

- **Inputs.** The question, the human's answer, the evidence, and the `XP-NNN` / `DEP-NNN` / `IMP-NNN` / `DEF-NNN` IDs it affects.
- **Agent.** Migration Strategist records; the human decides.
- **Artifact.** `docs/modernization/decision-register.md`.
- **Exit.** Every porting decision — port, retire, rewrite, substitute, reproduce vs fix as policy, comparison policy — has a `DEC-NNN` row: question, answer, evidence, date, affected IDs. "What did we decide about X?" has one location. Do not restate the answer in analysis ledgers.

### `/plan-migration`

- **Inputs.** Accepted assessment, decision register, path inventory, dependency graph, impedance analysis, oracle doc, recovered purpose/domain when present, defect ledger, target stack.
- **Agent.** Migration Strategist.
- **Artifact.** `docs/modernization/migration-plan.md`. Recommend ADRs; do not take over the Architect's ADR files.
- **Human gate.** **M4: Approve migration plan.**
- **Exit.** A staging strategy, slice plan, and per-slice prerequisite table. A slice may be listed as inventory `XP-NNN` IDs before those paths are detailed. Each slice names only the `DEP-NNN`, `DEC-NNN`, and `DEF-NNN` IDs that bind *that* slice. Recalibrate forecast after the first completed port slice.

The per-slice loop in the plan is recover → refine → design → implement → UAT. Check off a resolved prerequisite in the slice row or port story, not in the global inventory.

### `/plan-path-tests`

- **Inputs.** One `XP-NNN` path detail, linked `REQ-NNN` / `Sn` when present, oracle tier, defect decisions that bind the path.
- **Agent.** Architect.
- **Artifact.** `docs/modernization/test-plans/XP-NNN-tests.md`.
- **Exit.** Happy-path, edge, and error scenarios; oracle strategy for *this* path; comparison rules (`exact`, `tolerance-based` with the actual bound, or `semantic`). Comparison is decided per path. A profile hint is not a gate. This artifact is what Phase P and `## 8b. Parity Plan` are built from.

### `/plan-port-story`

- **Inputs.** Story ID, migration-plan slice, in-scope `XP-NNN` details and test plans, linked `REQ-NNN` / `Sn`, oracle doc, defect ledger, decision register, purpose, domain model, ADRs, design doc.
- **Agent.** Architect.
- **Artifact.** `docs/features/{STORY-ID}-*.md` using the port-story template.
- **Human gate.** Standard **Gate 7: Approve story spec**, with modernization readiness checks.
- **Exit.** An implementation-ready port story with `### 1b. Legacy source touchpoints`, a **Slice prerequisites** table copied from the migration-plan row, `Phase P`, `## 8b. Parity Plan`, a `Covers XP` test-plan column, and `Z8`. The story may check off prerequisites. It may not edit analysis snapshots.

### `/complete-port-story`

- **Inputs.** Approved port story, path test plans, oracle doc, defect ledger, and no unresolved `E4` / `E5` claim in covered scope without a recorded `DEC-NNN`.
- **Agents.** Implementer, Auditor, QA, Docs-PM.
- **Artifacts.** Code, tests, story review, parity report, QA matrix, documentation updates, validation result.
- **Human gate.** **M5: Accept parity evidence**, followed by the normal **Gate 8** QA evidence and **Gate 9** documentation approval.
- **Exit.** Port story completed with parity evidence, QA evidence, documentation, and completion metadata.

### `/verify-parity`

- **Inputs.** Port story `Phase P`, `## 8b. Parity Plan`, path test plan comparison rules, linked `XP-NNN`, oracle refs, defect decisions.
- **Agent.** QA.
- **Artifact.** `docs/modernization/parity/{STORY-ID}-parity.md`.
- **Human gate.** Supports **M5**.
- **Exit.** A parity report whose first non-comment line is `PARITY SUMMARY:` and whose matrix records `PASS`, `FAIL`, or `BLOCKED` for the story's parity claims. Binding comparison rules come from the path test plan. Do not apply a global numeric default because a path-level rule is missing — mark `BLOCKED` and return to `/plan-path-tests`.

---

## Evidence Grades

Modernization evidence has two questions:

1. **What proves the recovered fact?**
2. **Is that proof strong enough to plan, implement, or claim parity?**

The default evidence grades are:

| Grade | Meaning | Planning consequence |
|---|---|---|
| `E1 verified` | Observed by executing the legacy system or oracle. | Strongest basis for parity and acceptance data. |
| `E2 documented` | Stated in user documentation, release notes, help text, or accepted support material. | Strong basis for requirements; still reconcile against executable behavior when possible. |
| `E3 code-derived` | Read from legacy source, configuration, schema, or tests. | Useful, but not automatically product intent. |
| `E4 inferred` | Deduced from commit history, names, structure, or analogy. | Blocks implementation-ready port planning unless accepted by the user. |
| `E5 unknown` | Missing or unresolved. | Blocks affected scope until resolved, deferred, or explicitly accepted as risk. |

Each row carries exactly one grade. `E1 verified / E3 code-derived` is not a grade; it is two claims. Split the row.

The grade is not decorative metadata; it controls readiness for the scope that claim binds.

---

## Oracle Tiers

Parity is only as strong as the oracle behind it.

| Tier | Meaning | What can be claimed |
|---|---|---|
| `T1 executable` | The legacy system can be run repeatedly in a controlled environment. | Repeated legacy-vs-new comparison is possible. |
| `T2 recorded` | Legacy behavior can be frozen into fixture outputs, but not repeated cheaply. | Parity can be checked against a fixed corpus, not an independently rerunnable system. |
| `T3 documented-only` | The legacy system cannot be run; expected behavior comes from documentation or user-supplied acceptance data. | Parity is limited to documented expectations; it is not independently provable. |

The workflow forbids claiming parity confidence above the oracle tier. A `T3 documented-only` project can still be migrated, but the artifacts must say that parity depends on documented or user-accepted expectations.

Comparison rules are per execution path. The workflow profile may hint at a numeric or text default. That hint never gates a slice and never substitutes for a missing path test-plan rule.

---

## Defect Decisions

Legacy defects are not automatically fixed during a port. A behavior that looks wrong may be:

- A bug users depend on.
- A bug users want fixed now.
- A bug users want preserved for cutover and fixed later.
- A misunderstanding caused by weak evidence.

The defect ledger records the decision before implementation:

| Decision | Meaning |
|---|---|
| `reproduce-faithfully` | The port should match the legacy behavior, even if it looks wrong. |
| `fix-now` | The port should intentionally change the behavior and test the corrected expectation. |
| `fix-later` | The port should preserve legacy behavior for now and create or link deferred work. |

An agent may discover suspicious behavior. It does not decide which category applies. That decision belongs to the human gate.

Every defect names the execution path it affects. Owner policy questions that are not defects — retire vs port, substitute vs wrap, per-path vs shared comparison — belong in the decision register, not the defect ledger.

---

## Decision Register Versus ADRs

| Record | Use when |
|---|---|
| `DEC-NNN` | Porting choices: which paths to port, retire, or rewrite; which dependency route to take; whether a mismatch is in or out of slice scope. |
| `ADR-NNN` | Binding *target* design: persistence, process boundary, named target dependency, integration model, cutover mechanism. |
| `DEF-NNN` | A specific legacy mismatch on a named path, with reproduce / fix-now / fix-later. |
| `RISK-NNN` | Assessment risks that affect the M1 verdict. |
| `IMP-NNN` | Snapshot impedance mismatches. Later choices cite them; they are not updated to "resolved." |

---

## Where The Lane Rejoins The Standard Lifecycle

The modernization lane is an alternate entry point, not a different delivery system.

- `/recover-domain` satisfies the purpose and domain-model work from recovered evidence rather than from a raw idea.
- `/refine-feature` consumes path details (and user docs) and writes normal `REQ-NNN` / `Sn` scenarios.
- `/design-application` and `/plan-project` keep their normal responsibilities.
- The walking skeleton remains preferred when feasible. If `ASSESSMENT.md` says no useful skeleton can run yet, the first port slice may be a black-box proof slice instead.
- `/plan-path-tests` then `/plan-port-story` replace `/plan-story` for migration slices.
- `/complete-port-story` is the normal implementation/review/QA/document/validate tail with `/verify-parity` inserted between review and QA.
- Standard Gate 8 and Gate 9 remain unchanged: QA evidence and documentation still close the story.

A slice owner should be able to work from: the migration-plan row (including prerequisites), the in-scope path details, the path test plans, the cited `DEC-NNN` / `DEF-NNN` rows, and the port story. They should not need to re-read the global inventories except as reference.

In short: modernization changes how intent is recovered and how parity is proved. It does not remove the artifact trail from purpose to shipped evidence.

---

## Compatibility Aliases

These commands remain as aliases so existing installs do not fail silently. They do not write the old artifacts.

| Old command | Runs |
|---|---|
| `/map-legacy` | `/inventory-paths` |
| `/mine-history` | folded into `/inventory-paths` (status) and `/trace-path` (citations) |
| `/catalog-behavior` | `/trace-path` |
| `/trace-flow` | `/trace-path` |
| `/analyze-translation-gap` | `/analyze-impedance` |

`BEH-NNN` from earlier iterations is superseded by `XP-NNN`. `GAP-NNN` is superseded by `IMP-NNN`.

---

## Read Next

- [PROCESS.md](PROCESS.md) — the standard story lifecycle and nine human gates.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — agents, commands, templates, artifacts, evidence, and gates.
- [ROLES.md](ROLES.md) — what each agent owns and how work hands off.
- [TRACEABILITY.md](TRACEABILITY.md) — how recovered legacy evidence links forward to story evidence.
- [SETUP.md](SETUP.md) — how to install the workflow assets.
