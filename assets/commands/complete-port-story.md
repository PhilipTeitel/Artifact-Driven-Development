# complete-port-story

**Replaced by** [`/complete-story`](complete-story.md).

This command is a compatibility alias. Do not insert a separate `/verify-parity` step. Parity is a `parity` test level in the story test plan; `/qa-story` verifies those rows as ordinary acceptance criteria.

**Command-agent binding:** This command is role-bound as an orchestrator. Before executing any step, load the configured house rules and this command spec, then execute `/complete-story` with the same story ID and follow `complete-story.md` as the source of truth.
