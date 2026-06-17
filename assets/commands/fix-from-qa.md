# fix-from-qa

This directs the **Implementer** to repair a story using the most recent **QA evidence matrix** as input. It closes the loop after `/qa-story` reports configured fail or blocked criteria (defaults: `FAIL` or `BLOCKED`). Before acting, resolve the workflow profile and use its story paths, QA result values, agent directory, and status vocabulary.

## Why this exists

Without an explicit feedback command, "fix the QA failures" gets translated through free-form prompts and tends to (a) re-touch passing code paths, (b) skip the red-first workflow, or (c) silently change the design. This command constrains the implementer to the failed criteria and keeps the red-first discipline.

## Inputs

- A story document matching the configured story glob (default `docs/features/{STORY-ID}-*.md`).
- A recent QA evidence matrix from `/qa-story {STORY-ID}` — either pasted into the chat by the user, present in the story doc, or recoverable from the prior message.

If neither the matrix nor a clear list of configured fail/blocked criteria can be found, the implementer must stop and ask the user to re-run `/qa-story` first.

## Steps

1. Find the story document using the configured story glob (default `docs/features/{STORY-ID}-*.md`).
2. Read the story document fully (binding constraints, ports & adapters, test plan).
3. Read the QA matrix and extract the list of criterion IDs with the configured fail or blocked result values.
4. For **each** failing criterion, follow the **QA-driven repair mode** in the configured Implementer agent definition (default `~/.cursor/agents/implementer.md`):
   - Reproduce the failure (run the cited test or recreate the cited check).
   - Apply the **red-first** workflow: tighten or add the test that proves the fix, observe it fail for the right reason, implement the fix, observe it pass.
   - Check the criterion's box only after the targeted test passes locally.
5. Do not modify code paths that are exclusively covered by configured pass criteria unless required to fix a fail/blocked one. If you must, list the affected pass IDs in the **Risk to PASS criteria** column of the Remediation Summary so QA re-checks them.
6. Output:
   - The standard **End-of-Session Summary** (per the implementer agent).
   - The **Remediation Summary** table (per the implementer agent's QA-driven repair mode), with one row per configured fail/blocked criterion addressed.
7. Tell the user (or the calling command) to re-run `/qa-story {STORY-ID}` to verify the fixes and the unaffected pass criteria.

## Hard rules

- Do not edit acceptance criteria text. If a criterion is wrong, stop and emit a **Conflict report** instead.
- Do not change linked ADRs or binding constraints. If a fix requires an ADR change, stop and emit a **Conflict report**.
- Do not relax tests to make them pass. If a test is wrong, fix the test (and call that out), then re-run.
- Do not check off any criterion that is still marked with the configured fail or blocked value in the matrix without a passing test demonstrating the fix.

## Examples

- `/fix-from-qa {STORY-ID}` — rerun implementer in repair mode for the story against the most recent QA matrix
- `/fix-from-qa {STORY-ID}` (after pasting a QA matrix from a separate session) — implementer uses the pasted matrix as authoritative input

This command is available in chat with `/fix-from-qa`.
It expects one argument, the story ID, like so: `/fix-from-qa {STORY-ID}`.
