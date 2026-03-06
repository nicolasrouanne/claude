---
title: Slack MCP Setup
parent: Guides
---

# Slack MCP Setup

How to set up the Slack MCP server (`slack-mcp-server`) to read and post messages from Claude Code.

## Token types

The server supports three authentication modes:

| Token type | Env var | Posts as | Channel access | Expires |
|------------|---------|---------|----------------|---------|
| Bot token (`xoxb-`) | `SLACK_MCP_XOXB_TOKEN` | The bot app | Only channels where the bot is invited | No |
| User token (`xoxp-`) | `SLACK_MCP_XOXP_TOKEN` | You | All channels you're a member of | No |
| Browser session (`xoxc-`/`xoxd-`) | `SLACK_MCP_XOXC_TOKEN` + `SLACK_MCP_XOXD_TOKEN` | You | All channels you're a member of | Yes (on logout) |

**Recommended: user token (`xoxp-`)**. Posts as you, no need to invite a bot to channels, and doesn't expire.

If both `XOXP` and `XOXB` are set, the server uses the user token and ignores the bot token.

## Creating a Slack app and getting a user token

### 1. Create or edit a Slack app

Go to [api.slack.com/apps](https://api.slack.com/apps). Either create a new app or edit an existing one.

If creating from scratch: **Create New App** > **From an app manifest** > select your workspace > paste the manifest below.

### 2. App manifest

```json
{
  "display_information": {
    "name": "Claude Code",
    "description": "Claude Code Slack integration"
  },
  "oauth_config": {
    "scopes": {
      "bot": [],
      "user": [
        "channels:read",
        "channels:history",
        "chat:write",
        "groups:read",
        "groups:history",
        "im:read",
        "im:write",
        "im:history",
        "mpim:read",
        "mpim:history",
        "users:read",
        "search:read"
      ]
    }
  },
  "settings": {
    "org_deploy_enabled": false,
    "socket_mode_enabled": false,
    "token_rotation_enabled": false
  }
}
```

If editing an existing app: go to **App Manifest** (JSON tab), merge the `user` scopes above, save, and reinstall.

### 3. Install to workspace

Go to **Install App** (or **OAuth & Permissions** > **Reinstall to Workspace** if updating scopes). Authorize the app.

### 4. Copy the user token

After installation, go to **OAuth & Permissions**. Copy the **User OAuth Token** (starts with `xoxp-`).

### 5. Store the token

Add it to your shell config (e.g. `~/.zshrc`):

```bash
export SLACK_QRAFT_USER_TOKEN="xoxp-..."
```

Then `source ~/.zshrc`.

### 6. Configure `.mcp.json`

```json
{
  "mcpServers": {
    "slack-qraft": {
      "command": "/opt/homebrew/bin/slack-mcp-server",
      "args": ["-t", "stdio"],
      "env": {
        "SLACK_MCP_XOXP_TOKEN": "${SLACK_QRAFT_USER_TOKEN}",
        "SLACK_MCP_ADD_MESSAGE_TOOL": "true"
      }
    }
  }
}
```

### 7. Restart Claude Code

The MCP server is initialized at startup. Restart Claude Code to pick up the new token.

## Optional env vars

| Env var | Description |
|---------|-------------|
| `SLACK_MCP_ADD_MESSAGE_TOOL` | `true` to enable posting messages (disabled by default to prevent spam) |
| `SLACK_MCP_REACTION_TOOL` | `true` to enable emoji reactions, or comma-separated channel IDs to limit |
| `SLACK_MCP_MARK_TOOL` | `true` to enable marking channels as read |
| `SLACK_MCP_ATTACHMENT_TOOL` | `true` to enable downloading attachments |

## Multiple workspaces

Create one Slack app per workspace, each with its own token and MCP server entry. Example with two workspaces:

```json
{
  "mcpServers": {
    "slack-qraft": {
      "command": "/opt/homebrew/bin/slack-mcp-server",
      "args": ["-t", "stdio"],
      "env": {
        "SLACK_MCP_XOXP_TOKEN": "${SLACK_QRAFT_USER_TOKEN}",
        "SLACK_MCP_ADD_MESSAGE_TOOL": "true"
      }
    },
    "slack-episto": {
      "command": "/opt/homebrew/bin/slack-mcp-server",
      "args": ["-t", "stdio"],
      "env": {
        "SLACK_MCP_XOXB_TOKEN": "${SLACK_EPISTO_BOT_TOKEN}",
        "SLACK_MCP_ADD_MESSAGE_TOOL": "true"
      }
    }
  }
}
```
