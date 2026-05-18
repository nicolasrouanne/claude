---
name: notion-article
description: Write and publish a blog article to Notion based on conversation context, a file, or a topic. Optionally cross-post to LinkedIn, Twitter, and Slack.
title: /notion-article
parent: Skills
permalink: /skills/notion-article/
nav_order: 5
---

# Notion Article Writer

Publish a Notion article based on conversation context, a file, or a topic. This skill owns the **publishing mechanics**; the tone and structure live in `.claude/knowledge/writing-style.md` (universal voice + "Notion / long-form docs" section) — read it before drafting.

## Destinations

| Destination | Parent | Languages | Used for |
|---|---|---|---|
| **Articles database** | `ac7ebcbdc95543a288361516f2043e8b` (data source `410f70e5-33d0-434f-86b2-ef36dd1398d0`) | EN + FR, linked via `Translation` | External-facing posts (qraft.tech blog, cross-post to LinkedIn / X / Slack) |
| **Tech subpage** | `189218ed56d78019b206d49417bafa31` (page `Tech` in qrafttech) | FR only | Internal write-ups, TBMA decks |

Ask with AskUserQuestion if the destination isn't obvious. Default to **Tech subpage** for internal infra / tooling / process; default to **Articles database** when the user mentions blog, publication, LinkedIn, or X.

## Workflow

1. Gather context from the conversation, a file path, or a topic argument.
2. Ask the user: destination (if not obvious), title (propose one, let them edit), angle.
3. Read `.claude/knowledge/writing-style.md` and apply it.
4. Draft and publish per destination (below).

### Articles database

Write English first, then French, then link both. Properties for each language version:

| Property | Value |
|---|---|
| Title | the article title (translated for FR) |
| Language | `EN` or `FR` |
| Date | today |
| Author | `8aaaff03-f1fc-4020-b3aa-2b6f1e7016e2` (Nicolas) |
| Translation | URL of the sibling-language page |

Set both `Translation` relations after both pages exist:

```json
{"Translation": "https://www.notion.so/[page-id]"}
```

### Tech subpage

FR only. Plain Notion page (no database properties). Parent = `189218ed56d78019b206d49417bafa31`. Optional icon emoji aligned with the topic.

## Argument forms

- `/notion-article` — summarize the current conversation into an article.
- `/notion-article ./notes/meeting-notes.md` — transform those notes.
- `/notion-article "topic description"` — write about that topic, ask clarifying questions if needed.

## Cross-posting

After publishing an **Articles-database** post, invoke `/cross-post` with the English page URL to offer LinkedIn / X / Slack cross-posting. Tech subpages are internal — do not cross-post.
