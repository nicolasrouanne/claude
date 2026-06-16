---
name: cloudflare-workers-nextjs
description: Deploy a Next.js 16 app to Cloudflare Workers via OpenNext, with Workers Builds for automatic PR preview deployments.
title: /cloudflare-workers-nextjs
parent: Skills
permalink: /skills/cloudflare-workers-nextjs/
nav_order: 21
---

# Cloudflare Workers + Next.js + OpenNext

Wire a Next.js 16 app to deploy on Cloudflare Workers (not Pages) through the OpenNext adapter, and set up Cloudflare Workers Builds so every push to a non-production branch creates a preview deploy with a unique URL.

Proven in `car-tco/frontend/` and `immo-brain/web/`. Use it as the canonical recipe for any new Next.js project that needs Cloudflare deploy previews.

## When to Use This Skill

- Adding a Next.js app to a repo and wanting Cloudflare deploys + PR previews
- Workers Builds reports a failure on a new connection and you need the known-good config
- Onboarding a new project that should match the existing Cloudflare deployment pattern

## Your Task

### 1. Scaffold (if needed) and install dependencies

If the Next.js app doesn't exist yet, scaffold it inside a subdirectory (`web/`, `frontend/`, etc.):

```bash
pnpm create next-app@latest web --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-pnpm --turbopack --no-git --yes
```

Then, in the app directory:

```bash
pnpm add @opennextjs/cloudflare
pnpm add -D wrangler
```

Wrangler stays a devDep (local), never global. This way `pnpm install` reproduces the exact version on any machine and on Cloudflare's CI.

### 2. Clean up the scaffold

`create-next-app` (Next.js 16) creates a `pnpm-workspace.yaml` that contains only `ignoredBuiltDependencies` with no `packages:` field. This is malformed — `pnpm install --frozen-lockfile` (which Cloudflare Workers Builds uses) errors with `packages field missing or empty`. Manual `pnpm install` may not catch it depending on version.

**Fix**: delete the workspace file and move `ignoredBuiltDependencies` into `package.json` under the standard `pnpm` key:

```jsonc
// package.json
{
  // ...
  "pnpm": {
    "ignoredBuiltDependencies": ["sharp", "unrs-resolver"]
  }
}
```

```bash
rm pnpm-workspace.yaml
```

This is the canonical pnpm configuration for non-monorepo projects.

### 3. Create the three required config files

#### `next.config.ts`

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {};

export default nextConfig;
```

**Even if the config object is empty, the file must exist.** `@opennextjs/cloudflare` explicitly looks for `next.config.{ts,js}` and exits with `Error: next.config.js not found. Please make sure you are running this command inside a Next.js app.` Keep it as a minimal, commented placeholder.

**If the app uses Cloudflare bindings (KV, R2, D1) during `next dev`** — add the init call at the bottom:

```ts
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

Static landings, route handlers that don't access bindings: not needed.

#### `open-next.config.ts`

```ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";

export default defineCloudflareConfig({});
```

This minimal config is sufficient for static-leaning apps (landings, marketing sites, anything without ISR cache requirements).

**If you need persistent incremental cache across worker instances** (ISR with frequent revalidation, large per-user-cached responses): swap the empty config for an explicit `OpenNextConfig` with `incrementalCache: r2IncrementalCache` and bind an R2 bucket in `wrangler.{jsonc,toml}`. See `car-tco/frontend/open-next.config.ts` for the verbose override pattern.

#### `wrangler.jsonc`

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "your-app-name",
  "main": ".open-next/worker.js",
  "compatibility_date": "2025-08-31",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS"
  }
}
```

The `name` becomes the public URL: `https://<name>.<account>.workers.dev`. `.toml` works equally well — pick the format that matches the rest of the codebase.

### 4. Add the package.json scripts

```jsonc
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "build:cf": "opennextjs-cloudflare build",
    "preview": "opennextjs-cloudflare build && wrangler dev",
    "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy"
  }
}
```

Why `build:cf` separately from `build`: plain `pnpm build` (CI, lint pipelines, IDE hooks, `next dev` precheck) must stay fast — it's just `next build`. The Cloudflare-specific build runs only when shipping or in Workers Builds.

### 5. Configure Cloudflare Workers Builds (dashboard)

Connect the repo at https://dash.cloudflare.com → Workers & Pages → choose worker → Settings → Builds → Connect to Git.

| Field | Value |
|---|---|
| Git account / Repository | your GitHub account / repo |
| Production branch | `main` |
| Builds for non-production branches | ✅ checked |
| **Root directory** (Advanced settings) | the app subdir, e.g. `web` or `frontend` |
| **Build command** | `pnpm build:cf` |
| Deploy command (production) | `npx wrangler deploy` |
| Non-production deploy command | `npx wrangler versions upload` |
| API Token | leave on default |
| Build variables | usually empty; runtime secrets live on the worker |

**Two fields are easy to miss and both will silently fail:**

- **Root directory** is under "Advanced settings" (collapsed). If you leave it empty, Cloudflare clones the repo and looks for `package.json` at the root — won't find it for monorepo-style layouts. Symptom: `pnpm install` errors immediately.
- **Build command** must be set. Cloudflare doesn't infer it from `package.json` scripts. If empty, it skips straight to the deploy command and you get: `✘ The entry-point file at ".open-next/worker.js" was not found.`

