---
name: workspace
description: Load full working context into the conversation — uncommitted diffs, branch diffs, and open Cursor tab contents — so Claude understands what you're working on.
---

# Load Working Context

Recontextualize Claude by loading the full content of what the user is currently working on. This skill acts as if the user pointed Claude at every relevant file, diff, and change.

## Your Task

Execute the following steps **in order of priority**. For each section, **read the actual content** — don't just list files.

### 1. Uncommitted Changes (highest priority)

```bash
# Full diff of all uncommitted changes (staged + unstaged)
git diff HEAD

# List untracked files
git status --short | grep '^??' | sed 's/^?? //'
```

- Run `git diff HEAD` and **include the full diff output** in your response
- For untracked files, **read their content** using the Read tool
- This is the most important context — it shows what the user is actively changing right now

### 2. Branch Diff vs Base Branch

If on a feature branch (not `main`, `master`, or `develop`):

```bash
CURRENT=$(git branch --show-current)

# Find base branch
if git rev-parse --verify origin/develop >/dev/null 2>&1; then
  BASE="origin/develop"
elif git rev-parse --verify origin/main >/dev/null 2>&1; then
  BASE="origin/main"
fi

# Commits on this branch
git log --oneline "$BASE".."$CURRENT"

# Full diff of this branch vs base
git diff "$BASE"..."$CURRENT"
```

- Show the list of commits on this branch
- **Include the full diff** of the branch vs the base branch
- If uncommitted changes overlap with branch diff, note that the uncommitted changes are the latest state

### 3. Open Cursor Tabs (context enrichment)

Read open editor tabs from Cursor's SQLite state and **read each file's content**.

**Step 1: Find the workspace**

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

**Step 2: Extract tab file paths**

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

**Step 3: Read each file**

- Use the **Read tool** to read the full content of every open tab file
- Skip files that don't exist on disk (deleted tabs)
- Skip binary files (images, fonts, etc.)
- Read files in parallel when possible for speed
- Files already covered by diffs above still get read in full — diffs show changes, but full file content gives Claude the complete picture

### 4. Handling Edge Cases

- **Cursor not running / no workspace found**: Skip tab reading silently, proceed with diffs only
- **On main/develop branch**: Skip branch diff section, only show uncommitted changes + tabs
- **No uncommitted changes**: Skip that section
- **Large files (>500 lines)**: Still read them, Claude can handle it
- **macOS only**: The Cursor SQLite path is macOS-specific (`~/Library/Application Support/Cursor/`). On Linux, adjust to `~/.config/Cursor/`.

## Output Format

After loading everything, present a brief **summary** of what was loaded:

```
## Context Loaded

### Uncommitted Changes
- `path/to/file.vue`: [1-line description of changes]
- `path/to/other.ts`: [1-line description]

### Branch: feature/xyz (4 commits ahead of develop)
- commit1 message
- commit2 message
- ...

### Open Cursor Tabs (N files read)
- path/to/file1.vue
- path/to/file2.ts
- ...

Ready to help — I have full context of your current work.
```

The summary is just a recap. The real value is that Claude has now **read all the content** and can reference it in subsequent responses.
