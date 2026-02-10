---
name: workspace
description: Read open Cursor editor tabs to understand what the user is working on.
title: /workspace
parent: Skills
permalink: /skills/workspace/
nav_order: 9
---

# Load Cursor Context

Read the files currently open in Cursor so Claude understands what the user is looking at.

## Your Task

### 1. Find the Cursor Workspace

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
for dir in ~/Library/Application\ Support/Cursor/User/workspaceStorage/*/; do
  if [ -f "$dir/workspace.json" ]; then
    folder=$(python3 -c "import json; print(json.load(open('${dir}workspace.json')).get('folder',''))" 2>/dev/null)
    if echo "$folder" | grep -q "$(basename "$REPO_ROOT")"; then
      echo "$dir"
      break
    fi
  fi
done
```

### 2. Extract Open Tab Paths

```bash
sqlite3 "$WORKSPACE_DIR/state.vscdb" \
  "SELECT value FROM ItemTable WHERE key = 'memento/workbench.parts.editor';" \
  > /tmp/cursor_state.json
```

Parse with Python to get file paths:

```python
import json
with open('/tmp/cursor_state.json') as f:
    data = json.load(f)
state = data.get('editorpart.state', {})
grid = state.get('serializedGrid', {}).get('root', {})

def extract_tabs(node):
    tabs = []
    if node.get('type') == 'leaf':
        for editor in node.get('data', {}).get('editors', []):
            try:
                val = json.loads(editor.get('value', '{}'))
                path = val.get('resourceJSON', {}).get('fsPath', '')
                if path:
                    tabs.append(path)
            except:
                pass
    elif node.get('type') == 'branch':
        for child in node.get('data', []):
            tabs.extend(extract_tabs(child))
    return tabs

for tab in extract_tabs(grid):
    print(tab)
```

### 3. Read Each File

- Use the **Read tool** to read the full content of every open tab file
- Skip files that don't exist on disk (deleted tabs)
- Skip binary files (images, fonts, etc.)
- Read files **in parallel** for speed

### 4. Edge Cases

- **Cursor not running / no workspace found**: Tell the user Cursor state wasn't found
- **macOS only**: The path is macOS-specific (`~/Library/Application Support/Cursor/`). On Linux, use `~/.config/Cursor/`.

## Output Format

```
## Cursor Tabs Loaded (N files)
- path/to/file1.vue
- path/to/file2.ts
- ...

Ready to help — I've read everything you have open.
```
