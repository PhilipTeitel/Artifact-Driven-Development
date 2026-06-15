REVIEW SUMMARY: result=Pass TEST-critical=0 TEST-high=0 SEC-critical=0 SEC-high=0 REL-critical=0 REL-high=0 API-critical=0 API-high=0

# Story Review: S2-11 — Typer CLI composition root

**Reviewed against:** `docs/features/S2-11-typer-cli-composition-root.md`
**Date:** 2026-06-06
**Mode:** `/review-story`
**Gate result:** `Pass`

---

## Scope

- Story ID: S2-11
- Linked refined requirements (Sn IDs in scope): S1, S2, S3, S6, S7, S8, S9, S10, S11, S16, S19
- Files in scope (from Section 7 intersected with working tree):
  - `src/llm_wiki/adapters/cli/wiring.py` — created
  - `tests/integration/test_cli_commands.py` — created
  - `scripts/verify-s2-11-cli.sh` — created
  - `src/llm_wiki/adapters/cli/main.py` — modified
  - `README.md` — modified
  - `pyproject.toml` — modified (pytest `*_E3` function pattern for `lint_smoke_s9_E3`)
- Tests in scope (from Section 8a Test Plan):
  - `scripts/verify-s2-11-cli.sh` (static A1–A3, Y1, Y3)
  - `tests/integration/test_cli_commands.py::{invalid_vault_exits_s3_B1,no_partial_wiki_s3_B2,validate_success_s10_C1,validate_failure_s10_C2,init_creates_layout_s1_D1,init_idempotent_s2_D2,ingest_batch_smoke_s7_E1,query_smoke_s8_E2,lint_smoke_s9_E3,no_provider_error_s11_F1,real_storage_binding_Y2,test_init_works_without_provider}`
- Adapters in scope (from Section 4b):
  - `CLIConfigurationAdapter` for `ConfigurationPort`
  - `FilesystemWikiStorageAdapter` for `WikiStoragePort`
  - `MarkdownSchemaAdapter` for `SchemaPort`
  - `select_llm_provider()` for `LLMPort`
  - `TerminalUserInteractionAdapter` for `UserInteractionPort`

### Out-of-plan changes

- `pyproject.toml` — added `*_E3` to pytest `python_functions` so `lint_smoke_s9_E3` is collected; required for AC E3 evidence.

---

## Findings

### Test Coverage (`TEST-#`)

None.

### Reliability (`REL-#`)

None.

### Security (`SEC-#`)

None.

### API Contracts (`API-#`)

None.

---

## Required actions before QA

(none — gate passed)

---

## Notes

- Global Typer options (`--vault`, `--wiki-dir`, `--provider`) must appear **before** the subcommand (e.g. `llm-wiki --vault PATH init`). This matches Typer callback semantics and is exercised by integration tests.
- `build_context(require_llm=False)` defers `select_llm_provider` for `init`/`validate`; LLM commands set `require_llm=True` per S11.
- `test_init_works_without_provider` adds regression coverage beyond the story test plan for init-without-provider reliability.
