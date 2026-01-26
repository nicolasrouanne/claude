---
name: pr
description: Commit changes, create a branch, push, and open a pull request. If working from an issue, automatically links it with "Closes #X".
---

# Create Pull Request

Streamlined workflow to commit, branch, push, and create a PR in one command.

## Your Task

1. **Check git status** to see what changes exist (staged, unstaged, untracked)
2. **Check git log** to understand recent commit message style
3. **Determine if there's an associated issue**:
   - Check the conversation context for any GitHub issue references (#123, issue URL, etc.)
   - If found, note the issue number for the PR body
   - If not found and changes suggest an issue context, ask the user
4. **Create a branch** with an appropriate name based on the changes (e.g., `fix/thing`, `feat/thing`)
5. **Stage and commit** the changes with a descriptive commit message following the repo's style
6. **Push** the branch to origin with `-u` flag
7. **Create the PR** using `gh pr create`

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
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Important

- Always check `git status` and `git diff` before committing
- Never commit sensitive files (.env, credentials, etc.)
- Stage specific files rather than using `git add -A`
- Return the PR URL at the end so the user can access it
