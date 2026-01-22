---
name: promote-permissions
description: Review ephemeral permissions in settings.local.json and promote approved ones to versioned settings.json, then optionally create a PR
---

# Promote Permissions

Promote useful permissions from ephemeral `settings.local.json` files to the versioned `settings.json`.

## Your Task

1. **Read ephemeral permissions** from `~/.claude/settings.local.json`
2. **Read versioned permissions** from `~/dev/claude/config/settings.json` (the symlink target)
3. **Find new permissions** that exist in local but not in versioned
4. **Present each new permission** to the user with context about what it does
5. **Use AskUserQuestion** to let user select which permissions to promote
6. **Update** `~/dev/claude/config/settings.json` with approved permissions
7. **Create a commit** in `~/dev/claude` with a descriptive message
8. **Ask if user wants a PR** - if yes, create branch and open PR

## Permission Analysis

When presenting permissions, categorize them:

- **Safe read-only**: `git status`, `git log`, `ls`, `tree`, `cat`, `head`
- **Git operations**: `git add`, `git commit`, `git push`, `git checkout`
- **GitHub CLI**: `gh pr`, `gh issue`, `gh repo`
- **Build tools**: `npm`, `yarn`, `uv`, `pytest`, `bundle`
- **Potentially sensitive**: anything with credentials, tokens, or URLs

## Output Format

For each permission found, show:

```
Permission: Bash(git stash:*)
Category: Git operation (safe)
First seen: (if available from context)
Recommendation: Promote to versioned settings
```

Then ask user to approve with checkboxes.

## Files to Check

Primary:
- `~/.claude/settings.local.json` (user ephemeral)
- `~/dev/claude/config/settings.json` (versioned target)

Optional project-level:
- `~/dev/.claude/settings.local.json`
- `~/dev/samm/.claude/settings.local.json`
- `~/dev/episto/.claude/settings.local.json`

## Commit Message Format

```
chore(claude): promote permissions from local settings

Promoted:
- Bash(command1:*)
- Bash(command2:*)
- WebFetch(domain:example.com)
```

## PR Format

Branch: `claude/promote-permissions-YYYY-MM-DD`
Title: `chore(claude): promote permissions from local settings`
Body: List the promoted permissions and their categories
