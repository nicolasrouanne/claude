#!/usr/bin/env bash
# qraft-comms — local weekly PoC runner.
# Runs the /qraft-comms skill headless and logs. Read-only + drafts only.
# Invoked by launchd (com.qraft.comms.weekly.plist) or by hand for testing.
set -euo pipefail

# launchd gives a minimal environment — make node + claude reachable.
export PATH="/opt/homebrew/bin:/Users/nicolasrouanne/.nvm/versions/node/v22.19.0/bin:$PATH"

OUT_BASE="$HOME/qraft-comms"
mkdir -p "$OUT_BASE/drafts"
LOG="$OUT_BASE/run.log"

# Resolve the repo root that contains this skill (works from the worktree now,
# and from the live tree after merge), so the skill is discovered as a project skill.
REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"

{
  echo "----- $(date '+%F %T') qraft-comms start (repo: $REPO_ROOT) -----"
  cd "$REPO_ROOT"
  /opt/homebrew/bin/claude -p \
    "Use the qraft-comms skill to generate this week's Qraft communication drafts. Write the digest file as instructed. Do not publish anything." \
    --permission-mode acceptEdits
  echo "----- $(date '+%F %T') qraft-comms end (exit $?) -----"
} >> "$LOG" 2>&1
