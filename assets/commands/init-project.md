# init-project

This command sets up a new project scaffold for first-time use. **A human runs this** (no agent). It keeps project-to-project consistency: same template and structure so the architect and implementer always work from the same shape.

**Intended workflow:** (a) init-project → (b) architect designs the app → (c) architect creates the plan (epics/stories) → (d) architect creates the stories. Each step is separate so you can review and edit along the way and keep costs efficient.

Actions:

1. **Create a README.md from the standard template:**
   - Copy `~/.cursor/templates/readme-template.md` to your project root as `README.md`.
   - **You (human) may edit only:** the project title, the short description, and optionally the Table of Contents. Do **not** fill in any section from "High-Level Architecture" through "Backlog Items"—those are filled by the architect when designing and planning.
2. **Create the documentation directory structure:**
   - Create `docs/features` (and parent `docs` if needed). Story documents will live here (e.g. `docs/features/FND-1-initialize-frontend.md`).

3. *(Optional)* Add any other standard files (e.g. `.env.example`, `package.json`) per your team convention.

**Alternative:** If you prefer not to run init-project, you can point the architect at your requirements and ask it to design the app; the architect will create `README.md` from the template when it produces the design. Use init-project when you want the scaffold and directory in place first, then bring in the architect.

This command is available in chat with `/init-project`.

<!--
Copyright (c) 2026 Philip Teitel.
Licensed under the MIT License. See LICENSE for details.
-->
