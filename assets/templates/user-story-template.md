# {STORY-ID}: {Story Title}

**Story**: {One-sentence description of what this story delivers}
**Epic**: {Epic number} — {Epic name}
**Size**: {Small | Medium | Large}
**Status**: Open

---

## 1. Summary

{2-4 paragraphs explaining:}
- What this story accomplishes and why it matters
- How it fits into the broader epic / what depends on it
- The key design principle or constraint guiding the approach
- Pointers to purpose, domain model, requirements files, and ADRs (full ADR links live in section 2)

### 1a. Domain model touchpoints

{List the configured purpose and domain artifacts this story depends on, plus every domain term, entity, invariant, lifecycle, or consistency boundary the story touches. If none apply, state why. These entries give `/review-story` a concrete model-fidelity target.}

| Domain artifact section | Terms / entities / boundaries touched | Why it matters for this story |
|-------------------------|----------------------------------------|-------------------------------|
| `docs/PURPOSE.md#thesis` | {purpose thesis / anti-thesis / trade-off rule} | {one line} |
| `docs/DOMAIN.md#...` | `{Term}`, `{Entity.attribute}`, `{Boundary}` | {one line} |

<!-- INCLUDE WHEN a linked REQ has section 4b Legacy provenance. OMIT ENTIRELY otherwise. REQ is canonical; copy the rows this story implements. -->

### 1b. Legacy provenance

Copied from the linked `REQ-NNN` section 4b. Do not invent grades, comparison rules, or defect decisions here.

| Sn | XP-NNN | Evidence | DEC-NNN | DEF-NNN | Comparison rule | Oracle source |
|----|--------|----------|---------|---------|-----------------|---------------|
| S1 | `{XP-NNN}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` | `{DEC-NNN or none}` | `{DEF-NNN or none}` | `{from REQ}` | `{FIX-NNN / acceptance data / none}` |

---

## 2. Linked architecture decisions (ADRs)

{List every ADR in the configured decisions directory (default `docs/decisions/`) that constrains this story. If none apply, keep this section and write: **None — this story inherits only epic-level ADRs already linked from the configured design doc** (and name those ADRs).}

| ADR | Why it binds this story |
|-----|-------------------------|
| [`{decisionsDir}/ADR-NNN-slug.md`]({decisionsDir}/ADR-NNN-slug.md) | {one line} |

---

## 3. Definition of Ready (DoR)

{The Architect confirms all items before the story is implementation-ready. If any fail, stop planning and output a **Tensions / conflicts** list for the user.}

- [ ] Linked ADRs exist and are **Accepted** (or the story is explicitly labeled a **spike** and only **Proposed** ADRs apply)
- [ ] The configured purpose document and domain model exist, or this story explicitly creates / bootstraps them
- [ ] Section 1a lists every domain term, entity, invariant, lifecycle, and consistency boundary this story touches, or states why none apply
- [ ] The configured design doc, requirements, and ADRs do not contradict each other on persistence, dependencies, or integration boundaries
- [ ] Section 4 (Binding constraints) is filled with 3–8 bullets copied or restated from those ADRs
- [ ] Section 4b (Ports & Adapters) lists every port/adapter this story creates or modifies, or states explicitly that no integration boundaries are touched
- [ ] Section 8a (Test Plan) is filled and **every AC ID** (including Phase Y and Phase Z) is referenced by at least one planned test row
- [ ] For every adapter in Section 4b, Section 8a contains both a **contract test against the port** and an **integration test against the real backing service** (no mock of the boundary the adapter owns), and Phase Y has a `(binding)` criterion citing the integration test file
- [ ] Every Gherkin scenario ID from the linked refined requirements in the configured requirements directory (default `docs/requirements/REQ-NNN-*.md`) is mapped to at least one acceptance test row in Section 8a — or the story explicitly states why a given scenario ID is out of scope here
- [ ] Phase Y includes at least one criterion with **non-mock** evidence where wrong-stack substitution is a risk
- [ ] If linked REQ files include **4b. Legacy provenance**: Section 1b is copied from those rows; no covered claim is `E4 inferred` or `E5 unknown` without a `DEC-NNN`; each oracle-backed `XP-NNN` has a comparison rule in the REQ and a `parity` test row in Section 8a (or the REQ says oracle source is `none`)
- [ ] If this story implements recovered `Sn` IDs, the migration-plan prerequisite IDs that bind those `XP-NNN` (`DEP-NNN`, `DEC-NNN`, `DEF-NNN`) are listed under **Slice prerequisites** below and marked resolved

<!-- INCLUDE WHEN this story implements recovered Sn IDs from a modernization REQ. OMIT ENTIRELY otherwise. Copied from the migration-plan row for those XP IDs. Check off here; do not edit analysis snapshots. -->

### Slice prerequisites

| ID | Kind | What must be true | Status |
|----|------|-------------------|--------|
| `{DEP-NNN / DEC-NNN / DEF-NNN}` | `{dependency / decision / defect}` | `{the condition that unblocks implementation}` | `{unresolved / resolved}` |

---

## 4. Binding constraints (non-negotiable)

