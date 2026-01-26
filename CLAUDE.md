# Global Claude Code Instructions

## Versioning Preference

I maintain a dedicated repository for Claude Code configurations at `~/dev/claude/`.

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
