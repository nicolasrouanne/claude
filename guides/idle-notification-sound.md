# Set Up Audio Notifications for Claude Code Idle State

This guide explains how to configure Claude Code to play a sound when it's waiting for user input.

## Prerequisites

- Claude Code installed
- macOS (for `afplay` command) or Linux with audio playback tools
- Terminal access

## Overview

Claude Code supports **hooks** that execute custom commands in response to events. The `Notification` hook with the `idle_prompt` matcher triggers when Claude has been waiting for user input for more than 60 seconds.

| Event Type | Trigger |
| ---------- | ------- |
| `idle_prompt` | Claude is waiting for input (after 60s idle) |
| `permission_prompt` | Claude needs permission approval |
| `auth_success` | Authentication completed |

## Step-by-step Guide

### 1. Choose a Sound

List available system sounds on macOS:

```bash
ls /System/Library/Sounds/
```

Common options: `Glass.aiff`, `Ping.aiff`, `Submarine.aiff`, `Morse.aiff`

Preview a sound:

```bash
afplay /System/Library/Sounds/Submarine.aiff
```

### 2. Configure the Hook

Edit `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Submarine.aiff"
          }
        ]
      }
    ]
  }
}
```

Alternatively, use the interactive setup:

```bash
claude
# Then type: /hooks
```

### 3. Test the Configuration

Start a Claude Code session and let it complete a task. After 60 seconds of idle time, you should hear the notification sound.

## Alternative: Text-to-Speech

For a spoken notification instead of a sound:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "say 'Claude is waiting for your input'"
          }
        ]
      }
    ]
  }
}
```

## Linux Configuration

On Linux, replace `afplay` with your audio player:

```json
{
  "command": "paplay /usr/share/sounds/freedesktop/stereo/complete.oga"
}
```

Or use `spd-say` for text-to-speech:

```json
{
  "command": "spd-say 'Claude is waiting'"
}
```

## Related Resources

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [macOS System Sounds](file:///System/Library/Sounds/)
