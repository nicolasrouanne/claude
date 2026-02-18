---
name: review-apply
description: "Apply PR review feedback — reply to questions and implement requested changes. Usage: /review-apply [pr-url-or-number]"
title: /review-apply
parent: Skills
permalink: /skills/review-apply/
nav_order: 8
---

# Apply PR Review Feedback

Fetch review comments on a PR, reply to questions, and implement requested code changes. By default, uses the PR associated with the current branch.

## Your Task

1. **Parse the PR reference**:
   - If no argument provided: Use `gh pr view --json number` to get the PR for the current branch. If no PR exists for the current branch, ask the user to specify a PR.
   - If given just a number: Use the current repo. Run `gh repo view --json owner,name` to get the current repo's owner and name.
   - If given a full URL: Parse out the owner/repo/pr from it.
2. **Fetch ALL review feedback**:
   - **Main review comments**: Use `gh api repos/{owner}/{repo}/pulls/{pr}/reviews` to get all reviews. Extract the review `id`, `body`, `state`, and `user.login` for each. The `body` field contains the top-level review comment (the main message the reviewer wrote when submitting their review). Ignore reviews with an empty body.
   - **Inline comments**: Use `gh api repos/{owner}/{repo}/pulls/{pr}/comments` to get all inline/file comments. Parse out the comment ID, file path, body, and diff hunk for each.
   - **Process main review comments first**, then inline comments. Main review comments often contain the most important feedback or overarching requests.
3. **Classify each comment** (both main review comments and inline comments) as one of:
   - **Question**: The reviewer is asking why something was done, requesting clarification, or asking if something is needed. Reply directly on the PR.
   - **Change request**: The reviewer wants code to be modified. Implement the change.
   - **Acknowledgment/approval**: No action needed.
4. **For questions**: Reply using `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="..."`. Provide clear, concise technical explanations.
5. **For change requests**:
   - Check out the PR branch (use a worktree if the current branch has uncommitted changes)
   - Implement the requested changes
   - Run linters/tests relevant to the changed files (check CLAUDE.md for commands)
   - Commit with a message like `fix: address review feedback` and push
   - Reply to the comment confirming the change was made
6. **Report back** to the user: summarize what was handled in a table. Include both main review comments and inline comments. Show: comment summary, type (question/change request/acknowledgment), and action taken.

## Replying to Comments

- **Main review comments**: Reply using `gh api repos/{owner}/{repo}/pulls/{pr}/reviews/{review_id}/comments -f body="..."` (this adds a comment to the review thread)
- **Inline comments**: Use `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="..."` to reply in-thread
- Keep replies concise and technical
- When explaining "why", reference the code behavior (e.g. "this returns nil which is checked on line X")
- Use plain URLs for same-repo permalinks (no markdown links — GitHub auto-unfurls them)

## Implementing Changes

- If on a different branch, use `git worktree add` to avoid disrupting current work
- Only modify files mentioned in the review
- Run relevant linters/tests before pushing
- Commit and push to the PR branch
- Clean up worktree after

## Important

- Always fetch the full review context before acting
- Don't guess what a comment means — if ambiguous, ask the user to clarify
- Group related comments (e.g. "Same..." refers to the previous comment's topic)
- When a comment says "Same..." or similar, check the preceding comments to understand the context

## Usage Examples

- `/review-apply` - Reviews the PR associated with the current branch
- `/review-apply 35` - Reviews PR #35 in the current repo
- `/review-apply https://github.com/owner/repo/pull/123` - Reviews a specific PR URL
