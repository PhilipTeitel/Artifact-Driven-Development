# build-oracle

Probe or build the legacy oracle used to compare the port against legacy behavior. Before acting, resolve the workflow profile and use its configured oracle path, oracle template, evidence grades, legacy repo path, and path test-plan glob.

**Command-agent binding:** This command is role-bound to `agents.implementer`. Before executing any step, load the configured Implementer agent definition and follow it as binding role context.

This command has two modes: `probe` and `build`. `probe` classifies whether the legacy app can be executed safely. `build` creates harness or recorded fixture files in the target repo; it must not modify the legacy repo. Per-path comparison rules and FIX IDs live in path test plans. This document owns the tier and environment.

## Inputs

- Mode: `probe` or `build`.
- Legacy repo path and any required setup documentation.
- Optional `XP-NNN` IDs whose test plans already named FIX IDs (build mode).

## Steps

1. Resolve the workflow profile and read the configured oracle template (default `~/.cursor/templates/oracle-template.md`).
2. In `probe` mode:
   - Determine whether the legacy app can be built and run.
   - Identify containment requirements, obsolete dependencies, security isolation, data needs, secrets, and determinism hazards that affect the **tier**.
   - Classify the oracle tier as `T1 executable`, `T2 recorded`, or `T3 documented-only`.
3. In `build` mode:
   - Create or update target-repo harness or fixture files named by the relevant path test plans.
   - Do not edit the path test plan, path detail, or oracle comparison policy. If a named fixture cannot be produced, stop and report the gap.
   - Do not treat a workflow-profile numeric hint as a binding comparison rule.
4. Write or update the configured oracle document (tier, environment, containment, harness location). Do not grow a global fixture catalog.
5. **README hub.** If `## Modernization` exists, update only the Artifact index row **Oracle**. Do not edit Lane status (Migration Strategist) or path test-plan rows. Do not create the section.

## Hard rules

- Do not run vulnerable legacy code outside the documented containment plan.
- Do not store secrets, PII, or unsanitized production data in fixtures.
- Do not claim `T1 executable` unless repeated execution is actually possible in the documented environment.
- Do not claim parity for `T3 documented-only`; document acceptance-data coverage instead.
- Do not modify the legacy repo.

## Output

Return an Oracle Summary:

- Mode run.
- Oracle tier and evidence.
- Harness or fixture paths created or updated.
- Containment requirements.
- Determinism hazards that affect the tier.
- Open blockers.

## Examples

- `/build-oracle probe /path/to/legacy-repo`
- `/build-oracle build XP-001 XP-002`

This command is available in chat with `/build-oracle`.
It expects a mode (`probe` or `build`).
