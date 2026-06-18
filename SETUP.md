# Setup

This page explains how to install the Artifact-Driven Development Cursor workflow.

The reusable workflow lives in [`assets/`](assets/). It is copied into the user's Cursor configuration directory so the agents, commands, templates, and shared rules are available across projects.

## Prerequisites

- Cursor is installed.
- Git is installed.
- You have a local copy of this repository.

```sh
git clone <repo-url> Artifact-Driven-Development
cd Artifact-Driven-Development
```

## What Gets Installed

The install copies these files and directories:

| Source | Destination | Purpose |
|---|---|---|
| `assets/AGENTS.md` | `~/.cursor/AGENTS.md` | Shared house rules for all workflow agents |
| `assets/WORKFLOW.md` | `~/.cursor/WORKFLOW.md` | Workflow reference |
| `assets/workflow.config.yml` | `~/.cursor/workflow.config.yml` | Default workflow profile |
| `assets/agents/` | `~/.cursor/agents/` | Cursor agent definitions |
| `assets/commands/` | `~/.cursor/commands/` | Cursor slash commands |
| `assets/templates/` | `~/.cursor/templates/` | Artifact templates |

The workflow profile tells agents to ignore other application workflow sources, such as `~/.codex`, when resolving Cursor workflow material.

## Install On macOS Or Linux

Back up any existing Cursor workflow files before copying the ADD assets:

```sh
timestamp=$(date +%Y%m%d-%H%M%S)
backup_dir="$HOME/.cursor-backups/$timestamp"

mkdir -p "$backup_dir"

for path in AGENTS.md WORKFLOW.md workflow.config.yml agents commands templates; do
  if [ -e "$HOME/.cursor/$path" ]; then
    cp -R "$HOME/.cursor/$path" "$backup_dir/"
  fi
done
```

Copy the workflow assets:

```sh
mkdir -p "$HOME/.cursor/agents" "$HOME/.cursor/commands" "$HOME/.cursor/templates"

cp assets/AGENTS.md "$HOME/.cursor/AGENTS.md"
cp assets/WORKFLOW.md "$HOME/.cursor/WORKFLOW.md"
cp assets/workflow.config.yml "$HOME/.cursor/workflow.config.yml"

rsync -av assets/agents/ "$HOME/.cursor/agents/"
rsync -av assets/commands/ "$HOME/.cursor/commands/"
rsync -av assets/templates/ "$HOME/.cursor/templates/"
```

Reload Cursor after copying the files.

## Install On Windows PowerShell

From the repository root:

```powershell
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupDir = "$env:USERPROFILE\.cursor-backups\$Timestamp"
$CursorDir = "$env:USERPROFILE\.cursor"

New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
New-Item -ItemType Directory -Force -Path "$CursorDir\agents", "$CursorDir\commands", "$CursorDir\templates" | Out-Null

foreach ($Path in @("AGENTS.md", "WORKFLOW.md", "workflow.config.yml", "agents", "commands", "templates")) {
  $Existing = Join-Path $CursorDir $Path
  if (Test-Path $Existing) {
    Copy-Item -Recurse -Force $Existing $BackupDir
  }
}

Copy-Item -Force "assets\AGENTS.md" "$CursorDir\AGENTS.md"
Copy-Item -Force "assets\WORKFLOW.md" "$CursorDir\WORKFLOW.md"
Copy-Item -Force "assets\workflow.config.yml" "$CursorDir\workflow.config.yml"
Copy-Item -Recurse -Force "assets\agents\*" "$CursorDir\agents\"
Copy-Item -Recurse -Force "assets\commands\*" "$CursorDir\commands\"
Copy-Item -Recurse -Force "assets\templates\*" "$CursorDir\templates\"
```

Reload Cursor after copying the files.

## Verify The Install

Confirm the expected files exist.

macOS or Linux:

```sh
test -f "$HOME/.cursor/AGENTS.md"
test -f "$HOME/.cursor/workflow.config.yml"
ls "$HOME/.cursor/agents"
ls "$HOME/.cursor/commands"
ls "$HOME/.cursor/templates"
```

Windows PowerShell:

```powershell
Test-Path "$env:USERPROFILE\.cursor\AGENTS.md"
Test-Path "$env:USERPROFILE\.cursor\workflow.config.yml"
Get-ChildItem "$env:USERPROFILE\.cursor\agents"
Get-ChildItem "$env:USERPROFILE\.cursor\commands"
Get-ChildItem "$env:USERPROFILE\.cursor\templates"
```

In Cursor chat, the workflow slash commands should be available, including:

```text
/refine-feature
/design-application
/plan-project
/plan-story
/implement-story
/review-story
/qa-story
/document-story
```

You can also run:

```text
/validate-workflow-profile
```

That command checks profile completeness, workflow wiring, configured templates, status values, gates, methodology settings, and stack defaults.

## Use In A Project

Open the target application repository in Cursor. The default workflow writes project artifacts to:

- `README.md` for the design hub
- `docs/requirements/` for refined requirements
- `docs/decisions/` for ADRs
- `docs/features/` for story specs and story reviews
- `docs/reviews/` for diff reviews
- `audit-findings.md` for repository audit findings

A typical new feature flow is:

```text
/refine-feature @path/to/raw-notes.md
/design-application @docs/requirements/REQ-001-short-slug.md
/plan-project @docs/requirements/REQ-001-short-slug.md
/plan-story STORY-ID
/implement-story STORY-ID
/review-story STORY-ID
/qa-story STORY-ID
/document-story STORY-ID
```

For the full command sequence, see [`assets/WORKFLOW.md`](assets/WORKFLOW.md).

## Project-Level Overrides

The user-level profile at `~/.cursor/workflow.config.yml` provides defaults for all projects. A project can override those defaults by adding:

```text
.cursor/workflow.config.yml
```

Project-local values override the user profile key by key. Use this when a project needs different artifact paths, status vocabulary, command sequences, naming rules, or stack defaults.

The resolution order is:

1. Target project `.cursor/workflow.config.yml`
2. User profile `~/.cursor/workflow.config.yml`
3. Documented defaults in `~/.cursor/workflow.config.yml`

## Updating An Existing Install

After pulling changes to this repository, rerun the copy commands above. Keep the backup step if you've made any local changes to those files.

If the user customized the workflow, compare their current files against `assets/` before overwriting them.
