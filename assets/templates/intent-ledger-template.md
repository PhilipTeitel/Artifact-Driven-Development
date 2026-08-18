<!-- Intent ledger contract:
- Record intent-bearing evidence from docs, release notes, history, help text, tickets, and comments.
- Commit-message-only or naming-derived intent is E4 until corroborated.
- If a section has no content yet, write `None yet.`.
-->

# Intent Ledger

**Legacy repo:** `{path}`
**Date:** `{YYYY-MM-DD}`
**Sources mined:** `{docs/release notes/history/tickets/help}`

---

## 1. Intent statements

| ID | Statement | Affected area | Evidence grade | Source | Confidence | Downstream artifact |
|----|-----------|---------------|----------------|--------|------------|---------------------|
| INT-NNN | `{what the system appears intended to do}` | `{module/behavior/domain}` | `{E1/E2/E3/E4/E5}` | `{citation}` | `{high/medium/low}` | `{PURPOSE/DOMAIN/BEH/REQ/TBD}` |

## 2. Release-note and support commitments

| Version / date | Commitment or change | Behavior affected | Evidence | Port implication |
|----------------|----------------------|-------------------|----------|------------------|
| `{version}` | `{statement}` | `{BEH-NNN/TBD}` | `{grade + citation}` | `{preserve/change/confirm}` |

## 3. Commit-history signals

| Commit / tag | Signal | Evidence grade | Why it matters | Confirmation needed |
|--------------|--------|----------------|----------------|---------------------|
| `{sha/tag}` | `{message or diff summary}` | `{E3/E4}` | `{impact}` | `{yes/no + question}` |

## 4. User-documentation signals

| Document | Section | Statement | Evidence grade | Behavior / domain implication |
|----------|---------|-----------|----------------|-------------------------------|
| `{path}` | `{section}` | `{statement}` | `E2 documented` | `{BEH/term/field}` |

## 5. Tensions / conflicts

| Conflict | Sources | Impact | Required resolution |
|----------|---------|--------|---------------------|
| `{conflict}` | `{citations}` | `{impact}` | `{question}` |

## 6. Open intent questions

- [ ] `{question}`

## 7. Links

- Purpose document: `{purposeDoc}`
- Domain model: `{domainDoc}`
- Behavior catalog: `{behaviorGlob}`

*Created: {YYYY-MM-DD}*
