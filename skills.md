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
| [`/create-skill`](.claude/skills/create-skill/SKILL.md) | Create a new skill from conversation context, a file, or a description |
| [`/find-skills`](.claude/skills/find-skills/SKILL.md) | Discover and install skills from the open agent skills ecosystem |
| [`/merge`](.claude/skills/merge/SKILL.md) | Merge a PR with merge commit, then clean up worktree |
| [`/new-project`](.claude/skills/new-project/SKILL.md) | Scaffold a full-stack project with backend and Next.js frontend |
| [`/notion-article`](.claude/skills/notion-article/SKILL.md) | Write and publish a blog article to Notion (EN + FR) |
| [`/pr`](.claude/skills/pr/SKILL.md) | Commit, branch, push, and create a pull request |
| [`/promote-permissions`](.claude/skills/promote-permissions/SKILL.md) | Promote ephemeral permissions to versioned settings |
| [`/review-apply`](.claude/skills/review-apply/SKILL.md) | Apply PR review feedback — reply to questions and implement changes |
| [`/workspace`](.claude/skills/workspace/SKILL.md) | Load open Cursor editor tabs for context |
| [`/worktree`](.claude/skills/worktree/SKILL.md) | Create or clean up git worktrees for feature work |
