# document-legacy

Orchestrates slice-scoped recovery after a modernization assessment is accepted or conditionally accepted. Before acting, resolve the workflow profile and use its command directory, modernization paths, path glob, purpose path, domain path, defect ledger path, evidence grades, and legacy recovery sequence.

Recovery is per slice. Do not catalog the entire legacy system before the first port story.

## Command-Agent Binding And Delegation

Before executing the sequence, load the configured house rules, this command spec, and the active workflow profile. For each phase, read the phase command spec and its configured agent definition before acting:

| Phase command | Agent binding |
|---|---|
| `/trace-path` | `agents.archaeologist` |
| `/recover-domain` | `agents.modeler` |
| `/ledger-defects` | `agents.archaeologist` |

When subagent delegation is available, run each phase in the configured role subagent and pass the legacy repo path, assessment, slice scope, active workflow profile, command spec, and loaded agent definition as binding context. If subagent delegation is unavailable, continue in the current chat only after loading the same agent definition and state in the output which phases used this fallback.

## Inputs

- Accepted or conditionally accepted modernization assessment.
- Scope: migration-plan slice, or explicit `XP-NNN` IDs. If omitted, use the assessment's candidate first slice.
- User documentation, release notes, or other source material.

## Preconditions

- `/assess-modernization` has produced a configured assessment document, or the user explicitly accepts skipping that gate.
- The path inventory exists so `XP-NNN` IDs are stable.
- Legacy repo remains read-only.

## Sequence

1. Read the configured modernization assessment and stop if its verdict is `no-go` unless the user identifies a condition-resolution scope.
2. Resolve the `XP-NNN` IDs in scope. Do not trace paths outside that scope.
3. Run `/trace-path` for each in-scope path (or one grouped detail when they are the same operation).
4. Run `/recover-domain` using those path details and user documentation.
5. Run `/ledger-defects` for mismatches those paths surface. Refuse mis-posed system-wide defects.
6. Recommend `/refine-feature` against the ready path details, then `/plan-path-tests`.
7. Confirm README Artifact index rows for Path details, Purpose/Domain, and Defect ledger were updated by those phases. Do not rewrite **Lane status** (Migration Strategist) or Architect design sections.

## Output

Return a Legacy Documentation Summary:

- Scope (`XP-NNN` IDs).
- Path-detail files created.
- Purpose and domain artifacts created or updated.
- Defect decisions recorded and still open for this slice.
- Weak evidence blockers (`E4` / `E5`) in this slice.
- Delegation phases used or fallback phases used.
- Suggested next command.

## Examples

- `/document-legacy slice: VS-1`
- `/document-legacy XP-001 XP-002`

This command is available in chat with `/document-legacy`.
It expects an assessment and a slice or `XP-NNN` scope.
