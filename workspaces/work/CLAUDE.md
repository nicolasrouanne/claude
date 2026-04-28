# Qraft — Non-dev workspace

This is the workspace for qraft non-dev tasks:
- Time tracking (toggl)
- Content editing (notion)
- File management (gogcli / Google Drive)
- Client communications

## Notion

Always use the local Notion MCP server (`mcp__notion__API-*` tools) for all Notion operations. Never use the claude.ai Notion connector (`mcp__claude_ai_Notion__*`) — it connects to a different workspace and won't have access to Qraft pages.

## Skills utiles

- `/cii` — Dossier CII/CIR (Finalli, données de référence, temps personnel)
- `/cra` — Suivi du temps (Toggl, Billi CRA, git commits, réconciliation)
- `/toggl-calendar` — Timesheet Toggl par client/jour
- `/billi-cra` — Sync CRA Billi ↔ Excel/Sheets
