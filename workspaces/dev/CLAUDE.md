# Dev workspace

Shared conventions for all development projects.

## Project structure
- `personal/` — personal dev projects (car-tco, roucraft)
- `claude/` — Claude Code configurations
- `qraft/` — qraft internal tooling
- `tries/` — experiments and spikes
- Everything else — client projects

## MCP config inheritance

Claude Code only loads `.mcp.json` from the session's project root, not from parent directories. The symlink `~/dev/.mcp.json → workspaces/dev/.mcp.json` only fires for sessions rooted directly at `~/dev/`.

For sub-projects under `~/dev/` (clients, qraft, tries…) that need the same MCP servers, symlink their root `.mcp.json` to this workspace config:

```bash
ln -s ~/dev/claude/workspaces/dev/.mcp.json ~/dev/<subproject>/.mcp.json
```

If the sub-project is a tracked git repo, also add `.mcp.json` to its `.gitignore` — the symlink points at your home and shouldn't be committed.
