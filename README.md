# Claude Documentation

This folder contains documentation, guides, and notes related to Claude and Claude Code. It serves as a personal wiki for configuration, workflows, tips, and integrations.

## Contents

| Document | Description |
| -------- | ----------- |
| [Settings Architecture](./guides/settings-architecture.md) | Complete guide to Claude Code settings hierarchy, permissions, and MCP configuration |
| [Audio Notifications](./guides/idle-notification-sound.md) | How to set up audio notifications for Claude Code events (task completion, idle, permissions) |

## Skills

Custom slash commands available in Claude Code:

| Skill | Description |
| ----- | ----------- |
| `/promote-permissions` | Review ephemeral permissions and promote them to versioned settings, optionally creating a PR |

## Structure

```
claude/
├── README.md          # This file - index of all documentation
├── .claude/
│   └── skills/        # Custom Claude Code skills
│       └── promote-permissions/
├── config/            # Configuration files (symlinked from ~/.claude/)
│   └── settings.json  # User-level Claude settings
├── guides/            # Step-by-step tutorials and how-tos
└── notes/             # Personal notes and learnings
```

## Quick Setup

The root `~/.claude/settings.json` is symlinked to this repo:

```bash
ln -sf ~/dev/claude/config/settings.json ~/.claude/settings.json
```

## Adding a New Document

1. Create a new `.md` file in the appropriate folder
2. Add an entry to the Contents table above
3. Use descriptive filenames (e.g., `mcp-server-setup.md`)
