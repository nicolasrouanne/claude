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

> **Whose work gets posted.** Posts go out under **Nicolas's** name. So the signal that matters is what **Nicolas** personally contributed to or is aware of — not everything his teammates shipped. His git identity is `Nicolas Rouanne <nico.rouanne@gmail.com>` and GitHub handle `nicolasrouanne`. Prefer angles he can defend line by line; never draft a post about a teammate's PR he didn't touch or follow.

## Your Task

### 1. Sense recent Qraft activity (read-only)

Gather signal over the period from **four** sources, then cross-reference them. The unifying filter: **keep only what Nicolas contributed to or is aware of** (see the "Whose work gets posted" note above).

**a. Git — filtered to Nicolas's contributions.** For each git repo under `~/dev` (notably `episto`, `billi`, `cevidentia`, `embarq`, `kado_brain`, `chutt`, `claude`):
  - His own commits: `git -C <repo> log --since="<period>" --no-merges --author='nico.rouanne@gmail.com' --pretty=format:'%s'`
  - PRs he authored or reviewed (where `gh` is configured): `gh pr list --state all --search "author:@me updated:>=<date>"` and `gh pr list --state merged --search "reviewed-by:@me merged:>=<date>"`.
  - You **may** also scan the full team log for *context*, but only turn a teammate's work into an angle if Nicolas clearly followed it (reviewer, mentioned, or it shows up in his Notion/Claude activity). Skip chore/lint/bump noise.

**b. Notion — pages Nicolas edited himself.** Via the local Notion MCP, `mcp__notion__API-post-search` with an empty query sorted by `last_edited_time` descending. Keep pages edited within the period whose content he authored (technical write-ups, strategy notes, blog drafts). Also pull the **"idées de post" DB** (title contains "idées" / "post") for any unprocessed idea rows. If a search result is too large, it's saved to a file — parse it for `title` + `last_edited_time`. If you can't find something, note it and continue.

**c. Claude Code conversations — what Nicolas actually drove this week.** List recent session transcripts: `find ~/.claude/projects -maxdepth 2 -name '*.jsonl' -mtime -<days>` (skip `subagents/` and `wf_*`), then extract the first user prompt of each (`grep -m1 '"type":"user"'` + parse the JSON `message.content`). These reveal Qraft themes invisible in git — research he ran, docs he asked for, initiatives he's shaping.

**d.** *(Optional)* Recent merged team PRs via `gh pr list --state merged --search "merged:>=<date>"` — for background context only, per the filter above.

**Exclusions — never turn these into a post:**
- **Client-confidential**: contract/MSA negotiations, pricing, meeting prep, staff evaluations (e.g. Edgescale, ARRC, Chutt cadrage, semiannual dev reviews).
- **Litigation-private**: anything SAMM (see the litigation memories) — never public, ever.
- **Personal**: Nicolas's non-Qraft life (property, notaires, cars, personal knowledge base).

When you write the digest's *Activité sensée*, list an **Écarté** line naming what you dropped and why (teammate-only / confidential / private), so the filtering is auditable.

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
<bullets grouped by source (git / Notion / Claude convs), each with its source>
Écarté : <teammate-only / confidential / private items dropped, and why>

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

### 5. (Optional) Notify Slack — DM Nicolas

Send a 3-line summary + the digest file path to Nicolas as a **Slack DM** in the `slack-qraft` workspace (`mcp__slack-qraft__conversations_add_message`). Resolve his DM channel with `mcp__slack-qraft__users_search` ("Nicolas Rouanne" → `DMChannelID`). This is the "control away from your computer" hook. If a dedicated `#nico-agents` channel exists, you may post there instead. Never create a channel automatically; if Slack isn't available, skip silently.

## Hard constraints

- **Never publish / post to social / notion-publish.** Drafts only.
- **Read-only** except: writing the digest file, and the optional Slack notification to Nicolas's own channel.
- Do not auto-invoke `/cross-post` or `/notion-article`.
- If there isn't enough real activity, **say so honestly** — never invent news.

## Scheduling (local PoC)

See `schedule/` in this skill: `run.sh` (headless runner) + `com.qraft.comms.plist` (launchd, **daily 08:30**) + `README.md` (load / unload / test). **Run `/qraft-comms` by hand once first** to approve permissions and check the output, then enable the timer.
