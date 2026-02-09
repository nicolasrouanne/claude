---
name: new-project
description: Scaffold a new full-stack project with backend (Scalingo) and Next.js frontend (Cloudflare Pages), initialize git/GitHub, and create planning issues.
---

# New Project Scaffolder

Create a new full-stack monorepo with `api/` backend deployed on Scalingo and `web/` frontend (Next.js) deployed on Cloudflare Pages.

## Input Handling

- **Argument required**: project name (kebab-case), e.g. `/new-project my-app`
- Optionally followed by a description: `/new-project my-app "A tool that does X"`
- If no argument, ask the user for project name and description

## Your Task

### 1. Gather Information

Ask the user using AskUserQuestion:
- **Project description** (if not provided as argument)
- **Backend stack**: Python (FastAPI) or Node.js (NestJS)
- **Scalingo region**: osc-fr1 (default) or osc-secnum-fr1
- **GitHub visibility**: Public or private

### 2. Create Project Structure

```
~/dev/<project-name>/
├── api/                        # Backend
├── web/                        # Next.js frontend
├── docs/                       # Product documentation (empty)
├── PLAN.md                     # Agent team workflow
└── README.md
```

### 3. Backend Setup (api/)

#### If Python (FastAPI):

Scaffold a minimal FastAPI app with:
- `uv` as package manager (pyproject.toml, uv.lock)
- Python 3.12 (.python-version)
- `Procfile` for Scalingo: `web: PYTHONPATH=. python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- FastAPI app with CORS middleware and `/health` + `/api/hello` endpoints
- Dev tooling: `ruff` (linter/formatter), `ty` (type checker), `pytest`
- Standard .gitignore for Python

#### If Node.js (NestJS):

Scaffold a minimal NestJS app with:
- `pnpm` as package manager
- `Procfile` for Scalingo: `web: node dist/main.js`
- NestJS app with CORS enabled and `/health` + `/api/hello` endpoints
- Dev tooling: `eslint`, `prettier`
- Standard .gitignore for Node

### 4. Frontend Setup (web/)

Scaffold a Next.js 16 app with:
- `pnpm` as package manager
- TypeScript, Tailwind CSS 4, shadcn/ui
- OpenNext.js + Cloudflare Workers adapter (wrangler.toml, open-next.config.ts)
- Dev tooling: `eslint`, `prettier`
- Scripts: `dev`, `build`, `preview` (opennextjs-cloudflare), `deploy` (opennextjs-cloudflare)
- `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
- `.env.production` with `NEXT_PUBLIC_API_URL=https://<project-name>-api.<region>.scalingo.io/api`
- Minimal API client in `src/lib/api.ts` using `NEXT_PUBLIC_API_URL`
- Standard .gitignore for Next.js + Cloudflare

### 5. Root Files

- **README.md**: Project title, description, tech stack table, quick start commands
- **PLAN.md**: Agent team workflow with 4 phases:
  1. Discovery (product + devils-advocate)
  2. Design (product + devils-advocate)
  3. Build (backend-dev + frontend-dev, supervised by devils-advocate)
  4. Validate (devils-advocate)

Adapt roles and deliverables to the specific project.

### 6. Initialize Git and GitHub

1. `git init`
2. `git add -A && git commit -m "feat: scaffold project structure"`
3. `gh repo create <project-name> --<visibility> --source . --push`

### 7. Create GitHub Issues

Create one issue per planning phase from PLAN.md using `gh issue create`:
- Phase 1: Discovery - Product research & validation (`planning` label)
- Phase 2: Design - Detailed specifications (`planning` label)
- Phase 3a: Build - Backend API (`backend` label)
- Phase 3b: Build - Frontend UI (`frontend` label)
- Phase 4: Validate - Testing & deployment (`devops` label)

### 8. Install Dependencies

Run in parallel:
- Backend: `uv sync` (Python) or `pnpm install` (Node)
- Frontend: `pnpm install`

### 9. Final Report

Print a summary with project location, GitHub repo URL, created issue URLs, and quick start commands.

## Guidelines

**DO:**
- Keep the scaffold minimal - just enough to run and deploy
- Use modern tooling: uv/ruff/ty (Python), pnpm/eslint/prettier (Node/TS)
- Create the `docs/` directory (empty, ready for specs)

**DON'T:**
- Don't add business logic beyond hello/health endpoints
- Don't deploy anything - just set up the structure
- Don't create a CLAUDE.md (user will add as needed)

## Example Usage

```
/new-project my-app
/new-project my-app "A marketplace for vintage furniture"
```
