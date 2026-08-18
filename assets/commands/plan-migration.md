# plan-migration

Plan the modernization staging strategy, cutover approach, ADR triggers, and slice order after recovery documentation exists. Before acting, resolve the workflow profile and use its configured migration plan path, migration plan template, assessment path, translation gap path, dependency ledger path, oracle path, defect ledger path, design doc, ADR directory, staging strategies, structure-fidelity choices, and parity settings.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured migration plan document (default `docs/modernization/migration-plan.md`) using the configured migration plan template (default `~/.cursor/templates/migration-plan-template.md`). Create or recommend ADRs using the configured ADR template when the plan makes binding technical decisions.

## Inputs

- Accepted modernization assessment.
- Recovered purpose, domain model, behavior catalog, and refined requirements when available.
- Translation gaps, dependency ledger, oracle doc, and defect ledger.
- Target language, version, and framework.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured migration plan and ADR templates.
2. Read the accepted assessment, recovered docs, dependency ledger, translation gaps, oracle, defect ledger, and target-stack notes.
3. Choose a staging strategy from the configured strategies (`strangler`, `phased-rewrite`, `big-bang-parallel-run`) or stop if none fits.
4. Define slices in dependency order, mapping each to `BEH-NNN`, `Sn`, oracle evidence, structure fidelity, dependencies, exit criteria, and forecast confidence.
5. Decide whether each slice should preserve legacy structure first or refactor now.
6. Document cutover, rollback, coexistence, data-sharing, deferred modernization debt, and forecast recalibration.
7. Create or recommend ADRs for target stack, process boundaries, persistence, dependency substitutions, integration model, and cutover.

## Hard rules

- Do not plan implementation before unresolved `E4` / `E5` behavior is accepted or resolved.
- Do not promise a target date without forecast confidence and recalibration trigger.
- Do not convert a monolith to services/events by default; tie decomposition to purpose, domain boundaries, operations, and migration risk.
- Do not silently change defect policy; use the defect ledger.

## Outputs

- Configured migration plan.
- ADRs created or recommended.
- Summary of staging strategy, first slice, forecast confidence, cutover assumptions, and open decisions.

## Examples

- `/plan-migration @docs/modernization/ASSESSMENT.md target: C# .NET 8 ASP.NET Core`
- `/plan-migration @docs/requirements/ @docs/modernization/translation-gaps.md`

This command is available in chat with `/plan-migration`.
It expects an assessment and target-stack context.
