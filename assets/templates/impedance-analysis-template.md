<!-- Technology and impedance analysis contract:
- Decision support: what about the two stacks changes how a path should be ported.
- Seeded language-family sections are CONDITIONAL. Include only the family that matches the discovered source stack. Omit the others entirely. Never fill N/A rows.
- Include hosting/deployment notes only when an execution path is a service, job host, or UI — not for a class library with no host.
- IMP-NNN rows are snapshot findings. Later pattern choices are DEC-NNN or ADR-NNN, cited from those artifacts.
- One evidence grade per row. Name affected XP IDs; do not restate path behavior.
- After Status: Snapshot, append Errata or produce vN+1.
-->

# Technology and Impedance Analysis

**Source stack:** `{language} {version} / {framework}`
**Target stack:** `{language} {version} / {framework}`
**Version:** `{v1}`
**Status:** `{Draft | Snapshot}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Migration Strategist (`/analyze-impedance`)

## Summary

{One paragraph: the mismatches that actually change port/rewrite/adapter choices, which paths they affect, and whether any of them bind the first slice. Point to IMP IDs; do not retell the path inventory.}

---

## 1. Source characteristics that matter for porting

| Characteristic | Observation | Evidence |
|----------------|-------------|----------|
| `{language standard, runtime, memory model, numeric types, build, …}` | `{fact}` | `{E1\|E2\|E3\|E4\|E5}` `{citation}` |

Keep this short. Omit characteristics that do not change a porting decision.

## 2. Target characteristics that differ

| Characteristic | Difference from source | Evidence |
|----------------|------------------------|----------|
| `{runtime, numeric types, arrays, I/O, concurrency, packaging, …}` | `{what differs}` | `{grade}` `{citation}` |

## 3. Impedance mismatches

| ID | Mismatch | Severity | Affected XP IDs | Candidate pattern | Evidence |
|----|----------|----------|-----------------|-------------------|----------|
| IMP-NNN | `{source construct vs target analogue}` | `{critical/high/medium/low}` | `{XP-NNN, …}` | `{preserve \| wrap \| rewrite \| adapter}` | `{grade}` `{citation}` |

Candidate pattern is a recommendation, not a decision. Record the decision as `DEC-NNN` or `ADR-NNN`.

<!-- INCLUDE WHEN source language is Fortran or the repo contains Fortran compilation units.
     OMIT ENTIRELY otherwise. -->

## 4. Fortran family notes

Use this section only to instantiate `IMP-NNN` rows that apply to *this* repo. Do not copy the whole checklist as live work.

Check only the constructs actually present: `COMMON` / global state, `EQUIVALENCE` / storage aliasing, implicit typing, column-major arrays, unstructured `GOTO`, fixed-form I/O, `real*4` / `real*8` numeric semantics. Each present construct becomes one `IMP-NNN` row in §3.

<!-- INCLUDE WHEN source language is C or the repo contains C compilation units that will be ported.
     OMIT ENTIRELY otherwise. -->

## 5. C family notes

Check only constructs actually present: pointer arithmetic, unions/casts, manual memory management, `#ifdef` variants, undefined-behavior reliance, native libraries. Each present construct becomes one `IMP-NNN` row in §3.

<!-- INCLUDE WHEN source is legacy Java (EE/EJB/Struts/JSP/app-server) that will be ported.
     OMIT ENTIRELY otherwise. -->

## 6. Legacy Java family notes

Check only constructs actually present: EJB/container services, Struts/JSP lifecycle, container-managed transactions, raw collections, app-server config. Each present construct becomes one `IMP-NNN` row in §3.

<!-- INCLUDE WHEN source is .NET Framework (not already .NET Core/.NET 5+) that will be ported.
     OMIT ENTIRELY otherwise. -->

## 7. .NET Framework family notes

Check only constructs actually present: AppDomains, Remoting, WCF, WebForms, GAC / machine.config, `ConfigurationManager`, culture-dependent parsing. Each present construct becomes one `IMP-NNN` row in §3.

<!-- INCLUDE WHEN at least one active execution path is a hosted service, web UI, or scheduled host.
     OMIT ENTIRELY for libraries and CLI-only tools with no host. -->

## 8. Hosting and operations

| Concern | Observation | Affected XP IDs | Evidence |
|---------|-------------|-----------------|----------|
| `{process model, config, deployment, runtime host}` | `{fact}` | `{XP-NNN}` | `{grade}` `{citation}` |

## 9. Open impedance questions

- [ ] `{question that would change a preserve/wrap/rewrite choice}`

## Errata

| Date | Row | Correction | Evidence |
|------|-----|------------|----------|
| `{YYYY-MM-DD}` | `{IMP-NNN}` | `{corrected fact}` | `{grade}` `{citation}` |

Write `None.` when there are no errata.

## Links

- Path inventory: `{pathInventoryDoc}`
- Dependency inventory: `{dependencyInventoryDoc}`
- Decision register: `{decisionRegisterDoc}`
