<!-- Dependency ledger contract:
- Every dependency row must name support status, target-stack path, and substitution decision.
- Use `blocked` when there is no credible replacement, wrapper, or reimplementation route.
- If a section has no content yet, write `None yet.`.
-->

# Dependency Ledger

**Legacy repo:** `{path}`
**Source stack:** `{sourceStack}`
**Target stack:** `{targetStack}`
**Date:** `{YYYY-MM-DD}`

---

## 1. Dependency summary

| Category | Count | Unsupported | Blocked | Notes |
|----------|-------|-------------|---------|-------|
| `{runtime/framework/native/db/ui/build}` | `{N}` | `{N}` | `{N}` | `{notes}` |

## 2. Dependency inventory

| ID | Dependency | Version | Category | Used by | Support status | License | Evidence |
|----|------------|---------|----------|---------|----------------|---------|----------|
| DEP-NNN | `{name}` | `{version}` | `{runtime/framework/library/native/build/deploy}` | `{module}` | `{supported/unsupported/unknown}` | `{license/TBD}` | `{grade + citation}` |

## 3. Target substitution decisions

| DEP ID | Target equivalent | Decision | Impedance mismatch | ADR needed? | Verification |
|--------|-------------------|----------|--------------------|-------------|--------------|
| DEP-NNN | `{library/framework/wrapper/TBD}` | `{substitute/wrap/reimplement/drop/blocked}` | `{semantic/lifecycle/data/numeric/API mismatch}` | `{yes/no + ADR-NNN}` | `{test/script/proof}` |

## 4. Obsolete or vulnerable dependencies

| DEP ID | Issue | Severity | Containment needed | Mitigation |
|--------|-------|----------|--------------------|------------|
| DEP-NNN | `{unsupported/CVE/license}` | `{critical/high/medium/low}` | `{yes/no}` | `{mitigation}` |

## 5. Blockers

| DEP ID | Why blocked | Affected behavior | Required decision |
|--------|-------------|-------------------|-------------------|
| DEP-NNN | `{reason}` | `{BEH-NNN/TBD}` | `{question}` |

## 6. Links

- Assessment: `{assessmentDoc}`
- Translation gaps: `{translationGapDoc}`
- ADRs: `{decisionsDir}`

*Created: {YYYY-MM-DD}*
