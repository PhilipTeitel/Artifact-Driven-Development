# review-diff

This directs the **auditor** agent to run the same focused review as `/review-story` but against an **arbitrary git diff** instead of a single story's changed surface. Use it for PR-style reviews, branch comparisons, hotfixes, or post-hoc audits of work that wasn't tracked through the `/plan-story` → `/implement-story` workflow.

## Why this exists

`/review-story` is anchored to a story document (Section 7 file list, Section 8a test plan, Section 4b adapters). For changes that happened outside that flow — a hotfix branch, a vendored library import, a pre-existing PR — there's no story to anchor against. `/review-diff` performs the same reliability/security/api-contracts/test-coverage checks but uses the diff as the scope source.

## Inputs

- A base ref to diff against. Defaults to the project's main branch (`main` or `master`, auto-detected). The user can pass any ref the working tree can reach (`origin/main`, a commit SHA, a tag).
- Optional: a target ref. Defaults to `HEAD`.
- Optional: a story ID when the diff is believed to be a post-complete follow-up. If provided, the auditor reads that story's `Completion Metadata` and `Post-complete Follow-up Ledger` for context but still reviews the diff as the source of truth.

## Steps

The auditor:

1. Reads `~/.cursor/templates/story-review-template.md` and uses it as a strict contract.
2. Resolves the diff: `git diff <base-ref>...<target-ref>` for files and `git log <base-ref>..<target-ref>` for commit context.
3. Identifies scope: changed files, test files added or modified, and any port/adapter files modified.
4. Runs the same per-category rubric as `/review-story`:
   - Test coverage on the changed surface (any new behavior must have a test added in the same diff; any modified adapter must have a non-mock integration test in the diff or already in the repo and still passing).
   - Reliability, security, and API contract checks scoped to changed files.
5. If a story ID is provided, checks whether the diff matches one or more ledger rows (including `Change ref` and `Review ref`). Missing or stale ledger entries are reported as documentation drift, not silently ignored. When the review is for a post-complete follow-up, the ledger row's `Review ref` should point to the written `docs/reviews/...` artifact.
6. Writes findings to `docs/reviews/diff-{base-ref-slug}--{target-ref-slug}-{YYYYMMDD}.md` using the review template (auto-create `docs/reviews/` if missing).
7. The **first line** of the output file is the single-line `REVIEW SUMMARY:` so the result is grep-friendly.
8. Sets `Gate result` to `Block` on any `high`/`critical` finding; otherwise `Pass`.

## Notes

- Out-of-plan detection does not apply here (there is no story plan); instead, all changed files are in scope by definition.
- Adapter test gating still applies: a modified adapter without an integration test in the diff or existing tests is a `TEST-#` `high` finding.
- For `hotfix-diff` work, this is the default quality gate before handoff.
- For `story-followup` work, prefer `/patch-story` first when the change clearly belongs to one completed story; use `/review-diff` when risk is unclear or when the diff spans multiple stories.
- This command does not modify the diffed code.

## Examples

- `/review-diff` — review the working tree against the auto-detected main branch
- `/review-diff origin/main` — review against the remote main branch
- `/review-diff v1.4.0` — review since the v1.4.0 tag
- `/review-diff origin/main feature/oto-9` — review the feature branch against main
- `/review-diff origin/main HEAD OTO-2` — review a diff in the context of a completed story follow-up

This command is available in chat with `/review-diff`.
It accepts zero, one, two, or three arguments: `<base-ref>`, optionally `<target-ref>`, and optionally `<story-id>`.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
