# complete-port-story

Orchestrates the SDLC tail for a modernization port story: implementation, review gate, parity verification, QA verification, documentation updates, and story validation. Before acting, resolve the workflow profile (target project `.cursor/workflow.config.yml`, then user `~/.cursor/workflow.config.yml`) and use its command directory, story paths, parity report path, review gate, QA result values, status vocabulary, and complete port story sequence. For each phase, read and follow the corresponding command spec under the configured command directory as the source of truth for steps and rules.

## Command-Agent Binding And Delegation

Before executing the sequence, load the configured house rules, this command spec, and the active workflow profile. For each phase, read the phase command spec and its configured agent definition before acting:

| Phase command | Agent binding |
|---|---|
| `/implement-story` | `agents.implementer` |
| `/review-story` | `agents.auditor` |
| `/verify-parity` | `agents.qa` |
| `/qa-story` | `agents.qa` |
| `/fix-from-qa` | `agents.implementer` |
| `/document-story` | `agents.docsPm` |
| `/validate-story` | `agents.qa` |

When subagent delegation is available, run each phase in the configured role subagent and pass the story ID, active workflow profile, command spec, loaded agent definition, oracle doc, parity report path, and defect ledger as binding context. If subagent delegation is unavailable, continue in the current chat only after loading the same agent definition and state in the output which phases used this fallback.

## Preconditions

- Story was created with `/plan-port-story`.
- Story has Phase P criteria and Z8 unless explicitly marked as a spike or documentation-only story.
- Covered behavior has no unresolved `E4` / `E5` provenance blockers.
- Oracle and defect ledger are current for covered behaviors.

## Sequence

1. Run `/implement-story {STORY-ID}`. The Implementer follows parity-first red-first behavior for Phase P.
2. Run `/review-story {STORY-ID}`. The Auditor must include `PAR-#` and `PROV-#` review categories for port stories.
3. If review gate blocks, return to implementation or planning depending on the finding.
4. Run `/verify-parity {STORY-ID}`. If parity is `FAIL` or `BLOCKED`, route mismatches through the defect ledger or implementation repair before continuing.
5. Run `/qa-story {STORY-ID}`.
6. If QA fails or blocks, run `/fix-from-qa {STORY-ID}` and then repeat `/verify-parity` and `/qa-story` for affected criteria.
7. Run `/document-story {STORY-ID}`.
8. Run `/validate-story {STORY-ID} complete`.

## Output

Return a Port Story Completion Summary:

- Story ID and final status.
- Review result and review artifact.
- Parity result and parity report.
- QA result.
- Documentation updates.
- Validation result.
- Any fallback phases used instead of subagent delegation.
- Remaining defects, deferred modernization debt, or forecast recalibration notes.

## Examples

- `/complete-port-story CALC-1`
- `/complete-port-story IMPORT-2`

This command is available in chat with `/complete-port-story`.
It expects one argument, the story ID.
