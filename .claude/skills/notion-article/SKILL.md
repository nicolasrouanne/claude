---
name: notion-article
description: Write and publish a blog article to Notion based on conversation context, a file, or a topic
---

# Notion Article Writer

Write blog articles based on context and publish them to the Notion Articles database.

## Your Task

1. **Gather context** from one of these sources:
   - Current conversation (default if no argument provided)
   - A file path passed as argument
   - A topic/description passed as argument

2. **Ask the user** using AskUserQuestion:
   - Language: EN or FR
   - Title suggestion (propose one based on context, let them edit)
   - Any specific angle or focus they want

3. **Write the article** following the tone guidelines below

4. **Publish to Notion** using the Articles database:
   - Database ID: `ac7ebcbdc95543a288361516f2043e8b`
   - Data Source ID: `410f70e5-33d0-434f-86b2-ef36dd1398d0`

5. **Set properties**:
   - Title: the article title
   - Language: EN or FR
   - Date: today's date
   - Author: `8aaaff03-f1fc-4020-b3aa-2b6f1e7016e2` (Nicolas)

6. **Ask if user wants a translation** - if yes, create the translated version and link them via the Translation property

## Tone Guidelines

**DO:**
- Write in first person ("I discovered...", "J'ai trouvé...")
- Use short, punchy sentences
- Include concrete examples and code snippets
- Be conversational, like explaining to a colleague
- Share genuine insights and "aha moments"
- Acknowledge limitations and mistakes honestly

**DON'T:**
- Use corporate buzzwords ("revolutionize", "game-changer", "leverage")
- Write grandiloquent titles ("The Future of X is Here")
- Be overly formal or distant
- Add unnecessary disclaimers
- Pad with filler content

## Article Structure

```markdown
**Author:** Nicolas Rouanne
**Date:** [Today's date in format: January 22, 2026 / 22 janvier 2026]
---

## [Opening hook - a question, confession, or surprising statement]

[1-2 paragraphs setting up the problem or context]

## [Main content sections]

[Use ## for major sections, ### for subsections]
[Include code blocks with ``` when relevant]
[Keep paragraphs short - 2-4 sentences max]

## [Practical takeaways or what I learned]

[Summarize key points]
[Be honest about limitations]

---
*[Optional closing note about how it was written/context]*
```

## Example Prompts for Context

If the user says `/notion-article` with no arguments, summarize the current conversation into an article.

If they provide a file: `/notion-article ./notes/meeting-notes.md` - transform those notes into a polished article.

If they provide a topic: `/notion-article "How we set up our CI/CD pipeline"` - write about that topic, asking clarifying questions as needed.

## Translation Linking

When creating a translation:
1. Create the translated article first
2. Get its page ID from the response
3. Update both articles' Translation property to link to each other

Use the relation property format:
```json
{"Translation": "https://www.notion.so/[page-id]"}
```
