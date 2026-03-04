#!/usr/bin/env python3
"""
Toggl Calendar — per-day, per-client timesheet for a calendar month.

Usage:
    python3 toggl_calendar.py 2026-01
    python3 toggl_calendar.py 2026-01 2026-02   # range (inclusive)

Requires: TOGGL_API_TOKEN environment variable
"""

import json
import math
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from calendar import monthrange

PARIS = timezone(timedelta(hours=1))
DAY_SECS = 5.5 * 3600  # 1 work day = 5h30m
WORKSPACE_ID = 2584215
API_BASE = "https://api.track.toggl.com/api/v9"


def round_half(x):
    """Round to nearest 0.5, ties round up. e.g. 1.13→1.0, 1.37→1.5, 0.25→0.5"""
    return math.floor(x * 2 + 0.5) / 2


def api_get(path, token):
    result = subprocess.run(
        ["curl", "-s", "--user", f"{token}:api_token", f"{API_BASE}{path}"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def fetch_data(start_date, end_date, token):
    # end_date is exclusive in Toggl API, add 1 day
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    end_exclusive = end_dt.strftime("%Y-%m-%d")

    entries = api_get(f"/me/time_entries?start_date={start_date}&end_date={end_exclusive}", token)
    projects = api_get(f"/workspaces/{WORKSPACE_ID}/projects?active=both", token)
    clients = api_get(f"/workspaces/{WORKSPACE_ID}/clients", token)

    return entries, projects, clients


def build_project_client_map(projects, clients):
    client_map = {c["id"]: c["name"] for c in clients}
    return {
        p["id"]: client_map.get(p.get("client_id"), "Sans client")
        for p in projects
    }


def build_daily(entries, project_client, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    daily = defaultdict(lambda: defaultdict(int))

    for e in entries:
        if e.get("duration", 0) <= 0:
            continue
        entry_start = datetime.fromisoformat(e["start"]).astimezone(PARIS)
        entry_date = entry_start.date()
        if not (start <= entry_date <= end):
            continue
        day = entry_date.strftime("%Y-%m-%d")
        client = project_client.get(e.get("project_id"), "Sans client")
        daily[day][client] += e["duration"]

    return daily


def apply_carry_forward(daily, all_days, all_clients):
    """Two-level carry-forward rounding.

    Day-level: determines how many 0.5-slots exist for the day based on total
    hours worked, so a day can never round to more than its real hours warrant.

    Client-level debt: tracks raw hours accumulated per client minus hours
    already assigned. Clients with the most uncompensated time get priority
    for the day's slots, preserving monthly totals without inflating daily ones.
    """
    day_running = 0.0
    day_assigned = 0.0
    client_running = defaultdict(float)   # raw hours accumulated, never rounded
    client_assigned = defaultdict(float)  # hours credited so far
    results = {}

    for day in all_days:
        day_data = daily[day]
        total_day_secs = sum(day_data.values())

        # 1. Day-level carry-forward → number of 0.5-slots for today
        day_running += total_day_secs / DAY_SECS
        day_new_total = round_half(day_running)
        day_value = day_new_total - day_assigned
        day_assigned = day_new_total
        slots = int(round(day_value * 2))

        # 2. Accumulate raw hours per client (no rounding)
        for c in all_clients:
            client_running[c] += day_data.get(c, 0) / DAY_SECS

        # 3. Assign slots to clients with highest uncompensated debt
        day_alloc = {c: 0.0 for c in all_clients}
        if slots > 0:
            # Only consider clients who worked today
            active = [c for c in all_clients if day_data.get(c, 0) > 0]
            for _ in range(slots):
                # Pick the active client with the highest debt
                best = max(active, key=lambda c: client_running[c] - client_assigned[c])
                day_alloc[best] += 0.5
                client_assigned[best] += 0.5

        results[day] = day_alloc

    return results, client_running, client_assigned


def print_table(results, all_days, all_clients, running, assigned):
    col = 10
    header = f"{'Date':<12}" + "".join(f"{c:<{col}}" for c in all_clients) + "Total"
    print(header)
    print("-" * len(header))

    for day in all_days:
        weekday = datetime.strptime(day, "%Y-%m-%d").strftime("%a")
        row = f"{day} {weekday:<3}"
        total = 0
        for c in all_clients:
            val = results[day][c]
            total += val
            row += f"{(f'{val:.1f}' if val else '-'):<{col}}"
        row += f"{total:.1f}"
        print(row)

    print()
    print("Monthly totals:")
    grand = 0
    for c in all_clients:
        print(f"  {c:<16} {assigned[c]:.1f} d  (raw {running[c]:.2f} d)")
        grand += assigned[c]
    print(f"  {'TOTAL':<16} {grand:.1f} d")


def parse_args(args):
    if not args:
        # Default: current month
        now = datetime.now()
        start = now.strftime("%Y-%m-01")
        last_day = monthrange(now.year, now.month)[1]
        end = now.strftime(f"%Y-%m-{last_day}")
        return start, end

    if len(args) == 1:
        # Single YYYY-MM
        year, month = map(int, args[0].split("-"))
        last_day = monthrange(year, month)[1]
        return f"{year:04d}-{month:02d}-01", f"{year:04d}-{month:02d}-{last_day:02d}"

    if len(args) == 2:
        # Two YYYY-MM months, inclusive range
        year1, month1 = map(int, args[0].split("-"))
        year2, month2 = map(int, args[1].split("-"))
        last_day = monthrange(year2, month2)[1]
        return f"{year1:04d}-{month1:02d}-01", f"{year2:04d}-{month2:02d}-{last_day:02d}"

    raise ValueError("Usage: toggl_calendar.py [YYYY-MM] [YYYY-MM]")


def main():
    token = os.environ.get("TOGGL_API_TOKEN")
    if not token:
        print("Error: TOGGL_API_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    start_date, end_date = parse_args(sys.argv[1:])
    print(f"Fetching {start_date} → {end_date}...")

    entries, projects, clients = fetch_data(start_date, end_date, token)
    project_client = build_project_client_map(projects, clients)
    daily = build_daily(entries, project_client, start_date, end_date)

    all_days = sorted(daily.keys())
    all_clients = sorted({c for d in daily.values() for c in d})

    results, running, assigned = apply_carry_forward(daily, all_days, all_clients)
    print()
    print_table(results, all_days, all_clients, running, assigned)


if __name__ == "__main__":
    main()