{Restate in story-local language. The Implementer must satisfy every bullet; silent substitution of dependencies, storage, or transport is forbidden. Each bullet maps to a Phase Y criterion ID.}

1. **Y1** — {e.g. Vector embeddings persisted only via …}
2. **Y2** — {e.g. Do not use … for persistence}
3. **Y3** — …

---

## 4b. Ports & Adapters

{Required when this story creates or modifies any integration boundary (persistence, external service, message bus, file system, embedding/vector store, etc.). If no integration boundaries are touched, write **Not applicable — this story does not introduce or modify any port or adapter** and explain in one sentence why.

For every port and adapter affected by this story, fill the table. The Test Plan in Section 8a must contain a contract test row per port and an integration test row per adapter, and Phase Y must contain a `(binding)` criterion citing the integration test for each adapter.}

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `ExampleStore` | `src/ports/example-store.ts` | `SqliteExampleStore` (`src/adapters/sqlite/example-store.ts`) | local SQLite DB at `var/test/example.db` | new in this story |

---

## 5. API Endpoints + Schemas

{For each endpoint that is new or modified, provide a table:}

| Attribute | Value |
|-----------|-------|
| Method    | GET / POST / PUT / DELETE |
| Path      | `/api/...` |
| Auth      | none (MVP) / required |
| Query     | query parameters, if any |
| Response  | `TypeName` |

{Show the TypeScript interface for any NEW or CHANGED types that must be added to `shared/types.ts`:}

```ts
export interface ExampleResponse {
  // fields with types and inline comments explaining semantics
}
```

{If no API changes are needed, state that explicitly and explain why.}

---

## 6. Frontend Flow

### 6a. Component / Data Hierarchy

```
{ASCII tree showing how components, hooks, and data sources compose}
```

### 6b. Props & Contracts

{Table of components/hooks with their exact interfaces, state, and notes:}

| Component / Hook | Props / Signature | State | Notes |
|------------------|-------------------|-------|-------|
| ... | ... | ... | ... |

### 6c. States (Loading / Error / Empty / Success)

| State   | UI Behavior |
|---------|-------------|
| Loading | ... |
| Error   | ... |
| Empty   | ... |
| Success | ... |

{If frontend work is not applicable for this story, state that explicitly.}

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `path/to/file` | ... |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `path/to/file` | ... |

### Files UNCHANGED (confirm no modifications needed)

- `path/to/file` — reason unchanged

---

## 8. Acceptance Criteria Checklist

{Organize into phases (A, B, C, ...) that follow a logical implementation order.
**Required format:** Each criterion MUST use markdown task syntax so it can be checked off: `- [ ] **ID** — criterion title` (e.g. `- [ ] **A1** — ...`). Do not use plain bullets or bold-only IDs — the `- [ ]` is required.
Each criterion must be specific and verifiable — not vague ("works correctly") but precise ("returns 200 with ProjectRow[] containing resolved names").
Include one evidence bullet per criterion using this exact syntax: `- Evidence: \`path/to/file.test.ts::proof_name(command_or_runner)\``.
For **binding** or **stack** criteria, evidence may be a manifest check, grep, or script using the configured evidence examples, e.g. `- Evidence: \`package.json lists "some-pkg"\`` or `- Evidence: \`scripts/verify-stack.mjs(npm run verify:stack)\`` — tag the criterion title with **(binding)** so QA runs the real check.}

### Phase A: {Phase Name}

- [ ] **A1** — {Criterion title}
  - {Detailed verification statement}
  - Evidence: `apps/api/src/foo.test.ts::returns_200_A1(vitest)`
  - {Additional constraint or edge case, if any}

- [ ] **A2** — ...

### Phase B: {Phase Name}

- [ ] **B1** — ...

### Phase Y: Binding & stack compliance

{Map every bullet from Section 4 (Binding constraints) **and** every adapter row from Section 4b (Ports & Adapters) into a `(binding)` criterion here. Rules:

- For each adapter listed in Section 4b, Phase Y must contain at least one `(binding)` criterion whose **Evidence** points to the **integration test** for that adapter from Section 8a — not a unit test that mocks the boundary the adapter owns.
- For each port listed in Section 4b, Phase Y should contain at least one `(binding)` criterion citing the contract test from Section 8a.
- Manifest greps and `package.json` checks are acceptable evidence only when no adapter or port is involved (e.g. "library X is the chosen JSON parser"). When an adapter exists, prefer the integration-test evidence.

Use **(binding)** in the criterion title so QA runs the real check.}

- [ ] **Y1** — **(binding)** {Restate constraint from Section 4 or adapter row from Section 4b}
  - {Verification statement}
  - Evidence: `tests/integration/sqlite-example-store.test.ts::persists_via_sqlite_Y1(vitest)` or contract/static/script as appropriate

- [ ] **Y2** — **(binding)** ...

### Phase Z: Quality Gates

{Always include these standard quality gates as the final phase, substituting configured stack commands and type/import policy values from the workflow profile:}

