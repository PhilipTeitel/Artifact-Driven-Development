# Traceability

Traceability is the ability to answer, for any line of shipped code: *why does this exist, who decided it should look like this, and how do we know it works?*

This methodology achieves traceability by chaining artifacts. Each artifact has a defined predecessor and a defined successor. Purpose and domain model carry the conceptual center; the story spec is the central hub where intent, meaning, decisions, and design meet implementation, review, QA, documentation, and completion metadata.

---

## The traceability model

```mermaid
flowchart LR
    purpose["Purpose<br/>thesis, job,<br/>trade-off rule"]
    domain["Domain Model<br/>language, data dictionary,<br/>invariants"]
    requirements["Requirements<br/>requirements<br/>Scenarios S1, S2, S3"]
    adr["architecture decision records<br/>Binding decisions"]
    design["Design notes<br/>Architecture and<br/>operating context"]
    skeleton["Walking Skeleton<br/>running proof and<br/>reflection deltas"]
    backlog["Backlog<br/>Epics and stories"]
    story["Story Spec<br/>Acceptance criteria<br/>Test plan<br/>File touchpoints"]
    tests["Tests<br/>Unit / contract / integration"]
    code["Code<br/>Changed files"]
    review["Review Artifact<br/>Pass or Block"]
    qa["QA Evidence Matrix<br/>PASS / FAIL / BLOCKED"]
    docs["Docs Update<br/>README / API / Runbook"]
    metadata["Completion Metadata<br/>+ Follow-up Ledger"]

    purpose --> requirements
    purpose --> domain
    purpose --> design
    domain --> design
    requirements --> domain
    requirements --> story
    domain --> story
    adr --> story
    design --> story
    design --> skeleton
    domain --> skeleton
    purpose --> skeleton
    skeleton --> backlog
    backlog --> story
    story --> tests
    story --> code
    purpose --> review
    domain --> review
    story --> review
    story --> qa
    tests --> qa
    code --> qa
    review --> metadata
    qa --> metadata
    story --> docs
    docs --> metadata
```

Every arrow into the story spec is a piece of context the implementer is allowed to rely on. Every arrow into the review artifact is a rubric the auditor uses to judge whether the changed surface remains faithful to the model. Every arrow out is evidence that the intent was delivered. Completion metadata closes the loop by recording the review summary, QA result, documentation diff, and any follow-up ledger entries in one place.

Each box in the diagram is a distinct artifact — defined by what it carries, not by where it is recorded. The current implementation bundles related artifacts into a small number of files for trace co-location: the story spec, story acceptance evidence, QA evidence matrix, completion metadata, and post-complete follow-up ledger entries all ride in the same `docs/features/{STORY-ID}-*.md` document because keeping the trace co-located makes it readable. They are still separate artifacts with separate owners. See [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) for the artifact set and the composition matrix.

Modernization adds provenance to the left side of the trace. Recovered behavior becomes an ordinary `REQ-NNN`. A story should be traceable not only back to purpose, domain, requirements, and ADRs, but also — through that REQ's section 4b — back to the execution-path citation, `DEC-NNN`, `DEF-NNN`, evidence grade, and oracle fixture that justified the recovered behavior.

```mermaid
flowchart LR
    legacySources["Legacy sources<br/>docs, code, history,<br/>observed behavior"]
    pathInv["Execution Path Inventory"]
    depInv["Dependency Inventory"]
    depGraph["Dependency Graph"]
    impedance["Impedance Analysis"]
    pathDetail["Path Detail<br/>XP-NNN"]
    defectLedger["Defect Ledger<br/>DEF-NNN"]
    decReg["Decision Register<br/>DEC-NNN"]
    oracle["Oracle<br/>T1, T2, or T3"]
    recoveredPurpose["Recovered Purpose"]
    recoveredDomain["Recovered Domain"]
    requirements["Requirements<br/>REQ-NNN and Sn<br/>section 4b provenance"]
    adr["ADRs"]
    migrationPlan["Migration Plan"]
    story["Story spec"]
    qaEvidence["QA Evidence Matrix<br/>including parity rows"]
    docsUpdate["Documentation Update"]

    legacySources --> pathInv
    legacySources --> depInv
    pathInv --> depGraph
    depInv --> depGraph
    pathInv --> impedance
    depInv --> impedance
    pathInv --> pathDetail
    pathDetail --> defectLedger
    pathDetail --> recoveredPurpose
    pathDetail --> recoveredDomain
    recoveredPurpose --> requirements
    recoveredDomain --> requirements
    pathDetail --> requirements
    defectLedger --> requirements
    decReg --> requirements
    oracle --> requirements
    pathInv --> migrationPlan
    depGraph --> migrationPlan
    decReg --> migrationPlan
    requirements --> adr
    requirements --> story
    adr --> story
    migrationPlan --> story
    story --> qaEvidence
    qaEvidence --> docsUpdate
```

