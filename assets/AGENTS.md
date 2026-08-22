# House Rules for All Agents

These are the standing rules every agent in this workspace must follow. They are inherited by `architect`, `implementer`, `qa`, `docs-pm`, `auditor`, `archaeologist`, `migration-strategist`, and any configured role, and they apply across all projects unless a project-level `AGENTS.md` overrides a specific rule.

When an agent prompt repeats one of these rules in its own file, this file is the source of truth — agent prompts should reference this file rather than restate it.

## 0. Workflow profile

Before applying any workflow path, status vocabulary, command sequence, review gate, naming pattern, or stack default, read the workflow profile. Resolution order is:

1. Target project `.cursor/workflow.config.yml`
2. User profile `~/.cursor/workflow.config.yml`
3. The documented defaults in `~/.cursor/workflow.config.yml`

Project-local values override user-profile values key-by-key. If no profile is available, use the defaults documented in the user profile. Treat `AGENTS.md` as policy and the workflow profile as configuration.

---

## 0b. Command-agent binding

Slash commands are workflow entrypoints; configured agent files are binding role contracts. Before executing any command that directs a named role (architect, modeler, implementer, auditor, QA, docs-pm, or another configured role), agents must:

1. Resolve the active workflow profile using the profile precedence rules.
2. Read the command spec from the configured commands directory.
3. Read this house-rules file from the configured `cursor.rulesFile`.
4. Read the role's configured agent definition from the active profile's `agents` mapping.
5. Treat the loaded agent definition as mandatory role context for the command. If the command and agent definition conflict, stop and report the conflict instead of silently choosing one.

Orchestrator commands must prefer delegating each role phase to the configured subagent when the runtime supports delegation. If delegation is unavailable, the current chat may execute the phase only after loading the same configured agent definition and stating that fallback was used.

---

## 1. Source-of-truth discipline

- **Do not invent requirements.** Every design decision must trace to a requirement file the user provided. Unspecified items are marked `TBD` or returned to the user as questions — never silently filled in.
- **Purpose is canonical for intent.** The configured purpose document (default `docs/PURPOSE.md`) states what the product fundamentally is, the job it exists to do, the north-star outcome, and the trade-off rule. Requirements, design, stories, and code must serve that purpose. If a requested change contradicts the thesis or anti-thesis, stop and surface the tension.
- **Domain model is canonical for language and data meaning.** The configured domain model (default `docs/DOMAIN.md`) owns the ubiquitous language, data dictionary, core entities, relationships, invariants, lifecycles, and consistency boundaries. Do not introduce new runtime domain terms, fields, or entity meanings without updating or explicitly deferring the domain model.
- **Stop and ask on conflict.** If the configured design doc (default `README.md`), requirements files (default `docs/requirements/`), and ADRs (default `docs/decisions/`) disagree on a binding constraint (persistence, transport, named dependencies, auth boundary, integration model), stop work and emit a **Tensions / conflicts** list. Do not pick the easier path.
- **No silent domain drift.** If code, tests, or story language use a synonym for a domain term, change the local wording to the configured term or stop and ask whether the domain model should add an alias. If code needs a new invariant, state transition, or relationship, record it in the domain model before treating it as implementation-ready.
- **No silent substitution.** An agent may not change persistence location, transport, embedding/vector stack, or a named dependency versus the story or its linked ADRs. If the spec is wrong or impossible, stop and output a **Conflict report** citing the doc sections.
- **Workflow source paths.** Agents, commands, templates, and rules live at the paths configured in the workflow profile (defaults: `~/.cursor/agents`, `~/.cursor/commands`, `~/.cursor/templates`, and `~/.cursor/AGENTS.md`). Paths listed under `cursor.excludedWorkflowSources` (default `~/.codex`) belong to other applications and must not be treated as Cursor workflow source material.

## 1b. Change routing and friction budget

Before implementing a requested change, classify it and choose the lightest workflow lane that preserves traceability:

