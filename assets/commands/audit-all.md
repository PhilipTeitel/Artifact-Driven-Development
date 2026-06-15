# audit-all

Run the full audit workflow for the repository and write all results into `audit-findings.md` in the target repo root.

The auditor agent (`~/.cursor/agents/auditor.md`) executes each step. Use `~/.cursor/templates/audit-template.md` as a strict contract, not loose guidance.

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

Execute these commands sequentially in this exact order:
1. `map-repo`
2. `audit-tooling`
3. `audit-reliability`
4. `audit-db`
5. `audit-api-contracts`
6. `audit-security`
7. `audit-performance`
8. `audit-test-coverage`
9. `triage-audit-findings`

Do not run these commands in parallel. They share `audit-findings.md` as state, so parallel execution risks clobbering findings written by earlier steps.

Before each step:
- read the current `audit-findings.md`
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

This command is useful as a recurring repo health check, a pre-release sweep, or a scoped audit of a single package or set of paths. The output is intentionally one file (`audit-findings.md`) so the same report can be re-run, diffed, and shared.

For story-scoped reviews of a single feature's changed surface, prefer `/review-story` — it runs only the categories most likely to catch story-scoped escapes against only the files the story changed and produces the grep-friendly `REVIEW SUMMARY:` line that gates Phase Z's `Z6` quality gate.

## Examples

- `/audit-all` — full repo health check
- `/audit-all package: api` — audit only one package
- `/audit-all paths: src/payments,src/billing` — audit a focused set of paths

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
