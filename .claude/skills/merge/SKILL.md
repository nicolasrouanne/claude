---
name: merge
description: "Merge a PR (with merge commit) and prune merged branches. Usage: /merge [pr-number]"
title: /merge
parent: Skills
permalink: /skills/merge/
nav_order: 3
---

# Merge PR and Clean Up

Merge a pull request using a merge commit, then prune stale local branches.

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

4. **Prune merged branches**:
   ```bash
   git checkout main
   git pull origin main
   git fetch --prune
   git branch --merged main | grep -v '^\*\|main' | xargs -r git branch -d
   ```
   Report which branches were pruned. If none, say "No stale branches to clean up."

## Important

- Always use merge commits (`--merge`), per project git preferences.
- If the merge fails, show the error and do not proceed to cleanup.
