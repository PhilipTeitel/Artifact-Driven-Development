# S1-1: Ship wiki SCHEMA.md template

**Story**: Add the repo-shipped `templates/wiki/SCHEMA.md` that defines vault layers, ingest/query/lint workflows, default exclude paths, link conventions, and log entry format so Stage 1 commands and Stage 2 `SchemaPort` share one contract.
**Epic**: 1 — Stage 1 — Cursor daily driver
**Size**: Small
**Status**: Complete

---

## 1. Summary

This story delivers the **canonical SCHEMA template** copied into a user's vault at init time (`wiki/SCHEMA.md`). It is the configuration layer of the LLM-wiki pattern: it tells Cursor agents (Stage 1) and, later, the Python CLI (Stage 2) how to treat vault sources vs wiki pages, which paths to skip during ingest, and how to maintain `index.md` and `log.md`.

Without this file, `/init-wiki` (S1-2) has nothing authoritative to copy, and ingest/query/lint commands cannot align on excludes or log format. The template lives in **this repository** at `templates/wiki/SCHEMA.md`; it is not written directly into a user's vault until init runs in a later story.

**Requirements:** [REQ-001](REQ-001-llm-wiki-cli.md) scenarios **S4** (schema content) and **S13** (log heading format documented for operators and agents). **S1** (init creates SCHEMA) is implemented in **S1-2** — this story only ships the source template init will copy.

**Out of scope for S1-1:** Cursor commands, vault init, `index.md` / `log.md` creation, `.ingested.json`, Python `SchemaPort` parser implementation, and any modification of a user's Obsidian vault.

**Guiding constraint:** Content must match [ADR-003](ADR-003-vault-wiki-layout.md) minimum sections and default excludes so Stage 2 parsing does not require template churn.

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this story |
|-----|-------------------------|
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](ADR-003-vault-wiki-layout.md) | Defines `SCHEMA.md` minimum sections, default excludes, log heading format, link conventions, and repo path `templates/wiki/SCHEMA.md` |
| [`docs/decisions/ADR-002-port-interfaces.md`](ADR-002-port-interfaces.md) | `SchemaPort` will parse the **Excludes** section — template must use a stable, bullet-list layout |
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](ADR-001-hexagonal-architecture.md) | Stage 1 template is the behavioral contract Stage 2 must not contradict |

---

## 3. Definition of Ready (DoR)

- [x] Linked ADRs exist and are **Accepted**
- [x] README, requirements, and ADRs do not contradict each other on SCHEMA location, excludes, or log format
- [x] Section 4 (Binding constraints) is filled from ADR-003
- [x] Section 4b states no port/adapter work in this story
- [x] Section 8a maps every in-scope AC to tests; **S4** and **S13** appear in **Covers Sn**
- [x] No adapters in Section 4b — hexagonal pairing rule N/A
- [x] Phase Y includes **(binding)** criteria with non-mock evidence via `scripts/verify-wiki-schema-template.sh`
- [x] **S1**, **S2**, **S5**, **S14**, **S18** are explicitly out of scope (init/commands/QA epic gate)

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — Template path is exactly `templates/wiki/SCHEMA.md` in this repo (ADR-003).
2. **Y2** — SCHEMA includes all five ADR-003 sections: **Layers**, **Workflows**, **Excludes**, **Conventions**, **Index and log**.
3. **Y3** — **Excludes** lists default paths: `.obsidian/`, `wiki/` (with note that wiki dir name may be overridden via future `--wiki-dir`), and dotfiles `.*`.
4. **Y4** — **Conventions** require standard markdown links `[text](path)` and explicitly disallow Obsidian `[[wikilinks]]` for wiki pages.
5. **Y5** — **Index and log** documents log heading format exactly: `## [YYYY-MM-DD] {operation} | {title}` with `{operation}` ∈ `init`, `ingest`, `query`, `lint` (lowercase).
6. **Y6** — **Workflows** describes ingest, query, and lint at a level sufficient for a Cursor agent to follow without inventing contradictory rules (aligned with REQ-001 S6–S9 intent).
7. **Y7** — This story does **not** add files under a user vault; repo-only change.

---

## 4b. Ports & Adapters

