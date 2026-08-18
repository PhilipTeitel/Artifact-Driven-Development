<!-- Legacy map contract:
- Inventory the legacy repo without choosing a target design.
- Every non-obvious fact needs an evidence grade and citation.
- If a section has no content yet, write `None yet.`.
-->

# Legacy Map

**Legacy repo:** `{path}`
**Date:** `{YYYY-MM-DD}`
**Mapped by:** `/map-legacy`

---

## 1. Scope and coverage

| Area | Coverage | Evidence | Notes |
|------|----------|----------|-------|
| `{module/package}` | `{deep/light/skipped}` | `{grade + citation}` | `{notes}` |

## 2. Stack and runtime inventory

| Layer | Technology | Version | Evidence | Support status | Notes |
|-------|------------|---------|----------|----------------|-------|
| Runtime | `{Fortran/C/Java/.NET/etc.}` | `{version}` | `{grade + citation}` | `{supported/unsupported/unknown}` | `{notes}` |

## 3. Build, run, and deployment entrypoints

| Entrypoint | Command / file | Purpose | Evidence | Works? |
|------------|----------------|---------|----------|--------|
| `{make target / .sln / script}` | `{command}` | `{purpose}` | `{grade + citation}` | `{yes/no/unknown}` |

## 4. Application topology

| Unit | Type | Responsibilities | Dependencies | Evidence |
|------|------|------------------|--------------|----------|
| `{module}` | `{app/service/batch/library/ui}` | `{responsibilities}` | `{dependencies}` | `{grade + citation}` |

## 5. Entrypoints and user-visible surfaces

| Surface | Trigger | Inputs | Outputs | Linked behavior |
|---------|---------|--------|---------|-----------------|
| `{screen/command/job/API}` | `{trigger}` | `{inputs}` | `{outputs}` | `{BEH-NNN/TBD}` |

## 6. Data stores and file formats

| Store / format | Location | Producer | Consumer | Schema known? | Evidence |
|----------------|----------|----------|----------|---------------|----------|
| `{database/file/message}` | `{path/connection}` | `{producer}` | `{consumer}` | `{yes/no/partial}` | `{grade + citation}` |

## 7. External interfaces

| Interface | Direction | Protocol / mechanism | Contract source | Evidence |
|-----------|-----------|----------------------|-----------------|----------|
| `{system}` | `{inbound/outbound}` | `{protocol}` | `{docs/schema/code/TBD}` | `{grade + citation}` |

## 8. Tests and existing verification assets

| Asset | Type | Coverage | Runs? | Evidence |
|-------|------|----------|-------|----------|
| `{path}` | `{unit/integration/manual/regression/golden}` | `{coverage}` | `{yes/no/unknown}` | `{grade + citation}` |

## 9. Complexity and risk hotspots

| Hotspot | Evidence | Why it matters | Candidate first action |
|---------|----------|----------------|------------------------|
| `{module/file}` | `{grade + citation}` | `{risk}` | `{action}` |

## 10. Open mapping questions

- [ ] `{question}`

## 11. Links

- Assessment: `{assessmentDoc}`
- Dependency ledger: `{dependencyLedgerDoc}`
- Translation gaps: `{translationGapDoc}`

*Created: {YYYY-MM-DD}*
