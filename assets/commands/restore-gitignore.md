---
description: Restore .gitignore from your canonical copy (run after Cursor updates)
---

# Restore .gitignore after Cursor overwrote it

Cursor can overwrite `~/.cursor/.gitignore` on updates. Your canonical version is kept in this folder so it is not touched.

**One-time restore (run in Terminal):**

```bash
~/.cursor/commands/restore-gitignore.sh
```

Or:

```bash
cp ~/.cursor/commands/gitignore-canonical.txt ~/.cursor/.gitignore
```

**To change the canonical rules:** Edit `commands/gitignore-canonical.txt`, then run the restore (or copy it to `.gitignore`) and commit both files.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
