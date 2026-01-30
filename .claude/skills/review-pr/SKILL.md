---
name: review-pr
description: Fetch PR review comments, reply to questions, and implement requested changes. Usage: /review-pr <pr-url-or-number>
---

# Handle PR Review

Fetch review comments on a PR, reply to questions, and implement requested code changes.

## Your Task

1. **Fetch the review comments**: Use `gh api repos/{owner}/{repo}/pulls/{pr}/comments` to get all review comments. Parse out the comment ID, file path, body, and diff hunk for each.
2. **Classify each comment** as one of:
   - **Question**: The reviewer is asking why something was done, requesting clarification, or asking if something is needed. Reply directly on the PR.
   - **Change request**: The reviewer wants code to be modified. Implement the change.
   - **Acknowledgment/approval**: No action needed.
3. **For questions**: Reply using `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="..."`. Provide clear, concise technical explanations.
4. **For change requests**:
   - Check out the PR branch (use a worktree if the current branch has uncommitted changes)
   - Implement the requested changes
   - Run linters/tests relevant to the changed files (check CLAUDE.md for commands)
   - Commit with a message like `fix: address review feedback` and push
   - Reply to the comment confirming the change was made
5. **Report back** to the user: summarize what was a question (replied), what was a change (implemented), and what needed no action.

## Replying to Comments

- Use `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="..."` to reply in-thread
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
