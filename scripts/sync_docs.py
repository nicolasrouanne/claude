#!/usr/bin/env python3
"""Regenerate skill tables in README.md and skills.md from .claude/skills/.

Source of truth: each SKILL.md's `name` and `description` frontmatter.
Pass --check to fail on drift instead of rewriting (for CI).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / ".claude" / "skills"
START_MARKER = "<!-- skills:start -->"
END_MARKER = "<!-- skills:end -->"


class Skill(NamedTuple):
    name: str
    description: str
    dir_name: str


def read_frontmatter_field(text: str, key: str) -> str:
    """Extract a value from the leading `---` YAML frontmatter block."""
    block = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not block:
        return ""
    line = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', block.group(1), re.MULTILINE)
    return line.group(1) if line else ""


def find_skill_file(skill_dir: Path) -> Path:
    """Return the SKILL.md inside a skill directory (case-insensitive)."""
    for child in skill_dir.iterdir():
        if child.is_file() and child.name.lower() == "skill.md":
            return child
    sys.exit(f"error: no SKILL.md in {skill_dir}")


def load_skills() -> list[Skill]:
    """Load every skill under .claude/skills/, sorted by name."""
    skills: list[Skill] = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        text = find_skill_file(skill_dir).read_text()
        skills.append(Skill(
            name=read_frontmatter_field(text, "name") or skill_dir.name,
            description=read_frontmatter_field(text, "description"),
            dir_name=skill_dir.name,
        ))
    return sorted(skills)


def render_table(skills: list[Skill], link: Callable[[Skill], str]) -> str:
    """Render a Markdown table; `link(skill)` produces the URL for the first cell."""
    header = "| Skill | Description |\n| ----- | ----------- |"
    rows = "\n".join(f"| [`/{s.name}`]({link(s)}) | {s.description} |" for s in skills)
    return f"{header}\n{rows}"


def replace_between_markers(text: str, replacement: str) -> str:
    """Return `text` with the content between START_MARKER and END_MARKER replaced."""
    pattern = rf"({re.escape(START_MARKER)}).*?({re.escape(END_MARKER)})"
    return re.sub(pattern, rf"\1\n\n{replacement}\n\n\2", text, flags=re.DOTALL)


def main() -> int:
    check_only = "--check" in sys.argv
    skills = load_skills()

    targets: list[tuple[Path, str]] = [
        (REPO / "README.md", render_table(skills, lambda s: f"./.claude/skills/{s.dir_name}/SKILL.md")),
        (REPO / "skills.md", render_table(skills, lambda s: f"{{{{ site.baseurl }}}}/skills/{s.dir_name}/")),
    ]

    drift = False
    for path, table in targets:
        original = path.read_text()
        updated = replace_between_markers(original, table)
        if updated == original:
            continue
        drift = True
        if check_only:
            print(f"drift: {path.name}", file=sys.stderr)
        else:
            path.write_text(updated)
            print(f"updated: {path.name}")

    return 1 if check_only and drift else 0


if __name__ == "__main__":
    sys.exit(main())
