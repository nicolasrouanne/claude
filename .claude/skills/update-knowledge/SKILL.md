---
name: update-knowledge
description: Update .claude/knowledge/ files with architectural context and design rationale learned during the current session.
title: /update-knowledge
parent: Skills
permalink: /skills/update-knowledge/
nav_order: 20
---

<!-- Based on https://blog.junsuzuki.xyz/blog/beyond-claude-md-repo-scoped-knowledge-layer -->

# Update Knowledge Base

Capture architectural context, design rationale, and non-obvious patterns learned during this session into `.claude/knowledge/` files.

## Determine Target Location

First, detect where to write knowledge files:

1. **Check if we're in a git repository** with `git rev-parse --show-toplevel`
2. **If yes** (repo context): write to `<repo-root>/.claude/knowledge/`. Update the Knowledge Base table in the repo's `CLAUDE.md` if you create new files.
3. **If no** (no repo, spike, ad hoc session): write to `~/dev/claude/.claude/knowledge/`. These are cross-project insights. Update `~/dev/claude/.claude/knowledge/INDEX.md` if you create new files (create the index if it doesn't exist).

Create the target `.claude/knowledge/` directory if it doesn't exist yet.

## Your Task

1. **Review the conversation** for insights that would be valuable in future sessions:
   - Design decisions and their rationale (know-why)
   - Non-obvious patterns, gotchas, or procedural sequences (know-how)
   - Architectural constraints or trade-offs
   - Integration quirks with external services
   - Edge cases and failure modes discovered

2. **Check existing knowledge files** in the target directory to avoid duplication

3. **Update or create knowledge files**:
   - If an existing file covers the topic, update it with new insights
   - If no file covers it, create a new one with a descriptive name
   - Use kebab-case filenames (e.g., `auth-flow-gotchas.md`)
   - Trim stale content that no longer applies

## Knowledge File Format

Keep files focused and scannable:

```markdown
# Topic Title

## Section
Concise explanation of the pattern, gotcha, or rationale.
Include code snippets only when they clarify the point.
```

## What Belongs in Knowledge Files

- Architecture decisions and why alternatives were rejected
- Sync ordering, dependency chains, pipeline sequencing
- Workarounds for external API limitations
- Testing patterns specific to this project
- Integration-specific gotchas
- Procedural details (conventions, naming patterns, file structures)
- Edge cases that are easy to forget

## What Does NOT Belong

- Information derivable from reading the code (signatures, config values)
- Git history or changelog items
- Anything already in CLAUDE.md or docs/
- Ephemeral task details or session logs
- Deprecated features
