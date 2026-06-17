# audit-db

Audit this codebase for concrete database and persistence defects. Focus on SQL files, ORM schemas and models, migrations, seeds and fixtures, test data, and query patterns. Look for missing or weak primary keys, missing or incorrectly defined foreign keys, missing, redundant, or misordered indexes, schema drift across migrations, unsafe nullability or defaults that weaken data integrity, and overly broad or inefficient queries such as `SELECT *`. Before acting, resolve the workflow profile and use its configured audit file, audit template, and finding prefixes.

Read the configured audit file in the target repo root first and use it as the shared audit state. If it does not exist, create it from the configured audit template.

Update only:
- relevant rows in `Findings Summary`
- `Detailed Findings` -> `Database`

Do not overwrite unrelated sections or findings owned by other audit commands.
Use only the configured database finding prefix for rows and headings created by this command (default `DB-#`).
Keep the report aligned to the template exactly. Do not replace category findings with tables.

Before adding a finding:
- check whether the same issue is already captured elsewhere in the configured audit file
- if the risk is primarily an API, reliability, or performance issue with a shared root cause, note the overlap instead of creating a weaker duplicate
- omit speculative schema concerns that are not supported by concrete code, migration, fixture, or query evidence

Search recipes:
- missing or weak primary keys, foreign keys, unique constraints, or nullability safeguards
- redundant, missing, or misordered indexes on realistic query paths
- migration drift, incompatible defaults, or fixtures that hide integrity problems
- broad reads, `SELECT *`, or query shapes that can cause correctness or scalability issues

Only report issues you can tie to concrete schema definitions, queries, migrations, or data fixtures. For each finding, include:
- severity
- confidence
- file and line
- evidence checked
- affected schema, query, or data path
- failure mode or integrity/performance risk
- root cause
- minimal safe fix
- behavior to preserve
- a regression test idea
- verification
- related finding IDs or overlaps
- decision
- `Why not now` (`n/a` for `fix now`)

Prefer findings that can plausibly cause production correctness, integrity, or scalability problems.
