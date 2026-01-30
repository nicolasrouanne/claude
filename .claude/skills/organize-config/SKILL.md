# Organize Config Skill

Review and organize Claude Code configurations across user and project levels.

## Overview

This skill audits Claude configurations and helps determine the appropriate location for:
- **Instructions** (CLAUDE.md files)
- **Skills** (.claude/skills/)

**For permissions**, use `/promote-permissions` instead - it handles settings.local.json → settings.json promotion with full automation (branches, commits, PRs).

## Configuration Locations

### User-Level (`~/.claude/`)
Personal preferences that should follow you across all projects:
- **CLAUDE.md**: Personal coding style, global preferences, tool preferences
- **skills/**: Personal utility skills

### Project-Level (`$CWD/.claude/`)
Team-shared configurations specific to a codebase:
- **CLAUDE.md**: Codebase conventions, architecture notes, project-specific rules
- **skills/**: Project workflows (deploy, test, etc.)

## Audit Process

### Step 1: Gather Current Configuration

Read CLAUDE.md and skills from:
```
~/.claude/CLAUDE.md
~/.claude/skills/
$CWD/.claude/CLAUDE.md
$CWD/.claude/skills/
```

### Step 2: Categorize Each Item

**Instructions Classification:**

| Category | Location | Examples |
|----------|----------|----------|
| Personal style | User | "Use functional style", "Prefer X over Y" |
| Global tooling | User | Git preferences, formatting tools |
| Codebase rules | Project | Architecture patterns, file structure |
| Team conventions | Project | PR format, commit style, naming |
| Build/deploy info | Project | Scripts, environments, CI/CD |

**Skills Classification:**

| Category | Location | Examples |
|----------|----------|----------|
| Generic utilities | User | `/format-json`, `/summarize` |
| Project workflows | Project | `/deploy`, `/release`, `/test` |
| Team processes | Project | `/pr`, `/review` |

### Step 3: Present Findings

For each item, display:
- Current location
- Content summary
- Recommended location with reasoning
- Potential conflicts or duplicates

### Step 4: Collect Decisions

For each item needing attention:
1. **Keep current** - Leave as-is
2. **Move to user** - Personal preference
3. **Move to project** - Team-relevant
4. **Duplicate** - Useful in both places
5. **Remove** - No longer needed

## Decision Guidelines

### Move to User Root (`~/.claude/`) when:
- Applies to all your projects
- Personal coding preferences
- Won't be useful to other team members

### Move to Project (`$CWD/.claude/`) when:
- Specific to this codebase
- Other team members would benefit
- References project-specific paths, scripts, or tools
- Documents project architecture or conventions

### Keep in Both when:
- Universal best practice + project-specific details
- You want personal defaults that projects can override

## CLAUDE.md Organization Tips

**User CLAUDE.md should contain:**
- Your coding style preferences
- Your preferred tools/frameworks
- Personal git/GitHub workflows
- Default behaviors you always want

**Project CLAUDE.md should contain:**
- Codebase architecture overview
- Build and test commands
- Naming conventions for this project
- Important files/directories
- Team PR/commit guidelines
- Project-specific integrations

**Avoid in Project CLAUDE.md:**
- Personal preferences that don't affect the team
- Tool configurations that are user-specific
- Credentials or secrets

## Output Format

Present a summary table:

```
Configuration Audit Summary
===========================

PERMISSIONS (settings.local.json -> settings.json)
--------------------------------------------------
[MOVE TO USER]   Bash(git *)         Generic git operations
[MOVE TO PROJECT] Bash(npm run dev)  Project-specific script
[KEEP LOCAL]     Bash(secret-tool)   One-time use

INSTRUCTIONS (CLAUDE.md)
------------------------
[MOVE TO USER]   "Use TypeScript strict mode" - Personal preference
[KEEP IN PROJECT] "API routes in /src/api" - Project structure
[DUPLICATE]      "PR format guidelines" - Useful globally + project-specific

SKILLS
------
[MOVE TO USER]   /format-json - Generic utility
[KEEP IN PROJECT] /deploy - Project-specific workflow
```

## After Organizing

Remind user to:
1. Commit project-level changes to the project repo
2. Commit user-level changes to their claude config repo (`~/dev/claude/`)
3. Review any duplicates for consistency
