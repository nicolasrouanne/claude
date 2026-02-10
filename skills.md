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
| [`/create-skill`]({% link .claude/skills/create-skill/SKILL.md %}) | Create a new skill from conversation context, a file, or a description |
| [`/find-skills`]({% link .claude/skills/find-skills/SKILL.md %}) | Discover and install skills from the open agent skills ecosystem |
| [`/merge`]({% link .claude/skills/merge/SKILL.md %}) | Merge a PR with merge commit, then clean up worktree |
| [`/new-project`]({% link .claude/skills/new-project/SKILL.md %}) | Scaffold a full-stack project with backend and Next.js frontend |
| [`/notion-article`]({% link .claude/skills/notion-article/SKILL.md %}) | Write and publish a blog article to Notion (EN + FR) |
| [`/pr`]({% link .claude/skills/pr/SKILL.md %}) | Commit, branch, push, and create a pull request |
| [`/promote-permissions`]({% link .claude/skills/promote-permissions/SKILL.md %}) | Promote ephemeral permissions to versioned settings |
| [`/review-apply`]({% link .claude/skills/review-apply/SKILL.md %}) | Apply PR review feedback — reply to questions and implement changes |
| [`/workspace`]({% link .claude/skills/workspace/SKILL.md %}) | Load open Cursor editor tabs for context |
| [`/worktree`]({% link .claude/skills/worktree/SKILL.md %}) | Create or clean up git worktrees for feature work |