After connecting, push any commit on a non-production branch to trigger the first preview build. The preview URL appears in the GitHub PR check status and follows the pattern:

```
https://<8-char-version-id>-<worker-name>.<account>.workers.dev
```

### 6. Set runtime secrets

Secrets persist on the worker across redeploys and across versions. Set them once via the CLI from the app directory:

```bash
echo "<value>" | pnpm wrangler secret put SECRET_NAME
```

Or via the dashboard: Worker → Settings → Variables and Secrets → Add → Encrypt.

Preview deploys created via `wrangler versions upload` **inherit production secrets** — no separate config needed.

### 7. First manual deploy (optional, to validate before Workers Builds)

From the app directory:

```bash
pnpm wrangler login          # interactive, browser OAuth
pnpm run deploy              # NOT `pnpm deploy` — see gotcha below
```

Output ends with `https://<name>.<account>.workers.dev`. This is the production URL; Workers Builds will keep updating it on `main` pushes.

## Gotchas

### `pnpm-workspace.yaml` scaffolded by `create-next-app` breaks `pnpm install --frozen-lockfile`

Next.js 16's `create-next-app` writes a `pnpm-workspace.yaml` that only declares `ignoredBuiltDependencies` — no `packages:` field. Strict mode (which Cloudflare Workers Builds uses) errors with `packages field missing or empty`. Workaround: delete the file and move `ignoredBuiltDependencies` into `package.json` under the `pnpm` key. See step 2.

### `pnpm deploy` collides with a pnpm builtin

`pnpm deploy` is a pnpm-built-in command for monorepo target deployment. Running it on a non-deployment-target package fails with `ERR_PNPM_NOTHING_TO_DEPLOY`. Always use `pnpm run deploy` to force the custom script. (`pnpm build:cf` doesn't collide; only the specific builtin names — `deploy`, `add`, `install`, `update`, `remove`, `dlx`, `exec`, etc.)

### Missing `next.config.ts` breaks the OpenNext build

Next.js itself runs fine without `next.config.ts`. OpenNext's adapter does not — it checks for the file and exits with `Error: next.config.js not found.` Keep an empty `next.config.ts` even if you have no config.

### Workers Builds "Deploy command" runs without "Build command"

Cloudflare Workers Builds does not automatically run the package's `build` script. If you only fill the Deploy command field, it skips straight to deploy. The error is misleading (`The entry-point file at ".open-next/worker.js" was not found`) — looks like a missing-file bug, but it's a missing-step config issue. Always set Build command explicitly.

### Resend `onboarding@resend.dev` only delivers to the account owner

When wiring transactional email via Resend without a verified domain: the test sender `onboarding@resend.dev` can only deliver to the email address used to create the Resend account. Verify a domain in Resend (5 min of DNS records) to send to anyone else.

### Workers Builds vs runtime secrets

Workers Builds doesn't manage runtime secrets — set them on the worker via `wrangler secret put`. The "Build variables" field in the dashboard is for build-time env vars (e.g. `NEXT_PUBLIC_*` that get inlined into the bundle), not runtime secrets.

## Debugging a failing Workers Build

1. Open the build URL from the GitHub PR check.
2. Read the log top-to-bottom. Look for the **first** non-progress line.
3. Match against the gotchas above:
   - `packages field missing or empty` → step 2 (delete `pnpm-workspace.yaml`)
   - `The entry-point file at ".open-next/worker.js" was not found` → dashboard Build command field is empty
   - `next.config.js not found` → restore `next.config.ts` even if empty
   - Anything about R2/KV bindings → swap the empty `defineCloudflareConfig({})` for an explicit one with `"dummy"` overrides (see car-tco)
4. Use `pnpm wrangler tail` to read live worker logs after a deploy succeeds — invaluable for runtime errors on the deployed worker.

## Input Handling

- **No argument**: walk through the steps above for the current project.
- **App subdirectory as argument** (e.g. `/cloudflare-workers-nextjs web`): assume Next.js already exists at that path and skip scaffolding, jump to wiring the four config files.

## Tools Used

- `pnpm` / `npm` — package management
- `wrangler` (Cloudflare CLI) — auth, deploy, secret management, log tailing
- `@opennextjs/cloudflare` — Next.js → Workers adapter
- Cloudflare dashboard — Workers Builds connection (interactive, user does the clicks)
- GitHub repo (push triggers builds)

## Reference Implementations

- `~/dev/personal/immo-brain/web/` — pnpm-based, minimal `defineCloudflareConfig({})`, `wrangler.jsonc`, no `initOpenNextCloudflareForDev()` (no bindings used in dev)
- `~/dev/personal/car-tco/frontend/` — npm-based, explicit `OpenNextConfig` with `"dummy"` overrides, `wrangler.toml`, `initOpenNextCloudflareForDev()` enabled

When debugging a new project, diff against one of these as the source of truth. Prefer the immo-brain layout for new projects (less configuration); fall back to car-tco's verbose pattern if OpenNext defaults misbehave.

## Example Usage

```
/cloudflare-workers-nextjs
/cloudflare-workers-nextjs web
```
