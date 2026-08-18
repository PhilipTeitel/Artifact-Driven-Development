# document-legacy

Orchestrates recovery documentation after a modernization assessment is accepted or conditionally accepted. Before acting, resolve the workflow profile and use its command directory, modernization paths, behavior glob, purpose path, domain path, defect ledger path, evidence grades, and legacy recovery sequence.

## Command-Agent Binding And Delegation

Before executing the sequence, load the configured house rules, this command spec, and the active workflow profile. For each phase, read the phase command spec and its configured agent definition before acting:

| Phase command | Agent binding |
|---|---|
| `/catalog-behavior` | `agents.archaeologist` |
| `/trace-flow` | `agents.archaeologist` |
| `/recover-domain` | `agents.modeler` |
| `/ledger-defects` | `agents.archaeologist` |

When subagent delegation is available, run each phase in the configured role subagent and pass the legacy repo path, assessment, active workflow profile, command spec, and loaded agent definition as binding context. If subagent delegation is unavailable, continue in the current chat only after loading the same agent definition and state in the output which phases used this fallback.

## Inputs

- Accepted or conditionally accepted modernization assessment.
- Behavior, screen, entrypoint, or module scope to document.
- User documentation, release notes, or other source material.

## Preconditions

- `/assess-modernization` has produced a configured assessment document, or the user explicitly accepts skipping that gate.
- Legacy repo remains read-only.

## Sequence

1. Read the configured modernization assessment and stop if its verdict is `no-go` unless the user identifies a condition-resolution scope.
2. Run `/catalog-behavior` for the requested scope.
3. Run `/trace-flow` for the highest-risk or first planned behavior; repeat as needed for additional critical flows.
4. Run `/recover-domain` using the behavior catalog, intent ledger, and user documentation.
5. Run `/ledger-defects` for known mismatches, suspicious behavior, or legacy bugs surfaced during recovery.
6. Recommend `/refine-feature` against the ready `BEH-NNN` artifacts so recovered behavior becomes normal ADD requirements with `Sn` scenarios.

## Output

Return a Legacy Documentation Summary:

- Behavior artifacts created or updated.
- Flow artifacts created or updated.
- Purpose and domain artifacts created or updated.
- Defect decisions recorded and open.
- Weak evidence blockers (`E4` / `E5`).
- Delegation phases used or fallback phases used.
- Suggested next command.

## Examples

- `/document-legacy @docs/modernization/ASSESSMENT.md`
- `/document-legacy scope: pricing calculator`

This command is available in chat with `/document-legacy`.
It expects an assessment or source scope for recovery documentation.