- **`full-story`** — new capability, broad refactor, persistence/auth/API change, adapter/port change, named dependency change, or any work that changes a binding constraint. Use the full `/refine-feature` → `/design-application` or `/plan-project` → `/plan-story` → `/complete-story` lane.
- **`story-followup`** — small behavior fix, debugging result, UI polish, copy adjustment, or local refinement tied to a completed story and not changing its binding constraints. Use `/patch-story {STORY-ID}` and append an entry to that story's Post-complete Follow-up Ledger (including `Change ref` and `Review ref` when applicable).
- **`hotfix-diff`** — unplanned bug fix or branch diff that does not map cleanly to one story. Use `/review-diff` and write the review artifact under the configured reviews directory (default `docs/reviews/`).
- **`docs-only`** — documentation-only updates. Update the relevant docs and record the verification note; use `/review-diff` when the docs affect setup, API contracts, or operational behavior.
- **`modernization-port`** — brownfield modernization, language/framework port, or replacement of a legacy application. Use `/assess-modernization` before design, then `/plan-migration` → `/document-legacy` (scoped to the next slice's `XP-NNN` IDs) → `/refine-feature` or `/recover-domain` → `/plan-path-tests` → `/design-application` or `/plan-project` → `/plan-port-story` → `/complete-port-story`. Do not skip the assessment unless the user explicitly accepts the unknown feasibility risk. Do not catalog the entire legacy system before the first slice.
- **`trivial-code`** — non-behavioral typo, formatting, comment, or mechanical cleanup. Keep verification minimal and use `/review-diff` only when risk is unclear.

When a completed story needs follow-up work, do not silently reopen or rewrite its original acceptance criteria. Preserve the configured complete story status (default `Complete`) as "the planned criteria passed" and record later work in the follow-up ledger unless the change invalidates the original criteria or changes a binding constraint. If it does, stop and route to `full-story` or emit a conflict report.

## 1c. Brownfield and modernization discipline

When working on a brownfield modernization or language/framework port, the legacy application is evidence, not automatically the requirement. User-facing documentation, release notes, executable behavior, source code, and commit history can disagree; agents must surface those tensions instead of flattening them.

- **Evidence grades are mandatory and singular.** Every recovered claim must carry exactly one configured evidence grade (defaults: `E1 verified`, `E2 documented`, `E3 code-derived`, `E4 inferred`, `E5 unknown`) plus a citation. The grade is the weakest grade that applies to the actionable part of the claim. Compound grades (`E1 / E3`) are invalid; split the row.
- **Analysis snapshots are immutable.** Execution path inventory, dependency inventory, dependency graph, impedance analysis, and path details describe what is. After `Status: Snapshot`, only the owning agent may append `## Errata` or produce `vN+1`. Other agents must not edit them. Later decisions go in the decision register, defect ledger, migration plan, or story spec, citing the analysis ID.
- **One owner, one writer.** An agent may not write artifacts it does not own. Cross-references cite IDs; they do not duplicate state.
- **Slice prerequisites gate delivery.** Global inventories inform sequencing. They do not gate a slice. Each slice and port story carries a short prerequisite table of the `DEP-NNN`, `DEC-NNN`, and `DEF-NNN` IDs that bind it. Check off resolved prerequisites there.
- **`undecided` is not `no-route`.** Dependency dispositions are `available`, `reimplementable`, `undecided`, or `no-route`. Do not write `blocked`. Owner-pending questions and dead ends must not look identical.
- **Provenance blocks readiness for the bound scope.** A port story is not implementation-ready when any covered claim remains `E4` or `E5` unless a `DEC-NNN` accepts or resolves the uncertainty. Unresolved claims on other slices do not block this one.
- **Oracle tier honesty.** Classify the legacy oracle before planning parity work. `T1 executable` supports repeated legacy-vs-new comparison, `T2 recorded` supports a frozen fixture corpus, and `T3 documented-only` means parity is not independently provable. Do not claim parity confidence above the oracle tier.
- **Comparison is per path.** Binding numeric, text, and semantic rules live in the path test plan. A workflow-profile hint is not a gate. Do not file a system-wide tolerance defect.
- **Defects are path-scoped.** Every `DEF-NNN` names one or more `XP-NNN` IDs. Refuse a defect that asks a system-wide question the methodology says has no system-wide answer.
- **No silent behavior improvement.** If the legacy behavior appears wrong, record it in the configured defect ledger and choose `reproduce-faithfully`, `fix-now`, or `fix-later`. Do not "clean up" behavior during the port without a recorded decision and test expectation.
- **Parity-first is the red-first specialization.** For port stories, characterization/parity tests are the first failing tests. Phase P criteria must cite oracle fixtures, the path's comparison rule, and defect-ledger decisions before implementation changes are made.
- **Assessment and migration plan are binding once accepted.** The configured modernization assessment and migration plan govern staging strategy, target stack assumptions, structure-fidelity choices, cutover approach, and risk mitigations. If implementation discovers evidence that contradicts them, stop and record a `DEC-NNN` plus any needed plan/assessment update before continuing. Do not "fix" the contradiction by editing an analysis snapshot.
- **Templates omit non-applicable sections.** Do not fill seeded language-family, hosting, or API/UI sections with "not applicable" rows. Reserve and retired items belong in an appendix.
- **Every modernization document opens with one paragraph** covering what it is, the key findings, and where to look next.
- **README hub.** On the modernization-port lane, the configured design doc (default `README.md`) carries a `## Modernization` section: what this repo is, lane status, and an artifact index of links. `/assess-modernization` creates that file from the README template if it does not exist. Each later command updates **only the Artifact index row it owns**, except `/assess-modernization`, `/record-decision`, and `/plan-migration`, which also update **What this is** / **Lane status**. Do not copy analysis tables into the hub. Do not edit another agent's index row or any Architect design section from a discovery command.

## 2. Hexagonal port/adapter pairing

- For every **port** (interface that defines an integration boundary) there must be at least one **contract test** that any adapter for that port can be run against.
- For every **adapter** (concrete implementation of a port) there must be at least one **integration test** that exercises the adapter against the **real backing service or fixture** — not a mock of the boundary the adapter itself owns.
- Story plans that introduce or modify a port or adapter must list both kinds of tests in the story's Test Plan and include a `(binding)` Phase Y criterion that cites the integration test file.

## 3. Test-first by default (red-first rule)

- For each acceptance criterion (`A1`, `B2`, etc.), the implementer commits or runs the failing test **before** writing the production code that makes it pass.
- The end-of-session summary must list, per AC, the failing test path/name and the diff that turned it green.
- **Explicit one-line exception:** the implementer may skip red-first for a specific AC by writing a one-line justification in the End-of-Session Summary (examples: `pure rename`, `type-only change`, `formatting only`, `dependency bump with no behavior change`). Every other AC follows the strict rule. Vague exceptions like "trivial" are not acceptable.

## 4. Coding standards

- **No `any` types.** When `stack.typePolicy.disallowAny` is true in the workflow profile, use the type contracts from the story document and the project's shared types module.
- **Type-aware imports.** Where the project defines a path alias for shared types (default example: `@shared/types`), use it instead of relative paths.
- Prefer boring, maintainable solutions. Define interfaces before implementations.

## 5. Logging and supportability

Code runs in high-availability environments and must be supportable from logs alone.

- **Use the project's logger.** If the README or existing code specifies a logger (Pino, Winston, structlog, slog, etc.) or middleware (request-ID generation), use it. If no logger is established, introduce a minimal structured (JSON) logger with level support so logging is consistent from the start.
- **What to log:**
  - Entry/exit of significant operations (API handlers, service methods, background jobs, anything that can fail or takes noticeable time).
  - **Every** error path. `catch` blocks and error branches must log before rethrowing or returning. Include error message, stack trace where available, and relevant context (request ID, entity ID, operation name).
  - Key state transitions (circuit breaker open/close, queue paused, config reloaded, connection pool exhausted) with enough context to correlate with timestamps.
- **Correlation.** Include request/correlation/trace IDs in every log payload when the project uses them.
- **Log levels.** `debug` for detailed development flow; `info` for normal operation completion and startup/shutdown; `warn` for degraded or recoverable conditions; `error` for failures requiring attention.
- **No sensitive data.** Never log passwords, tokens, PII, or full request/response bodies unless the project explicitly documents it as acceptable.

## 6. Story status discipline

The story document at the configured story glob (default `docs/features/{STORY-ID}-*.md`) is the single source of truth for story progress.

- The header `**Status**:` field moves through the configured story statuses (defaults: `Open` → `In Progress` → `Complete`).
- Acceptance criteria boxes (`- [ ]` → `- [x]`) are checked **immediately** after the criterion is verified to pass — not batched at the end.
- If work stops mid-story, leave the configured active status (default `In Progress`). Unchecked boxes show exactly where the next session resumes.
- Docs-PM derives backlog status from the story document; never edit the configured design doc backlog row's status without first updating the story.

## 7. Communication style

- Be concise and evidence-driven. Prefer bullets, tables, and short paragraphs.
- Cite specific file paths and line ranges when reporting findings or changes.
- When stopping for input, say exactly what is blocking and what input is needed.
