# qraft-comms — local scheduling PoC (launchd)

Minimal, reversible, local. Proves the "recurring routine" rung without any cloud/creds work (creds live on this Mac).

## Files
- `run.sh` — headless runner: `claude -p` → the `/qraft-comms` skill → writes `~/qraft-comms/drafts/<date>.md`, logs to `~/qraft-comms/run.log`.
- `com.qraft.comms.plist` — launchd LaunchAgent, fires **every day at 08:30**. `RunAtLoad` is false (won't run on load).

## First: run it by hand (do this once before relying on the timer)
```bash
# Interactive — lets you see the output and approve any permissions (saved for the unattended runs):
#   in a Claude Code session opened from the worktree:  /qraft-comms
# Or exercise the exact headless runner the timer will use:
bash "/Users/nicolasrouanne/dev/claude/.claude/worktrees/qraft-comms-skill/.claude/skills/qraft-comms/schedule/run.sh"
cat ~/qraft-comms/drafts/*.md   # check the latest digest
```

## Enable the daily timer
```bash
cp "/Users/nicolasrouanne/dev/claude/.claude/worktrees/qraft-comms-skill/.claude/skills/qraft-comms/schedule/com.qraft.comms.plist" \
   ~/Library/LaunchAgents/com.qraft.comms.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.qraft.comms.plist
launchctl list | grep qraft   # confirm it's registered
```

## Fire it on demand (test the schedule path)
```bash
launchctl start com.qraft.comms
tail -f ~/qraft-comms/run.log
```

## Disable / remove
```bash
launchctl bootout gui/$(id -u)/com.qraft.comms
rm ~/Library/LaunchAgents/com.qraft.comms.plist
```

## After merging the skill to `main`
The skill becomes active in the live tree (`~/.claude/skills` → `~/dev/claude/.claude/skills`). Repoint the plist's `ProgramArguments` from the worktree path to:
`/Users/nicolasrouanne/dev/claude/.claude/skills/qraft-comms/schedule/run.sh`
then `launchctl bootout` + `bootstrap` again. You can then delete the worktree.

## Notes / limits (PoC)
- Runs only while the Mac is awake/on. This is the deliberate trade-off vs a cloud routine — but it needs no cred provisioning. Cloud scheduling is a later, separate decision (see the Notion strategy doc).
- `--permission-mode acceptEdits` + your existing settings allowlist. If an unattended run stalls/fails on a permission, run `/qraft-comms` interactively once to approve it (saved to `settings.local.json`).
- Daily cadence means the skill reads the last 3 digests and only surfaces what's *new* — a quiet day produces a one-line "rien de neuf" digest by design.