- [ ] **Z1** — `{stack.buildCommand}` passes with zero build/type errors
- [ ] **Z2** — `{stack.lintCommand}` passes (or only has pre-existing warnings)
- [ ] **Z3** — Configured type policy passes (default: no `any` types in any new or modified file)
- [ ] **Z4** — Configured shared type import policy passes (default: imports from shared use `@shared/types` alias, not relative paths)
- [ ] **Z5** — New or modified code includes appropriate logging for errors and significant operations per the implementer's logging guidelines
- [ ] **Z6** — `/review-story {STORY-ID}` satisfies the configured review gate (default: zero `high` or `critical` `TEST-#`, `SEC-#`, `REL-#`, or `API-#` findings on the changed surface, with the configured machine-checkable summary line in the review output)
- [ ] **Z7** — `/review-story {STORY-ID}` satisfies the configured model-fidelity gate (default: zero `high` or `critical` `MODEL-#` findings; no new domain nouns, data fields, invariants, lifecycles, or consistency-boundary changes absent from `docs/DOMAIN.md`; no contradiction of `docs/PURPOSE.md`)

---

## 8a. Test Plan

{Required for **every** story (per the configured methodology profile's red-first setting — tests cannot drive code if they aren't planned). One row per planned test. Every AC ID from Section 8 must appear in the **Covers AC** column of at least one row. Every Gherkin scenario ID from the linked refined requirements that this story implements must appear in **Covers Sn** of at least one row.

Test levels (use the smallest level that proves the behavior end-to-end at that boundary):

- `unit` — a single function/class with no I/O
- `contract` — exercises a port with a generic test suite that any adapter for that port must pass
- `integration` — exercises an adapter against the **real** backing service or a hermetic fixture for it (no mocks of the boundary under test)
- `parity` — compares new behavior to the legacy oracle, fixture, or acceptance data named by the linked REQ section 4b, using that path's comparison rule
- `e2e` / `ui` — full-stack or browser-driven flow

Hexagonal rule (per the configured methodology profile): every port in Section 4b needs at least one configured contract test row; every adapter needs at least one configured integration test row. Defaults are `contract` and `integration`.

When Section 1b is present, add a **Covers XP** column and at least one `parity` row per oracle-backed `XP-NNN`. Comparison rules come from the REQ, not a global default. If the REQ says oracle source is `none`, do not invent a parity row.}

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | unit | `path/to/file.test.ts::returns_200_A1` | A1 | S1 | happy path |
| 2 | contract | `tests/contract/example-store.contract.ts::round_trip` | Y1 | S1, S2 | runs against every adapter |
| 3 | integration | `tests/integration/sqlite-example-store.test.ts::persists_via_sqlite_Y2` | Y1 | S1 | binding — real SQLite, not mocked |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | ... | ... |

---

## Implementation Order

{Numbered list of steps in the recommended sequence for the Implementer.
Each step should reference a specific file and map to one or more acceptance criteria.
When Section 8a contains `parity` rows, those characterization tests are the first failing tests — before other production-code work for the covered `Sn`.}

1. `path/to/file` — {what to do} (covers A1, A2)
2. ...
3. **Verify** — {build/test/curl check at this checkpoint}
4. ...
5. **Final verify** — full build + visual check

---

## 10. Completion Metadata

{Filled by `/complete-story` after implementation, review, QA, and docs handoff are complete. Preserve this section as the baseline for what the configured complete story status (default `Complete`) meant at the time the story was completed.}

| Field | Value |
|-------|-------|
| Completed at | `{YYYY-MM-DD}` |
| Completion ref | `{commit SHA, branch ref, or "TBD if not committed"}` |
| Final review summary | `{configured review summary line, default REVIEW SUMMARY: ...}` |
| Final QA command | `{command that produced all configured pass results, e.g. stack.testCommand with targeted args}` |
| QA result | `{all configured pass results / link or pasted summary}` |
| Docs handoff | `{docs updated / no docs update needed, with reason}` |

---

## 11. Post-complete Follow-up Ledger

{Append-only. Use this for small verified changes after the story already has the configured complete status: debugging fixes, polish, copy tweaks, UI refinements, or other local changes that do not alter binding constraints or invalidate the original acceptance criteria. If a follow-up changes original acceptance criteria, persistence/auth/API boundaries, adapters, or ADR-backed constraints, stop and plan a new story instead. Record `Change ref` (commit SHA, PR URL, or `uncommitted` / `TBD`) so each follow-up is traceable in version control; use `Review ref` when `/review-diff` produced an artifact for the follow-up.}

| ID | Date | Change class | Intent | Files touched | Verification | Change ref | Review ref | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|------------|------------|-------------|-----------|
| F1 | `{YYYY-MM-DD}` | `{configured workflow lane, e.g. story-followup / trivial-code / docs-only}` | `{one sentence}` | `{paths}` | `{command or inspection proof}` | `{commit SHA, PR URL, or "uncommitted" / "TBD"}` | `{none / configured diff review path}` | `{none / docs path}` | `{none / explain affected AC}` |

---

*Created: {YYYY-MM-DD} | Story: {STORY-ID} | Epic: {Epic number} — {Epic name}*
