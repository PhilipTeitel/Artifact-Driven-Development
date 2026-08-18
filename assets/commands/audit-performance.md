# audit-performance

Audit this codebase for meaningful performance issues on realistic hot paths. Focus on repeated I/O, N+1 behavior, unbounded queries or loops, expensive parsing, cache misuse, blocking work on request paths, and pathological user-controlled operations. Before acting, resolve the workflow profile and use its configured audit file, audit template, and finding prefixes.

**Command-agent binding:** This command is role-bound to `agents.auditor`. Before executing any step, load the configured Auditor agent definition and follow it as binding role context.

Read the configured audit file in the target repo root first and use it as the shared audit state. If it does not exist, create it from the configured audit template.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `Performance`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only the configured performance finding prefix for rows and headings created by this command (default `PERF-#`).
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same issue already exists in the configured audit file
- if another category already captured the root cause, keep a performance finding only when the hot-path or scalability impact adds unique value
- omit micro-optimizations, hypothetical bottlenecks, or issues without a realistic hot path and verification path

Search recipes:
- repeated I/O or N+1 reads on request, job, or batch paths
- unbounded loops, pagination gaps, or user-controlled work amplification
- expensive parsing, serialization, or synchronous CPU work on latency-sensitive paths
- ineffective caching, duplicate fetches, or unnecessary fan-out

Ignore micro-optimizations. For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- why this is on a hot or scalable path
- expected impact
- root cause
- minimal safe fix
- behavior to preserve
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)
