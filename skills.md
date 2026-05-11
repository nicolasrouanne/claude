---
title: Skills
nav_order: 5
has_children: true
---

# Skills

Custom slash commands available in Claude Code. Each skill is a `SKILL.md` file that defines a reusable workflow invoked with `/skill-name`.

Skills are stored in `~/.claude/skills/` (user-level) or `.claude/skills/` (project-level) and are symlinked from this repo.

| Skill | Description |
| ----- | ----------- |
| [`/billi-cra`]({{ site.baseurl }}/skills/billi-cra/) | Import/export CRAs between Excel and Billi (bidirectional sync) |
| [`/cii`]({{ site.baseurl }}/skills/cii/) | Dossier CII/CIR — accès Finalli et extraction temps personnel |
| [`/cra`]({{ site.baseurl }}/skills/cra/) | Suivi du temps — réconciliation Toggl, Billi CRA et git commits |
| [`/create-skill`]({{ site.baseurl }}/skills/create-skill/) | Create a new skill from conversation context, a file, or a description |
| [`/cross-post`]({{ site.baseurl }}/skills/cross-post/) | Cross-post content to LinkedIn, Twitter/X, and Slack |
| [`/find-skills`]({{ site.baseurl }}/skills/find-skills/) | Discover and install skills from the open agent skills ecosystem |
| [`/gogcli`]({{ site.baseurl }}/skills/gogcli/) | CLI for Gmail, Calendar, Drive, Contacts, Tasks, Sheets |
| [`/merge`]({{ site.baseurl }}/skills/merge/) | Merge a PR with merge commit, then clean up worktree |
| [`/new-project`]({{ site.baseurl }}/skills/new-project/) | Scaffold a full-stack project with backend and Next.js frontend |
| [`/notion-article`]({{ site.baseurl }}/skills/notion-article/) | Write and publish a blog article to Notion (EN + FR) |
| [`/pr`]({{ site.baseurl }}/skills/pr/) | Commit, branch, push, and create a pull request |
| [`/promote-permissions`]({{ site.baseurl }}/skills/promote-permissions/) | Promote ephemeral permissions to versioned settings |
| [`/review-apply`]({{ site.baseurl }}/skills/review-apply/) | Apply PR review feedback — reply to questions and implement changes |
| [`/sentry-triage`]({{ site.baseurl }}/skills/sentry-triage/) | Triage unresolved Sentry issues — analyze root causes and prioritize by impact |
| [`/tmba-process`]({{ site.baseurl }}/skills/tmba-process/) | Process a "Tech My Breath Away" meeting (Notion + Drive) |
| [`/toggl-calendar`]({{ site.baseurl }}/skills/toggl-calendar/) | Per-day, per-client timesheet calendar from Toggl |
| [`/transcribe`]({{ site.baseurl }}/skills/transcribe/) | Transcribe audio files using whisper-cpp locally |
| [`/update-knowledge`]({{ site.baseurl }}/skills/update-knowledge/) | Update `.claude/knowledge/` with architectural context and design rationale |
| [`/workspace`]({{ site.baseurl }}/skills/workspace/) | Load open Cursor editor tabs for context |
