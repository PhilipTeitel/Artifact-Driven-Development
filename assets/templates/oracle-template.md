<!-- Oracle contract:
- Classify the legacy oracle tier. That is this document's job.
- Per-path fixtures and comparison rules live in path test plans, not here.
- T3 documented-only cannot claim independent parity.
- After the probe, treat tier and environment as a snapshot unless a new probe is run (vN+1).
- Omit unused environment rows. Do not write N/A.
-->

# Legacy Oracle

**Legacy repo:** `{path}`
**Oracle tier:** `{T1 executable | T2 recorded | T3 documented-only}`
**Version:** `{v1}`
**Status:** `{Draft | Snapshot}`
**Date:** `{YYYY-MM-DD}`
**Owner:** Implementer (`/build-oracle`)

## Summary

{One paragraph: which tier applies, whether containment is required, and what that means for the first slice's parity claims. Point to path test plans for fixtures and comparison rules.}

---

## 1. Oracle tier decision

| Tier | Selected? | Evidence | Consequence |
|------|-----------|----------|-------------|
| T1 executable | `{yes/no}` | `{grade}` `{citation}` | Repeated legacy-vs-new comparison is possible. |
| T2 recorded | `{yes/no}` | `{grade}` `{citation}` | Use frozen corpus; do not require live legacy execution in every run. |
| T3 documented-only | `{yes/no}` | `{grade}` `{citation}` | Parity is unprovable; require user acceptance data. |

Exactly one tier is selected.

## 2. Legacy execution environment

| Requirement | Value | Evidence |
|-------------|-------|----------|
| OS / image | `{value}` | `{grade}` `{citation}` |
| Runtime / compiler | `{value}` | `{grade}` `{citation}` |
| Network | `{none/limited/required}` | `{grade}` `{citation}` |
| Secrets | `{none/required/TBD}` | `{grade}` `{citation}` |

## 3. Containment and security

| Risk | Isolation control | Evidence | Owner |
|------|-------------------|----------|-------|
| `{vulnerable dependency / unsafe input / old runtime}` | `{networkless container/VM/sandbox}` | `{grade}` `{citation}` | `{owner}` |

Write `None.` when the probe found no containment requirement.

## 4. Determinism hazards that affect the tier

| Hazard | Why it affects repeated runs | Control |
|--------|------------------------------|---------|
| `{timestamp / RNG / locale / order / uninitialized memory}` | `{one line}` | `{control or unknown}` |

Path-specific hazards belong in that path's test plan.

## 5. Harness location

| Kind | Path | Notes |
|------|------|-------|
| `{probe notes / harness / fixture root}` | `{path or none}` | `{build-oracle build writes files; test plans name FIX IDs}` |

## 6. Open oracle questions

- [ ] `{question that would change the tier, not a per-path fixture question}`

## Links

- Assessment: `{assessmentDoc}`
- Path test plans: `{pathTestPlanGlob}`
- Parity reports: `{parityReportPattern}`
