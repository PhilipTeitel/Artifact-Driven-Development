# init-wiki

Initialize the LLM wiki layout in an Obsidian vault: create the wiki subdirectory (default `wiki/`), copy starter files from this repository when missing, and append an init entry to `log.md`. **Never modify vault source notes** outside the wiki subdirectory.

**Repo templates (copy sources):**

- `templates/wiki/SCHEMA.md`
- `templates/wiki/index.md`
- `templates/wiki/log.md`

Resolve template paths relative to the **ADD-LLM-wiki repository root** (the workspace when developing this repo, or a multi-root workspace that includes it). If templates are not found, stop and tell the user to open the ADD-LLM-wiki repo or add it to the workspace.

**Do not create** `wiki/.ingested.json` at init — that file is created on first ingest (S1-3).

---

## Prerequisites

- Cursor workspace is the user's vault **or** contains the vault as a subfolder.
- ADD-LLM-wiki `templates/wiki/*` files are readable (see paths above).
- Optional: user may specify a non-default wiki directory in chat (e.g. “use wiki dir `notes-wiki`”) for parity with future `--wiki-dir`.

---

## Step 1: Resolve vault root (S3)

Starting at the **workspace root**, walk **up** parent directories until **either**:

1. A `.obsidian/` directory exists (Obsidian vault root), **or**
2. `{wiki_dir}/SCHEMA.md` exists (wiki already initialized; `wiki_dir` defaults to `wiki` until overridden in Step 2).

If neither is found before the filesystem root:

- **Stop.** Do not create any files.
- Tell the user clearly: open the Obsidian vault as the workspace, or run from a folder inside the vault. Mention that `.obsidian/` marks a vault, or an existing `{wiki_dir}/SCHEMA.md` is accepted.

Record the resolved path as `{vault_root}`.

---

## Step 2: Choose `wiki_dir`

- **Default:** `wiki` (directory `{vault_root}/wiki/`).
- **Override:** If the user specified another name in this invocation (e.g. `notes-wiki`), use that instead. No leading/trailing slashes.

All paths below use `{vault_root}/{wiki_dir}/`.

---

## Step 3: Create wiki directory and copy templates (S1, S2)

1. Create `{vault_root}/{wiki_dir}/` if it does not exist.
2. For each row, copy **only if the destination file is missing**. Use byte-identical copy from the repo template. **Never overwrite** an existing file.

| Destination | Source template |
|-------------|-----------------|
| `{wiki_dir}/SCHEMA.md` | `templates/wiki/SCHEMA.md` |
| `{wiki_dir}/index.md` | `templates/wiki/index.md` |
| `{wiki_dir}/log.md` | `templates/wiki/log.md` |

**Idempotent rules (S2):**

- If `SCHEMA.md`, `index.md`, or `log.md` already exists, **leave its body unchanged** (do not merge, truncate, or replace).
- Do not overwrite, delete, or rewrite any other `**/*.md` under `{wiki_dir}/` (existing wiki pages stay as-is).
- Track each path as **created** or **already present (skipped)**.

---

## Step 4: Append init log entry (S13)

After Step 3 completes successfully:

1. Ensure `{wiki_dir}/log.md` exists (create from template in Step 3 if it was missing).
2. **Append** at the end of `log.md` (do not modify prior lines):

```markdown
## [YYYY-MM-DD] init | LLM wiki initialized
```

Use today's date in `YYYY-MM-DD`. Adjust the title after `|` if helpful (e.g. partial re-init). The `{operation}` must be `init`.

On **re-init** when all three core files already existed: still append a short init summary entry after successful completion (duplicate init lines are acceptable per S2).

If Step 3 failed or vault resolution failed, **do not** append to `log.md`.

---

## Step 5: Report summary to the user (S2)

Print a clear table or list:

| Path | Status |
|------|--------|
| `{wiki_dir}/` | created / already existed |
| `{wiki_dir}/SCHEMA.md` | created / skipped (already present) |
| `{wiki_dir}/index.md` | created / skipped |
| `{wiki_dir}/log.md` | created / skipped |
| Log entry | appended / not appended (reason) |

Include `{vault_root}` and `{wiki_dir}` in the summary.

---

## Prohibitions (S5, S2, ADR-003)

- **Immutability (S5):** Do **not** create, modify, delete, or rename any markdown **outside** `{vault_root}/{wiki_dir}/`. Vault sources (e.g. `daily/`, `notes/`) are read-only.
- **No overwrites (S2):** Do not overwrite existing `SCHEMA.md`, `index.md`, `log.md`, or any wiki page content.
- **Scope (Y4):** Do not write files outside `{wiki_dir}/` except this chat summary.
- **No `.ingested.json`** at init.

---

## Smoke / development fixture

To verify locally in this repo: workspace `{vault_root}` = `test/vault` (contains `.obsidian/`). Run this command; expect `test/vault/wiki/SCHEMA.md`, `index.md`, and `log.md`. Confirm `test/vault/daily/**/*.md` are unchanged.

Binding verifier: `bash scripts/verify-init-wiki-command.sh`
