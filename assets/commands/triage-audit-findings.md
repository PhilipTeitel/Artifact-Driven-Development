# triage-audit-findings

Read the configured audit file in the target repo root (default `audit-findings.md`) and reconcile triage using the `Decision` field from each detailed finding. Before acting, resolve the workflow profile and use its configured audit template, finding prefixes, and severity/confidence vocabulary.

Use the configured audit template (default `~/.cursor/templates/audit-template.md`) as a strict contract. Preserve all headings and heading order. If a required section has no content yet, write `None yet.`.

Treat `Decision` as the source of truth:
- `fix now` -> include the finding in `Fix Plan` -> `Selected Fixes`
- `defer` -> include the finding in `Deferred Findings`

Before updating triage:
- review severity, confidence, verification path, and expected fix scope for each finding whose prefix is not the configured test-coverage prefix
- look for near-duplicate or overlapping findings across categories
- prefer the highest-confidence, narrowest-blast-radius framing when two findings describe the same underlying defect

Update:
- `Findings Summary` so the `Fix now?` column matches each finding's `Decision` and the `Confidence` column matches the detailed finding
- `Fix Plan` -> `Selected Fixes` using only non-test-prefix findings marked `fix now`
- `Deferred Findings` using only non-test-prefix findings marked `defer`

For each selected fix, fill:
- why this is a strong fix candidate (severity, blast radius, reversibility)
- expected fix size (`small`, `medium`, `large`)
- narrowest files to change
- existing tests to anchor on
- lightest new or updated regression test
- smallest validation commands
- behavior to preserve
- commit message

When a deferred finding is missing `Why not now`, add it in the detailed finding using a concise reason such as:
- `broad blast radius`
- `unclear reproduction`
- `needs environment access`
- `cross-service change`
- `insufficient time`
- `other: duplicate of <ID>` or another short explanation when needed

When findings overlap:
- do not invent a new merged finding ID
- keep the strongest finding as the primary candidate
- update `Related finding IDs or overlaps` in the detailed findings when needed to make the overlap explicit
- if two findings are effectively duplicates, prefer deferring the weaker one with `Why not now: other: duplicate of <ID>`

Rank `fix now` candidates using this order:
1. severity
2. confidence
3. expected fix size
4. verification simplicity
5. locality of change

Use details already present in the report when possible. If information is missing, write `TBD` rather than inventing it.

Do not rewrite `System Map`. Only edit detailed findings when needed to restore template conformance, add missing triage metadata, or resolve clear duplicate/overlap ambiguity.
