# Global Claude Code Instructions

## Versioning Preference

I maintain a dedicated repository for Claude Code configurations at `~/dev/claude/`.
- Skills: `~/dev/claude/.claude/skills/` (symlinked from `~/.claude/skills`)
- Settings: `~/dev/claude/config/settings.json`
- **Always edit files in `~/dev/claude/`, never in `~/.claude/` directly**

When creating or modifying any of the following, remind me to commit and push to this repo:
- Settings files (`settings.json`, hooks, permissions)
- Skills (`.claude/skills/`)
- Guides or documentation
- CLAUDE.md files

After making changes to versioned Claude configs, ask: "Would you like to commit and push these changes to your claude repo?"

## GitHub Formatting

When posting comments to GitHub issues/PRs, use plain URLs (not markdown links) for permalinks to the same repository. GitHub auto-unfurls same-repo links, so markdown format like `[text](url)` creates unwanted code previews. Just paste the URL directly.

## Git Preferences

- Never push directly to main. Always create a branch and PR, even for small changes.
- When merging PRs, always use merge commits (`gh pr merge --merge`), not squash or rebase.
- When already on an unmerged feature branch, use `git worktree` to create a new branch for separate work. This keeps work isolated and avoids mixing changes.
- **Never merge PRs without explicit user approval.** Always ask before merging, even if CI passes and linting is clean. Validation is not approval.

## Workflow Conventions

- When asked to create a plan or analysis, default to posting it as a GitHub issue or document — do NOT start implementing unless explicitly asked to implement.

## Code Style & Principles

- Prefer simple, minimal solutions over complex ones. When proposing configurations, sampling logic, permissions, or refactorings, start with the simplest viable approach. Ask before adding complexity.
- When using factory data (polyfactory/factory_boy), always generate realistic values using Faker. Never set fields to None unless the field is explicitly nullable and optional.

## Security

- When promoting or suggesting permissions/security settings, err on the side of restrictive. Never recommend wildcard or broad permissions (e.g., `source:*`, `rm:*`, `kill:*`) without explicit user confirmation.

## Tech Stack

- Primary languages: Python (backend), TypeScript (frontend/mobile), Ruby
- Use ruff for Python linting
- For React Native testing, use Jest (not Vitest)
