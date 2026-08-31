# plan-path-tests

**Replaced by** [`/refine-feature`](refine-feature.md).

This command is a compatibility alias. Do not write `docs/modernization/test-plans/XP-NNN-tests.md`. Comparison rules and oracle sources belong in the requirements file (`REQ-NNN` section 4b and Constraints). Story-level tests belong in `/plan-story` Section 8a as `parity` rows.

**Command-agent binding:** This command is role-bound to `agents.architect`. Before executing any step, load the configured Architect agent definition, then:

1. If the caller named a path detail or `XP-NNN`, tell them to run `/refine-feature` against that path detail (or to add section 4b to the existing REQ that already covers it).
2. If the caller named an existing REQ, tell them to record the comparison rule and oracle source on that REQ — do not create a parallel test-plan file.
3. Suggested next command is `/design-application` or `/plan-story`, not `/plan-port-story`.
