# Roles

Each agent owns a specific kind of judgment. Roles exist so that no single agent is asked to refine requirements, write code, audit risk, verify acceptance, and update documentation in one breath. Separating concerns is what keeps context clean at each step.

This document describes what each agent does, what it does *not* do, and how work hands off to the next role.

---

## Architect

The architect operates before implementation begins. Its job is to turn ambiguity into something an implementer can act on without guessing.

- **Owns.** Refined requirements, application design, architecture decision records, backlog, and story specs.
- **Primary inputs.** Raw notes, tickets, transcripts, prior requirements, prior architecture decision records, the project's existing design.
- **Primary outputs.** requirements, design sections in the README, new architecture decision records, backlog rows, and `docs/features/{STORY-ID}-*.md` story specs.
- **Commands.** `/refine-feature`, `/design-application`, `/plan-project`, `/plan-story`, `/validate-story ready`.
- **Does not.** Implement code. Make a binding technical decision without writing it down as an architecture decision record. Re-open completed stories to retrofit new scope.
- **Hands off to.** Implementer, once a story spec is approved and validated as ready.

When the architect uncovers a decision that will bind future work — persistence, transport, auth, embedding stack, named dependencies, integration model — it captures that decision in an architecture decision record before any downstream step can depend on it.

---

## Implementer

The implementer operates against an approved story spec. Its job is to turn that spec into working, tested code without renegotiating the spec.

- **Owns.** Code changes, tests, and the story document's status and criteria checkboxes.
- **Primary inputs.** The approved story spec and its linked architecture decision records, plus the existing code.
- **Primary outputs.** Production code, tests, and an updated story document. Status moves `Open` → `In Progress` → `Complete`; acceptance criteria boxes move `[ ]` → `[x]` as each one passes.
- **Commands.** `/implement-story`, `/fix-from-qa`, `/patch-story` (including `/validate-story followups` after ledger append).
- **Does not.** Reinterpret requirements. Substitute named dependencies, persistence choices, or transport. Silently change the design. Mark the story complete with unchecked criteria.
- **Hands off to.** Auditor (via `/review-story`) once all criteria are checked.

The implementer uses red-first tests by default for each acceptance criterion. Exceptions are explicit, one-line, and noted in the end-of-session summary; "trivial" is not an acceptable exception.

If implementation reveals that the plan is wrong, the implementer escalates back to architect rather than hiding the change in code.

---

## Auditor

The auditor provides the review gates. Its job is to look at the changed surface — not the original story — and find the classes of mistake that QA does not.

- **Owns.** Story review artifacts, diff review artifacts, repository map, and audit findings.
- **Primary inputs.** The story document and the changed files; or a git diff range; or the full repository for a periodic audit.
- **Primary outputs.** `docs/features/{STORY-ID}-review.md` with a machine-readable `REVIEW SUMMARY:` line and a `Pass` or `Block` result; or `docs/reviews/*.md`; or `audit-findings.md`.
- **Commands.** `/review-story`, `/review-diff`, `/reconcile-story`, `/map-repo`, `/audit-all`, `/triage-audit-findings`, and the seven category audits.
- **Does not.** Verify acceptance criteria — that is QA's job. Re-design the work — that is the architect's job. Fix the code — that is the implementer's job. The auditor identifies; others repair.
- **Hands off to.** Implementer (on `Block`) or QA (on `Pass`) for per-story review; back to architect or implementer for audit findings.

Per-story review focuses on the changed surface for reliability, security, API contract, and test coverage issues. Full-repo audits are periodic health checks, not part of normal story completion.

---

## QA

QA verifies that the story's acceptance criteria are actually satisfied by executable evidence.

- **Owns.** The criterion evidence matrix.
- **Primary inputs.** The story's acceptance criteria and the tests, changed files, and other evidence cited by the implementer.
- **Primary outputs.** A matrix with `PASS`, `FAIL`, or `BLOCKED` for every criterion, each row citing the specific evidence that supports its result.
- **Commands.** `/qa-story`.
- **Does not.** Infer completion from code alone. Skip a criterion because the implementation "looks fine." Fix failed criteria — that is the implementer's job via `/fix-from-qa`.
- **Hands off to.** Implementer (for any `FAIL` or `BLOCKED` row) or Documenter (when all rows are `PASS` and the human has accepted the evidence).

QA exists as a separate role from review because the two ask different questions. Review asks "is this code safe and sound?" QA asks "did this code do the thing the story said it would?"

---

## Documenter

The documenter keeps project documentation aligned with what actually shipped. Its job is to synchronize the surfaces a future reader will look at — not to expand on them.

- **Owns.** README updates, API docs, OpenAPI specs, runbooks, setup instructions, environment docs, and completion metadata.
- **Primary inputs.** The completed story, the accepted QA matrix, the follow-up ledger.
- **Primary outputs.** Documentation diffs, updated backlog status (derived from the story), and recorded completion metadata.
- **Commands.** `/document-story`, `/validate-story complete`.
- **Does not.** Update unrelated documentation just because it is nearby. Edit the backlog status before the story document reflects the change. Add new behavioral claims that the story did not implement.
- **Hands off to.** The human, for the final documentation approval gate.

The documenter is driven by the story source of truth. If a surface did not change, the documenter does not touch it.

---

## Who owns what

Ownership is recorded per **artifact** (the conceptual output), not per file. A single file may carry several artifacts — the story spec file, for example, carries the story spec, the implementer's acceptance evidence, the QA evidence matrix, completion metadata, and follow-up ledger entries — but each artifact has exactly one owner.

| Artifact | Owner |
|---|---|
| Refined requirements | Architect |
| Application design | Architect (Documenter syncs when stories change it) |
| architecture decision record | Architect |
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

Single ownership per artifact is deliberate. Shared ownership has been observed to create context pollution — the architect adds an implementation detail, the implementer rewrites a requirement, and the trace from intent to evidence quietly breaks. Co-locating multiple artifacts in one file is a convenience for trace readability; it does not change the ownership boundary, which is the artifact itself.

---

## Read next

- [PROCESS.md](PROCESS.md) — how the roles hand off across the full lifecycle.
- [BUILDING-BLOCKS.md](BUILDING-BLOCKS.md) — the composition matrix showing which agent + command + template produces each artifact.
- [POST-STORY.md](POST-STORY.md) — how roles change after a story is complete.
