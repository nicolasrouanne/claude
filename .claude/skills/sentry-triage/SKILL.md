# Sentry Triage

Triage unresolved Sentry issues for any project. Analyze errors, identify root causes, prioritize by impact, and optionally apply fixes or update issue status.

## Invocation

```
/sentry-triage [project] [options]
```

- `project`: optional - a Sentry project slug, or `all` (default: `all`)
- Options: can include a Sentry issue URL, issue ID, or natural language filter (e.g., "last 24h", "critical", "affecting 100+ users")

## Workflow

### Step 0: Discover Sentry context

1. Use `mcp__sentry__find_organizations` to identify the organization slug and region URL
2. Use `mcp__sentry__find_projects` to list available projects
3. Cache these values for all subsequent calls

### Step 1: Fetch unresolved issues

Use `mcp__sentry__search_issues` to list unresolved issues. Apply the user's filters if provided.

- Default query: `unresolved issues from the last 7 days`
- If a specific project is requested, pass `projectSlugOrId` accordingly
- If triaging all projects, run searches for each project in parallel
- Request up to 25 issues per project

### Step 2: Prioritize and categorize

Group fetched issues into priority tiers based on:

1. **Critical** - High event count (100+ events), many affected users (10+), or unhandled exceptions
2. **High** - Moderate event count (10-99), recurring pattern, or affecting core functionality
3. **Medium** - Low event count (<10), limited user impact, or edge-case scenarios
4. **Low** - Informational, single occurrence, or non-impactful warnings

For each issue, present a summary table:

```
| Priority | Issue ID | Title | Events | Users | First Seen | Project |
```

### Step 3: Deep-dive on selected issues

For each critical/high issue (or issues the user selects):

1. **Get details**: Use `mcp__sentry__get_issue_details` with the issue ID
2. **Analyze tags**: Use `mcp__sentry__get_issue_tag_values` for `environment`, `browser`, `url`, and `release` tags to understand distribution
3. **AI root cause**: Use `mcp__sentry__analyze_issue_with_seer` for AI-powered root cause analysis and fix suggestions
4. **Find relevant code**: Search the local codebase for files mentioned in the stacktrace using Grep/Glob/Read tools

Present findings in this format for each issue:

```
### [ISSUE-ID] Issue Title

**Impact**: X events, Y users, environments: [list]
**First seen**: date | **Last seen**: date
**Release**: version

**Stacktrace summary**:
- file:line - function description

**Root cause** (from Seer analysis):
- Explanation of why this is happening

**Suggested fix**:
- Code-level fix recommendation

**Affected code in this repo**:
- file_path:line_number - relevant code context
```

### Step 4: Take action (if requested)

If the user asks to act on issues:

- **Resolve**: Use `mcp__sentry__update_issue` with `status: 'resolved'`
- **Ignore**: Use `mcp__sentry__update_issue` with `status: 'ignored'`
- **Assign**: Use `mcp__sentry__update_issue` with `assignedTo` parameter
- **Fix**: Propose and implement code changes in the local codebase, following the project's code standards

### Step 5: Summary report

After triaging, provide a summary:

```
## Triage Summary

**Scope**: [projects triaged] | **Period**: [time range]
**Total issues reviewed**: N

| Priority | Count | Action Taken |
|----------|-------|-------------|
| Critical | X     | details     |
| High     | X     | details     |
| Medium   | X     | details     |
| Low      | X     | details     |

### Recommended next steps
- Actionable items ranked by impact
```

## Rules

- Always discover the organization slug and region URL dynamically at the start (Step 0)
- Run parallel searches when triaging multiple projects
- When analyzing stacktraces, map Sentry file paths to the local repository structure using the project's directory layout
- Prefer Seer analysis for root cause over manual guessing
- When suggesting fixes, follow the project's code standards (check CLAUDE.md or linter configs)
- Don't resolve or ignore issues without explicit user confirmation
- If there are no unresolved issues, report that the project is healthy
