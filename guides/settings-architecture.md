# Claude Code Settings Architecture

This guide documents the complete Claude Code configuration setup across all projects.

## Settings Hierarchy

Claude Code settings cascade from user-level to project-level:

```
~/.claude/settings.json          <- User defaults (VERSIONED via symlink)
~/.claude/settings.local.json    <- User ephemeral accepts (NOT versioned)
~/dev/.claude/settings.json      <- Dev-level defaults
~/dev/.claude/settings.local.json <- Dev-level ephemeral
~/dev/project/.claude/settings.json <- Project defaults
~/dev/project/.claude/settings.local.json <- Project ephemeral
```

**Key concept**:
- `settings.json` = curated, should be version-controlled
- `settings.local.json` = accumulates "Allow" clicks, ephemeral by design

## Current Setup

### User Level (~/.claude/)

| File | Status | Notes |
|------|--------|-------|
| `settings.json` | Symlink → `~/dev/claude/config/settings.json` | Version controlled |
| `settings.local.json` | Local | Ephemeral accepts |

### Dev Level (~/dev/.claude/)

Project-wide settings when running Claude in `~/dev/` without a specific project.

### Project Level

Each project can have its own `.claude/` directory:
- `samm/` - Python/uv project
- `episto/` - Multi-project (webapp, app, chat, etc.)
- `billi/` - (no Claude config yet)

## Permissions Strategy

### Read-only commands (always allowed)

These are in the versioned `settings.json`:

```json
"Bash(git status:*)",
"Bash(git log:*)",
"Bash(git diff:*)",
"Bash(ls:*)",
"Bash(tree:*)",
"Bash(file:*)",
"Bash(which:*)"
```

### Write operations (project-appropriate)

```json
"Bash(git add:*)",
"Bash(git commit:*)",
"Bash(git push:*)",
"Bash(gh pr:*)"
```

### Tool-specific (add to projects as needed)

- Rails: `bundle exec`, `bin/rails`
- Python: `uv run`, `pytest`
- Node: `npm`, `yarn`, `pnpm`

## MCP Configuration

MCP servers are managed via CLI, not config files:

```bash
# List current MCP servers
claude mcp list

# Add user-level MCP (all projects)
claude mcp add notion npx -y mcp-remote https://mcp.notion.com/mcp -s user

# Add project-level MCP
claude mcp add playwright npx -y @playwright/mcp -s project

# Remove MCP
claude mcp remove notion -s user
```

### Current MCP Servers

| Server | Scope | Command |
|--------|-------|---------|
| notion | user | `npx -y mcp-remote https://mcp.notion.com/mcp` |

## Managing Permissions

### Promotion workflow

1. Work normally, accepting permissions as needed
2. Run `/promote-permissions` periodically
3. Review and approve promotions
4. PR gets created to update versioned settings

### Manual promotion

```bash
# Compare local vs versioned
diff ~/.claude/settings.local.json ~/.claude/settings.json

# Edit versioned settings
vim ~/dev/claude/config/settings.json

# Commit
cd ~/dev/claude && git add -A && git commit -m "Update permissions"
```

## Hooks

Configured in `settings.json`:

```json
"hooks": {
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "afplay /System/Library/Sounds/Submarine.aiff &"
    }]
  }]
}
```

## Symlink Setup

The root settings.json is symlinked to this repo:

```bash
ln -sf ~/dev/claude/config/settings.json ~/.claude/settings.json
```

To verify:
```bash
ls -la ~/.claude/settings.json
# -> /Users/nicolasrouanne/dev/claude/config/settings.json
```
