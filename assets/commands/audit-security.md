# audit-security

Audit this codebase for concrete security defects in the running application. Focus on authentication, authorization, trust boundaries, tampering, injection risks, XSS, CSRF, SSRF, path traversal, unsafe deserialization, secrets exposure, weak token/session handling, replay flaws, repudiation risks (missing or spoofable audit trails), denial-of-service risks (resource exhaustion, brute force, or unbounded work), business-logic abuse, multi-tenant isolation failures, and sensitive logging.

Read `audit-findings.md` in the target repo root first and use it as the shared audit state. If it does not exist, create it from `~/.cursor/templates/audit-template.md`.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `Security`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only `SEC-#` finding IDs for rows and headings created by this command.
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same underlying defect is already recorded in `audit-findings.md`
- if the issue is better framed as reliability or API drift, only create a security finding when the exploitability or trust-boundary aspect adds unique risk
- omit best-practice commentary that is not tied to a concrete exploit path, trust boundary, or verification path

Search recipes:
- authorization checks missing at handler, resolver, job, or tenant boundaries
- raw input reaching SQL, filesystem, URL fetch, template, or process boundaries
- token, session, or webhook verification flaws
- user-controlled work that can cause resource exhaustion or privilege abuse

Only report issues you can tie to specific code paths. For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- exploit scenario
- root cause
- minimal safe fix
- behavior to preserve
- whether the fix has backward-compatibility or migration implications
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)

Avoid generic best-practice advice unless it is directly connected to an exploitable defect.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
