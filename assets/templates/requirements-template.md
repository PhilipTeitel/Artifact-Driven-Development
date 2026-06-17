<!--
Refined-requirements contract:
- This file is produced by /refine-feature (architect in Discovery / Refinement Mode).
- Save it under the configured requirements directory using the configured requirement naming pattern (default `docs/requirements/REQ-NNN-short-slug.md`). Use sequential three-digit `NNN` unless the profile overrides the pattern.
- Do not delete or renumber existing REQ files; append the next number.
- Every Gherkin scenario must have an ID matching the configured scenario ID pattern (default `Sn`). The architect references those IDs from story Test Plans so each scenario traces to a concrete test.
- Unresolved questions are listed under `Open questions` — they are blocking. Do not write design or stories until they are resolved (architect should stop and re-ask).
-->

# REQ-NNN: {Short feature title}

**Source material:** {bullet list of files, tickets, transcripts, or pasted notes the architect read in this refinement pass — link or quote provenance}
**Date:** {YYYY-MM-DD}
**Status:** Draft | Ready for Design | Superseded (link to REQ-MMM)

---

## 1. Goals

{2–5 bullets stating, in plain language, what the user is trying to achieve. Each goal must come from the source material — do not invent.}

- ...

## 2. Non-goals

{Things this feature explicitly will **not** do. This is the scope guard. Without it, implementations drift.}

- ...

## 3. Personas / actors

{Who triggers or is affected by this feature. One short paragraph per persona, including the context they operate in.}

- **{Persona name}** — {role, environment, what they care about}

## 4. User scenarios (Gherkin)

{Each scenario describes one observable user-visible behavior. Tag each with an `Sn` ID. Architect uses these IDs to map each scenario to at least one acceptance test in the story Test Plan.}

### S1 — {Short scenario title}

```gherkin
Given {precondition}
And   {additional context, if needed}
When  {action the persona takes}
Then  {observable outcome the user can verify}
And   {additional outcome, if needed}
```

### S2 — {Short scenario title}

```gherkin
Given ...
When  ...
Then  ...
```

{Add as many scenarios as needed. Cover happy path, the most important edge cases, and the most likely failure modes the user described or that the source material implies.}

## 5. Constraints

{Hard constraints from the source material: regulatory, performance, security, platform, integration, deadlines. These often translate into ADRs.}

- ...

## 6. Resolved questions

{During the discovery pass the architect asked the user clarifying questions. Each row is one resolved question with the user's answer, so future readers know what was decided and why. This is the audit trail of refinement.}

| # | Question | Resolution | Source |
|---|----------|------------|--------|
| 1 | ... | ... | user (YYYY-MM-DD) |

## 7. Open questions

{Questions the architect raised that the user has **not** yet answered. The presence of any open question blocks downstream design (`/design-application`) and story planning (`/plan-story`) for affected areas.}

- [ ] ...

## 8. Suggested ADR triggers

{If a scenario or constraint implies a long-lived binding decision (persistence, auth, transport, embedding/vector stack, named third-party dependency, in-process vs. out-of-process boundary), call it out here so the next `/design-application` or `/plan-project` run knows to create or reference an ADR.}

| Trigger | Why it likely needs an ADR | Related Sn |
|---------|----------------------------|------------|
| ... | ... | S1, S3 |

## 9. Links

- Source material: see header
- Related REQ files: {REQ-NNN ...}
- Related ADRs (if any already exist): {ADR-NNN ...}

---

*Created: {YYYY-MM-DD} | Refined by: architect in Discovery Mode*
