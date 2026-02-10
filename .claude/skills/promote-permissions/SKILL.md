---
name: promote-permissions
description: Review ephemeral permissions in settings.local.json and promote approved ones to versioned settings.json, then create a PR
title: /promote-permissions
parent: Skills
permalink: /skills/promote-permissions/
nav_order: 7
---

# Promote Permissions

Promote useful permissions from ephemeral `settings.local.json` files to versioned settings (user-level, project-level, or both).

## Your Task

1. **Detect current directory** and check if it's a git repo with `.claude/settings.json`
2. **Read ephemeral permissions** from BOTH:
   - `~/.claude/settings.local.json` (user-level ephemeral)
   - `$CWD/.claude/settings.local.json` (current project ephemeral, if exists)
3. **Read versioned permissions** from:
   - `~/dev/claude/config/settings.json` (user-level versioned, symlinked to ~/.claude/settings.json)
   - `$CWD/.claude/settings.json` (project-level versioned, if exists)
4. **Find new permissions** that exist in local files but not in versioned
5. **Present each permission** with category and **recommended destination** (see below)
6. **Use AskUserQuestion** to let user select which permissions to promote AND where
7. **Update** the appropriate settings.json file(s) with approved permissions
8. **Create commits and PRs** for each repo with changes (see Commit Workflow below)

## Promotion Destinations

For each permission, recommend where it should go:

### User-Level (`~/dev/claude/config/settings.json`)
Permissions that are useful across ALL projects:
- **General git operations**: `git status`, `git log`, `git stash`, `git diff`, `git add`, `git commit`, `git push`
- **GitHub CLI**: `gh pr`, `gh issue`, `gh repo`, `gh api`
- **Safe read-only**: `ls`, `tree`, `which`, `pwd`
- **General dev tools**: `node --version`, `python --version`, `uv --version`

### Project-Level (`$CWD/.claude/settings.json`)
Permissions specific to THIS project:
- **Project-specific scripts**: `npm run <script>`, `pnpm <command>`, project Makefile targets
- **Project build tools**: `uv run pytest`, `uv run ruff`, `eas build` (if specific to project)
- **Project-specific paths**: commands referencing project directories
- **MCP tools**: `mcp__*` permissions (usually project-configured)
- **WebFetch for project APIs**: domains specific to project services

### Both (User + Project)
Sometimes a permission makes sense in both places:
- Common tool patterns that you also want versioned with the project for team sharing
- Example: `Bash(uv run pytest:*)` - useful globally AND should be in project for teammates

## Output Format

For each permission found, show:

```
Permission: Bash(uv run pytest:*)
Source: ~/dev/samm/.claude/settings.local.json
Category: Build tool (test runner)
Recommendation: BOTH - useful globally + share with project team
```

Then use AskUserQuestion with options for each permission:
- "User settings only"
- "Project settings only"
- "Both user and project"
- "Skip (don't promote)"

Group permissions by recommended destination when presenting.

## Files to Check

**Always check:**
- `~/.claude/settings.local.json` (user ephemeral)
- `$CWD/.claude/settings.local.json` (current project ephemeral, if exists)

**Versioned targets:**
- `~/dev/claude/config/settings.json` (user-level versioned)
- `$CWD/.claude/settings.json` (project-level versioned, if exists and is a git repo)

**Known project directories** (mention if CWD matches):
- `~/dev/samm`
- `~/dev/episto`
- `~/dev/claude`

## Commit Workflow

**IMPORTANT: Always create a PR for every repo with changes. Do not ask whether to create PRs.**

### For User-Level Changes (`~/dev/claude`)
1. Create branch `claude/promote-permissions-YYYY-MM-DD`
2. Stage and commit changes to `config/settings.json`
3. Push and create PR

### For Project-Level Changes (`$CWD`)
1. Create branch `chore/promote-permissions-YYYY-MM-DD`
2. Stage and commit changes to `.claude/settings.json`
3. Push and create PR

If promoting to BOTH, create commits and PRs in both repos.

## Commit Message Format

```
chore(claude): promote permissions from local settings

Promoted to [user/project/both]:
- Bash(command1:*)
- Bash(command2:*)
- WebFetch(domain:example.com)
```

## PR Format

Branch: `[claude|chore]/promote-permissions-YYYY-MM-DD`
Title: `chore(claude): promote permissions from local settings`
Body: List the promoted permissions, their categories, and why they were promoted to this location