This is why evidence grades matter. A citation marked `E1 verified` and a claim marked `E4 inferred` are not interchangeable, even if both appear in a polished artifact. Each claim carries exactly one grade. Global inventories inform; the REQ provenance table and the story's slice prerequisite table are what gate implementation.

---

## The story spec as traceability hub

The story spec is the central handoff artifact for a reason: it is the only place where purpose, domain model, requirements, architecture decision records, design, acceptance criteria, tests, file touchpoints, and completion evidence all meet.

A well-formed story should make every one of these questions answerable without leaving the story document:

- **Which purpose does this serve?** Linked configured purpose artifact (`docs/PURPOSE.md` by default), including the thesis, trade-off rule, and anti-thesis relevant to the story.
- **Which domain model does this preserve?** Section 1a names the domain terms, entities, data dictionary fields, invariants, lifecycles, and consistency boundaries the story touches from the configured domain model (`docs/DOMAIN.md` by default).
- **Which requirement or scenario caused this work?** Linked requirements (`REQ-NNN-*.md`) and the specific scenario IDs (`S1`, `S2`...). Every Gherkin `Sn` ID the story implements must appear in the Test Plan's **Covers Sn** column of at least one row, or the story must state explicitly why a given `Sn` is out of scope.
- **Which architecture decision records or design constraints bind the implementation?** Linked architecture decision records and named binding constraints (Section 4), each mapped to a Phase Y `(binding)` criterion ID.
- **Which ports and adapters are in play?** Section 4b lists every port and adapter the story creates or modifies — port file, adapter implementation, and real backing service or fixture — or states explicitly that no integration boundaries are touched.
- **Which acceptance criteria define completion?** The criteria list, each with a stable ID (`A1`, `A2`..., `Y1`, `Z1`...) using markdown task syntax (`- [ ] **A1** — ...`) and exactly one `Evidence:` line per criterion.
- **Which tests or checks prove each criterion?** Section 8a Test Plan rows mapping criteria to test paths, with test level (`unit`, `contract`, `integration`, `parity`, `e2e` / `ui`) and **Covers AC** / **Covers Sn** columns filled. Every port needs at least one `contract` row; every adapter needs at least one `integration` row against the real backing service (no mock of the boundary the adapter owns). Phase Y `(binding)` criteria cite the integration tests for adapters.
- **Which recovered legacy path does this story implement?** When the linked REQ has section 4b, story section 1b copies `XP-NNN`, evidence grade, `DEC-NNN`, `DEF-NNN`, comparison rule, and oracle source. Slice prerequisites (`DEP-NNN`, `DEC-NNN`, `DEF-NNN`) come from the migration-plan row for those paths. REQ is canonical.
- **How is parity proved?** `parity` test rows in Section 8a, verified by `/qa-story` in the ordinary evidence matrix, using the REQ comparison rule. A `T3 documented-only` oracle must not be described as executable parity. A missing per-path comparison rule is not filled by a global default.
- **Which files changed?** The file touchpoints (planned) and the changed files (actual).
- **Which gates passed?** The review artifact reference (including Phase Z6: zero `high` or `critical` `TEST-#`, `SEC-#`, `REL-#`, or `API-#` findings from `/review-story`, and Phase Z7: zero `high` or `critical` `MODEL-#` findings) and the QA matrix reference.
- **Which documentation surfaces were updated?** The documentation diff, or an explicit note that no surface needed to change.
- **What follow-up work happened after completion?** Post-complete Follow-up Ledger rows with `Change ref` (commit SHA, PR URL, or `uncommitted` / `TBD`) and `Review ref` (`none` or a path under `docs/reviews/` when `/review-diff` produced an artifact).

If any of these is missing, the trace is incomplete. The story is not done.

`/validate-story` checks this contract mechanically. Use `ready` before implementation, `complete` after shipping, and `followups` after `/patch-story` or `/reconcile-story` appends ledger rows.

---

## The principles, anchored

The README's closing principles are not slogans. Each one names a specific artifact that enforces it.

