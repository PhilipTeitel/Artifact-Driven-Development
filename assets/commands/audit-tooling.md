# audit-tooling

Audit this codebase for developer-tooling and delivery risks that could cause regressions or slow safe changes. Focus on tests, CI, scripts, build config, environment loading, type-check or static-analysis coverage, lint gaps, migration safety, release workflow issues, workspace orchestration (npm/pnpm/yarn workspaces, Turborepo, Nx, Cargo workspaces, Go workspaces, Python monorepo tooling, etc.), root vs package scripts, task filtering or caching, CI job-to-package mapping, and language-specific module/path drift (TypeScript project references and path aliases, Python `pyproject` namespace packages, Go module replace directives, Rust workspace path deps). Before acting, resolve the workflow profile and use its configured audit file, audit template, stack defaults, and finding prefixes.

**Command-agent binding:** This command is role-bound to `agents.auditor`. Before executing any step, load the configured Auditor agent definition and follow it as binding role context.

Read the configured audit file in the target repo root first and use it as the shared audit state. If it does not exist, create it from the configured audit template.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `Tooling`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only the configured tooling finding prefix for rows and headings created by this command (default `TOOL-#`).
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same underlying issue is already captured elsewhere in the configured audit file
- if it overlaps with another finding, prefer tightening the existing finding or mark the overlap explicitly instead of creating a near-duplicate
- omit weak candidates that cannot be tied to a concrete workflow failure, verification path, or likely regression risk

Search recipes:
- missing root scripts or package scripts needed for safe incremental validation
- CI jobs that skip packages, tests, or typecheck paths
- broken workspace graph assumptions, cache/filter drift, or path-alias/project-reference drift
- environments or migrations that are easy to run locally but unsafe in CI or production

Only report problems with concrete engineering impact. For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- affected package, script, or CI job
- failure or workflow risk
- root cause
- minimal safe fix
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)

Prefer issues that materially affect safe incremental changes for the repo's stack and topology.
