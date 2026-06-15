# wiki-query

Answer a natural-language question using the LLM wiki: read `index.md` first, open relevant wiki pages, synthesize a cited answer in chat, then ask whether to file the answer as a new wiki page. **Filing requires explicit user confirmation** — default is read-only (no wiki writes after the answer unless the user confirms).

**Arguments:**

| Arg | Required | Description |
|-----|----------|-------------|
| `question` | yes | Natural-language question (remainder of command invocation) |

**Binding verifier:** `bash scripts/verify-wiki-query-command.sh`

---

## Prerequisites

- Wiki initialized: `{vault_root}/{wiki_dir}/SCHEMA.md` exists (run `/init-wiki` if missing).
- Vault root resolved the same way as `/init-wiki` (`.obsidian/` or existing `{wiki_dir}/SCHEMA.md` when walking up from workspace).
- Default `{wiki_dir}` is `wiki` unless the user overrides in chat (parity with init/ingest).

Read **`{wiki_dir}/SCHEMA.md`** before querying — especially the **Query** workflow and **Conventions** (standard markdown links only; no `[[wikilinks]]` in new wiki pages).

---

## Step 1: Resolve vault and wiki directory

1. Resolve `{vault_root}` (walk up for `.obsidian/` or `{wiki_dir}/SCHEMA.md`; stop with guidance if not found — same rules as `/init-wiki`).
2. Set `{wiki_dir}` (default `wiki`).
3. If `{vault_root}/{wiki_dir}/SCHEMA.md` is missing, **stop** and direct the user to run `/init-wiki`.
4. If `{vault_root}/{wiki_dir}/index.md` is missing, **stop** and direct the user to run `/init-wiki`.

---

## Step 2: Index-first navigation (S8)

**You MUST read `{wiki_dir}/index.md` before opening any other wiki page.** This is non-negotiable (index-first query).

1. **Read** `{vault_root}/{wiki_dir}/index.md` in full.
2. From the index (and the user's `question`), select relevant wiki page paths to read next.
3. **Read** only the selected pages under `{wiki_dir}/` — do **not** read vault sources outside the wiki subdirectory for answering (S5).

**Empty or sparse index:** If the index lists no pages (or none seem relevant), you may still read other `*.md` files under `{wiki_dir}/` **after** reading `index.md`, but you must have opened `index.md` first. If there are no wiki pages at all, explain that the wiki is empty and **do not offer filing** (nothing to cite).

**No vector search:** Do **not** use embeddings, vector databases, semantic search APIs, or RAG pipelines. Navigation is **index + direct page reads only** (README non-goal; parity with Stage 2 `QueryUseCase` without RAG).

---

## Step 3: Synthesize and present answer (S8)

1. Synthesize an answer to the user's `question` from the wiki pages you read.
2. **Include citations** to the wiki pages you used — markdown links `[title](wiki/path.md)` and/or explicit vault-relative paths (e.g. `wiki/topic.md`). Every factual claim drawn from the wiki should trace to at least one citation.
3. **Print the full answer in chat** before any filing prompt or wiki write.
4. If the wiki cannot answer the question, say so clearly and cite what you checked.

---

## Step 4: Filing gate — explicit confirmation (S8)

After presenting the answer, **ask the user** whether to file it as a new wiki page (yes/no). Use clear language, e.g.:

> File this answer as a new wiki page? Reply **yes** to create a page and update the index, or **no** to finish without changing wiki files.

**Rules:**

- **Default is no filing.** Do **not** create, modify, or append wiki files until the user explicitly confirms in chat (e.g. "yes", "file it", "save to wiki").
- If the user **declines** or does not confirm: **STOP.** No further wiki mutations — no new pages, no `index.md` changes, no `log.md` append (read-only query path).
- If the user confirms filing, proceed to Step 5.
- Do **not** infer confirmation from running the command alone; the question text is not consent to file.

---

## Step 5: File answer on confirm (S8, S13)

When the user **explicitly confirms** filing:

1. **Create** a new wiki page under `{vault_root}/{wiki_dir}/` with the answer content (agent-chosen path; e.g. `wiki/queries/2026-06-01-topic-slug.md` or flat `wiki/topic-slug.md`). Use **standard markdown links** only — **never** `[[wikilinks]]`.
2. **Update** `{wiki_dir}/index.md` with a link to the new page and a one-line summary.
3. **Append** to `{wiki_dir}/log.md` (do not modify prior log lines):

```markdown
## [YYYY-MM-DD] query | {title}
```

Use today's date; `{title}` describes the filed query (e.g. question topic or page title). `{operation}` must be `query` (S13).

4. Report: page path created, `index.md` updated, log entry appended.

**Do not** modify `.ingested.json` on query (ingest-only sidecar).

---

## Prohibitions (S5, Y8)

- **Immutability (S5):** Do **not** create, modify, delete, or rename any markdown **outside** `{vault_root}/{wiki_dir}/`. Vault sources remain read-only.
- **Scope:** Writes only under `{wiki_dir}/` when filing is confirmed (wiki pages, `index.md`, `log.md`). No writes elsewhere in the vault.
- **No RAG:** Do **not** use embeddings, vector stores, or semantic/vector search — index navigation and page reads only.

---

## States

| State | Behavior |
|-------|----------|
| Wiki not initialized | Direct user to `/init-wiki` |
| Empty wiki (no pages) | Answer explains no pages; no filing offer |
| Answer only (default) | Cited answer in chat; no wiki mutations |
| Filing confirmed | New page + `index.md` + `log.md` append |
| Filing declined | No mutations after answer |

---

## Smoke / development fixture

In this repo after `/init-wiki` and `/wiki-ingest` on `test/vault`:

```text
/wiki-query What themes appear in the ingested daily note?
```

Expect a cited answer in chat. Decline filing — confirm **no new** files under `test/vault/wiki/` beyond prior ingest artifacts.

Optional second run: confirm filing — expect a new page under `wiki/`, updated `index.md`, and a log line matching `## [YYYY-MM-DD] query |`.

Binding verifier: `bash scripts/verify-wiki-query-command.sh`