**Not applicable — this story does not introduce or modify any port or adapter.** It ships a markdown template only. Stage 2 `SchemaPort` / `MarkdownSchemaAdapter` are implemented in **S2-2** and **S2-4** and must parse the **Excludes** section produced here.

---

## 5. API Endpoints + Schemas

No HTTP API. No shared TypeScript types.

This story defines a **filesystem artifact contract** only: the structure and required headings of `templates/wiki/SCHEMA.md`. Downstream init (S1-2) copies this file to `{vault}/wiki/SCHEMA.md` unchanged except where the user later edits their vault copy.

---

## 6. Frontend Flow

Not applicable — no UI. Stage 1 Cursor commands consume SCHEMA as markdown documentation in a later epic.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `templates/wiki/SCHEMA.md` | Canonical schema template per ADR-003 |
| 2 | `scripts/verify-wiki-schema-template.sh` | Executable verifier for required sections, excludes, log format, link rule (binding evidence) |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `README.md` | Ensure **Getting Started** / project structure mentions `templates/wiki/SCHEMA.md` if missing (one line only; do not edit other design sections) |

### Files UNCHANGED (confirm no modifications needed)

- `docs/decisions/*` — ADRs already Accepted
- `.cursor/commands/*` — created in S1-2 onward
- `src/llm_wiki/*` — Stage 2 only
- User vault paths — no vault writes in this story

---

## 8. Acceptance Criteria Checklist

### Phase A: Template file present

- [x] **A1** — `templates/wiki/SCHEMA.md` exists and is valid markdown (renders without broken heading hierarchy)
  - File is non-empty and uses `#` / `##` headings for major sections
  - Evidence: `scripts/verify-wiki-schema-template.sh::A1_file_exists`

### Phase B: SCHEMA content (S4)

- [x] **B1** — **Layers** section describes three layers: vault sources (read-only), wiki (LLM-owned), schema (this file)
  - Evidence: `scripts/verify-wiki-schema-template.sh::B1_layers_s4`

- [x] **B2** — **Workflows** section documents ingest, query, and lint workflows
  - Each workflow has a `##` or `###` heading or bullet block named ingest, query, lint (case-insensitive match)
  - Evidence: `scripts/verify-wiki-schema-template.sh::B2_workflows_s4`

- [x] **B3** — **Excludes** section lists `.obsidian/`, `wiki/`, and `.*` as default excludes
  - Additional user excludes may be documented as editable bullets below defaults
  - Evidence: `scripts/verify-wiki-schema-template.sh::B3_excludes_s4`

- [x] **B4** — **Index and log** section references `index.md` and `log.md` update conventions
  - Describes that index is updated on ingest and query filing; log is append-only
  - Evidence: `scripts/verify-wiki-schema-template.sh::B4_index_log_s4`

### Phase C: Log format documentation (S13)

- [x] **C1** — SCHEMA documents the exact log heading prefix `## [YYYY-MM-DD] {operation} | {title}` and allowed `{operation}` values
  - Includes a copy-paste example line for grep-friendly logs
  - Evidence: `scripts/verify-wiki-schema-template.sh::C1_log_format_s13`

### Phase D: Link conventions

- [x] **D1** — **Conventions** section requires standard markdown links and states wiki pages must not use `[[wikilinks]]`
  - Evidence: `scripts/verify-wiki-schema-template.sh::D1_markdown_links`

### Phase Y: Binding & stack compliance

- [x] **Y1** — **(binding)** Template satisfies ADR-003 minimum sections and default excludes
  - Running verifier exits 0
  - Evidence: `scripts/verify-wiki-schema-template.sh::Y1_adr003_compliance(bash scripts/verify-wiki-schema-template.sh)`

- [x] **Y2** — **(binding)** Template path is `templates/wiki/SCHEMA.md` only (no duplicate SCHEMA templates elsewhere in repo)
  - Evidence: `scripts/verify-wiki-schema-template.sh::Y2_single_template_path`

### Phase Z: Quality Gates

- [x] **Z1** — `bash scripts/verify-wiki-schema-template.sh` exits 0
  - Evidence: `scripts/verify-wiki-schema-template.sh::Z1_verifier_passes(bash scripts/verify-wiki-schema-template.sh)`

- [x] **Z2** — `chmod +x scripts/verify-wiki-schema-template.sh` and shebang `#!/usr/bin/env bash` present
  - Evidence: `test -x scripts/verify-wiki-schema-template.sh`

