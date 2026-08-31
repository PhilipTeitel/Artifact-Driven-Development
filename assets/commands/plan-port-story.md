# plan-port-story

**Replaced by** [`/plan-story`](plan-story.md).

This command is a compatibility alias. Do not use a separate port-story template. Recovered legacy behavior reaches delivery through `REQ-NNN` section 4b; `/plan-story` copies that provenance into the ordinary story spec.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition, then execute `/plan-story` with the story ID and follow `plan-story.md` as the source of truth. Treat any extra `XP-NNN` or slice arguments as hints to read the matching REQ provenance and migration-plan row.
