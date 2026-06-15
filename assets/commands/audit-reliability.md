# audit-reliability

Audit this codebase for concrete reliability defects. Focus on unhandled errors, malformed-input crashes, race conditions, invalid assumptions at API boundaries, startup fragility, state leakage across requests, retries/timeouts, and data corruption risks.

Read `audit-findings.md` in the target repo root first and use it as the shared audit state. If it does not exist, create it from `~/.cursor/templates/audit-template.md`.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `Reliability`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only `REL-#` finding IDs for rows and headings created by this command.
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same defect is already recorded in `audit-findings.md`
- if another category already captured the same root cause, add or update overlap notes rather than duplicating it
- omit issues that would be low-confidence or that lack a concrete trigger and verification path

Search recipes:
- unhandled promise chains, missing `await`, or dropped errors at async boundaries
- invalid input paths that can crash parsing, decoding, or coercion
- shared mutable state, request leakage, or non-idempotent retries
- startup assumptions around env vars, config, downstream services, or schema state

Only report issues that can plausibly break production behavior. For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- failure mode
- trigger conditions
- root cause
- minimal safe fix
- behavior to preserve
- a regression test idea
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
