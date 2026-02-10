---
title: Permissions
nav_order: 6
---

# Permissions

My user-level Claude Code permissions from [`config/settings.json`](https://github.com/nicolasrouanne/claude/blob/main/config/settings.json). These are symlinked to `~/.claude/settings.json` and apply to all projects.

## Bash Permissions

### Claude CLI

| Command | Pattern |
| ------- | ------- |
| Claude MCP (app) | `Bash(/Applications/Claude.app/Contents/Resources/app/bin/claude mcp:*)` |
| Claude MCP (cli) | `Bash(claude mcp:*)` |

### Git (read-only)

| Command | Pattern |
| ------- | ------- |
| `git status` | `Bash(git status:*)` |
| `git log` | `Bash(git log:*)` |
| `git diff` | `Bash(git diff:*)` |
| `git show` | `Bash(git show:*)` |
| `git rev-parse` | `Bash(git rev-parse:*)` |
| `git remote` | `Bash(git remote:*)` |
| `git fetch` | `Bash(git fetch:*)` |
| `git stash list` | `Bash(git stash list:*)` |
| `git config` | `Bash(git config:*)` |
| `git ls-files` | `Bash(git ls-files:*)` |
| `git branch` | `Bash(git branch:*)` |
| `git tag` | `Bash(git tag:*)` |

### Git (write)

| Command | Pattern |
| ------- | ------- |
| `git add` | `Bash(git add:*)` |
| `git checkout` | `Bash(git checkout:*)` |
| `git commit` | `Bash(git commit:*)` |
| `git push` | `Bash(git push:*)` |
| `git pull` | `Bash(git pull:*)` |
| `git reset` | `Bash(git reset:*)` |
| `git merge` | `Bash(git merge:*)` |
| `git rebase` | `Bash(git rebase:*)` |
| `git cherry-pick` | `Bash(git cherry-pick:*)` |
| `git stash` | `Bash(git stash:*)` |
| `git mv` | `Bash(git mv:*)` |
| `git worktree` | `Bash(git worktree:*)` |
| `git am` | `Bash(git am:*)` |
| `git format-patch` | `Bash(git format-patch:*)` |
| `git lfs fetch` | `Bash(git lfs fetch:*)` |
| `git lfs pull` | `Bash(git lfs pull:*)` |
| `git rm` | `Bash(git rm:*)` |
| `git check-ignore` | `Bash(git check-ignore:*)` |
| `git clean` | `Bash(git clean:*)` |

### GitHub CLI

| Command | Pattern |
| ------- | ------- |
| `gh pr` | `Bash(gh pr:*)` |
| `gh gist` | `Bash(gh gist:*)` |
| `gh issue` | `Bash(gh issue:*)` |
| `gh repo` | `Bash(gh repo:*)` |
| `gh api` | `Bash(gh api:*)` |
| `gh run` | `Bash(gh run:*)` |
| `gh workflow` | `Bash(gh workflow:*)` |
| `gh release` | `Bash(gh release:*)` |
| `gh search` | `Bash(gh search:*)` |

### File system & utilities

| Command | Pattern |
| ------- | ------- |
| `ls` | `Bash(ls:*)` |
| `tree` | `Bash(tree:*)` |
| `file` | `Bash(file:*)` |
| `which` | `Bash(which:*)` |
| `pwd` | `Bash(pwd)` |
| `wc` | `Bash(wc:*)` |
| `du` | `Bash(du:*)` |
| `df` | `Bash(df:*)` |
| `stat` | `Bash(stat:*)` |
| `md5` | `Bash(md5:*)` |
| `shasum` | `Bash(shasum:*)` |
| `mkdir` | `Bash(mkdir:*)` |
| `touch` | `Bash(touch:*)` |
| `curl` | `Bash(curl:*)` |
| `grep` | `Bash(grep:*)` |
| `cat` | `Bash(cat:*)` |
| `find` | `Bash(find:*)` |
| `lsof` | `Bash(lsof:*)` |
| `open -a` | `Bash(open -a:*)` |

### Ruby / Rails

| Command | Pattern |
| ------- | ------- |
| `bin/rails generate` | `Bash(bin/rails generate:*)` |
| `bin/rails runner` | `Bash(bin/rails runner:*)` |
| `bin/rails db:migrate` | `Bash(bin/rails db:migrate:*)` |
| `bundle exec rspec` | `Bash(bundle exec rspec:*)` |
| `bundle exec puma` | `Bash(bundle exec puma:*)` |
| `bundle exec rubocop` | `Bash(bundle exec rubocop:*)` |
| `bundle install` | `Bash(bundle install:*)` |
| `bundle` | `Bash(bundle:*)` |

### Python

| Command | Pattern |
| ------- | ------- |
| `uv run` | `Bash(uv run:*)` |
| `uv sync` | `Bash(uv sync:*)` |
| `uv pip` | `Bash(uv pip:*)` |
| `uv venv` | `Bash(uv venv:*)` |
| `pytest` | `Bash(pytest:*)` |

### npm

| Command | Pattern |
| ------- | ------- |
| `npm install` | `Bash(npm install:*)` |
| `npm ci` | `Bash(npm ci:*)` |
| `npm test` | `Bash(npm test:*)` |
| `npm run build` | `Bash(npm run build:*)` |
| `npm run lint` | `Bash(npm run lint:*)` |
| `npm run dev` | `Bash(npm run dev:*)` |
| `npm run start` | `Bash(npm run start:*)` |
| `npm list` | `Bash(npm list:*)` |
| `npm outdated` | `Bash(npm outdated:*)` |
| `npm version` | `Bash(npm version:*)` |
| `npm search` | `Bash(npm search:*)` |
| `npx eslint` | `Bash(npx eslint:*)` |

### yarn

| Command | Pattern |
| ------- | ------- |
| `yarn install` | `Bash(yarn install:*)` |
| `yarn test` | `Bash(yarn test:*)` |
| `yarn build` | `Bash(yarn build:*)` |
| `yarn lint` | `Bash(yarn lint:*)` |
| `yarn dev` | `Bash(yarn dev:*)` |
| `yarn start` | `Bash(yarn start:*)` |
| `yarn list` | `Bash(yarn list:*)` |
| `yarn outdated` | `Bash(yarn outdated:*)` |
| `yarn add` | `Bash(yarn add:*)` |
| `yarn serve` | `Bash(yarn serve:*)` |

### pnpm

| Command | Pattern |
| ------- | ------- |
| `pnpm install` | `Bash(pnpm install:*)` |
| `pnpm test` | `Bash(pnpm test:*)` |
| `pnpm build` | `Bash(pnpm build:*)` |
| `pnpm lint` | `Bash(pnpm lint:*)` |
| `pnpm dev` | `Bash(pnpm dev:*)` |
| `pnpm start` | `Bash(pnpm start:*)` |
| `pnpm list` | `Bash(pnpm list:*)` |

### Homebrew

| Command | Pattern |
| ------- | ------- |
| `brew install` | `Bash(brew install:*)` |
| `brew list` | `Bash(brew list:*)` |
| `brew info` | `Bash(brew info:*)` |
| `brew search` | `Bash(brew search:*)` |
| `brew update` | `Bash(brew update)` |
| `brew upgrade` | `Bash(brew upgrade:*)` |
| `brew services list` | `Bash(brew services list)` |
| `brew services start` | `Bash(brew services start:*)` |
| `brew services stop` | `Bash(brew services stop:*)` |

### Docker

| Command | Pattern |
| ------- | ------- |
| `docker run` | `Bash(docker run:*)` |
| `docker stop` | `Bash(docker stop:*)` |
| `docker rm` | `Bash(docker rm:*)` |
| `docker logs` | `Bash(docker logs:*)` |
| `docker compose exec` | `Bash(docker compose exec:*)` |
| `docker compose ps` | `Bash(docker compose ps:*)` |

### nvm

| Command | Pattern |
| ------- | ------- |
| `nvm use` | `Bash(nvm use:*)` |
| `nvm ls` | `Bash(nvm ls:*)` |
| `nvm list` | `Bash(nvm list:*)` |
| `nvm alias` | `Bash(nvm alias:*)` |
| `nvm current` | `Bash(nvm current:*)` |

### Other

| Command | Pattern |
| ------- | ------- |
| `test` | `Bash(test:*)` |
| `try` | `Bash(try:*)` |
| `afplay` | `Bash(afplay:*)` |
| `env` | `Bash(env)` |
| `echo` | `Bash(echo:*)` |
| `xxd` | `Bash(xxd:*)` |
| `unzip` | `Bash(unzip:*)` |
| `claude auth status` | `Bash(claude auth status:*)` |
| `tmux list-sessions` | `Bash(tmux list-sessions:*)` |

## Web Search

`WebSearch` is enabled globally.

## Hooks

### Stop Hook

Plays a sound when Claude finishes a task:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Submarine.aiff &"
          }
        ]
      }
    ]
  }
}
```

## Environment Variables

| Variable | Value |
| -------- | ----- |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `1` |

## Teammate Mode

`tmux` — teammates are spawned as tmux sessions.

## MCP Tool Permissions

Notion MCP tools (user-level scope):

| Tool | Description |
| ---- | ----------- |
| `mcp__notion__notion-search` | Search Notion pages |
| `mcp__notion__notion-fetch` | Fetch Notion page content |
| `mcp__notion__notion-create-pages` | Create new Notion pages |
| `mcp__notion__notion-update-page` | Update existing pages |
| `mcp__notion__notion-move-pages` | Move pages between parents |
| `mcp__notion__notion-duplicate-page` | Duplicate a page |
| `mcp__notion__notion-create-database` | Create databases |
| `mcp__notion__notion-update-database` | Update databases |
| `mcp__notion__notion-create-comment` | Add comments |
| `mcp__notion__notion-get-comments` | Read comments |
| `mcp__notion__notion-get-teams` | List teams |
| `mcp__notion__notion-get-users` | List users |
