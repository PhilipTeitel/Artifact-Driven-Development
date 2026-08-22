# Roles

Each agent owns a specific kind of judgment. Roles exist so that no single agent is asked to refine requirements, write code, audit risk, verify acceptance, and update documentation in one breath. Separating concerns is what keeps context clean at each step.

This document describes what each agent does, what it does *not* do, and how work hands off to the next role.

---

## Modeler

The modeler operates before technical design and returns whenever new domain meaning appears. Its job is to make purpose and conceptual meaning explicit enough for the rest of the workflow to judge fidelity.

- **Owns.** Purpose and domain model / data dictionary artifacts. On a modernization repo, the README Artifact index rows for Purpose and Domain model.
- **Primary inputs.** Raw ideas, transcripts, product notes, approved refined requirements, resolved user answers, or recovered legacy behavior and intent artifacts.
- **Primary outputs.** `docs/PURPOSE.md` and `docs/DOMAIN.md`.
- **Commands.** `/define-purpose`, `/model-domain`, `/recover-domain`.
- **Does not.** Design architecture, write code, write story acceptance criteria, or review implementation. It names the product center and domain meaning; other agents use those artifacts.
- **Hands off to.** Architect, once purpose and domain model are approved.

When the modeler finds a missing lifecycle, invariant, data field meaning, or consistency boundary, it records an open modeling question instead of guessing. Those questions block affected design or story work.

In modernization work, the modeler can run in legacy recovery mode. It builds or updates purpose and domain artifacts from evidence-graded execution path details, user documentation, release notes, and the path inventory. It treats legacy implementation names as candidate terms, not domain truth.

---

## Archaeologist

The archaeologist operates at the front of a brownfield modernization. Its job is to recover what can be known from the legacy application without turning weak evidence into requirements.

- **Owns.** Execution path inventory, dependency graph, execution path details, and defect ledger (records; the human decides).
- **Primary inputs.** Legacy repositories, user documentation, release notes, changelogs, commit history, support notes, screenshots, observed runs, and oracle outputs.
- **Primary outputs.** `docs/modernization/execution-path-inventory.md`, `docs/modernization/dependency-graph.md`, `docs/modernization/paths/XP-NNN-*.md`, and `docs/modernization/defect-ledger.md`.
- **Commands.** `/inventory-paths`, `/map-dependency-graph`, `/trace-path`, `/ledger-defects`, `/document-legacy`.
- **Does not.** Choose the target architecture, staging strategy, target framework, implementation approach, or whether a suspicious legacy behavior should be fixed. Does not write the dependency inventory, impedance analysis, decision register, migration plan, or path test plans. Does not edit snapshot cells to record later decisions — appends Errata or produces `vN+1` when a fact was wrong. Does not edit README Lane status or other agents' Artifact index rows.
- **Hands off to.** Migration Strategist for feasibility and planning, Modeler for recovered purpose/domain work, Architect for requirements, path test plans, and port-story planning.

Every recovered claim needs exactly one evidence grade and a citation. `E4 inferred` and `E5 unknown` facts remain blockers for the scope they bind until resolved or explicitly accepted. Path details are slice-scoped: do not catalog the whole system before the first slice.

---

## Migration Strategist

The migration strategist operates before target implementation planning. Its job is to decide whether the migration is feasible, what conditions must be true for a given slice, and how the work should be staged.

- **Owns.** Modernization assessment, dependency inventory, impedance analysis, decision register (records; the human decides), migration plan, ADR triggers for target-stack decisions, and the README hub cells **What this is** and **Lane status**. `/assess-modernization` creates the README hub when the file is missing.
- **Primary inputs.** Path inventory, dependency graph, path details when present, oracle classification, recovered purpose/domain/requirements, defect ledger, target-stack notes, and project constraints.
- **Primary outputs.** `docs/modernization/ASSESSMENT.md`, `docs/modernization/dependency-inventory.md`, `docs/modernization/impedance-analysis.md`, `docs/modernization/decision-register.md`, `docs/modernization/migration-plan.md`, and recommended ADRs.
- **Commands.** `/inventory-dependencies`, `/analyze-impedance`, `/assess-modernization`, `/record-decision`, `/plan-migration`.
- **Does not.** Recover raw behavior facts from code, write implementation code, write path test plans, take over Architect-owned ADR files, or soften unresolved feasibility risks. Does not edit Archaeologist snapshots. Does not use `blocked` as a dependency disposition — `undecided` and `no-route` are distinct. Does not gate a slice on global unresolved counts.
- **Hands off to.** Human decision gates for assessment and migration-plan approval, then Architect for design, path test plans, and port-story planning.

