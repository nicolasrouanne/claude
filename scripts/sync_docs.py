#!/usr/bin/env python3
"""Regenerate skill tables in README.md and skills.md from .claude/skills/.

Source of truth: each SKILL.md's `name` and `description` frontmatter.
Pass --check to fail on drift instead of rewriting (for CI).
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
START, END = "<!-- skills:start -->", "<!-- skills:end -->"


def field(text: str, key: str) -> str:
    """Extract `key: value` from the leading `---` frontmatter block."""
    fm = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not fm:
        return ""
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm.group(1), re.MULTILINE)
    return m.group(1) if m else ""


skills = []
for d in sorted((REPO / ".claude/skills").iterdir()):
    skill_md = next((c for c in d.iterdir() if c.name.lower() == "skill.md"), None)
    if not skill_md:
        sys.exit(f"error: no SKILL.md in {d}")
    text = skill_md.read_text()
    skills.append((field(text, "name") or d.name, field(text, "description"), d.name))
skills.sort()

rows = "\n".join(["| Skill | Description |", "| ----- | ----------- |"])
readme = rows + "\n" + "\n".join(
    f"| [`/{n}`](./.claude/skills/{d}/SKILL.md) | {desc} |" for n, desc, d in skills
)
index = rows + "\n" + "\n".join(
    f"| [`/{n}`]({{{{ site.baseurl }}}}/skills/{d}/) | {desc} |" for n, desc, d in skills
)

check = "--check" in sys.argv
drift = False
for path, block in [(REPO / "README.md", readme), (REPO / "skills.md", index)]:
    old = path.read_text()
    new = re.sub(rf"({re.escape(START)}).*?({re.escape(END)})", rf"\1\n{block}\n\2", old, flags=re.DOTALL)
    if new == old:
        continue
    drift = True
    if check:
        print(f"drift: {path.name}", file=sys.stderr)
    else:
        path.write_text(new)
        print(f"updated: {path.name}")

sys.exit(1 if check and drift else 0)
