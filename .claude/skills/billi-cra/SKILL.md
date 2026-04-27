---
name: billi-cra
description: Import CRAs from an Excel file into Billi, or export CRAs from Billi to Excel. Bidirectional sync of activity reports.
---

# billi-cra

Sync CRAs (Comptes Rendus d'Activité) between an Excel file and the Billi platform API.

## Directions

- **Excel -> Billi** : Read an Excel file, create/update activity reports on Billi via API
- **Billi -> Excel** : Fetch activity reports from Billi API, write to an Excel file

## Usage

```
/billi-cra import <path-to-excel>
/billi-cra export <path-to-excel> [--year 2025]
```

If no direction is specified, ask the user.

## Auth

1. Get credentials from 1Password: `op item get "Billi Qraft - Agency User" --vault Qraft --fields label=username,label=password`
2. Get a Bearer token:
```bash
curl -s -X POST https://api.billi.so/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"password","email":"<email>","password":"<password>"}'
```
Token expires in 7200s.

## Excel format

The expected Excel format has one sheet with:
- **Row 1**: `TOTAL` + sum per person
- **Row 3**: Headers — `Date`, then one column per freelancer name
- **Row 4+**: One row per calendar day, with duration values (0, 0.5, or 1) per person

Dates are datetime objects in column A. Empty or 0 cells mean no work that day.

## Import flow (Excel -> Billi)

### Step 1: Read Excel and extract data
Use `openpyxl` to parse the file. Group entries by person and month. Filter to the target year.

### Step 2: Map people to Billi missions
- Fetch missions: `GET /missions` with Bearer token
- Match each Excel column name to a freelancer on a mission
- Get the `mission_rate_id` from each mission's `mission_rates` array (`is_default: true`)
- If no mission exists for a person, ask the user whether to create one

### Step 3: Create activity reports (one per person per month)
**Important: activities cannot be added at creation time.** Two-step process:

```bash
# Step 3a: Create the empty CRA
POST /activity_reports
{"format": "billi", "month": "2025-01-01T00:00:00.000Z", "mission_id": <id>}

# Step 3b: Add activities via update
PUT /activity_reports/<cra_id>
{"activities_attributes": [
  {"date": "2025-01-06T00:00:00.000Z", "duration": 0.5, "mission_rate_id": <rate_id>},
  {"date": "2025-01-07T00:00:00.000Z", "duration": 1.0, "mission_rate_id": <rate_id>}
]}
```

### Validation rules
- `duration`: only 0, 0.5, or 1.0
- One activity per day per CRA
- Activity dates must be in the same month as the CRA
- One non-cancelled CRA per mission per month
- CRA must be in `draft` state to add/modify activities

### Step 4: Report results
Print a summary table: person, month, CRA ID, total duration, number of activities.

## Export flow (Billi -> Excel)

### Step 1: Fetch CRAs from Billi
```bash
GET /activity_reports
```
Filter by year. Each CRA includes `activities[]` with `date` and `duration`.

### Step 2: Build Excel
- Group by freelancer
- Create one column per freelancer, one row per day of the year
- Use `openpyxl` to write the file

### Step 3: Save and report
Save to the specified path and print summary.

## Key API details

- **Creating a mission** requires `mission_rates_attributes` with at least one default rate
- **Activities require `mission_rate_id`** — fetch from `GET /missions/:id` -> `mission_rates[].id`
- Use `uv run --with openpyxl --with requests python3` for Python dependencies
- Always check the Billi API codebase (`~/dev/billi/billi/api/`) and Bruno collections (`api/bruno/`) for the latest API contract if something fails
