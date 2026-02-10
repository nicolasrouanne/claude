---
name: merge
description: Merge a PR (with merge commit), then clean up worktree and prune merged branches via /worktree clean. Usage: /merge [pr-number]
title: /merge
parent: Skills
permalink: /skills/merge/
nav_order: 3
---

# Merge PR and Clean Up

Merge a pull request using a merge commit, then delegate cleanup to `/worktree clean`.

## Your Task

1. **Identify the PR to merge**:
   - If a PR number or URL is provided as an argument, use that.
   - Otherwise, detect the current branch and find its associated PR:
     ```bash
     gh pr view --json number,title,state,mergeStateStatus
     ```
   - If no PR is found, tell the user and stop.

2. **Check PR is ready to merge**:
   - Verify the PR state is `OPEN`.
   - Check `mergeStateStatus` — if it's `BLOCKED`, `BEHIND`, or `DIRTY`, warn the user and stop.

3. **Merge the PR**:
   ```bash
   gh pr merge <number> --merge
   ```
   - Always use `--merge` (merge commit), never squash or rebase.
   - Do NOT pass `--delete-branch` — branch cleanup is handled by `/worktree clean`.

4. **Delegate cleanup to `/worktree clean`**:
   After a successful merge, invoke the `/worktree clean` skill to:
   - Remove the worktree (if in one)
   - Prune all local branches that have been merged into main

## Important

- Always use merge commits (`--merge`), per project git preferences.
- If the merge fails, show the error and do not proceed to cleanup.
- If not in a worktree, `/worktree clean` will still prune merged branches.
