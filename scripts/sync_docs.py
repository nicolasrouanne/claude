#!/usr/bin/env python3
"""Regenerate skill tables in README.md and skills.md from .claude/skills/.

Single source of truth: each skill's frontmatter (`name`, `description`).
Tables in README.md and skills.md sit between `<!-- skills:start -->` and
`<!-- skills:end -->` markers and are rewritten in place.

Usage:
    python scripts/sync_docs.py          # rewrite docs
    python scripts/sync_docs.py --check  # exit 1 if docs would change (CI)
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / ".claude" / "skills"
README = REPO / "README.md"
SKILLS_INDEX = REPO / "skills.md"

START = "<!-- skills:start -->"
END = "<!-- skills:end -->"


@dataclass
class Skill:
    name: str
    description: str
    skill_file: Path  # path to SKILL.md, relative to repo root

    @property
    def dir_name(self) -> str:
        return self.skill_file.parent.name


def parse_frontmatter(text: str) -> dict[str, str]:
    """Tiny YAML frontmatter parser — handles `key: value` and `key: "quoted"`.

    Sufficient for skill frontmatter; not a general YAML parser.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    out: dict[str, str] = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        out[key.strip()] = value
    return out


def find_skill_file(skill_dir: Path) -> Path | None:
    """Find SKILL.md (case-insensitive) inside a skill directory."""
    for child in skill_dir.iterdir():
        if child.is_file() and child.name.lower() == "skill.md":
            return child
    return None


def load_skills() -> list[Skill]:
    skills: list[Skill] = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        f = find_skill_file(d)
        if f is None:
            print(f"warn: no SKILL.md in {d}", file=sys.stderr)
            continue
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        name = fm.get("name") or d.name
        description = fm.get("description", "").strip()
        if not description:
            print(f"warn: missing description in {f}", file=sys.stderr)
        skills.append(Skill(name=name, description=description, skill_file=f))
    skills.sort(key=lambda s: s.name)
    return skills


def render_readme_table(skills: list[Skill]) -> str:
    lines = ["| Skill | Description |", "| ----- | ----------- |"]
    for s in skills:
        rel = s.skill_file.relative_to(REPO).as_posix()
        lines.append(f"| [`/{s.name}`](./{rel}) | {s.description} |")
    return "\n".join(lines)


def render_skills_md_table(skills: list[Skill]) -> str:
    lines = ["| Skill | Description |", "| ----- | ----------- |"]
    for s in skills:
        lines.append(
            f"| [`/{s.name}`]({{{{ site.baseurl }}}}/skills/{s.dir_name}/) | {s.description} |"
        )
    return "\n".join(lines)


def replace_block(text: str, replacement: str, path: Path) -> str:
    pattern = re.compile(
        rf"({re.escape(START)})(.*?)({re.escape(END)})", re.DOTALL
    )
    if not pattern.search(text):
        raise SystemExit(
            f"error: {path} is missing the {START} / {END} markers"
        )
    return pattern.sub(rf"\1\n{replacement}\n\3", text)


def main() -> int:
    check = "--check" in sys.argv
    skills = load_skills()

    targets = [
        (README, render_readme_table(skills)),
        (SKILLS_INDEX, render_skills_md_table(skills)),
    ]

    drift = False
    for path, block in targets:
        original = path.read_text(encoding="utf-8")
        updated = replace_block(original, block, path)
        if updated != original:
            drift = True
            if check:
                print(f"drift: {path.relative_to(REPO)} is out of date", file=sys.stderr)
            else:
                path.write_text(updated, encoding="utf-8")
                print(f"updated: {path.relative_to(REPO)}")

    if check and drift:
        print(
            "\nRun `python scripts/sync_docs.py` and commit the result.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
