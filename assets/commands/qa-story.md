# qa-story

This directs the QA agent to validate the given user story's acceptance criteria using tests and quality checks, then present criterion-by-criterion evidence. Before acting, resolve the workflow profile and use its story glob, QA result values, evidence examples, and stack commands.

**Command-agent binding:** This command is role-bound to `agents.qa`. Before executing any step, load the configured QA agent definition and follow it as binding role context.

## Steps

1. Find the story document using the configured story glob (default `docs/features/{STORY-ID}-*.md`).
2. Read the entire story document, including all acceptance criteria and `Evidence:` lines.
3. For each criterion ID (A1, A2, B1, ..., Z1), verify the cited evidence reference and run only the checks needed to confirm pass/fail.
4. When Section 8a contains `parity` rows, verify those criteria against the linked REQ section 4b comparison rule and oracle source. Record the result in the same evidence matrix. Do not write a separate parity report.
5. Output a Criteria Evidence Matrix with one row per criterion: ID, result using configured QA values (defaults: `PASS`/`FAIL`/`BLOCKED`), evidence reference, verification command, and proof.
6. Output summary counts for the configured QA result values and list any remediation needed for failed or blocked criteria.

If you cannot find the story document, stop and tell the user — do not infer results.

## What to do with the result

- All configured pass results: hand off to `/document-story {STORY-ID}` so Docs-PM can update the configured design doc backlog row and any affected docs.
- Any configured fail or blocked result: run `/fix-from-qa {STORY-ID}` to put the implementer into QA-driven repair mode against this matrix, then re-run `/qa-story {STORY-ID}` to verify. Iterate until all pass.

This command will be available in chat with /qa-story.
It expects one argument, the story ID, like so: `/qa-story {STORY-ID}`.
