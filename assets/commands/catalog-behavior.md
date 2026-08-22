# catalog-behavior

**Replaced by** [`/trace-path`](trace-path.md).

This command is a compatibility alias. Do not write `docs/modernization/behaviors/BEH-NNN-*.md`. Execution paths use `XP-NNN`.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition, then execute `/trace-path` with the equivalent `XP-NNN` IDs (look them up in the path inventory; if the inventory does not exist, run `/inventory-paths` first). Follow `trace-path.md` as the source of truth.
