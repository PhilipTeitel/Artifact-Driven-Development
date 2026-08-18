# build-oracle

Probe or build the legacy oracle used to compare the port against legacy behavior. Before acting, resolve the workflow profile and use its configured oracle path, oracle template, parity tolerances, evidence grades, legacy repo path, defect ledger path, and parity report pattern.

**Command-agent binding:** This command is role-bound to `agents.implementer`. Before executing any step, load the configured Implementer agent definition and follow it as binding role context.

This command has two modes: `probe` and `build`. `probe` classifies whether the legacy app can be executed safely. `build` creates the harness or recorded fixture corpus in the target repo; it must not modify the legacy repo.

## Inputs

- Mode: `probe` or `build`.
- Legacy repo path and any required setup documentation.
- Optional behavior IDs, fixtures, or acceptance data to include.

## Steps

1. Resolve the workflow profile and read the configured oracle template (default `~/.cursor/templates/oracle-template.md`).
2. In `probe` mode:
   - Determine whether the legacy app can be built and run.
   - Identify containment requirements, obsolete dependencies, security isolation, data needs, secrets, and determinism hazards.
   - Classify the oracle tier as `T1 executable`, `T2 recorded`, or `T3 documented-only`.
3. In `build` mode:
   - Create or update target-repo oracle harness files and fixture records referenced by the oracle document.
   - Use the configured parity tolerances and text normalization rules.
   - Link fixtures to `BEH-NNN`, `DEF-NNN`, and future `P` criteria.
4. Write or update the configured oracle document.

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
- Determinism hazards.
- Open blockers.

## Examples

- `/build-oracle probe /path/to/legacy-repo`
- `/build-oracle build BEH-001 BEH-002`

This command is available in chat with `/build-oracle`.
It expects a mode (`probe` or `build`).