The migration strategist never promises parity above the oracle tier. A `T3 documented-only` oracle can support documented expectations, not independently provable legacy-vs-new comparison. Comparison rules are per path; they are not a global assessment gate.

---

## Architect

The architect operates before implementation begins. Its job is to turn ambiguity into something an implementer can act on without guessing.

- **Owns.** Refined requirements, application design, architecture decision records, walking-skeleton story, backlog, story specs, port-story specs, path test plans, and the README Artifact index rows **Path test plans** and **Port stories**. Preserves an existing `## Modernization` section when adding design.
- **Primary inputs.** Approved purpose, approved domain model, raw notes, tickets, transcripts, prior requirements, prior architecture decision records, the project's existing design, and for modernization work the migration plan, path details, path test plans, oracle doc, defect ledger, decision register, and impedance analysis.
- **Primary outputs.** requirements, design sections in the README, new architecture decision records, walking-skeleton story, backlog rows, `docs/modernization/test-plans/XP-NNN-tests.md`, and `docs/features/{STORY-ID}-*.md` story or port-story specs.
- **Commands.** `/refine-feature`, `/design-application`, `/plan-skeleton`, `/plan-project`, `/plan-story`, `/plan-path-tests`, `/plan-port-story`, `/validate-story ready`.
- **Does not.** Implement code. Make a binding technical decision without writing it down as an architecture decision record. Re-open completed stories to retrofit new scope. Edit Archaeologist or Migration Strategist analysis snapshots.
- **Hands off to.** Implementer, once a story spec is approved and validated as ready.

When the architect uncovers a decision that will bind future work — persistence, transport, auth, embedding stack, named dependencies, integration model — it captures that decision in an architecture decision record before any downstream step can depend on it.

---

## Implementer

The implementer operates against an approved story spec. Its job is to turn that spec into working, tested code without renegotiating the spec.

- **Owns.** Code changes, tests, the story document's status and criteria checkboxes, and the README Artifact index row **Oracle** when running `/build-oracle`.
- **Primary inputs.** The approved story spec and its linked architecture decision records, plus the existing code. For port stories, also the path test plan, oracle doc, parity plan, defect ledger, and accepted legacy evidence.
- **Primary outputs.** Production code, tests, and an updated story document. Status moves `Open` → `In Progress` → `Complete`; acceptance criteria boxes move `[ ]` → `[x]` as each one passes.
- **Commands.** `/implement-story`, `/fix-from-qa`, `/patch-story` (including `/validate-story followups` after ledger append), `/build-oracle`.
- **Does not.** Reinterpret requirements. Substitute named dependencies, persistence choices, or transport. Silently change the design. Mark the story complete with unchecked criteria.
- **Hands off to.** Auditor (via `/review-story`) once all criteria are checked.

The implementer uses red-first tests by default for each acceptance criterion. Exceptions are explicit, one-line, and noted in the end-of-session summary; "trivial" is not an acceptable exception.

For port stories, parity-first is the red-first specialization. Phase P criteria and characterization tests come first, and they cite oracle fixtures, the path test plan's comparison rule, and defect-ledger decisions before implementation changes are made.

If implementation reveals that the plan is wrong, the implementer escalates back to architect rather than hiding the change in code.

---

## Auditor

The auditor provides the review gates. Its job is to look at the changed surface — not the original story — and find the classes of mistake that QA does not.

- **Owns.** Story review artifacts, diff review artifacts, repository map, and audit findings.
- **Primary inputs.** The story document, configured purpose/domain artifacts, and the changed files; or a git diff range; or the full repository for a periodic audit. For port stories, also the path details, path test plans, oracle doc, defect ledger, and parity plan.
- **Primary outputs.** `docs/features/{STORY-ID}-review.md` with a machine-readable `REVIEW SUMMARY:` line and a `Pass` or `Block` result; or `docs/reviews/*.md`; or `audit-findings.md`.
- **Commands.** `/review-story`, `/review-diff`, `/reconcile-story`, `/map-repo`, `/audit-all`, `/triage-audit-findings`, and the seven category audits.
- **Does not.** Verify acceptance criteria — that is QA's job. Re-design the work — that is the architect's job. Fix the code — that is the implementer's job. The auditor identifies; others repair.
- **Hands off to.** Implementer (on `Block`) or QA (on `Pass`) for per-story review; back to architect or implementer for audit findings.

Per-story review focuses on the changed surface for reliability, security, API contract, test coverage, and model-fidelity issues. Port-story review also reports parity and provenance issues as `PAR-#` and `PROV-#` findings. Full-repo audits are periodic health checks, not part of normal story completion.

---

## QA

QA verifies that the story's acceptance criteria are actually satisfied by executable evidence.

