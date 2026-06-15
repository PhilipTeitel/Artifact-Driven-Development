# LLM Wiki Schema

This file configures how agents and tools maintain the LLM wiki inside your Obsidian vault. **Vault sources are read-only**; the wiki layer is LLM-owned; **this file is the schema** (configuration).

Copy source: `templates/wiki/SCHEMA.md` in the ADD-LLM-wiki repository. After init, this file lives at `wiki/SCHEMA.md` (or `{wiki-dir}/SCHEMA.md` when using `--wiki-dir` in Stage 2).

---

## Layers

| Layer | Location | Who writes | Purpose |
|-------|----------|------------|---------|
| **Vault sources** | Markdown outside the wiki subdirectory | You (human) | Curated source material — articles, notes, imports. **Read-only** for ingest/query/lint/init tools. |
| **Wiki** | Wiki subdirectory (default `wiki/`) | LLM + tools | Summaries, entity pages, cross-links, filed query answers. |
| **Schema** | This file (`SCHEMA.md` in the wiki dir) | You + LLM | Workflows, excludes, and conventions. |

---

## Workflows

### Ingest

1. Choose a markdown source **outside** the wiki subdirectory (respect **Excludes** below).
2. Read the source; summarize key takeaways with the human when not in batch mode.
3. Create or update wiki pages (summary, entities, cross-references).
4. Update `index.md` with new or changed pages.
5. Append an entry to `log.md` using the log heading format below.
6. Record the source path in `.ingested.json` (do not modify the source file).

**Batch mode:** process every `.md` file in a directory without interactive prompts; skip paths in **Excludes** and sources already listed in `.ingested.json`.

### Query

1. Read `index.md` to locate relevant wiki pages, then read those pages.
2. Synthesize an answer with citations to wiki pages.
3. Present the answer to the user.
4. If the user confirms filing, create a new wiki page, update `index.md`, and append to `log.md`.

### Lint

1. Check the wiki for contradictions, stale claims, orphan pages, missing concept pages, and missing cross-references.
2. Print a report with **suggested** fixes only — **do not** auto-apply changes to wiki pages.
3. Append a lint entry to `log.md`.

---

## Excludes

Paths matching these patterns are **not** ingest sources (relative to vault root). One glob per bullet; add your own below the defaults.

- `.obsidian/`
- `wiki/` — default wiki subdirectory; if you use `--wiki-dir` (Stage 2 CLI), exclude that directory name instead
- `.*` — dotfiles and hidden paths

<!-- User-editable: add more exclude globs below -->

---

## Conventions

- Use **standard markdown links** only: `[text](path)` relative to the vault or wiki as appropriate.
- **Do not** use Obsidian `[[wikilinks]]` in wiki pages.
- Wiki may start **flat** at init; the LLM may create subfolders as the wiki grows.
- Link to source material when a wiki page is derived from a specific note.

---

## Index and log

### index.md

- Catalog of wiki pages: link, one-line summary, optional metadata.
- Update on every **ingest** and when a **query** answer is filed into the wiki.
- Agents read `index.md` first when answering queries.

### log.md

- **Append-only** chronological record of init, ingest, query, and lint operations.
- Each entry is a markdown heading followed by free-form body text.

**Log heading format (required):**

```text
## [YYYY-MM-DD] {operation} | {title}
```

- `{operation}` must be one of: `init`, `ingest`, `query`, `lint` (lowercase).
- Entries must be grep-friendly, e.g. `grep '^## \[' wiki/log.md`.

**Example:**

```markdown
## [2026-05-30] ingest | Weekly planning note
Processed source `notes/planning.md`; added summary and updated entity pages.
```

Allowed operations for `{operation}`: `init`, `ingest`, `query`, `lint`.
