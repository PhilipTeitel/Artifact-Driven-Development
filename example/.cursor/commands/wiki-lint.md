# wiki-lint

Health-check the LLM wiki: scan pages and cross-references, print a human-readable report with **suggested** fixes only, and append a lint entry to `log.md`. **Do not apply fixes to wiki pages** — report-only (S9).

**Arguments:**

| Arg | Required | Description |
|-----|----------|-------------|
| `focus` | no | Optional free-text focus (e.g. `orphans only`, `broken links`) — narrow checks when the user supplies it; full lint when omitted |

**Binding verifier:** `bash scripts/verify-wiki-lint-command.sh`

---

## Prerequisites

- Wiki initialized: `{vault_root}/{wiki_dir}/SCHEMA.md` exists (run `/init-wiki` if missing).
- Vault root resolved the same way as `/init-wiki` (`.obsidian/` or existing `{wiki_dir}/SCHEMA.md` when walking up from workspace).
- Default `{wiki_dir}` is `wiki` unless the user overrides in chat (parity with init/ingest/query).

**You MUST read `{wiki_dir}/SCHEMA.md` before linting** — especially the **Lint** workflow and **Conventions** (standard markdown links only; no `[[wikilinks]]` in wiki pages).

---

## Step 1: Resolve vault and wiki directory

1. Resolve `{vault_root}` (walk up for `.obsidian/` or `{wiki_dir}/SCHEMA.md`; stop with guidance if not found — same rules as `/init-wiki`).
2. Set `{wiki_dir}` (default `wiki`).
3. If `{vault_root}/{wiki_dir}/SCHEMA.md` is missing, **stop** and direct the user to run `/init-wiki`.
4. **Read** `{vault_root}/{wiki_dir}/SCHEMA.md` in full before scanning wiki pages (required).

---

## Step 2: Scan wiki (S9)

Read `{wiki_dir}/index.md` and all wiki pages under `{wiki_dir}/` (except treat `log.md` as append-only history, not a lint target for content rewrites). Do **not** read or modify vault sources outside the wiki subdirectory (S5).

If the user supplied optional `focus`, prioritize the matching check categories; still note if other categories were skipped.

Run these **five check categories** (S9):

| # | Category | What to look for |
|---|----------|------------------|
| 1 | **Contradictions** | Conflicting facts or claims across wiki pages (quote both sides). |
| 2 | **Stale claims** | Statements that may be outdated vs sources, index, or newer pages; cite evidence. |
| 3 | **Orphan pages** | Wiki pages not linked from `index.md` and with no inbound links from other wiki pages. |
| 4 | **Missing concept pages** | Important entities or topics mentioned repeatedly but without a dedicated wiki page (suggest a new page path). |
| 5 | **Missing / broken cross-references** | Standard markdown links `[text](path)` that point to missing files, wrong paths, or `[[wikilinks]]` where conventions require markdown links. |

**Empty wiki:** If there are no wiki pages beyond `SCHEMA.md`, `index.md`, and `log.md`, report **no pages to lint**; you may still append a log entry in Step 4.

**Large wikis:** If a full scan would exceed reasonable context, ask the user to opt into a subset or sampling before continuing.

---

## Step 3: Print report (S9)

Print a **human-readable report in chat** before any write. Structure:

1. **Summary** — counts by category (issues found / clean).
2. **Findings** — each issue with location (path), short description, and evidence quote or link target when helpful.
3. **Suggested fixes** — for every finding, include a clearly labeled **Suggestion:** line (what the user or a follow-up ingest/query session could do). These are recommendations only.

**Rules:**

- Label suggestions explicitly (e.g. **Suggestion:**, **Suggested fix:**) — not applied edits.
- **Do not** create, modify, delete, or rename any `wiki/**/*.md` file in this step except as allowed in Step 4 (`log.md` append only).
- **Do not** auto-apply fixes, merge pages, rewrite bodies, or update `index.md` during lint.
- A **clean wiki** is valid: report success with no findings.

---

## Step 4: Append lint log entry (S13)

After printing the report, **append** to `{vault_root}/{wiki_dir}/log.md` (do not modify prior log lines):

```markdown
## [YYYY-MM-DD] lint | {title}
```

Use today's date in `YYYY-MM-DD`. `{title}` summarizes the lint run (e.g. `3 issues found` or `wiki clean`). `{operation}` must be `lint` (S13).

Include a short body under the heading: category counts and a one-line summary of the worst finding (or "no issues").

If vault resolution failed or `SCHEMA.md` is missing, **do not** append to `log.md`.

---

## Prohibitions (S5, S9, Y4)

- **No auto-fix (S9):** Do **not** apply fixes to wiki pages automatically. Suggestions stay in chat only.
- **Writable wiki files:** The **only** wiki mutation allowed is **appending** to `log.md`. Do **not** modify `SCHEMA.md`, `index.md`, wiki page bodies, or `.ingested.json` during lint.
- **Immutability (S5):** Do **not** create, modify, delete, or rename any markdown **outside** `{vault_root}/{wiki_dir}/`. Vault sources remain read-only.

---

## States

| State | Behavior |
|-------|----------|
| Wiki not initialized | Direct user to `/init-wiki`; no log append |
| Empty wiki | Report no pages to lint; may append log |
| Issues found | Full report + suggestions; append log; no page edits |
| Clean wiki | Report success; append log |

---

## Smoke / development fixture

In this repo after `/init-wiki` and `/wiki-ingest` on `test/vault`:

```text
/wiki-lint
```

Expect a report in chat and a new `## [YYYY-MM-DD] lint |` line in `test/vault/wiki/log.md`. Confirm **no other** wiki markdown files changed except `log.md` (compare mtimes or git status).

Optional: `/wiki-lint orphans only` — report should emphasize orphan checks.

Binding verifier: `bash scripts/verify-wiki-lint-command.sh`
