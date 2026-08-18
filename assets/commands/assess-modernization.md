# assess-modernization

Orchestrates the feasibility assessment for a brownfield modernization or language/framework port. Before acting, resolve the workflow profile (target project `.cursor/workflow.config.yml`, then user `~/.cursor/workflow.config.yml`) and use its command directory, modernization paths, evidence grades, source stack, target stack, oracle tier, assessment statuses, and modernization assessment template. For each phase, read and follow the corresponding command spec under the configured command directory (defaults: `map-legacy.md`, `mine-history.md`, `inventory-dependencies.md`, `analyze-translation-gap.md`, `build-oracle.md`) as the source of truth for steps and rules.

## Command-Agent Binding And Delegation

Before executing the sequence, load the configured house rules, this command spec, and the active workflow profile. For each phase, read the phase command spec and its configured agent definition before acting:

| Phase command | Agent binding |
|---|---|
| `/map-legacy` | `agents.archaeologist` |
| `/mine-history` | `agents.archaeologist` |
| `/inventory-dependencies` | `agents.migrationStrategist` |
| `/analyze-translation-gap` | `agents.migrationStrategist` |
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

## Sequence

1. Run `/map-legacy` to produce the configured legacy map.
2. Run `/mine-history` when documentation, history, release notes, or issue exports are available; otherwise record the missing source as a risk.
3. Run `/inventory-dependencies`.
4. Run `/analyze-translation-gap`.
5. Run `/build-oracle probe`.
6. Read the configured modernization assessment template (default `~/.cursor/templates/modernization-assessment-template.md`).
7. Synthesize the configured assessment document (default `docs/modernization/ASSESSMENT.md`) with:
   - feasibility verdict (`go`, `go-with-conditions`, or `no-go`);
   - risk register (`RISK-NNN`);
   - obstacle catalog;
   - oracle tier and consequences;
   - walking-skeleton feasibility;
   - conditions required to proceed or raise confidence;
   - tensions / conflicts.

## Output

Return a Modernization Assessment Summary:

- Verdict and oracle tier.
- Highest risks and blockers.
- Conditions to proceed.
- Whether a normal walking skeleton is viable or a black-box first slice is required.
- Artifacts created or updated.
- Delegation phases used or fallback phases used.
- Suggested next command (`/document-legacy` for go/go-with-conditions, or the first condition to resolve for no-go).

## Examples

- `/assess-modernization /path/to/legacy-repo target: C# .NET 8 ASP.NET Core`
- `/assess-modernization /path/to/legacy-repo @docs/user-guide.pdf @release-notes/`

This command is available in chat with `/assess-modernization`.
It expects a legacy repo path unless one is configured.
