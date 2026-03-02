---
name: pr
description: Commit changes, create a branch, push, and open a pull request. If working from an issue, automatically links it with "Closes #X".
title: /pr
parent: Skills
permalink: /skills/pr/
nav_order: 6
---

# Create Pull Request

Streamlined workflow to commit, branch, push, and create a PR in one command.

## Your Task

1. **Check git status and diff** to see what changes exist (staged, unstaged, untracked)
2. **Check git log** to understand recent commit message style
3. **Identify relevant changes**: Only include files and changes from the current conversation context. Ignore pre-existing uncommitted changes that are unrelated to the current task.
4. **Determine if there's an associated issue**:
   - Check the conversation context for any GitHub issue references (#123, issue URL, etc.)
   - If found in conversation, note the issue number for the PR body
   - If NOT found in conversation, **search recent open issues**: `gh issue list --state open --limit 20` and review titles
   - If an issue clearly matches the changes, link it automatically (no need to ask)
   - If unsure about a potential match, ask the user with `AskUserQuestion` listing the candidates
   - If no issue seems related and you're confident there isn't one, don't link and don't ask
5. **Create a feature branch**: The session runs in a `--worktree` so you're already on an isolated branch based on `origin/main`. Rename it to a descriptive branch name: `git branch -m <branch-name>`
6. **Run linters/tests before committing**: Check the project's CLAUDE.md or README for lint/test commands (e.g. rubocop, eslint, rspec). Run the relevant ones for the changed files. Fix any issues before proceeding.
7. **Stage and commit** only the relevant changes with a descriptive commit message following the repo's style
8. **Push** the branch to origin with `-u` flag
9. **Create the PR** using `gh pr create --base main`

## PR Body Format

If there's an associated issue, the PR body MUST start with `Closes #X`:

```markdown
Closes #123

## Summary
- Bullet points describing the changes

## Test plan
- [ ] Test steps

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

If there's NO associated issue, omit the `Closes` line:

```markdown
## Summary
- Bullet points describing the changes

## Test plan
- [ ] Test steps

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Branch Naming

Use conventional prefixes:
- `fix/` - Bug fixes
- `feat/` - New features
- `chore/` - Maintenance, CI, tooling
- `refactor/` - Code refactoring
- `docs/` - Documentation changes

Keep branch names short and descriptive (e.g., `fix/idempotent-mobile-build`).

## Commit Message Format

Follow the repository's existing commit style. Generally use conventional commits:
- `fix: description` for bug fixes
- `feat: description` for new features
- `chore: description` for maintenance

Always append:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Important

- Always check `git status` and `git diff` before committing
- Never commit sensitive files (.env, credentials, etc.)
- Stage specific files rather than using `git add -A`
- **Always target `main`** as the PR base branch
- **Only include changes from the current conversation context** — do not pull in unrelated uncommitted work
- Return the PR URL at the end so the user can access it
