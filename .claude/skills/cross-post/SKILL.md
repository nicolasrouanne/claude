---
name: cross-post
description: Cross-post content to LinkedIn, Twitter/X, and Slack. Adapts content to each platform's format and constraints.
title: /cross-post
parent: Skills
permalink: /skills/cross-post/
nav_order: 11
---

# Cross-Post to Social Media

Cross-post content to LinkedIn, Twitter/X, and Slack. Can be used standalone or called from other skills (e.g., notion-article).

## Your Task

1. **Gather context** from one of these sources:
   - An article URL passed as argument (e.g., a Notion page URL)
   - A file path passed as argument
   - Current conversation context

2. **Ask the user** which platforms to cross-post to using AskUserQuestion with multiSelect:
   - LinkedIn
   - Twitter/X
   - Slack

   Only proceed with platforms the user selects.

3. **Generate platform-appropriate content** for each selected platform

4. **Show the user a preview** of each post before publishing

5. **Post using the corresponding MCP tool** and report results with links

## Platform-Specific Formats

### LinkedIn
Professional tone, 2-3 short paragraphs:
```
[Hook - personal insight or question]

[1-2 sentences on what I learned/built/discovered]

[Call to action + link to full article]

#relevantHashtags
```

Example:
```
I spent last week deep-diving into MCP servers and how they can automate content distribution.

The result? A workflow that publishes my articles to Notion, then cross-posts to LinkedIn, Twitter, and Slack—all from a single command.

Full write-up with code examples: [link]

#AI #Automation #DeveloperTools
```

### Twitter/X
280 characters max. Key insight + link:
```
[Punchy statement or question]

[Link to article]
```

Example:
```
TIL you can set up MCP servers to automate posting across Slack, LinkedIn, and Twitter from Claude Code.

Here's how I did it: [link]
```

### Slack
Brief summary with the article link. Use the configured channel.
```
:newspaper: New article: [Title]

[1-2 sentence summary]

:link: [Notion URL]
```

## MCP Tools Used

- **Slack**: `slack-mcp` → `add_message` tool
- **Twitter**: `twitter-mcp` → `post_tweet` tool
- **LinkedIn**: `linkedin-mcp` → `create_post` tool

If a platform's MCP server is not configured, inform the user and skip it.
See issue #14 in the claude repo for setup instructions.