- **Owns.** The criterion evidence matrix and, for port stories, the parity report plus the README Artifact index row **Parity reports**.
- **Primary inputs.** The story's acceptance criteria and the tests, changed files, and other evidence cited by the implementer. For port stories, also the Phase P criteria, parity plan, path test plans, oracle doc, path details, and defect ledger.
- **Primary outputs.** A matrix with `PASS`, `FAIL`, or `BLOCKED` for every criterion, each row citing the specific evidence that supports its result. For port stories, QA also produces the parity report.
- **Commands.** `/qa-story`, `/verify-parity`.
- **Does not.** Infer completion from code alone. Skip a criterion because the implementation "looks fine." Fix failed criteria — that is the implementer's job via `/fix-from-qa`. Edit path test plans or analysis snapshots. Edit README sections other than the Parity reports index row.
- **Hands off to.** Implementer (for any `FAIL` or `BLOCKED` row) or Documenter (when all rows are `PASS` and the human has accepted the evidence).

QA exists as a separate role from review because the two ask different questions. Review asks "is this code safe and sound?" QA asks "did this code do the thing the story said it would?" For a port story, QA also asks "does the new behavior match the accepted legacy expectation, within the oracle tier and the path test plan's comparison rule?"

---

## Documenter

The documenter keeps project documentation aligned with what actually shipped. Its job is to synchronize the surfaces a future reader will look at — not to expand on them.

- **Owns.** README updates for backlog Status and setup surfaces the story changed, API docs, OpenAPI specs, runbooks, setup instructions, environment docs, and completion metadata.
- **Does not.** Update unrelated documentation just because it is nearby. Edit the backlog status before the story document reflects the change. Add new behavioral claims that the story did not implement. Edit `## Modernization`, Lane status, or Artifact index rows.
- **Primary inputs.** The completed story, the accepted QA matrix, the follow-up ledger.
- **Primary outputs.** Documentation diffs, updated backlog status (derived from the story), and recorded completion metadata.
- **Commands.** `/document-story`, `/validate-story complete`.
- **Hands off to.** The human, for the final documentation approval gate.

The documenter is driven by the story source of truth. If a surface did not change, the documenter does not touch it.

---

## Who owns what

Ownership is recorded per **artifact** (the conceptual output), not per file. A single file may carry several artifacts — the story spec file, for example, carries the story spec, the implementer's acceptance evidence, the QA evidence matrix, completion metadata, and follow-up ledger entries — but each artifact has exactly one owner.

| Artifact | Owner |
|---|---|
| Purpose | Modeler |
| Domain model / data dictionary | Modeler |
| Refined requirements | Architect |
| Application design | Architect (Documenter syncs when stories change it) |
| architecture decision record | Architect |
| Walking skeleton story | Architect (planned); Implementer/Auditor/QA/Documenter for the normal tail |
| Backlog | Architect (created); Documenter (status derived from story specs) |
| Story spec | Architect |
| Code and tests | Implementer |
| Story acceptance evidence (status, criteria checkboxes) | Implementer |
| Story review | Auditor |
| QA evidence matrix | QA |
| Documentation updates | Documenter |
| Completion metadata | Documenter |
| Post-complete follow-up ledger entry | Implementer (via `/patch-story`); Auditor (via `/reconcile-story` when drift is reconciled in place) |
| Audit findings | Auditor |
| Modernization assessment | Migration Strategist |
| Execution path inventory | Archaeologist |
| Dependency inventory | Migration Strategist |
| Dependency graph | Archaeologist |
| Technology and impedance analysis | Migration Strategist |
| Oracle strategy | Implementer (tier, environment, harness); Migration Strategist consumes |
| Execution path detail | Archaeologist |
| Decision register | Migration Strategist (records); Human (decides) |
| Defect ledger | Archaeologist (records); Human (decides) |
| Migration plan | Migration Strategist |
| Path test plan | Architect |
| Port story spec | Architect |
| Parity report | QA |
| Modernization hub — What this is / Lane status | Migration Strategist |
| Modernization hub — Artifact index row | Owner of the linked artifact (see [README template](assets/templates/readme-template.md)) |

Single ownership per artifact is deliberate. Shared ownership has been observed to create context pollution — the architect adds an implementation detail, the implementer rewrites a requirement, and the trace from intent to evidence quietly breaks. Co-locating multiple artifacts in one file is a convenience for trace readability; it does not change the ownership boundary, which is the artifact itself.

---

## Read next

- [PROCESS.md](PROCESS.md) — how the roles hand off across the full lifecycle.
- [MODERNIZATION.md](MODERNIZATION.md) — how Archaeologist and Migration Strategist extend the workflow for brownfield ports.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — the composition matrix showing which agent + command + template produces each artifact.
- [POST-STORY.md](POST-STORY.md) — how roles change after a story is complete.
