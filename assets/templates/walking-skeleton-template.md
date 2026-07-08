<!--
Walking-skeleton story contract:
- This file is produced by /plan-skeleton (architect in Skeleton Planning Mode).
- Save it using the configured story file pattern (default `docs/features/{STORY-ID}-{slug}.md`).
- It is a normal story document with special scope: prove the architecture and model with the thinnest running end-to-end slice before feature stories begin.
- The skeleton must execute through the composition root and every planned architectural boundary with real or hermetic-trivial adapters. It is not a prototype of isolated code.
-->

# {STORY-ID}: Walking Skeleton

**Story**: Create the thinnest running end-to-end slice that proves the approved purpose, domain model, architecture, composition root, and integration boundaries can execute together.
**Epic**: Skeleton — Architectural and model proof
**Size**: Small | Medium
**Status**: Open

---

## 1. Summary

{Explain why this skeleton exists, which purpose/domain/design artifacts it proves, and what later feature stories can safely assume once it passes. The skeleton should contain the least business behavior possible while still crossing every important boundary.}

### 1a. Domain model touchpoints

| Domain artifact section | Terms / entities / boundaries touched | Why it matters for this skeleton |
|-------------------------|----------------------------------------|----------------------------------|
| `docs/PURPOSE.md#thesis` | {purpose thesis / anti-thesis / trade-off rule} | Proves the running shape does not contradict the intended product shape |
| `docs/DOMAIN.md#aggregates--consistency-boundaries` | `{Boundary}` | Proves the composition root can wire boundaries without collapsing them |

---

## 2. Linked architecture decisions (ADRs)

| ADR | Why it binds this skeleton |
|-----|----------------------------|
| [`{decisionsDir}/ADR-NNN-slug.md`]({decisionsDir}/ADR-NNN-slug.md) | {one line} |

---

## 3. Definition of Ready (DoR)

- [ ] Configured purpose document exists and is approved, or the skeleton explicitly captures the current draft purpose risk
- [ ] Configured domain model exists and is approved, or the skeleton explicitly captures the current draft model risk
- [ ] Approved design identifies the composition root and primary boundaries to exercise
- [ ] Linked ADRs exist and are **Accepted** (or this skeleton is explicitly labeled a **spike** and only **Proposed** ADRs apply)
- [ ] Section 4 (Binding constraints) names the non-negotiable architectural and model constraints the skeleton proves
- [ ] Section 4b (Ports & Adapters) lists every port/adapter boundary the skeleton must cross
- [ ] Section 8a (Test Plan) includes at least one run/demo proof and at least one integration/e2e proof of the full path

---

## 4. Binding constraints (non-negotiable)

1. **Y1** — The skeleton must boot through the real composition root used by later feature work.
2. **Y2** — The skeleton must cross every planned port/adapter boundary with real or hermetic-trivial adapters; no mocked boundary can count as the skeleton proof.
3. **Y3** — The skeleton must preserve the domain language and consistency boundaries named in `docs/DOMAIN.md`.

---

## 4b. Ports & Adapters

| Port name | Port file | Adapter(s) | Real backing service / fixture | Notes |
|-----------|-----------|------------|--------------------------------|-------|
| `{PortName}` | `{path}` | `{AdapterName}` (`{path}`) | `{fixture/service}` | exercised by the skeleton path |

---

## 5. API Endpoints + Schemas

{Name the thin endpoint, command, UI action, job, or other driving surface that starts the skeleton path. If no public API exists, state the executable command or function entrypoint.}

| Attribute | Value |
|-----------|-------|
| Driving surface | `{command / route / UI action / job}` |
| Input | `{minimal input}` |
| Output | `{minimal observable output}` |

---

## 6. Frontend Flow

{If the product has a UI, describe the thinnest visible flow that starts the skeleton. If not applicable, state why.}

---

## 7. File Touchpoints

### Files to CREATE

| # | Path | Purpose |
|---|------|---------|
| 1 | `path/to/file` | composition root / skeleton use case / adapter / test |

### Files to MODIFY

| # | Path | Change |
|---|------|--------|
| 1 | `path/to/file` | wire skeleton path |

### Files UNCHANGED (confirm no modifications needed)

- `path/to/file` — reason unchanged

---

## 8. Acceptance Criteria Checklist

### Phase A: Running path

- [ ] **A1** — Skeleton boots through the real composition root
  - The configured run/demo command starts the application path used by later stories.
  - Evidence: `{path/to/skeleton.test}::boots_through_composition_root_A1({runner})`

- [ ] **A2** — Skeleton executes one end-to-end operation across every planned boundary
  - The operation uses the real or hermetic-trivial adapters listed in Section 4b and produces an observable output.
  - Evidence: `{path/to/skeleton.test}::executes_full_path_A2({runner})`

