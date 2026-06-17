# audit-api-contracts

Audit API handlers, schemas, and shared types for contract drift and compatibility risks. Focus on missing validation, inconsistent status codes, client/server schema mismatch, unsafe coercion, optional fields treated as required, and backward-incompatible behavior changes. Before acting, resolve the workflow profile and use its configured audit file, audit template, and finding prefixes.

Read the configured audit file in the target repo root first and use it as the shared audit state. If it does not exist, create it from the configured audit template.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `API Contracts`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only the configured API finding prefix for rows and headings created by this command (default `API-#`).
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same issue is already captured elsewhere in the configured audit file
- if another category already covers the same root cause, keep the API framing only when the contract mismatch adds unique risk
- omit low-confidence drift claims that are not tied to a concrete handler, schema, client type, or verification path

Search recipes:
- handler inputs that bypass schema validation or coerce unsafely
- response payloads or status codes that diverge from shared client/server contracts
- optional fields treated as required or required fields silently dropped
- backward-incompatible behavior changes without migration notes

For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- affected request/response contract
- failure mode or exploit scenario
- root cause
- minimal safe fix
- behavior to preserve
- any migration path needed
- regression test idea
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)
