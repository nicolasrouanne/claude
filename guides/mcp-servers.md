---
title: MCP Servers
parent: Guides
---

# MCP Servers

Inventory of all MCP servers configured in Claude Code, what they do, and how they're scoped.

See also: [MCP Server Scopes]({{ site.baseurl }}/guides/mcp-server-scopes/) for how scoping works.

## User-level servers

These are available in every project (`-s user`, stored in `~/.claude.json`).

| Server | Transport | URL / Command | Description |
|--------|-----------|---------------|-------------|
| **sentry** | HTTP | `https://mcp.sentry.dev/mcp` | Error monitoring — search issues, view events, analyze with Seer, triage bugs. Powers the `/sentry-triage` skill. |
| **notion** | Stdio | `npx @notionhq/notion-mcp-server` | Notion workspace — search, read/write pages, databases, comments. Powers the `/notion-article` skill. |
| **fireflies** | HTTP | `https://api.fireflies.ai/mcp` | Meeting transcription — search transcripts, get summaries, list contacts. |
| **resend** | Stdio | `node ~/dev/mcp/mcp-send-email/build/index.js --key env:RESEND_API_KEY` | Email sending via Resend — send emails, manage contacts, audiences, broadcasts. Custom MCP server. |
| **chrome-devtools** | Stdio | `npx chrome-devtools-mcp@latest` | Chrome DevTools automation — click, fill, navigate, screenshot, evaluate JS, inspect network/console. |
| **cloudflare-observability** | HTTP | `https://observability.mcp.cloudflare.com/mcp` | Workers analytics — query logs, inspect keys/values, debug serverless functions. |
| **cloudflare-bindings** | HTTP | `https://bindings.mcp.cloudflare.com/mcp` | Cloudflare D1 databases and KV store bindings. |
| **cloudflare-radar** | HTTP | `https://radar.mcp.cloudflare.com/mcp` | Cloudflare Radar — internet intelligence, traffic patterns, threat data. |
| **cloudflare-browser** | HTTP | `https://browser.mcp.cloudflare.com/mcp` | Browser rendering via Cloudflare Workers Browser API. |
| **cloudflare-ai-gateway** | HTTP | `https://ai-gateway.mcp.cloudflare.com/mcp` | AI Gateway — LLM proxy, caching, rate limiting, logging. |

## Project-level servers

These are scoped to specific projects (local scope, stored in `~/.claude.json` under `projects.<path>`).

| Server | Transport | Project(s) | Description |
|--------|-----------|------------|-------------|
| **playwright** | Stdio | `~` (home), `~/dev/episto/webapp`, `~/dev/episto/backoffice-ui-next` | Browser testing automation — navigate, click, fill forms, screenshot, run accessibility audits. |
| **expo-mcp** | HTTP | `~/dev/samm` | Expo/React Native tooling for the SAMM mobile app. |
| **slite** | Stdio | `~/dev/episto` | Slite wiki/documentation — search and read internal Episto docs. |
| **toggl** | Stdio | `~/dev` | Time tracking via Toggl — log time entries, list projects. |

## Adding a new server

```bash
# User-level (available everywhere)
claude mcp add -s user --transport http <name> <url>

# Project-level (only current directory)
claude mcp add --transport http <name> <url>

# Stdio server
claude mcp add -s user <name> -- npx <package>
```

## Health check

```bash
claude mcp list
```

Servers showing "Needs authentication" require re-authenticating via the OAuth flow (open Claude Code and interact with the server to trigger it).
