# inventory-dependencies

Inventory legacy dependencies and decide whether each can be substituted, wrapped, reimplemented, dropped, or is blocked for the configured target stack. Before acting, resolve the workflow profile and use its configured dependency ledger path, dependency ledger template, source stack, target stack, evidence grades, and ADR directory.

**Command-agent binding:** This command is role-bound to `agents.migrationStrategist`. Before executing any step, load the configured Migration Strategist agent definition and follow it as binding role context.

Write the result to the configured dependency ledger (default `docs/modernization/dependency-ledger.md`) using the configured dependency ledger template (default `~/.cursor/templates/dependency-ledger-template.md`).

## Inputs

- Legacy repo path and source stack.
- Target language, version, and framework when known.
- Optional architecture or platform constraints.

## What the Migration Strategist will do

1. Resolve the workflow profile and read the configured dependency ledger template.
2. Inventory runtime, framework, package, native, database, UI, deployment, and build dependencies from code, manifests, lockfiles, installers, and docs.
3. Record version, support status, license, usage surface, and evidence for each dependency.
4. For each dependency, choose `substitute`, `wrap`, `reimplement`, `drop`, or `blocked`.
5. Record impedance mismatches that prevent in-place substitution, such as lifecycle, transaction, threading, serialization, numeric, or UI event-model differences.
6. Identify ADR triggers for binding replacement choices.

## Hard rules

- Do not silently approve a replacement dependency because a modern package exists.
- Use `blocked` when the route is not credible yet.
- Every decision needs evidence and, when durable, an ADR reference or ADR recommendation.

## Outputs

- Configured dependency ledger.
- Summary of unsupported dependencies, blockers, ADR triggers, and highest substitution risks.

## Examples

- `/inventory-dependencies /path/to/legacy-repo target: C# .NET 8 ASP.NET Core`
- `/inventory-dependencies @docs/vendor-list.md`

This command is available in chat with `/inventory-dependencies`.
It expects a legacy repo path or configured legacy repo path and target-stack information when available.
