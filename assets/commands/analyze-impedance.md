# analyze-impedance

Analyze source-to-target impedance mismatches that change port, wrap, rewrite, or adapter choices. Before acting, resolve the workflow profile and use its configured impedance analysis path, impedance analysis template, source stack, target stack, evidence grades, path inventory, dependency inventory, and dependency graph.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured impedance analysis document (default `docs/modernization/impedance-analysis.md`) using the configured impedance analysis template (default `~/.cursor/templates/impedance-analysis-template.md`).

## Inputs

- Legacy repo path and source stack.
- Target language, version, and framework.
- Path inventory, dependency inventory, and dependency graph when present.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured impedance analysis template.
2. Record only source and target characteristics that change a porting decision.
3. Add `IMP-NNN` rows with severity, affected `XP-NNN` IDs, a candidate pattern (`preserve`, `wrap`, `rewrite`, `adapter`), and one evidence grade.
4. Include a seeded language-family section only when that family is the discovered source stack (Fortran, C, legacy Java, or .NET Framework). Omit the others entirely. Do not fill N/A rows.
5. Include hosting/operations notes only when an active path is a service, web UI, or scheduled host. Omit them for a class library with no host.
6. Candidate patterns are recommendations. Record chosen patterns as `DEC-NNN` or `ADR-NNN`, not by editing `IMP-NNN` rows later.
7. **README hub.** If `## Modernization` exists, update only the Artifact index row **Impedance analysis**. Do not edit Lane status here; `/assess-modernization` owns that during assessment. Do not create the section.

## Hard rules

- Do not claim a clean analogue without naming how it would be verified (the covering REQ will own the comparison rule).
- Treat numeric precision, formatting, culture, ordering, and undefined-behavior reliance as per-path concerns. Do not invent a global tolerance.
- After `Status: Snapshot`, append Errata or produce `vN+1`.
- If target stack is missing, write `TBD` and list the blocked analysis questions as open `DEC-NNN` candidates.

## Outputs

- Configured impedance analysis.
- Summary of critical/high `IMP-NNN` rows, which bind the likely first slice, and suggested next command (`/build-oracle probe`).

## Examples

- `/analyze-impedance source: Fortran 77 target: C# .NET 8`
- `/analyze-impedance /path/to/legacy-repo target: Java 21`

This command is available in chat with `/analyze-impedance`.
It expects source and target stack information, either configured or supplied.
