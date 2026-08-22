# mine-history

**Folded into** [`/inventory-paths`](inventory-paths.md) (path status) and [`/trace-path`](trace-path.md) (per-path citations).

This command is a compatibility alias. Do not write `docs/modernization/intent-ledger.md`. There is no separate intent ledger.

**Command-agent binding:** This command is role-bound to `agents.archaeologist`. Before executing any step, load the configured Archaeologist agent definition.

If the user asked for a whole-repo path list, execute `/inventory-paths` with the same arguments. If they named a path, behavior, or entrypoint, execute `/trace-path` once that `XP-NNN` exists. Follow those command specs as the source of truth.
