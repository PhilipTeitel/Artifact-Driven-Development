# SK-1: Walking Skeleton

**Story**: Create the thinnest Stage 2 CLI path that boots through the Typer composition root, resolves configuration, touches the wiki storage boundary, and prints a validation result for a fixture vault.
**Epic**: Skeleton — Architectural and model proof
**Size**: Small
**Status**: Open

---

## 1. Summary

This walking skeleton proves the Stage 2 Python shape before normal feature stories continue. It does not implement full init, ingest, query, or lint behavior. It proves that the product can run through the same composition root, configuration boundary, storage boundary, and domain language that later stories rely on.

The skeleton's thin operation is `llm-wiki validate --vault test/vault`. The command resolves vault configuration through `ConfigurationPort`, asks `WikiStoragePort` whether the configured wiki layout is present, and prints a minimal validation result. This is intentionally narrower than S2-3's full validation use case; it exists to verify wiring and expose intent/model feedback early.

### 1a. Domain model touchpoints

| Domain artifact section | Terms / entities / boundaries touched | Why it matters for this skeleton |
|-------------------------|----------------------------------------|----------------------------------|
| `docs/PURPOSE.md#thesis` | local-first persistent wiki under user control | Proves the CLI starts from a real vault fixture rather than a transient chat path |
| `docs/DOMAIN.md#2-ubiquitous-language` | `Vault`, `Wiki`, `Schema`, `Configuration` | Ensures code and tests use canonical language |
| `docs/DOMAIN.md#3-data-dictionary` | `Vault.root_path`, `Wiki.directory` | These are the minimum fields needed to locate the wiki |
| `docs/DOMAIN.md#6-aggregates--consistency-boundaries` | `Vault boundary`, `Wiki boundary`, `Configuration boundary` | The skeleton must cross boundaries without collapsing them into the CLI |

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this skeleton |
|-----|----------------------------|
| [`docs/decisions/ADR-001-hexagonal-architecture.md`](../decisions/ADR-001-hexagonal-architecture.md) | Requires domain/use cases to depend on ports and adapters to be wired at the composition root |
| [`docs/decisions/ADR-002-port-interfaces.md`](../decisions/ADR-002-port-interfaces.md) | Defines `ConfigurationPort` and `WikiStoragePort` boundaries the skeleton must cross |
| [`docs/decisions/ADR-003-vault-wiki-layout.md`](../decisions/ADR-003-vault-wiki-layout.md) | Defines wiki layout pieces the storage adapter checks |
| [`docs/decisions/ADR-005-python-cli-packaging.md`](../decisions/ADR-005-python-cli-packaging.md) | Defines Typer CLI entrypoint and console script |

---

## 3. Definition of Ready (DoR)

