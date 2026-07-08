# init-project

This command sets up a new project scaffold for first-time use. **A human runs this** (no agent). It keeps project-to-project consistency: same configured template and structure so the architect and implementer always work from the same shape. Resolve the workflow profile first and use its configured design doc, templates, and docs paths.

**Intended workflow:** (a) init-project → (b) architect designs the app → (c) architect creates the plan (epics/stories) → (d) architect creates the stories. Each step is separate so you can review and edit along the way and keep costs efficient.

Actions:

1. **Create the configured design doc from the standard template:**
   - Copy the configured design doc template (default `~/.cursor/templates/readme-template.md`) to your project root as the configured design doc (default `README.md`).
   - **You (human) may edit only:** the project title, the short description, and optionally the Table of Contents. Do **not** fill in any section from "High-Level Architecture" through "Backlog Items"—those are filled by the architect when designing and planning.
2. **Create the documentation directory structure:**
   - Create the configured features, requirements, decisions, and reviews directories as needed (defaults: `docs/features`, `docs/requirements`, `docs/decisions`, and `docs/reviews`). Story documents live in the configured features directory.
   - Leave the configured purpose and domain artifact paths ready for `/define-purpose` and `/model-domain` (defaults: `docs/PURPOSE.md` and `docs/DOMAIN.md`). Do not fill them during mechanical initialization.

3. *(Optional)* Add any other standard files (e.g. `.env.example`, `package.json`) per your team convention.

**Alternative:** If you prefer not to run init-project, you can point the architect at your requirements and ask it to design the app; the architect will create the configured design doc from the template when it produces the design. Use init-project when you want the scaffold and directory in place first, then bring in the architect.

This command is available in chat with `/init-project`.
