# SAMM Dev Environment Startup

Start the full development environment for SAMM: database, API server, iOS simulator, and mobile app.

## Usage

```
/samm-dev-env [options]
```

Options:
- `seed` - Reset and seed the database before starting
- `api` - Start only the API server (skip mobile)
- `mobile` - Start only the mobile app (skip API)

## Instructions

### 1. Start PostgreSQL (if not running)

```bash
brew services list | grep postgresql@17
# If not started:
brew services start postgresql@17
```

### 2. Boot iOS Simulator (if not booted)

```bash
# Check if booted
xcrun simctl list devices booted

# If no device booted, boot iPhone 17 Pro and open Simulator app
xcrun simctl boot "iPhone 17 Pro" && open -a Simulator
```

### 3. Seed Database (if `seed` option provided)

```bash
cd ~/dev/samm/api
PYTHONPATH=$(pwd) uv run python seeds/run_seeds.py reset
```

### 4. Start API Server (unless `mobile` only)

Run in background:

```bash
cd ~/dev/samm/api
uv run fastapi dev
```

Wait for the server to be ready (check for "Application startup complete" or test the health endpoint).

### 5. Start Mobile App (unless `api` only)

```bash
cd ~/dev/samm/mobile
pnpm ios
```

This will connect to the already-booted simulator.

## Taking Screenshots

To capture the simulator screen:

```bash
xcrun simctl io booted screenshot /path/to/screenshot.png
```

## Stopping Services

```bash
# Stop PostgreSQL
brew services stop postgresql@17

# Shutdown simulator
xcrun simctl shutdown booted
```
