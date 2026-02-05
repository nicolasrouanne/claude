# MCP Server Scopes in Claude Code

When adding an MCP server with `claude mcp add`, the `--scope` (`-s`) flag determines where the config is stored and where the server is available.

## The 3 scopes

| Scope | Flag | Stored in | Applies to |
|-------|------|-----------|------------|
| **User** | `-s user` | `~/.claude.json` → `mcpServers` | All projects |
| **Project** | `-s project` | `.mcp.json` at project root | Anyone cloning the repo |
| **Local** | `-s local` (default) | `~/.claude.json` → `projects.<path>.mcpServers` | Only you, only that exact directory |

## Key gotcha

**Local scope does NOT inherit to subdirectories.** Adding an MCP server from `~/dev/` only makes it available when you launch Claude Code from `~/dev/` itself, not from `~/dev/some-project/`.

This is because local-scoped servers are keyed by exact directory path in `~/.claude.json`, under `projects.<path>.mcpServers`. There is no parent directory traversal.

## Commands

```bash
# Add a server available everywhere
claude mcp add -s user --transport http sentry https://mcp.sentry.dev/mcp

# Add a server for the current project (committed to repo via .mcp.json)
claude mcp add -s project --transport http sentry https://mcp.sentry.dev/mcp

# Add a server only for the current directory (default behavior)
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Remove from a specific scope
claude mcp remove sentry -s local
claude mcp remove sentry -s user
claude mcp remove sentry -s project

# List configured servers
claude mcp list
```

## Rule of thumb

- **User scope** for services you always want across all projects (Sentry, Notion, Fireflies, etc.)
- **Project scope** for repo-specific servers that teammates should also use (committed to `.mcp.json`)
- **Local scope** for personal servers tied to a single project that you don't want to share
