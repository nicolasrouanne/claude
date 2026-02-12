---
name: worktree
description: "Create or clean up a git worktree for feature work, with permission inheritance. Usage: /worktree <branch-name> or /worktree clean"
title: /worktree
parent: Skills
permalink: /skills/worktree/
nav_order: 10
---

# Git Worktree Manager

Create isolated worktrees for feature branches and clean them up when done.

## Your Task

Parse the argument to determine the action:

- **Branch name** (e.g., `/worktree feat/my-feature`): Create a new worktree
- **`clean`** (e.g., `/worktree clean`): Clean up a worktree
- **No argument**: Ask the user what they want to do

### Create a Worktree

1. **Determine the repo name and paths**:
   ```bash
   REPO_ROOT=$(git rev-parse --show-toplevel)
   REPO_NAME=$(basename "$REPO_ROOT")
   BRANCH_NAME="$1"  # the argument passed
   WORKTREE_DIR="$(dirname "$REPO_ROOT")/${REPO_NAME}-${BRANCH_NAME//\//-}"
   ```

2. **Fetch latest main**:
   ```bash
   git fetch origin main
   ```

3. **Create the worktree**:
   ```bash
   git worktree add "$WORKTREE_DIR" origin/main
   ```

4. **Create the feature branch inside the worktree**:
   ```bash
   cd "$WORKTREE_DIR"
   git checkout -b "$BRANCH_NAME"
   ```

5. **Copy permissions** from the original repo:
   ```bash
   # Copy project-level local settings if they exist
   if [ -f "$REPO_ROOT/.claude/settings.local.json" ]; then
     mkdir -p "$WORKTREE_DIR/.claude"
     cp "$REPO_ROOT/.claude/settings.local.json" "$WORKTREE_DIR/.claude/settings.local.json"
   fi
   ```

6. **Report back**:
   ```
   Worktree created at: <path>
   Branch: <branch-name>
   Permissions: copied from original repo

   To work in it: cd <path>
   To clean up later: /worktree clean
   ```

### Clean Up a Worktree

1. **List existing worktrees**:
   ```bash
   git worktree list
   ```

2. **If only one non-main worktree exists**, clean it up directly. If multiple exist, ask the user which one using AskUserQuestion.

3. **Remove the worktree**:
   ```bash
   git worktree remove <path>
   ```
   If the worktree has uncommitted changes, warn the user and ask for confirmation before using `--force`.

4. **Clean up the branch** if it's been merged:
   ```bash
   # Only delete if the branch was merged or the user confirms
   git branch -d <branch-name>
   ```

5. **Prune all local branches already merged into main**:
   ```bash
   # Switch back to main and pull latest
   git checkout main
   git pull origin main

   # Prune remote tracking branches that no longer exist
   git fetch --prune

   # Delete all local branches that have been merged into main (except main itself)
   git branch --merged main | grep -v '^\*\|main' | xargs -r git branch -d
   ```
   Report which branches were pruned. If none, say "No stale branches to clean up."

6. **Report back**:
   ```
   Worktree removed: <path>
   Branch <branch-name>: deleted (merged) / kept (unmerged)
   Pruned branches: <list of deleted branches, or "none">
   ```

## Important

- Never create worktrees inside the repo directory — always alongside it (sibling directory)
- Always copy `.claude/settings.local.json` to preserve permissions
- When cleaning, warn about uncommitted changes before removing
- The worktree naming convention is `<repo-name>-<branch-with-dashes>` (e.g., `myapp-feat-login`)