- [ ] **A3** — Skeleton demo is runnable by a human
  - A documented command runs the skeleton against a real fixture and prints or displays the expected result.
  - Evidence: `{demo command or script}`

### Phase B: Intent feedback loop

- [ ] **B1** — Skeleton reflection captures intent deltas
  - After the demo, any "that is not what I meant" feedback is recorded as either a requirement delta for `/refine-feature` or a domain-model delta for `/model-domain`; if there are no deltas, record that explicitly.
  - Evidence: `{docs/requirements or docs/DOMAIN.md update / reflection note}`

### Phase Y: Binding & stack compliance

- [ ] **Y1** — **(binding)** Skeleton uses the real composition root
  - Evidence proves later feature stories will use the same wiring path.
  - Evidence: `{path/to/skeleton.test}::boots_through_composition_root_A1({runner})`

- [ ] **Y2** — **(binding)** Skeleton crosses real or hermetic-trivial adapters
  - Evidence proves no boundary in Section 4b is mocked for the skeleton proof.
  - Evidence: `{path/to/skeleton.test}::executes_full_path_A2({runner})`

- [ ] **Y3** — **(binding)** Skeleton preserves domain language and boundaries
  - Evidence proves the running path uses terms and boundaries from `docs/DOMAIN.md`.
  - Evidence: `/review-story {STORY-ID}`

### Phase Z: Quality Gates

- [ ] **Z1** — `{stack.buildCommand}` passes with zero build/type errors
- [ ] **Z2** — `{stack.lintCommand}` passes (or only has pre-existing warnings)
- [ ] **Z3** — Configured type policy passes (default: no `any` types in any new or modified file)
- [ ] **Z4** — Configured shared type import policy passes (default: imports from shared use `@shared/types` alias, not relative paths)
- [ ] **Z5** — New or modified code includes appropriate logging for errors and significant operations per the implementer's logging guidelines
- [ ] **Z6** — `/review-story {STORY-ID}` satisfies the configured review gate
- [ ] **Z7** — `/review-story {STORY-ID}` satisfies the configured model-fidelity gate

---

## 8a. Test Plan

| # | Level | File::test name | Covers AC | Covers Sn | Notes |
|---|-------|------------------|-----------|-----------|-------|
| 1 | integration / e2e | `{path/to/skeleton.test}::boots_through_composition_root_A1` | A1, Y1 | {Sn or N/A} | proves real composition root |
| 2 | integration / e2e | `{path/to/skeleton.test}::executes_full_path_A2` | A2, Y2 | {Sn or N/A} | crosses all Section 4b boundaries |
| 3 | manual / script | `{demo command}` | A3, B1 | {Sn or N/A} | human demo and reflection checkpoint |

---

## 9. Risks & Tradeoffs

| # | Risk / Tradeoff | Mitigation |
|---|-----------------|------------|
| 1 | Skeleton grows into a full feature | Keep only enough behavior to prove wiring and model shape |
| 2 | Skeleton uses mocks and proves nothing | Require real or hermetic-trivial adapters for every listed boundary |

---

## Implementation Order

1. Create the minimal domain/use-case path that can return an observable success result (covers A2).
2. Create or wire the real composition root that later stories will use (covers A1, Y1).
3. Add real or hermetic-trivial adapters for each Section 4b boundary (covers A2, Y2).
4. Add the integration/e2e skeleton proof (covers A1, A2, Y1, Y2).
5. Add the demo command or documented run path (covers A3).
6. Run the demo with the human, record reflection deltas, and route them to `/refine-feature` or `/model-domain` before feature stories begin (covers B1).
7. Run `/review-story`, `/qa-story`, and `/document-story` as normal.

---

## 10. Completion Metadata

| Field | Value |
|-------|-------|
| Completed at | `{YYYY-MM-DD}` |
| Completion ref | `{commit SHA, branch ref, or "TBD if not committed"}` |
| Final review summary | `{configured review summary line, including MODEL counts}` |
| Final QA command | `{command that produced all configured pass results}` |
| QA result | `{all configured pass results / link or pasted summary}` |
| Docs handoff | `{docs updated / no docs update needed, with reason}` |
| Reflection result | `{deltas recorded / no deltas}` |

---

## 11. Post-complete Follow-up Ledger

| ID | Date | Change class | Intent | Files touched | Verification | Change ref | Review ref | Docs impact | AC impact |
|----|------|--------------|--------|---------------|--------------|------------|------------|-------------|-----------|
| F1 | `{YYYY-MM-DD}` | `{configured workflow lane}` | `{one sentence}` | `{paths}` | `{command or inspection proof}` | `{commit SHA, PR URL, or "uncommitted" / "TBD"}` | `{none / configured diff review path}` | `{none / docs path}` | `{none / explain affected AC}` |

---

*Created: {YYYY-MM-DD} | Story: {STORY-ID} | Epic: Skeleton — Architectural and model proof*
