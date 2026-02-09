---
name: new-project
description: Scaffold a new full-stack project with Python/FastAPI backend (Scalingo) and Next.js frontend (Cloudflare Pages), initialize git/GitHub, and create planning issues.
---

# New Project Scaffolder

Create a new full-stack project following the established monorepo pattern: Python/FastAPI backend deployed on Scalingo (`api/`) and Next.js/TypeScript frontend deployed on Cloudflare Pages (`web/`).

## Input Handling

- **Argument required**: project name (kebab-case), e.g. `/new-project my-app`
- Optionally followed by a description in quotes: `/new-project my-app "A tool that does X"`
- If no argument provided, ask the user for project name and description using AskUserQuestion

## Your Task

### 1. Gather Information

Ask the user using AskUserQuestion:
- **Project description**: One-sentence summary of what this project does (if not provided as argument)
- **Scalingo region**: osc-fr1 (default) or osc-secnum-fr1
- **Visibility**: Public or private GitHub repo

### 2. Create Project Directory

```
~/dev/<project-name>/
├── api/                        # Python FastAPI backend
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry with CORS
│   │   └── routes.py           # API routes with /api prefix
│   ├── pyproject.toml           # uv project config
│   ├── .python-version          # Python 3.12
│   ├── Procfile                 # Scalingo deployment
│   └── .gitignore
├── web/                        # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout
│   │   │   └── page.tsx         # Home page
│   │   └── lib/
│   │       └── api.ts           # API client
│   ├── package.json             # Next.js + OpenNext + Cloudflare
│   ├── tsconfig.json
│   ├── next.config.ts
│   ├── wrangler.toml            # Cloudflare Workers config
│   ├── open-next.config.ts      # OpenNext.js Cloudflare adapter
│   ├── .env.local               # Dev API URL
│   ├── .env.production          # Prod API URL (Scalingo)
│   └── .gitignore
├── docs/                       # Product documentation
├── PLAN.md                     # Agent team workflow
└── README.md
```

### 3. Backend Setup (api/)

Create the following files:

**api/pyproject.toml:**
```toml
[project]
name = "<project-name>-api"
version = "0.1.0"
description = "<project-description>"
requires-python = ">=3.12"
dependencies = [
    "fastapi[standard]>=0.110.0",
    "httpx>=0.27.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.12.0",
]

[tool.ruff]
line-length = 100
```

**api/.python-version:**
```
3.12
```

**api/Procfile:**
```
web: PYTHONPATH=. python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**api/api/main.py:**
```python
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="<Project Title> API",
    description="<project-description>",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
