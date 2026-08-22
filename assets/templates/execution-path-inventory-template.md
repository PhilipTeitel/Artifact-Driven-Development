<!-- Execution path inventory contract:
- One row per executable path. This is the scoping foundation, not a design doc.
- Main table: active paths only. Suspected-dead, unknown, and retired paths go in the appendix.
- One evidence grade per row. Do not combine grades.
- After Status: Snapshot, do not edit cells to record later decisions. Append Errata or produce vN+1.
- Omit sections that do not apply. Do not write "not applicable" rows.
- No prose preamble that restates table cells. History lives in git.
-->

# Execution Path Inventory

**Legacy repo:** `{path}`
**Version:** `{v1}`
**Status:** `{Draft | Snapshot}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Archaeologist (`/inventory-paths`)

## Summary

{One paragraph: how many paths were found, how many are active, what the dominant trigger types are, and whether anything important is still `unknown`. Point to the dependency graph for "what comes with a path" and to the assessment for the verdict.}

---

## 1. Active paths

| ID | Trigger | Description | Evidence |
|----|---------|-------------|----------|
| XP-NNN | `{library API / CLI / job / endpoint / event / scheduled task}` `{name or signature}` | `{one line: what it does}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` |

## 2. Open inventory questions

- [ ] `{question that prevents classifying a path}`

<!-- INCLUDE WHEN at least one path is suspected-dead, unknown, or retired.
     OMIT ENTIRELY otherwise. Do not keep empty reserved rows in §1. -->

## Appendix. Inactive, unknown, and retired paths

| ID | Trigger | Status | Why classified this way | Evidence |
|----|---------|--------|-------------------------|----------|
| XP-NNN | `{trigger}` | `{suspected-dead \| unknown \| retired}` | `{one line}` | `{grade}` `{citation}` |

## Errata

| Date | Row | Correction | Evidence |
|------|-----|------------|----------|
| `{YYYY-MM-DD}` | `{XP-NNN}` | `{what was wrong and the corrected fact}` | `{grade}` `{citation}` |

Write `None.` when there are no errata.

## Links

- Dependency graph: `{dependencyGraphDoc}`
- Assessment: `{assessmentDoc}`
