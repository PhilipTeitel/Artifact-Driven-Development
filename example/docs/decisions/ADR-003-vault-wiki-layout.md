# ADR-003: Vault layout, SCHEMA.md, and wiki artifacts

**Status:** Accepted
**Date:** 2026-05-30

---

## Context

The LLM-wiki pattern places raw sources (read-only), wiki (LLM-owned), and schema (configuration) in distinct layers. REQ-001 targets existing Obsidian vaults with wiki in a configurable subdirectory (default `wiki/`), standard markdown links, markdown-only v1 sources, and sidecar ingest tracking (S1, S4, S5, S12, S13).

---

## Decision

### Vault detection (CLI `ConfigurationPort` / composition root)

Walk parent directories from CWD until **either**:

1. A `.obsidian/` directory exists (Obsidian vault root), or
2. `wiki/SCHEMA.md` exists (wiki initialized without `.obsidian` in path — edge case)

If `--vault` is provided, use that path after validating it meets the same rules. Failure exits non-zero with guidance (S3).

### Wiki directory layout at init

Under `{vault_root}/{wiki_dir}/` (default `wiki/`):

| Artifact | Purpose |
|----------|---------|
| `SCHEMA.md` | Layer descriptions, ingest/query/lint workflows, exclude globs, link conventions, log prefix format |
| `index.md` | Catalog of wiki pages (empty structure at init) |
| `log.md` | Append-only chronological record (may start empty or with init entry) |
| `.ingested.json` | Sidecar ingest tracking (created on first ingest, not required at init) |
| `*.md` pages | Flat at init; LLM may create subfolders later |

**Idempotent init (S2):** Never overwrite existing wiki pages, index content, or log history. Create only missing required files; report existing vs added.

### `SCHEMA.md` template (shipped from repo)

Repo ships `templates/wiki/SCHEMA.md` (copied by init / `/init-wiki`). Minimum sections:

1. **Layers** — vault sources (read-only), wiki (LLM-owned), schema (this file)
2. **Workflows** — ingest, query, lint (behavioral summary aligned with REQ-001 scenarios)
3. **Excludes** — default list:
   - `.obsidian/`
   - `{wiki_dir}/` (e.g. `wiki/`)
   - Dotfiles: `.*`
   - User-editable additional glob patterns (one per line or bullet list — parser accepts relative path globs from vault root)
4. **Conventions** — standard markdown links `[text](path)` (no `[[wikilinks]]`), log heading format
5. **Index and log** — how to update `index.md` and append to `log.md`

`SchemaPort` parses the **Excludes** section into a list of path patterns; ingest and `list_sources` skip matching paths.

### Log entry format (binding, S13)

Each append uses a markdown heading:

```markdown
## [YYYY-MM-DD] {operation} | {title}
```

Where `{operation}` is one of `init`, `ingest`, `query`, `lint` (lowercase). Body is free-form markdown below the heading.

### `wiki/.ingested.json` format

```json
{
  "version": 1,
  "sources": {
    "notes/article.md": "2026-05-30T14:22:00Z"
  }
}
```

- Keys: source paths **relative to vault root**, normalized to forward slashes.
- Values: ISO 8601 UTC timestamps of last successful ingest.
- Updated by `IngestUseCase` after successful ingest; never written into source files (S12).
- Batch ingest skips keys present unless user adds a future `--force` flag (out of v1 scope).

### Source immutability

`WikiStoragePort` must not expose write/delete to paths outside the wiki subdirectory. Use cases never call write on source paths.

### Link format

Wiki pages use standard markdown links relative to vault or wiki root as documented in SCHEMA.md — not Obsidian wikilinks.

---

## Consequences

**Positive**

- Shared contract for Stage 1 Cursor commands and Stage 2 CLI.
- Grep-friendly logs and simple ingest idempotency without touching sources.

**Negative / costs**

- Exclude parsing must stay tolerant of user edits to SCHEMA.md; malformed excludes should warn, not crash silently.

---

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Track ingested sources only via log.md grep | Fragile; REQ-001 resolved to `.ingested.json` sidecar |
| `CLAUDE.md` / `AGENTS.md` as schema filename | REQ-001 binds `wiki/SCHEMA.md` for Obsidian + CLI parity |
| Wikilinks for Obsidian-native UX | REQ-001 non-goal; standard markdown links required |

---

## Explicit non-decisions

- Wiki page taxonomy (entity vs concept folders) — LLM discretion after init.
- Frontmatter / Dataview conventions — user optional per pattern doc.
- Search engine / vector index — non-goal for v1.

---

## Links

- Requirements: [docs/requirements/REQ-001-llm-wiki-cli.md](REQ-001-llm-wiki-cli.md) — S1–S5, S7, S12–S14
- Pattern reference: [docs/requirements/llm-wiki.md](llm-wiki.md)
- Related ADRs: [ADR-002](ADR-002-port-interfaces.md)
