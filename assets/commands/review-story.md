# review-story

This directs the **auditor** agent to run a focused, lightweight review of a single story's **changed surface** as a soft gate between `/implement-story` and `/qa-story`. Before acting, resolve the workflow profile and use its configured story glob, review template, review artifact path, summary format, per-story categories, and review gate.

## Why this exists

`audit-all` is the right tool for whole-repo health checks but is too heavy and too broad to run after every story. `/review-story` runs only the audit categories most likely to catch story-scoped escapes — reliability, security, api-contracts, and test-coverage — and only against the files the story actually changed. The result drives Phase Z's `Z6` quality gate and tells the implementer whether it is safe to ask QA to verify.

## Inputs

- A story document matching the configured story glob (default `docs/features/{STORY-ID}-*.md`; Sections 4b Ports & Adapters, 7 Files to CREATE/MODIFY, and 8a Test Plan are required).
- Optional: a `git diff` against the configured default base branch — the auditor uses it to detect out-of-plan changes (files modified that are not listed in Section 7).

## Steps

The auditor:

1. Reads the configured story-review template (default `~/.cursor/templates/story-review-template.md`) and uses it as a strict contract.
2. Reads the story document and identifies the **scope**: files from Section 7, tests from Section 8a, adapters from Section 4b, and Sn IDs from the linked refined requirements.
3. Intersects Section 7 with the working-tree diff (when available); files in the diff but not in Section 7 are flagged as **Out-of-plan changes** and never silently included.
4. Runs the per-story rubric for each finding category against the scoped files only:
   - **Test coverage:** every AC has a referenced test that exists and runs; every adapter has a non-mock integration test; every implemented `Sn` is traceable to a test name (`audit-test-coverage` rubric, per-story mode).
   - **Reliability:** unhandled errors, missing `await`, race conditions, startup fragility on the changed surface.
   - **Security:** authn/authz, injection sinks, trust boundary, secret handling on the changed surface.
   - **API contracts:** schema/handler drift on endpoints touched.
5. Writes findings to the configured story-review artifact (default `docs/features/{STORY-ID}-review.md`) using the review template. The **first line** of that file must be the configured summary line (default `REVIEW SUMMARY:`) so QA and the quality gate can grep it.
6. Sets `Gate result` using the configured review gate (default: `Block` if any finding is `severity: high` or `critical`; otherwise `Pass`).
7. When the configured block value applies, populates **Required actions before QA** with one bullet per blocking finding referencing the finding ID and the remediation step.

## Outputs

- Configured story-review artifact (new or overwritten).
- A short chat summary repeating the configured review summary line and the gate result.

## Workflow placement

```
/implement-story  →  /review-story  →  /qa-story
                        |
                        ├─ configured pass  → /qa-story
                        └─ configured block → fix the listed actions, then re-run /review-story
```

`Z6` in the story's Phase Z requires this review to satisfy the configured review gate on the changed surface.

## Examples

- `/review-story {STORY-ID}` — review the story's changed surface

This command is available in chat with `/review-story`.
It expects one argument, the story ID, like so: `/review-story {STORY-ID}`.