```

**api/api/routes.py:**
```python
"""API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/hello")
async def hello() -> dict:
    return {"message": "Hello from <project-name>"}
```

**api/api/__init__.py:** empty file

**api/.gitignore:**
```
__pycache__/
.venv/
.ruff_cache/
.pytest_cache/
*.egg-info/
dist/
build/
```

### 4. Frontend Setup (web/)

**web/package.json:**
```json
{
  "name": "web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
    "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy"
  },
  "dependencies": {
    "@opennextjs/cloudflare": "^1.16.3",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^0.563.0",
    "next": "16.1.6",
    "radix-ui": "^1.4.3",
    "react": "19.2.3",
    "react-dom": "19.2.3",
    "tailwind-merge": "^3.4.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "eslint": "^9",
    "eslint-config-next": "16.1.6",
    "shadcn": "^3.8.4",
    "tailwindcss": "^4",
    "tw-animate-css": "^1.4.0",
    "typescript": "^5",
    "wrangler": "^4.63.0"
  }
}
```

**web/wrangler.toml:**
```toml
name = "<project-name>"
main = ".open-next/worker.js"
compatibility_date = "2025-08-31"
compatibility_flags = ["nodejs_compat"]

[assets]
directory = ".open-next/assets"
```

**web/open-next.config.ts:**
```typescript
import type { OpenNextConfig } from "@opennextjs/cloudflare";

const config: OpenNextConfig = {
  default: {
    override: {
      wrapper: "cloudflare-node",
      converter: "edge",
      proxyExternalRequest: "fetch",
      incrementalCache: "dummy",
      tagCache: "dummy",
      queue: "dummy",
    },
  },
  edgeExternals: ["node:crypto"],
  middleware: {
    external: true,
    override: {
      wrapper: "cloudflare-edge",
      converter: "edge",
      proxyExternalRequest: "fetch",
    },
  },
};

export default config;
```

**web/next.config.ts:**
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {};

export default nextConfig;
```

**web/tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**web/src/app/layout.tsx:**
```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "<Project Title>",
  description: "<project-description>",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
```

**web/src/app/page.tsx:**
```tsx
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold"><Project Title></h1>
      <p className="mt-4 text-lg text-gray-600"><project-description></p>
    </main>
  );
}
```

**web/src/app/globals.css:**
```css
@import "tailwindcss";
```

**web/src/lib/api.ts:**
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  return response.json();
}

export async function getHello(): Promise<{ message: string }> {
  return fetchApi("/hello");
}
```

**web/.env.local:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**web/.env.production:**
```
NEXT_PUBLIC_API_URL=https://<project-name>-api.<region>.scalingo.io/api
```

**web/.gitignore:** (standard Next.js gitignore)
```
/node_modules
/.pnp
.pnp.*
.yarn/*
!.yarn/patches
!.yarn/plugins
!.yarn/releases
!.yarn/versions
/coverage
/.next/
/out/
/build
.DS_Store
*.pem
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.env*
!.env.production
.open-next/
*.tsbuildinfo
next-env.d.ts
```

### 5. Root Files

**README.md:**
```markdown
# <Project Title>

<project-description>

## Tech Stack

| Layer    | Tech                    | Hosting          |
|----------|-------------------------|------------------|
| Backend  | Python 3.12, FastAPI    | Scalingo         |
| Frontend | Next.js 16, TypeScript  | Cloudflare Pages |

## Quick Start

### Backend
```bash
cd api
uv sync
uv run uvicorn api.main:app --reload
```

### Frontend
```bash
cd web
npm install
npm run dev
```

API runs on http://localhost:8000, frontend on http://localhost:3000.
```

**PLAN.md:** Create a plan following the car-tco pattern with 4 agent phases:
1. Discovery (product + devils-advocate)
2. Design (product + devils-advocate)
3. Build (backend-dev + frontend-dev, supervised by devils-advocate)
4. Validate (devils-advocate)

Adapt the agent roles and deliverables to the specific project.

### 6. Initialize Git and GitHub

Run the following commands sequentially:
1. `cd ~/dev/<project-name> && git init`
2. `git add -A && git commit -m "feat: scaffold project structure"`
3. `gh repo create <project-name> --<visibility> --source . --push`

### 7. Create GitHub Issues for Planning Phases

Create issues using `gh issue create` for each phase from the PLAN.md:

**Issue 1: Phase 1 - Discovery**
- Title: `Phase 1: Discovery - Product research & validation`
- Body: Product manager tasks, competitive analysis, brief, specs
- Labels: `planning`

**Issue 2: Phase 2 - Design**
- Title: `Phase 2: Design - Detailed specifications`
- Body: Technical specs, data model, API contract, UI wireframes
- Labels: `planning`

**Issue 3: Phase 3 - Build Backend**
- Title: `Phase 3a: Build - Backend API`
- Body: FastAPI routes, services, data layer, tests
- Labels: `backend`

**Issue 4: Phase 3 - Build Frontend**
- Title: `Phase 3b: Build - Frontend UI`
- Body: Next.js pages, components, API integration
- Labels: `frontend`

**Issue 5: Phase 4 - Validate & Deploy**
- Title: `Phase 4: Validate - Testing & deployment`
- Body: E2E tests, Scalingo deploy, Cloudflare Pages deploy
- Labels: `devops`

### 8. Install Dependencies

Run in parallel:
- `cd ~/dev/<project-name>/api && uv sync`
- `cd ~/dev/<project-name>/web && npm install`

### 9. Final Report

Print a summary:
- Project location: `~/dev/<project-name>/`
- GitHub repo URL
- Created issues (list with URLs)
- Next steps: "Run the project with `cd api && uv run uvicorn api.main:app --reload` and `cd web && npm run dev`"

## Guidelines

**DO:**
- Use exact versions from the car-tco reference for proven compatibility
- Create the `docs/` directory (empty, ready for specs)
- Set `.env.production` with the correct Scalingo URL pattern
- Create all GitHub issues with appropriate labels

**DON'T:**
- Don't add unnecessary dependencies beyond the base set
- Don't create complex business logic - just the scaffold
- Don't deploy anything - just set up the structure
- Don't create a CLAUDE.md in the project (the user will do that as needed)

## Example Usage

```
/new-project my-app
/new-project my-app "A marketplace for vintage furniture"
```
