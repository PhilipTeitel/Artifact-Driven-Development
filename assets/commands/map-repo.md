# map-repo

Map this repository before auditing it. Before acting, resolve the workflow profile and use its configured audit file, audit template, stack defaults, and finding prefixes. Works for any stack — TypeScript (npm/pnpm workspaces, Turborepo, Nx), Python (poetry, pip, uv, monorepo or single package), Go modules, Rust workspaces, JVM (Maven/Gradle), polyglot, or single-package projects.

**Command-agent binding:** This command is role-bound to `agents.auditor`. Before executing any step, load the configured Auditor agent definition and follow it as binding role context.

Write the result to the configured audit file in the target repo root (default `audit-findings.md`) using the configured audit template (default `~/.cursor/templates/audit-template.md`) as a strict structure. If the audit file does not exist, create it from the template first. Preserve all template headings and heading order. If a section has no content yet, write `None yet.`. Fill in at least:
- `Scope And Timebox` — including the `Scope` field (`whole-repo` | `package: <name>` | `paths: [<list>]`) and the detected stack(s)
- `System Map`
- `Findings Summary` with repo-level hotspots or likely candidates if concrete findings already exist
- `Root Causes` only when they are supported by code or config evidence

This command produces a compact system briefing inside that report so a human (and the per-category audit commands) can quickly understand the codebase and reason about safe changes.

## Stack detection

Detect and record:

- **Package/dependency manager(s):** `package.json` (npm/pnpm/yarn workspaces, Turborepo, Nx, Bun), `pyproject.toml` (poetry/uv/hatch), `requirements*.txt`, `Pipfile`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle(.kts)`, `Gemfile`, `mix.exs`, `composer.json`, etc.
- **Workspace topology:** monorepo vs single package; if monorepo, list the workspaces/packages and their roles.
- **Languages and runtimes** in use, with versions (from `engines`, `python_requires`, `go.mod`'s `go` directive, `rust-toolchain`, `Dockerfile` base images).
- **Build/test entrypoints:** root scripts (`package.json`, `Makefile`, `justfile`, `Taskfile.yml`, `scripts/`), per-package scripts, and CI workflow files (`.github/workflows`, `.gitlab-ci.yml`, `circleci`, `buildkite`, etc.).

## What to return

- workspace manager and task runner
- package or module inventory grouped as apps, services, workers, libraries, tooling, and shared config
- review coverage grouped into `Deeply reviewed packages`, `Lightly reviewed packages`, and `Not inspected yet`
- root entrypoints and the main runtime paths (HTTP, jobs, events, queues, scheduled tasks)
- architecture summary showing how packages depend on one another
- data-flow summary covering ingress, validation, business logic, persistence, and egress
- build system summary: root scripts, package scripts, language-specific config inheritance (e.g. tsconfig project references and path aliases for TS; `pyproject` workspace config for Python; `go.work` for Go; Cargo workspace for Rust), generated artifacts, and CI entrypoints
- test infrastructure summary: frameworks, test locations, integration vs unit boundaries, fixtures/mocks, and the smallest useful commands to verify a change
- risk hotspots: packages or boundaries most likely to yield meaningful audit findings
- safest likely fix candidates: issues that look local, testable, and low-risk

## Style

Keep it evidence-driven and concise. Prefer bullets and short tables over long prose. Include specific file paths and commands. If the repo lacks clear docs, infer structure from code and config rather than guessing. Be explicit when a package was only skimmed so later audit steps do not imply full coverage.

If concrete repo-level candidates already exist, prefer ones that are local, verifiable, and plausible to fix safely. Do not overwrite unrelated existing findings in the configured audit file; update the system-mapping portions and append only when needed.
