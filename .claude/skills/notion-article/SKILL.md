---
name: notion-article
description: Write and publish a blog article to Notion based on conversation context, a file, or a topic. Optionally cross-post to LinkedIn, Twitter, and Slack.
---

# Notion Article Writer

Write blog articles based on context and publish them to the Notion Articles database.

## Your Task

1. **Gather context** from one of these sources:
   - Current conversation (default if no argument provided)
   - A file path passed as argument
   - A topic/description passed as argument

2. **Ask the user** using AskUserQuestion:
   - Title suggestion (propose one based on context, let them edit)
   - Any specific angle or focus they want

3. **Write the article in English first** following the tone guidelines below

4. **Publish English version to Notion** using the Articles database:
   - Database ID: `ac7ebcbdc95543a288361516f2043e8b`
   - Data Source ID: `410f70e5-33d0-434f-86b2-ef36dd1398d0`

5. **Set properties** for English version:
   - Title: the article title
   - Language: EN
   - Date: today's date
   - Author: `8aaaff03-f1fc-4020-b3aa-2b6f1e7016e2` (Nicolas)

6. **Always translate to French** - create the French version with:
   - Translated title
   - Language: FR
   - Same date and author

7. **Link both articles** via the Translation property (both directions)

## Tone Guidelines

**DO:**
- Write in first person, conversational ("I wanted to...", "J'ai essayé...")
- State the goal clearly in the opening paragraph
- Share genuine insights and what you learned
- Include code snippets and concrete examples
- Be honest about limitations and what didn't work
- Keep paragraphs short (2-4 sentences)

**DON'T:**
- Write clickbait titles ("The Future of X is Here", "X Will Change Everything")
- Use rhetorical questions as dramatic hooks ("Can AI really...?")
- Be grandiose about simple things - match the tone to the scope
- Pad with filler or unnecessary backstory
- Use buzzwords ("game-changer", "revolutionize", "leverage", "unlock")

## Article Structure

```markdown
**Author:** Nicolas Rouanne
**Date:** [Today's date in format: January 22, 2026 / 22 janvier 2026]
---

[Opening: what you wanted to achieve and why, in 1-2 short paragraphs]

## [Setup / How it works]

[Code snippets, steps, or explanation]

## [What works]

[Results, with concrete examples]

## [What doesn't work / Limitations]

[Be honest about gaps]

## [Practical use / Takeaways]

[When is this actually useful, what you'd do differently]
```

Keep the scope honest. A small hack is a small hack - don't frame it as a breakthrough.

## Example Prompts for Context

If the user says `/notion-article` with no arguments, summarize the current conversation into an article.

If they provide a file: `/notion-article ./notes/meeting-notes.md` - transform those notes into a polished article.

If they provide a topic: `/notion-article "How we set up our CI/CD pipeline"` - write about that topic, asking clarifying questions as needed.

## Translation Workflow

Since we always create both versions:

1. Create the English article first, note its page ID
2. Create the French article, note its page ID
3. Update English article's Translation property to link to French
4. Update French article's Translation property to link to English

Use the relation property format:
```json
{"Translation": "https://www.notion.so/[page-id]"}
```

## Important

- **Always write English first** - this is the source language
- **Always translate to French** - no need to ask, just do it
- **Always link both articles** - bidirectional Translation property

---

## Cross-Posting to Social Media

After publishing to Notion, **ask the user** which platforms to cross-post to using AskUserQuestion with multiSelect:

- LinkedIn
- Twitter/X
- Slack

Only proceed with platforms the user selects.

### Platform-Specific Formats

#### LinkedIn
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

#### Twitter/X
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

#### Slack
Brief summary with the article link. Use the configured channel.
```
:newspaper: New article: [Title]

[1-2 sentence summary]

:link: [Notion URL]
```

### Cross-Posting Workflow

1. After Notion articles are created and linked, ask:
   "Which platforms should I cross-post to?" (multiSelect: LinkedIn, Twitter, Slack)

2. For each selected platform:
   - Generate platform-appropriate content
   - Show the user a preview
   - Post using the corresponding MCP tool

3. Report results with links to each post

### MCP Tools Used

- **Slack**: `slack-mcp` → `add_message` tool
- **Twitter**: `twitter-mcp` → `post_tweet` tool
- **LinkedIn**: `linkedin-mcp` → `create_post` tool

If a platform's MCP server is not configured, inform the user and skip it.
See issue #14 in the claude repo for setup instructions.
