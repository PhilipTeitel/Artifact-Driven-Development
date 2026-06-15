# wiki-ingest

Ingest one markdown source or a directory of sources into the LLM wiki: read vault notes **outside** the wiki subdirectory, summarize (interactive) or process sequentially (batch), then update wiki pages, `index.md`, `log.md`, and `wiki/.ingested.json`. **Never modify source files** or any markdown outside the wiki subdirectory (S5, S12).

**Arguments:**

| Arg | Required | Description |
|-----|----------|-------------|
| `path` | yes | Source file or directory, relative to vault root (e.g. `daily/2026-05-01.md` or `daily/`) |
| `batch` | no | Enable batch mode: pass `batch`, `--batch`, or include `batch` in the invocation (S7) |

**Binding verifier:** `bash scripts/verify-wiki-ingest-command.sh`

---

## Prerequisites

- Wiki initialized: `{vault_root}/{wiki_dir}/SCHEMA.md` exists (run `/init-wiki` if missing).
- Vault root resolved the same way as `/init-wiki` (`.obsidian/` or existing `{wiki_dir}/SCHEMA.md` when walking up from workspace).
- Default `{wiki_dir}` is `wiki` unless the user overrides in chat (parity with init).

Read **`{wiki_dir}/SCHEMA.md`** before selecting sources — especially the **Excludes** section and **Conventions** (standard markdown links only; no `[[wikilinks]]` in new wiki pages).

---

## Step 1: Resolve vault and wiki directory

1. Resolve `{vault_root}` (walk up for `.obsidian/` or `{wiki_dir}/SCHEMA.md`; stop with guidance if not found — same rules as `/init-wiki`).
2. Set `{wiki_dir}` (default `wiki`).
3. If `{vault_root}/{wiki_dir}/SCHEMA.md` is missing, **stop** and direct the user to run `/init-wiki`.
4. Read `{wiki_dir}/SCHEMA.md` and parse **Excludes** (bullet list of path globs relative to vault root). Skip any source whose vault-relative path matches an exclude pattern (S7).

---

## Step 2: Resolve source `path`

Normalize the user-supplied `path` to a vault-relative path with **forward slashes** (no leading `./`).

| Input | Mode |
|-------|------|
| Single `.md` file | **Interactive ingest** (S6) unless `batch` is set |
| Directory | **Batch ingest** (S7) when `batch` / `--batch` is present; otherwise ask the user to confirm batch or provide a single file |

If the path is excluded per SCHEMA, **skip** with a clear reason and do not write wiki artifacts for that path.

---

## Interactive ingest (S6) — single file

**Flow:** read → review → write (user must confirm takeaways before wiki writes unless they explicitly waive review in chat, e.g. “proceed without review”).

1. **Read** the source file at `{vault_root}/{path}` — **read-only**; do not modify the source (S5, S12).
2. **Present takeaways** to the user: short summary, proposed wiki page titles, and key entities/links. Wait for confirmation or edits.
3. After approval (or explicit waiver), **write/update** under `{vault_root}/{wiki_dir}/` only:
   - Create or update wiki page(s) with summaries and cross-references.
   - Use **standard markdown links** `[text](path)` only — **never** `[[wikilinks]]` in new or updated wiki pages (SCHEMA conventions).
   - **Update** `{wiki_dir}/index.md` with links to new or changed pages.
   - **Append** to `{wiki_dir}/log.md` (do not modify prior log lines):

```markdown
## [YYYY-MM-DD] ingest | {title}
```

Use today's date; `{title}` describes the ingest (e.g. source basename or topic). `{operation}` must be `ingest` (S13).

4. **Update** `{wiki_dir}/.ingested.json`:
   - On first ingest, create the file with `"version": 1` and a `"sources"` object.
   - Append or update `"sources"` with key = vault-relative `path` (forward slashes) and value = ISO 8601 UTC timestamp (e.g. `2026-06-01T12:00:00Z`) (S12).

5. Report: source path, pages created/updated, log entry appended, `.ingested.json` updated.

---

## Batch ingest (S7) — directory

Triggered when the user passes **`batch`**, **`--batch`**, or equivalent in the command args, and `path` is a directory.

1. Recursively list all `*.md` files under `{vault_root}/{path}`.
2. For each file, compute vault-relative path (forward slashes). **Skip** if:
   - Path matches any **Excludes** pattern from SCHEMA (S7), or
   - Path is already a key in `{wiki_dir}/.ingested.json` → `"sources"` (S12) — report as **skipped (already ingested)**.
3. For each remaining file, run the ingest pipeline **without interactive prompts between files** (no per-file review step in batch).
4. For each successful ingest: update wiki pages, `index.md`, append `log.md`, update `.ingested.json` — same artifacts as interactive mode.
5. Print a **summary**: processed count, skipped (exclude / already ingested) with reasons, failed (if any).

**Large directories:** If more than 50 files would be processed, stop and ask the user to confirm before continuing (mitigation for risk #2 in story).

---

## `.ingested.json` contract (S12)

Created on first successful ingest; never at init.

```json
{
  "version": 1,
  "sources": {
    "daily/2026-05-01.md": "2026-06-01T12:00:00Z"
  }
}
```

- Keys: vault-relative paths, forward slashes.
- Values: ISO 8601 UTC timestamps of last successful ingest.
- Batch re-ingest: **do not** re-process keys already present in `sources` unless a future `--force` exists (out of scope); list them as skipped.

---

## Prohibitions (S5, Y8)

- **Immutability:** Do **not** create, modify, delete, or rename any markdown **outside** `{vault_root}/{wiki_dir}/`. Vault sources remain read-only.
- **Scope:** Writes only under `{wiki_dir}/` (wiki pages, `index.md`, `log.md`, `.ingested.json`). No writes elsewhere in the vault.
- **Sources:** Never embed ingest state in source files; tracking is **only** via `.ingested.json`.

---

## States

| State | Behavior |
|-------|--------|
| Wiki not initialized | Direct user to `/init-wiki` |
| Source excluded | Skip with reason (SCHEMA Excludes) |
| Already ingested (batch) | Skip with reason (`.ingested.json`) |
| Success | Updated wiki pages + `index.md` + `log.md` + `.ingested.json` |

---

## Smoke / development fixture

In this repo after `/init-wiki` on `test/vault`:

```text
/wiki-ingest daily/2026-05-01.md
```

Expect `test/vault/wiki/.ingested.json` with key `daily/2026-05-01.md`, updated `index.md` and `log.md`, and **unchanged** `test/vault/daily/2026-05-01.md` content and mtime.

Batch:

```text
/wiki-ingest daily/ --batch
```

Second run should skip files already listed in `.ingested.json`.

Binding verifier: `bash scripts/verify-wiki-ingest-command.sh`
