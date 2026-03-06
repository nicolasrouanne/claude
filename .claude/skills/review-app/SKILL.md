---
name: review-app
description: "Deploy and test a PR on a review app. Adds the preview label, waits for deployment, then tests via API and Chrome DevTools. Usage: /review-app [pr-number] [test-instructions]"
title: /review-app
parent: Skills
permalink: /skills/review-app/
nav_order: 9
---

# Test on Review App

Deploy a PR to a review app environment and test it — first via API calls (backend), then via Chrome DevTools (end-to-end).

## Your Task

### 1. Parse the PR reference

- If no PR number provided: Use `gh pr view --json number,url` to get the PR for the current branch
- If a number is provided: Use that PR number
- Get PR details: `gh pr view <number> --json number,url,labels,body,headRefName`

### 2. Add the preview label

- Check if the PR already has the `🚀 preview` label
- If not, add it: `gh pr edit <number> --add-label "🚀 preview"`
- Inform the user that deployment has been triggered

### 3. Wait for deployment

- Watch the deployment workflow: `gh run list --branch <branch> --workflow "PR Environment - Deploy" --limit 1 --json status,conclusion,databaseId`
- Poll every 30 seconds until the workflow completes (use `gh run view <run-id> --json status,conclusion`)
- If deployment fails, report the error and stop: `gh run view <run-id> --log-failed`
- Once deployed, the review app is available at: `https://<PR_NUMBER>.pr-gcp.episto.fr`

### 4. Test via API (backend testing)

**Do this FIRST.** Test the backend directly via API calls to validate the changes before doing end-to-end testing.

- Base URL: `https://<PR_NUMBER>.pr-gcp.episto.fr/api`
- Use `curl` or the `WebFetch` tool to make API requests
- Test the specific endpoints affected by the PR changes
- Verify response codes, response bodies, and data integrity
- If the user provided test instructions, follow them for API testing
- If no specific instructions, infer what to test from the PR diff: `gh pr diff <number>`
- Report API test results to the user before proceeding

### 5. Test via Chrome DevTools (end-to-end testing)

**Do this SECOND**, after API tests pass. Use the Chrome DevTools MCP tools for browser-based end-to-end testing.

- Navigate to the review app: `mcp__chrome-devtools__navigate_page` to `https://<PR_NUMBER>.pr-gcp.episto.fr`
- Follow the user's test instructions to interact with the UI
- Use Chrome DevTools tools to:
  - `mcp__chrome-devtools__take_screenshot` — verify visual state
  - `mcp__chrome-devtools__click`, `mcp__chrome-devtools__fill` — interact with the UI
  - `mcp__chrome-devtools__list_network_requests` — verify API calls made by the frontend
  - `mcp__chrome-devtools__list_console_messages` — check for errors
  - `mcp__chrome-devtools__wait_for` — wait for elements or network requests
- Report any issues found (console errors, broken UI, failed requests)

### 6. Report results

Summarize the testing results in a table:

| Phase | Test | Result | Details |
|-------|------|--------|---------|
| API | endpoint description | pass/fail | response details |
| E2E | UI interaction | pass/fail | what happened |

## Database Modes

The review app supports two database modes (determined by the PR description):

- **Isolated (default)**: Creates a fresh `pr_<number>` database — clean slate, seeded data only
- **Shared**: Uses the `pullrequest` database — add `[shared-db]` to the PR description to use this mode

Consider the database mode when testing: isolated mode means no pre-existing data beyond seeds.

## Important

- **Always test API first, then E2E** — API tests are faster and catch backend issues before you spend time on browser testing
- If the review app is already deployed (label exists, no pending workflow), skip straight to testing
- The review app URL pattern is always `https://<PR_NUMBER>.pr-gcp.episto.fr`
- API endpoints are under `/api` path
- If no test instructions are provided, analyze the PR diff to determine what to test
- Ask the user for clarification if the changes are ambiguous and you're unsure what to test

## Usage Examples

- `/review-app` — Deploy and test the PR for the current branch
- `/review-app 42` — Deploy and test PR #42
- `/review-app 42 Test that the new filter on /api/v1/users works with role=admin` — Deploy PR #42 and run specific tests
