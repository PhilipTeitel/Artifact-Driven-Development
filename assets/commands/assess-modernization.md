# assess-modernization

Orchestrates the feasibility assessment for a brownfield modernization or language/framework port. Before acting, resolve the workflow profile (target project `.cursor/workflow.config.yml`, then user `~/.cursor/workflow.config.yml`) and use its command directory, modernization paths, evidence grades, source stack, target stack, oracle tier, assessment statuses, and modernization assessment template. For each phase, read and follow the corresponding command spec under the configured command directory (defaults: `inventory-paths.md`, `inventory-dependencies.md`, `map-dependency-graph.md`, `analyze-impedance.md`, `build-oracle.md`) as the source of truth for steps and rules.

The assessment document is the five-minute picture. Inventories behind it are reference. Conditions must bind the first slice, not global unresolved counts.

## Command-Agent Binding And Delegation

Before executing the sequence, load the configured house rules, this command spec, and the active workflow profile. For each phase, read the phase command spec and its configured agent definition before acting:

| Phase command | Agent binding |
|---|---|
| `/inventory-paths` | `agents.archaeologist` |
| `/inventory-dependencies` | `agents.migrationStrategist` |
| `/map-dependency-graph` | `agents.archaeologist` |
| `/analyze-impedance` | `agents.migrationStrategist` |
| `/build-oracle probe` | `agents.implementer` |
| assessment synthesis | `agents.migrationStrategist` |

When subagent delegation is available, run each phase in the configured role subagent and pass the legacy repo path, target stack, active workflow profile, command spec, and loaded agent definition as binding context. If subagent delegation is unavailable, continue in the current chat only after loading the same agent definition and state in the output which phases used this fallback.

## Inputs

- Legacy repo path, unless configured in `modernization.legacyRepoPath`.
- Target language, version, and framework when known.
- Optional source documentation, release notes, issue exports, or support artifacts.
- Optional scope restriction.

## Preconditions

- The target repo is where artifacts will be written.
- The legacy repo is treated as read-only.
- The user accepts that assessment may end with `no-go`.

## README hub

`/assess-modernization` is the command that opens a modernization repo.

1. If the configured design doc (default `README.md`) does not exist, create it from the configured README template. Include `## Modernization`. Omit High-Level Architecture through Environment Variables. Include Requirements (purpose/domain links may be `TBD`), an empty or placeholder Backlog Items heading, and License if the template has one.
2. If the design doc exists without `## Modernization`, insert that section from the template after the Table of Contents. Do not rewrite Architect-owned design sections or backlog rows.
3. Create `docs/modernization/` if it does not exist.
4. Fill **What this is** and **Lane status** after synthesis (step 8). Title and opening paragraph: this is a port of `{legacy}` from `{source}` to `{target}`.
5. Each phase command in the sequence updates **only its Artifact index row** when it finishes. Assessment synthesis updates the Assessment row plus Lane status (`Phase: Assessment`, verdict, oracle tier, `Gate: M1 pending`, next command).

Do not copy inventory tables into the README.

## Sequence

0. Open the README hub (README hub steps 1–3): create or insert `## Modernization` with Artifact index rows at `missing`, and create `docs/modernization/`. Leave **What this is** / **Lane status** until after synthesis.
1. Run `/inventory-paths` to produce the execution path inventory.
2. Run `/inventory-dependencies`.
3. Run `/map-dependency-graph`. If it reports a dependency missing from the inventory, return to step 2.
4. Run `/analyze-impedance`.
5. Run `/build-oracle probe`.
6. Read the configured modernization assessment template (default `~/.cursor/templates/modernization-assessment-template.md`).
7. Synthesize the configured assessment document (default `docs/modernization/ASSESSMENT.md`) with:
   - a one-paragraph summary a reader can use in under five minutes;
   - feasibility verdict (`go`, `go-with-conditions`, or `no-go`);
   - scope snapshot (counts and links, not copied tables);
   - conditions that bind the **first slice** only;
   - `RISK-NNN` rows that affect the verdict or that slice;
   - oracle tier and walking-skeleton feasibility.
8. Recommend `/record-decision` for any `undecided` dependency or owner question that binds the first slice. Do not edit inventory cells to record those answers.
9. Update the README hub: **What this is**, **Lane status**, and the Assessment index row. Confirm phase-command index rows were written.

## Output

Return a Modernization Assessment Summary:

- Verdict and oracle tier.
- Candidate first slice (`XP-NNN` IDs).
- Conditions that bind that slice.
- Whether a normal walking skeleton is viable or a black-box first slice is required.
- Artifacts created.
- Delegation phases used or fallback phases used.
- Suggested next command (`/record-decision` for open first-slice questions, otherwise `/plan-migration` or `/document-legacy` scoped to the first slice).
- Whether the design doc / Modernization hub was created or updated.

## Examples

- `/assess-modernization /path/to/legacy-repo target: C# .NET 8`
- `/assess-modernization /path/to/legacy-repo @docs/user-guide.pdf`

This command is available in chat with `/assess-modernization`.
It expects a legacy repo path unless one is configured.
