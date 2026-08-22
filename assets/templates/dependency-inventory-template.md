<!-- Dependency inventory contract:
- External dependencies only: runtime libraries, native libraries, build tools, vendored code, OS tools, data stores, network services.
- Disposition is exactly one of: available, reimplementable, undecided, no-route. Never "blocked".
- undecided = owner decision needed. no-route = no known replacement. They are not the same.
- Dispositions are snapshot classifications. Later substitution choices are DEC-NNN rows, not cell edits.
- One evidence grade per row.
- After Status: Snapshot, append Errata or produce vN+1. Do not rewrite cells to reflect decisions.
- Omit unused category sections. Do not write N/A rows.
-->

# Dependency Inventory

**Legacy repo:** `{path}`
**Source stack:** `{sourceStack}`
**Target stack:** `{targetStack}`
**Version:** `{v1}`
**Status:** `{Draft | Snapshot}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Migration Strategist (`/inventory-dependencies`)

## Summary

{One paragraph: how many dependencies, how many `no-route`, how many `undecided` (name the decisions), and whether any `no-route` item binds a plausible first slice. Point to the decision register for later choices and to the graph for affected paths.}

---

## 1. Counts

| Disposition | Count | Notes |
|-------------|-------|-------|
| available | `{N}` | `{optional}` |
| reimplementable | `{N}` | `{optional}` |
| undecided | `{N}` | `{point at the questions; do not call them blocked}` |
| no-route | `{N}` | `{these bind only the paths that use them}` |

## 2. Inventory

| ID | Dependency | Version | License | Support | Disposition | Decision needed | Evidence |
|----|------------|---------|---------|---------|-------------|-----------------|----------|
| DEP-NNN | `{name}` | `{version or unknown}` | `{license or unknown}` | `{supported \| unsupported \| unknown}` | `{available \| reimplementable \| undecided \| no-route}` | `{question, or none}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` |

<!-- INCLUDE WHEN any row has support status unsupported, a known CVE, or a license conflict.
     OMIT ENTIRELY otherwise. -->

## 3. Support, license, and vulnerability notes

| DEP ID | Issue | Severity | Evidence |
|--------|-------|----------|----------|
| DEP-NNN | `{unsupported / CVE / license}` | `{critical/high/medium/low}` | `{grade}` `{citation}` |

## 4. Open inventory questions

- [ ] `{question that prevents assigning a disposition}`

## Errata

| Date | Row | Correction | Evidence |
|------|-----|------------|----------|
| `{YYYY-MM-DD}` | `{DEP-NNN}` | `{corrected fact}` | `{grade}` `{citation}` |

Write `None.` when there are no errata.

## Links

- Dependency graph: `{dependencyGraphDoc}`
- Decision register: `{decisionRegisterDoc}`
- Impedance analysis: `{impedanceDoc}`
