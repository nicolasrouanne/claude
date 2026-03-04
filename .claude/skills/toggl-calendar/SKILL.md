---
name: toggl-calendar
description: "Per-day, per-client timesheet calendar from Toggl. Shows work days per client per day, in 0.5-day increments with carry-forward rounding."
title: /toggl-calendar
parent: Skills
permalink: /skills/toggl-calendar/
---

# Toggl Calendar

Generate a per-day, per-client timesheet for a calendar month (or range).

## Configuration

- **Script**: `~/dev/claude/scripts/toggl_calendar.py`
- **Toggl API Token**: environment variable `TOGGL_API_TOKEN`
- **Workspace**: `2584215`
- **Work day**: 5.5 hours
- **Rounding**: carry-forward to nearest 0.5 — fractions accumulate across days so no hours are lost

## Your Task

1. **Parse the date range** from the user's message:
   - "January" / "january 2026" → `2026-01`
   - "last month" → previous calendar month
   - "january and february" / "jan-feb 2026" → `2026-01 2026-02`
   - No date → current month (script default)

2. **Run the script** via Bash:
   ```bash
   python3 ~/dev/claude/scripts/toggl_calendar.py 2026-01
   # or for a range:
   python3 ~/dev/claude/scripts/toggl_calendar.py 2026-01 2026-02
   ```

3. **Display the output** as-is — the script formats everything.

## Rounding Algorithm

For each client, across all days in order:
```
running   += raw_today          # raw = seconds / (5.5 × 3600)
new_total  = floor(running × 2 + 0.5) / 2   # round cumulative to nearest 0.5
day_value  = new_total − already_assigned
already_assigned = new_total
```

This ensures small fractions roll forward and are counted eventually, rather than being permanently discarded by per-day rounding.

## Guidelines

- **DO** run the script directly — don't re-implement the logic inline
- **DON'T** hardcode the API token
- **DON'T** modify any Toggl data (read-only)
