# document-story

This directs the Docs-PM to review the given story and update all related documentation. Before acting, resolve the workflow profile and use its story paths, design doc, docs paths, and status mapping. The story document in the configured features directory (default `docs/features/`) is the source of truth for status.

**Command-agent binding:** This command is role-bound to `agents.docsPm`. Before executing any step, load the configured Docs-PM agent definition and follow it as binding role context.

## Steps

1. Find the story document using the configured story glob (default `docs/features/{STORY-ID}-*.md`).
2. Read the entire story document, noting the `**Status**:` field, checked acceptance criteria, `## 10. Completion Metadata`, and `## 11. Post-complete Follow-up Ledger`.
3. Report the current status: story ID, title, status, fraction of acceptance criteria completed (e.g. "7/10 criteria done"), and count of follow-up ledger entries.
4. Update any project documentation affected by the story or its follow-up ledger:
   - Configured design doc (default `README.md`) — if setup steps, env vars, or run commands changed
   - API docs / OpenAPI spec — if endpoints were added or modified
   - Runbooks or guides — if operational procedures changed
5. If follow-up ledger rows list a docs impact, verify the referenced docs were updated or explain why no docs change is required.
6. If no documentation updates are needed, state that explicitly and why.
7. Output: docs changed, docs handoff text suitable for `Completion Metadata`, what to verify, and the current story status summary.

If you cannot find the story document, stop and tell the user — do not guess at status.

This command will be available in chat with /document-story.
It expects one argument, the story ID, like so: `/document-story {STORY-ID}`.