- [x] **Z3** — No `any` types — **N/A** (no application code in this story)

- [x] **Z4** — `@shared/types` imports — **N/A**

- [x] **Z5** — Application logging — **N/A** (markdown + shell verifier only)

- [x] **Z6** — `/review-story S1-1` reports zero `high` or `critical` findings on changed surface
  - Evidence: review output summary line

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `scripts/verify-wiki-schema-template.sh::A1_file_exists` | A1 | — | file presence |
| 2 | integration | `scripts/verify-wiki-schema-template.sh::B1_layers_s4` | B1, Y1 | S4 | three layers |
| 3 | integration | `scripts/verify-wiki-schema-template.sh::B2_workflows_s4` | B2, Y1 | S4 | ingest/query/lint |
| 4 | integration | `scripts/verify-wiki-schema-template.sh::B3_excludes_s4` | B3, Y1 | S4 | default excludes |
| 5 | integration | `scripts/verify-wiki-schema-template.sh::B4_index_log_s4` | B4, Y1 | S4 | index + log conventions |
| 6 | integration | `scripts/verify-wiki-schema-template.sh::C1_log_format_s13` | C1, Y1 | S13 | log heading contract |
| 7 | integration | `scripts/verify-wiki-schema-template.sh::D1_markdown_links` | D1 | S4 | no wikilinks rule |
| 8 | integration | `scripts/verify-wiki-schema-template.sh::Y2_single_template_path` | Y2 | — | one template only |
| 9 | integration | `scripts/verify-wiki-schema-template.sh::Z1_verifier_passes` | Z1 | — | full script exit 0 |

**Verifier implementation notes (for implementer):** Use `grep`/`rg` against `templates/wiki/SCHEMA.md` for required strings and section headings. Script may print `PASS: <check>` / `FAIL: <check>` and exit non-zero on any failure. Checks should be named to match rows above (comments in script).

**Intentionally out of scope Sn mapping:** S1, S2 (init behavior → S1-2); S5 (immutability at runtime → S1-2+); S14, S18 (commands/E2E → S1-2–S1-6).

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | User changes wiki dir from default `wiki/` | SCHEMA **Excludes** documents `wiki/` default and notes `--wiki-dir` override for Stage 2; S1-2 init may substitute path when copying |
| 2 | Exclude format too free-form for future `SchemaPort` | Use bullet list with one glob per line under **Excludes**; document format in SCHEMA |
| 3 | Verifier too brittle on prose | Match section headings and required phrases, not full paragraph text |

---

## Implementation Order

1. Create `templates/wiki/` directory if missing.
2. Author `templates/wiki/SCHEMA.md` with five ADR-003 sections and example log line (covers B1–D1).
3. Implement `scripts/verify-wiki-schema-template.sh` with checks matching Section 8a (red-first: run script, confirm failures, then fill template until green).
4. `chmod +x scripts/verify-wiki-schema-template.sh` and run full verifier (covers Z1, Z2, Y1, Y2).
5. Optionally add one line to README **Getting Started** pointing at `templates/wiki/SCHEMA.md` if not already present.
6. **Final verify** — `bash scripts/verify-wiki-schema-template.sh` exit 0; manual read of SCHEMA for agent clarity.

### SCHEMA.md content outline (implementer reference)

```markdown
# LLM Wiki Schema

## Layers
(vault sources read-only; wiki LLM-owned; this file is schema)

## Workflows
### Ingest
### Query
### Lint

## Excludes
- `.obsidian/`
- `wiki/`
- `.*`
(user may add more bullets)

## Conventions
(markdown links; no [[wikilinks]]; flat wiki at init)

## Index and log
(index.md catalog rules; log.md append-only; heading format with example)
```

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | 2026-05-30 |
| Completion ref | `caac9c0` |
| Final review summary | `REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0` |
| Final QA command | `bash scripts/verify-wiki-schema-template.sh` |
| QA result | All criteria PASS (15/15); verifier exit 0 |
| Docs handoff | README backlog S1-1 → Done; Available Scripts lists schema verifier |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|-------------|-----------|
| — | — | — | — | — | — | — | — |

---

*Created: 2026-05-30 | Story: S1-1 | Epic: 1 — Stage 1 — Cursor daily driver*