| Principle | Enforced by |
|---|---|
| Purpose defines the center | `docs/PURPOSE.md`, with the product thesis, job, north-star outcome, trade-off rule, anti-thesis, and success signals |
| Domain model defines meaning | `docs/DOMAIN.md`, with ubiquitous language, data dictionary fields, entities, relationships, invariants, lifecycles, and consistency boundaries |
| Requirements define behavior | refined requirements in `docs/requirements/REQ-NNN-*.md`, with Gherkin scenarios that become trace points downstream |
| architecture decision records preserve binding technical decisions | architecture decision records in `docs/decisions/`, linked from the story spec, that prevent silent substitution of persistence, transport, auth, or named dependencies |
| Design notes describe architecture and operating context | The design section of the project `README`, updated by `/design-application` |
| Walking skeletons expose tacit intent | `docs/features/SK-1-*.md` (or configured skeleton story), implemented and demoed before feature backlog planning; reflection deltas route back to `/refine-feature` or `/model-domain` |
| Epics and stories organize delivery | The backlog rows in the project `README`, maintained by `/plan-project` |
| Story specs turn intent into implementation-ready instructions | `docs/features/{STORY-ID}-*.md`, produced by `/plan-story`; validated by `/validate-story ready` |
| Tests, model-fidelity review, QA evidence, and documentation close the loop | The test plan (with **Covers AC** and **Covers Sn**), story-review artifact including `MODEL-#` counts, QA matrix, and documentation diff — all referenced from the story's completion metadata; post-complete follow-ups recorded in the ledger with **Change ref** and **Review ref** |
| Legacy behavior is evidence, not automatically requirement | `docs/modernization/paths/XP-NNN-*.md`, path inventory, and defect ledger, each with singular evidence grades and citations |
| Parity confidence cannot exceed the oracle tier | `docs/modernization/oracle.md`, REQ section 4b, story `parity` test rows, and the QA evidence matrix |

A principle without an artifact is a hope. Anchoring each one to a specific file is what turns the methodology from intent into discipline.

---

## How the trace stays intact

Four rules keep the trace from quietly breaking.

### Single source of truth per concern

Each concern has exactly one canonical file. Purpose lives in `docs/PURPOSE.md`. Domain language and data meaning live in `docs/DOMAIN.md`. Requirements live in `docs/requirements/`. Decisions live in architecture decision records and, for porting choices, the decision register. Design lives in the `README` design section. Story scope lives in the story document. Path facts live in the path detail. Dependency dispositions live in the dependency inventory until a `DEC-NNN` supersedes them for planning. Comparison rules for recovered paths live on the covering REQ. Documentation lives in the surfaces it describes. The README `## Modernization` section is a **navigation hub**, not a second copy of those files: if a hub row disagrees with the linked artifact, the artifact wins (fix the row unless you own a still-Draft file). If two canonical files appear to disagree, work stops and a conflict is surfaced — the workflow does not pick the easier path, and it does not rewrite the analysis snapshot to hide the disagreement.

### No silent model drift

An agent may not introduce new runtime domain terms, fields, entity meanings, invariants, lifecycle states, or consistency boundaries without updating or explicitly deferring the configured domain model. The Auditor enforces this with `MODEL-#` findings during `/review-story`.

### No silent substitution

An agent may not change a persistence location, transport, embedding stack, or named dependency versus what the story or its linked architecture decision records specify. If the spec is wrong or impossible, the agent stops and emits a conflict report citing the affected sections.

This rule exists because the most common failure mode in AI-assisted development is the model "improving" a binding decision without telling anyone.

### No silent behavior improvement

In modernization work, an agent may not decide that legacy behavior should be cleaned up during the port. If behavior appears wrong, the defect ledger records the human decision: `reproduce-faithfully`, `fix-now`, or `fix-later`. The auditor and QA enforce this with `PAR-#` and `PROV-#` findings and `parity` test rows.

### Story status discipline

The story document is the single source of truth for story progress. Status transitions and acceptance criteria checkboxes are updated *as work happens*, not batched at the end. The backlog status is derived from the story document, never the other way around.

This keeps the trace navigable from either direction: from a shipped feature back to the intent that caused it, or from a requirement forward to the evidence that satisfied it.

### Post-complete follow-up trace

After a story is `Complete`, small verified changes do not reopen the story. They append rows to the Post-complete Follow-up Ledger with **Change ref** pointing at version control (commit SHA or PR URL) and **Review ref** pointing at a `/review-diff` artifact when one was produced. `/validate-story followups` confirms ledger rows are structurally consistent. `/reconcile-story` uses the same ledger when reconciling working-tree drift that was never recorded.

---

## Read next

- [PROCESS.md](PROCESS.md) — when in the lifecycle each artifact is produced.
- [MODERNIZATION.md](MODERNIZATION.md) — how legacy evidence, oracle tiers, defect decisions, and REQ provenance extend the trace.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — the composition matrix that names the agent, command, and template behind each artifact.
- [POST-STORY.md](POST-STORY.md) — how the trace is preserved for follow-ups, patches, and diffs without forcing every change through a full story.
