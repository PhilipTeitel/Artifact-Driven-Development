# validate-workflow-profile

Validate that a copied or customized Cursor workflow profile is complete enough for the agents, commands, and templates to use consistently.

## Inputs

- Optional profile path. Default resolution order:
  1. Target project `.cursor/workflow.config.yml`
  2. User profile `~/.cursor/workflow.config.yml`
  3. Documented defaults in `~/.cursor/workflow.config.yml`
- Optional mode:
  - `profile` — validate only the selected profile file.
  - `wiring` — validate that referenced agents, commands, and templates exist.
  - `all` — run both checks. This is the default.

## Checks

1. Resolve the active profile using the configured precedence order and report which file supplied each value when an override is present.
2. Verify these required top-level sections exist:
   - `profile`
   - `cursor`
   - `agents`
   - `templates`
   - `paths`
   - `workflow`
   - `methodology`
   - `status`
   - `review`
   - `qa`
   - `modernization`
   - `stack`
   - `naming`
   - `git`
   - `templateHandling`
3. Verify required path and template keys are present and non-empty:
   - `paths.designDoc`
   - `paths.purposeDoc`
   - `paths.domainDoc`
   - `paths.featuresDir`
   - `paths.requirementsDir`
   - `paths.decisionsDir`
   - `paths.reviewsDir`
   - `paths.auditFile`
   - `paths.storyGlob`
   - `paths.storyFilePattern`
   - `paths.modernizationDir`
   - `paths.assessmentDoc`
   - `paths.legacyMapDoc`
   - `paths.intentLedgerDoc`
   - `paths.dependencyLedgerDoc`
   - `paths.translationGapDoc`
   - `paths.defectLedgerDoc`
   - `paths.migrationPlanDoc`
   - `paths.oracleDoc`
   - `paths.behaviorGlob`
   - `paths.flowsDir`
   - `paths.parityReportPattern`
   - `templates.behaviorCatalog`
   - `templates.defectLedger`
   - `templates.dependencyLedger`
   - `templates.intentLedger`
   - `templates.legacyFlow`
   - `templates.legacyMap`
   - `templates.migrationPlan`
   - `templates.modernizationAssessment`
   - `templates.oracle`
   - `templates.parityReport`
   - `templates.portStory`
   - `templates.translationGap`
   - `templates.readme`
   - `templates.purpose`
   - `templates.domain`
   - `templates.skeleton`
   - `templates.adr`
   - `templates.requirements`
   - `templates.story`
   - `templates.audit`
   - `templates.storyReview`
4. Verify required agent bindings are present and non-empty:
   - `agents.architect`
   - `agents.archaeologist`
   - `agents.auditor`
   - `agents.docsPm`
   - `agents.implementer`
   - `agents.migrationStrategist`
   - `agents.modeler`
   - `agents.qa`
5. Verify workflow wiring:
   - every command named in `workflow.lanes`, `workflow.completeStorySequence`, `workflow.auditSequence`, `workflow.modernizationAssessSequence`, `workflow.legacyRecoverySequence`, and `workflow.completePortStorySequence` has a corresponding command spec in the configured commands directory
   - every configured template path exists
   - every configured agent path exists
   - every role-based command spec contains a `Command-agent binding:` line naming a configured `agents.<role>` key
   - orchestrator commands that sequence role work (for example `complete-story`, `audit-all`, `assess-modernization`, `document-legacy`, and `complete-port-story`) document subagent delegation and loaded-agent fallback behavior
6. Verify status and gate compatibility:
   - story statuses include open, active, and complete values
   - backlog statuses include open, active, and complete values
   - QA result values include pass, fail, and blocked values
   - review result values include pass and block values
   - assessment status values include go, go-with-conditions, and no-go values
   - `review.gate.blockOnSeverity` is non-empty
   - `review.summaryFormat` starts with `review.summaryLineLabel`
7. Verify methodology compatibility:
   - if `methodology.hexagonalPortsAdapters` is `required`, `methodology.portTestTypes` includes both configured contract and integration concepts
   - if `methodology.gherkinScenarioTraceability` is `required`, `naming.scenarioIdPattern` is set
   - if `methodology.modelFidelity` is `required`, `review.perStoryCategories` includes `Model Fidelity` and configured finding prefixes include `MODEL`
   - if `methodology.provenanceTraceability` is `required`, `review.perStoryCategories` includes `Provenance` and configured finding prefixes include `PROV`
   - if `methodology.parityEvidence` is `required`, `review.perStoryCategories` includes `Parity`, configured finding prefixes include `PAR`, and `templates.parityReport` is wired
   - if `methodology.walkingSkeleton` is `required`, `templates.skeleton` and `plan-skeleton` are wired
   - if `methodology.redFirstTesting` is `required`, `qa.evidenceReferenceExamples` is non-empty
8. Verify modernization defaults:
   - `modernization.legacyRepoPath`, `modernization.sourceStack`, and `modernization.targetStack` exist (they may be `TBD` until a project overrides them)
   - `modernization.oracleTier` is one of `T1 executable`, `T2 recorded`, or `T3 documented-only`
   - `modernization.evidenceGrades` defines `E1`, `E2`, `E3`, `E4`, and `E5`
   - `modernization.stagingStrategies` includes `strangler`, `phased-rewrite`, and `big-bang-parallel-run`
   - `modernization.structureFidelity` includes `preserve-then-refactor` and `refactor-now`
   - `modernization.defectPolicy` is set
   - `modernization.parity.numericTolerance` and `modernization.parity.textNormalization` are set
   - `templates.portStory` contains Phase P and Z8
   - `templates.parityReport` starts with `PARITY SUMMARY:`
9. Verify stack defaults:
   - `stack.packageManager`, `stack.buildCommand`, `stack.lintCommand`, and `stack.testCommand` are set
   - if `stack.typePolicy.disallowAny` is true, the profile also defines the shared type policy or explicitly documents why it does not apply
10. Verify template handling:
   - `templateHandling.neutralizeProjectSpecificExamples` is set so copied templates do not leak old project examples
11. Scan the profile for unresolved placeholder tokens such as `{TODO}`, `{path}`, `{STORY-ID}` in values that must be concrete at runtime. Placeholder tokens are allowed in naming patterns and artifact patterns.

## Output

Return a Workflow Profile Validation Matrix:

| Check | Result | Evidence | Fix recommendation |
|-------|--------|----------|--------------------|

Use configured QA-style result values when available (defaults: `PASS`, `FAIL`, `BLOCKED`).

Also return:

- Active profile path
- Overrides detected
- Missing or unreadable referenced files
- Missing command-agent bindings
- Missing or unreadable configured agent definitions
- Incompatible settings
- Unresolved placeholders

## Examples

- `/validate-workflow-profile`
- `/validate-workflow-profile .cursor/workflow.config.yml`
- `/validate-workflow-profile ~/.cursor/workflow.config.yml wiring`

This command is available in chat with `/validate-workflow-profile`.
