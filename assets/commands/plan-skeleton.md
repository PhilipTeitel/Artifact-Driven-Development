# plan-skeleton

This directs the **Architect** to create the walking-skeleton story from approved purpose, domain model, requirements, design, and ADRs. Before acting, resolve the workflow profile and use its configured purpose path, domain path, design doc, decisions directory, features directory, skeleton template, story file pattern, methodology settings, and status vocabulary.

The walking skeleton runs after `/design-application` and before `/plan-project` or feature `/plan-story` work. It proves that the intended product shape, domain model, architecture, composition root, and integration boundaries can execute together in the thinnest possible end-to-end slice.

## Why this exists

Some intent is tacit. Users often recognize "that is not what I meant" only when they see a running thing. The walking skeleton creates a cheap, traceable running slice early enough that purpose and domain deltas can still be folded back into artifacts before feature stories harden around the wrong model.

## Inputs

- Configured purpose document (default `docs/PURPOSE.md`).
- Configured domain model (default `docs/DOMAIN.md`).
- Approved refined requirements.
- Configured design doc (default `README.md`) containing the high-level architecture.
- Accepted ADRs for binding architectural decisions.

If purpose or domain artifacts are missing, stop and recommend `/define-purpose` or `/model-domain` unless the user explicitly asks for a spike that creates them.

## What the Architect will do

1. Resolve the workflow profile and read the configured walking-skeleton template (default `~/.cursor/templates/walking-skeleton-template.md`).
2. Read the configured purpose and domain artifacts, design doc, and linked ADRs.
3. Identify the composition root, driving surface, ports, adapters, and consistency boundaries the skeleton must exercise.
4. Create one skeleton story using the configured story file pattern. Recommended ID: `SK-1` unless the project uses a different story namespace.
5. Keep scope minimal:
   - one trivial end-to-end operation;
   - real or hermetic-trivial adapters for every planned boundary in scope;
   - no feature-complete business behavior beyond what proves the path;
   - one demo command and one integration/e2e proof.
6. Include a reflection checkpoint acceptance criterion that records human feedback after the demo:
   - requirement delta -> route to `/refine-feature`;
   - domain/model delta -> route to `/model-domain`;
   - no delta -> record that explicitly.
7. Update the configured design doc backlog or skeleton section with a link to the generated skeleton story when that section exists. Do not rewrite completed or in-progress backlog rows.

## Hard rules

- Do not create a mock-only skeleton. Mocks can support unit tests, but the skeleton proof must cross real or hermetic-trivial adapters at the boundaries it claims to prove.
- Do not plan full feature behavior. If a criterion is not needed to prove the running path, defer it to normal feature stories.
- Do not silently change purpose, domain language, architecture, ADRs, ports, or adapters. Stop with a **Tensions / conflicts** list when they disagree.
- Do not let the reflection checkpoint remain informal chat. Deltas must become requirements or domain model updates.

## Outputs

- A walking-skeleton story at the configured story path.
- A short chat summary listing: story ID/path, composition root, driving surface, boundaries exercised, demo command, and reflection routing.

## Follow-on loop

After `/plan-skeleton`, run:

```text
/implement-story SK-1
/review-story SK-1
/qa-story SK-1
/document-story SK-1
```

Then run the skeleton demo with the human:

1. If the demo reveals "that is not what I meant," record the delta in source material and rerun `/refine-feature` and/or `/model-domain`.
2. If the demo holds, proceed to `/plan-project` and normal feature `/plan-story` work.

This command is available in chat with `/plan-skeleton`.
It expects optional story ID/title arguments, for example: `/plan-skeleton SK-1`.
