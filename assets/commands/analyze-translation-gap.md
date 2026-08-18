# analyze-translation-gap

Analyze source-language, runtime, framework, data, build, deployment, and operational gaps between the legacy stack and the configured target stack. Before acting, resolve the workflow profile and use its configured translation gap path, translation gap template, source stack, target stack, evidence grades, dependency ledger, and ADR directory.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured translation gap document (default `docs/modernization/translation-gaps.md`) using the configured translation gap template (default `~/.cursor/templates/translation-gap-template.md`).

## Inputs

- Legacy repo path and source stack.
- Target language, version, and framework.
- Optional dependency ledger and legacy map if already produced.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured translation gap template.
2. Read the legacy map, dependency ledger, source stack, and target stack.
3. Fill the seeded gap matrix for the relevant source family: Fortran, C, legacy Java, or .NET Framework.
4. Add project-specific `GAP-NNN` entries for constructs, framework behavior, data representation, numeric semantics, concurrency, build, deployment, and operations.
5. For each gap, record target analogue, risk, migration pattern, verification strategy, skeleton impact, and evidence.
6. Mark translation gaps that require ADRs or user decisions.

## Hard rules

- Do not claim a clean analogue without naming the verification strategy.
- Treat numeric precision, formatting, culture, ordering, and undefined-behavior reliance as parity risks until characterized.
- If target stack is missing, write `TBD` and list the blocked analysis sections.

## Outputs

- Configured translation gap document.
- Summary of critical and high gaps, skeleton blockers, ADR triggers, and open target-stack questions.

## Examples

- `/analyze-translation-gap source: Fortran 77 target: C# .NET 8`
- `/analyze-translation-gap /path/to/legacy-repo target: Java 21 Spring Boot`

This command is available in chat with `/analyze-translation-gap`.
It expects source and target stack information, either configured or supplied.
