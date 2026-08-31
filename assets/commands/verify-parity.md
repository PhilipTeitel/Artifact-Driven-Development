# verify-parity

**Replaced by** [`/qa-story`](qa-story.md).

This command is a compatibility alias. Do not write `docs/modernization/parity/{STORY-ID}-parity.md`. Oracle comparison evidence belongs in the story's QA matrix for any criterion covered by a `parity` test row.

**Command-agent binding:** This command is role-bound to `agents.qa`. Before executing any step, load the configured QA agent definition, then execute `/qa-story` with the same story ID and follow `qa-story.md` as the source of truth.
