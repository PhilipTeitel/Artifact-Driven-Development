# audit-all

Run the full audit workflow for the repository and write all results into the configured audit file in the target repo root (default `audit-findings.md`). Before acting, resolve the workflow profile and use its configured auditor agent, audit template, audit command sequence, finding prefixes, and severity vocabulary.

**Command-agent binding:** This command is role-bound to `agents.auditor`. Before executing any step, load the configured Auditor agent definition and follow it as binding role context.

The configured auditor agent executes each step. When subagent delegation is available, run the configured Auditor subagent for the audit sequence and pass the active workflow profile, this command spec, the loaded Auditor definition, and the configured audit command sequence as binding context. If subagent delegation is unavailable, continue in the current chat only after loading the same Auditor definition and state in the output that the loaded-agent fallback was used. Use the configured audit template (default `~/.cursor/templates/audit-template.md`) as a strict contract, not loose guidance.

Requirements:
- set the `Scope` field in `Scope And Timebox` (default `whole-repo` unless the user passes a package or path scope)
- keep all headings and heading order exactly as the template defines them
- do not omit any template section; if a section has no content yet, write `None yet.`
- do not add new top-level sections
- do not use tables under `Detailed Findings`
- under `Detailed Findings`, use only the bullet fields defined in the template for each category
- ensure every finding appears in both `Findings Summary` and its matching category subsection
- ensure every selected fix appears in both `Fix Plan` and `Execution Log`
- prefer high-confidence findings with a concrete verification path
- avoid adding near-duplicate findings when an earlier step already captured the same defect

Execute the configured audit command sequence sequentially. Default order:
1. `map-repo`
2. `audit-tooling`
3. `audit-reliability`
4. `audit-db`
5. `audit-api-contracts`
6. `audit-security`
7. `audit-performance`
8. `audit-test-coverage`
9. `triage-audit-findings`

Do not run these commands in parallel. They share the configured audit file as state, so parallel execution risks clobbering findings written by earlier steps.

Before each step:
- read the current configured audit file
- preserve all sections owned by earlier commands
- update only the sections owned by the command being executed
- preserve higher-confidence findings unless you are clearly tightening or de-duplicating them

After all steps:
- ensure `Findings Summary` reflects the findings added across all categories
- ensure `Fix Plan` contains only the strongest, safest candidates given the scope and any time budget noted in `Scope And Timebox`
- keep `Deferred Findings` for important issues that should be reported but not fixed immediately
- ensure the final report still matches the template exactly
- if a command generated drift from the template, normalize the report back to the template structure before finishing

Mid-run sanity check:
- after `audit-db`, do a brief pass over the report before continuing
- tighten or remove speculative findings that lack a concrete trigger or verification path
- mark clear overlaps so later commands do not restate the same underlying issue in weaker terms

## Use cases

This command is useful as a recurring repo health check, a pre-release sweep, or a scoped audit of a single package or set of paths. The output is intentionally one configured audit file so the same report can be re-run, diffed, and shared.

For story-scoped reviews of a single feature's changed surface, prefer `/review-story` — it runs the configured per-story categories against only the files the story changed and produces the configured grep-friendly review summary line that gates Phase Z's `Z6` quality gate.

## Examples

- `/audit-all` — full repo health check
- `/audit-all package: api` — audit only one package
- `/audit-all paths: src/payments,src/billing` — audit a focused set of paths