- [ ] Configured purpose document exists and is approved, or the skeleton explicitly captures the current draft purpose risk
- [ ] Configured domain model exists and is approved, or the skeleton explicitly captures the current draft model risk
- [ ] Approved design identifies the composition root and primary boundaries to exercise
- [ ] Linked ADRs exist and are **Accepted**
- [ ] Section 4 (Binding constraints) names the architectural and model constraints the skeleton proves
- [ ] Section 4b (Ports & Adapters) lists every boundary the skeleton crosses
- [ ] Section 8a (Test Plan) includes one integration proof and one human-run demo proof

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — The skeleton boots through `llm_wiki.adapters.cli.main:app`, the same Typer composition root used by later CLI stories.
2. **Y2** — The skeleton resolves vault and wiki settings through `ConfigurationPort`, not direct environment or argparse reads in domain code.
3. **Y3** — The skeleton checks fixture wiki layout through `WikiStoragePort`, not direct filesystem access inside the use case.
4. **Y4** — The skeleton uses the domain language from `docs/DOMAIN.md`: `Vault`, `Wiki`, `Schema`, and `Configuration`.

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ConfigurationPort` | `src/llm_wiki/ports/configuration.py` | `CLIConfigurationAdapter` (`src/llm_wiki/adapters/cli/configuration.py`) | CLI args plus environment fixture | Resolves `Vault.root_path` and `Wiki.directory` |
| `WikiStoragePort` | `src/llm_wiki/ports/wiki_storage.py` | `FilesystemWikiStorageAdapter` (`src/llm_wiki/adapters/storage/filesystem.py`) | `test/vault/` fixture on disk | Checks `wiki/SCHEMA.md`, `wiki/index.md`, `wiki/log.md` |

---

## 5. API Endpoints + Schemas

No HTTP API.

| Attribute | Value |
|-----------|-------|
| Driving surface | `llm-wiki validate --vault test/vault` |
| Input | Vault path and optional `--wiki-dir` |
| Output | Exit 0 and a short validation message when the fixture wiki layout is present |

---

## 6. Frontend Flow

Not applicable — terminal CLI only.

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `src/llm_wiki/ports/configuration.py` | `ConfigurationPort` protocol subset needed by skeleton |
| 2 | `src/llm_wiki/ports/wiki_storage.py` | `WikiStoragePort` protocol subset needed by skeleton |
| 3 | `src/llm_wiki/domain/use_cases/validate_skeleton.py` | Thin use case that checks fixture wiki layout through ports |
| 4 | `src/llm_wiki/adapters/cli/configuration.py` | CLI configuration adapter |
| 5 | `src/llm_wiki/adapters/storage/filesystem.py` | Filesystem wiki storage adapter |
| 6 | `tests/integration/test_sk1_walking_skeleton.py` | End-to-end proof through Typer runner and real fixture |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `src/llm_wiki/adapters/cli/main.py` | Wire `validate` command through composition root |
| 2 | `pyproject.toml` | Ensure console script and test dependencies support the skeleton |
| 3 | `test/vault/wiki/SCHEMA.md` | Ensure fixture has required schema file if missing |
| 4 | `test/vault/wiki/index.md` | Ensure fixture has required index file if missing |
| 5 | `test/vault/wiki/log.md` | Ensure fixture has required log file if missing |

### Files UNCHANGED (confirm no modifications needed)

- `.cursor/commands/` — Stage 1 commands are not part of this skeleton.
- `docs/requirements/REQ-001-llm-wiki-cli.md` — requirement deltas only if the skeleton reflection reveals missing intent.

---

## 8. Acceptance Criteria Checklist

### Phase A: Running path

- [ ] **A1** — Skeleton boots through the real composition root
  - `llm-wiki validate --vault test/vault` invokes `llm_wiki.adapters.cli.main:app` and uses composition-root wiring.
  - Evidence: `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A1_boots_through_composition_root(pytest)`

- [ ] **A2** — Skeleton crosses configuration and storage boundaries
  - The validate path obtains `Vault.root_path` and `Wiki.directory` through `ConfigurationPort` and checks wiki layout through `WikiStoragePort`.
  - Evidence: `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A2_crosses_configuration_and_storage_boundaries(pytest)`

- [ ] **A3** — Skeleton demo is runnable by a human
  - From the example project root, `llm-wiki validate --vault test/vault` exits 0 and prints a validation success message.
  - Evidence: `llm-wiki validate --vault test/vault`

### Phase B: Intent feedback loop

- [ ] **B1** — Skeleton reflection captures intent deltas
  - After the demo, any "that is not what I meant" feedback is recorded as either a requirement delta for `/refine-feature` or a domain-model delta for `/model-domain`; if there are no deltas, record that explicitly in Completion Metadata.
  - Evidence: `docs/requirements/REQ-001-llm-wiki-cli.md`, `docs/DOMAIN.md`, or Completion Metadata reflection note

### Phase Y: Binding & stack compliance

- [ ] **Y1** — **(binding)** Skeleton uses the real Typer composition root
  - Evidence proves later CLI stories use the same entrypoint.
  - Evidence: `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A1_boots_through_composition_root(pytest)`

- [ ] **Y2** — **(binding)** Skeleton uses `ConfigurationPort`
  - Domain code does not read env vars, CLI args, or `os.environ` directly.
  - Evidence: `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A2_crosses_configuration_and_storage_boundaries(pytest)`

- [ ] **Y3** — **(binding)** Skeleton uses `WikiStoragePort`
  - Domain code does not inspect the filesystem directly.
  - Evidence: `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A2_crosses_configuration_and_storage_boundaries(pytest)`

- [ ] **Y4** — **(binding)** Skeleton preserves domain language and boundaries
  - Review confirms no invented domain terms, no missing data dictionary fields, and no boundary collapse.
  - Evidence: `/review-story SK-1`

### Phase Z: Quality Gates

- [ ] **Z1** — `pytest tests/integration/test_sk1_walking_skeleton.py` passes
- [ ] **Z2** — `ruff check .` passes (or only has pre-existing warnings)
- [ ] **Z3** — Configured type policy passes (no `Any` in new skeleton code)
- [ ] **Z4** — Imports preserve the package structure from ADR-001
- [ ] **Z5** — New or modified code includes appropriate logging or terminal output for the validation path
- [ ] **Z6** — `/review-story SK-1` satisfies the configured review gate
- [ ] **Z7** — `/review-story SK-1` satisfies the configured model-fidelity gate

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration | `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A1_boots_through_composition_root` | A1, Y1, Z1 | S10, S16 | proves Typer app path and composition root |
| 2 | integration | `tests/integration/test_sk1_walking_skeleton.py::test_SK1_A2_crosses_configuration_and_storage_boundaries` | A2, Y2, Y3, Z1 | S10, S16, S19 | uses CLI configuration + filesystem fixture |
| 3 | manual / script | `llm-wiki validate --vault test/vault` | A3, B1 | S10 | human demo and reflection checkpoint |
| 4 | review | `/review-story SK-1` | Y4, Z6, Z7 | S16, S19 | includes model-fidelity gate |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Skeleton expands into full validation behavior | Limit to layout-present check; leave full missing/malformed reporting to S2-3 |
| 2 | Skeleton duplicates later story scope | Treat later stories as replacements/refinements of this wiring, not additional product behavior |
| 3 | Fixture proves only happy path | Acceptable for skeleton; failure behavior remains in normal stories |

---

## Implementation Order

1. `src/llm_wiki/ports/configuration.py` and `src/llm_wiki/ports/wiki_storage.py` — define the minimal protocol subsets (covers Y2, Y3).
2. `src/llm_wiki/domain/use_cases/validate_skeleton.py` — create the thin use case that checks required wiki files through ports (covers A2).
3. `src/llm_wiki/adapters/cli/configuration.py` and `src/llm_wiki/adapters/storage/filesystem.py` — add real adapters against CLI args and fixture filesystem (covers A2, Y2, Y3).
4. `src/llm_wiki/adapters/cli/main.py` — wire `validate` through the composition root (covers A1, Y1).
5. `tests/integration/test_sk1_walking_skeleton.py` — prove the command boots and crosses both boundaries (covers A1, A2, Y1, Y2, Y3).
6. Run the human demo and record reflection deltas or "no deltas" (covers A3, B1).
7. Run `/review-story SK-1`, `/qa-story SK-1`, and `/document-story SK-1` as normal.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `TBD` |
| Completion ref | `TBD: not committed` |
| Final review summary | `TBD` |
| Final QA command | `TBD` |
| QA result | `TBD` |
| Docs handoff | `TBD` |
| Reflection result | `TBD` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Change ref | Review ref | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|------------|------------|-------------|-----------|
| F1 | `TBD` | `story-followup` | `TBD` | `TBD` | `TBD` | `TBD` | `none` | `TBD` | `TBD` |

---

*Created: 2026-07-01 | Story: SK-1 | Epic: Skeleton — Architectural and model proof*
