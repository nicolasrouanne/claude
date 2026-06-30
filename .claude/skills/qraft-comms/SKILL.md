---
name: qraft-comms
description: Generate Qraft communication drafts on a schedule — sense recent activity, propose 3 distinct post angles, and fully draft the strongest one. Read-only + drafts only (never publishes).
title: /qraft-comms
parent: Skills
permalink: /skills/qraft-comms/
nav_order: 32
---

# Qraft Comms — Communication Drafts

Generate Qraft communication material: sense what shipped, propose **3 distinct post angles**, and fully draft the strongest one — ready to hand to `/notion-article` (blog) or `/cross-post` (socials).

> **This skill is read-only + drafts only.** It never publishes, never posts to social, never sends anything. Output is a draft digest for Nicolas to review and approve. This is the v0 "cell" of the agent operating model — see the Notion strategy doc *Operating Model AI-augmenté*.

## Inputs

- Optional period as the first argument. **Default: since the last digest** in `~/qraft-comms/drafts/`, falling back to the **last 7 days** if there is none. Example override: `/qraft-comms 14d`.

## Context to load first (read-only)

1. `~/dev/claude/.claude/knowledge/qraft-context.md` — what Qraft is, the 3 pillars, clients, vocabulary.
2. `~/dev/claude/.claude/knowledge/writing-style.md` — Nicolas's voice. The drafted post **must** follow it (esp. the long-form/Notion + Slack registers and the "avoid" list).
3. **The last 3 digests** in `~/qraft-comms/drafts/` — so you don't repeat yourself. This runs daily; only surface what's **new** since the last run.

## Your Task

### 1. Sense recent Qraft activity (read-only)

Gather signal over the period:

- **Git activity** across Qraft repos. For each git repo under `~/dev` (notably `episto`, `billi`, `cevidentia`, `embarq`, `kado_brain`, `chutt`, `claude`), run:
  `git -C <repo> log --since="<period>" --no-merges --pretty=format:'%s'`
  and collect the notable, non-trivial subjects — shipped features, migrations, integrations, AI/agentic work. Skip chore/lint/bump noise.
- **Notion "idées de post" DB.** Search the local Notion MCP (`mcp__notion__API-post-search`) for the post-ideas database (title contains "idées" / "post"). Pull any unprocessed idea rows. If you can't find it, note that and continue.
- *(Optional)* Recent merged PRs via `gh pr list --state merged --search "merged:>=<date>"` for repos where `gh` is configured.

### 2. Propose 3 distinct angles

Pick three through **different lenses** so they don't overlap — diversity beats one obvious take — and **don't repeat angles already drafted in the last 3 digests**:

- **Technical insight** — a concrete thing built/learned this period (the avant/après write-up shape from writing-style.md, with a real detail).
- **Client / product value** — a problem solved for a client or product, framed for CTOs/tech leads (Qraft's target).
- **Agentic engineering / behind-the-scenes** — Qraft's positioning (Claude Code, MCP, agents in prod, "vos équipes agentic").

For each angle give: a one-line **hook** + a 1-line **rationale** (why it lands) + suggested **platform** (LinkedIn / X / Slack) + the **source** activity it draws from.

> **If nothing material is new** since the last digest, write a one-line "rien de neuf aujourd'hui" digest and stop — do not pad or invent. A quiet day is a valid output.

### 3. Draft the strongest one in full

Write ONE complete post (default **French**; mention an EN variant is available) for its suggested platform, in Nicolas's voice per writing-style.md:

- Direct first sentence, narrative frame, share the reasoning, honest/vulnerable tail, semantic emoji only.
- No buzzwords, no clickbait, none of the long-form "avoid" constructions.
- Self-contained and paste-ready for `/notion-article` or `/cross-post` — but **do not call them**.

### 4. Write the digest (the only write)

Write to `~/qraft-comms/drafts/<YYYY-MM-DD>.md` (create the dir if needed):

```
# Qraft Comms — <date>

## Activité sensée
<bullets: what shipped / ideas pulled, each with its source>

## 3 angles
1. <hook> — <platform> — <rationale> — source: <...>
2. ...
3. ...

## Post rédigé (<platform>, FR)
<the full draft>

## Pour publier (à ta main)
- Blog : `/notion-article` avec ce texte
- Réseaux : `/cross-post` avec ce texte
```

Then print a 3-line summary to stdout (so the scheduled runner captures it in the log).

### 5. (Optional) Notify Slack

If a `#nico-agents` channel exists in the `slack-qraft` workspace, post a 3-line summary + the digest file path there (`mcp__slack-qraft__conversations_add_message`). This is the "control away from your computer" hook. If the channel or tool isn't available, skip silently — never create the channel automatically.

## Hard constraints

- **Never publish / post to social / notion-publish.** Drafts only.
- **Read-only** except: writing the digest file, and the optional Slack notification to Nicolas's own channel.
- Do not auto-invoke `/cross-post` or `/notion-article`.
- If there isn't enough real activity, **say so honestly** — never invent news.

## Scheduling (local PoC)

See `schedule/` in this skill: `run.sh` (headless runner) + `com.qraft.comms.plist` (launchd, **daily 08:30**) + `README.md` (load / unload / test). **Run `/qraft-comms` by hand once first** to approve permissions and check the output, then enable the timer.
