#!/usr/bin/env python3
"""init_skill.py — 创建 Skill 目录结构 + 模板 SKILL.md

用法:
  init_skill.py <skill-name> --path <output-directory> [--components scripts,references,assets]

输出: 在 output-directory 下创建 <skill-name>/ 目录，包含模板 SKILL.md 和指定的子目录
"""

import argparse
import re
import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
description: [TODO: One sentence on what the skill does, plus specific triggers — keywords, scenarios, file types — that should activate it. Max 1024 characters. No < or >.]
---

# {title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables.]

## Choose a Structure

Pick the structure pattern that best fits this skill, then delete this section.

- **Workflow-Based** — sequential steps (best for procedures with clear order)
- **Task-Based** — multiple independent operations (best for tool collections)
- **Reference/Guidelines** — standards or specifications (best for style guides)
- **Capabilities-Based** — interrelated features (best for integrated systems)

See `references/skill-anatomy.md` for examples of each.

## [TODO: Replace with the first main section]

[TODO: Add content. Patterns to consider:
 - Step-by-step workflow (see references/workflows.md)
 - Output template or examples (see references/output-patterns.md)
 - Decision tree for branching tasks
 - Concrete user-request examples

For deterministic operations, prefer scripts/ over inline code.
For domain knowledge or schemas, prefer references/.
For boilerplate or templates, prefer assets/.]
"""


def kebab_check(name: str) -> str | None:
    """返回错误描述，None 表示合格"""
    if not re.match(r"^[a-z0-9-]+$", name):
        return "name must be hyphen-case (lowercase letters/digits/hyphens only)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return "name cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return f"name too long ({len(name)} chars). Maximum is 64."
    return None


def init_skill(name: str, root: Path, components: list[str]) -> Path:
    err = kebab_check(name)
    if err:
        print(f"❌ {err}: {name}", file=sys.stderr)
        sys.exit(1)

    skill_dir = root / name
    if skill_dir.exists():
        print(f"❌ Already exists: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # 创建目录
    skill_dir.mkdir(parents=True)
    title = " ".join(w.capitalize() for w in name.split("-"))
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, title=title), encoding="utf-8"
    )
    print(f"  ✓ {skill_dir}/SKILL.md")

    valid_components = {"scripts", "references", "assets"}
    for c in components:
        if c not in valid_components:
            print(f"  ⚠ Unknown component '{c}', skipping", file=sys.stderr)
            continue
        sub = skill_dir / c
        sub.mkdir()
        print(f"  ✓ {sub}/")

    return skill_dir


def main():
    p = argparse.ArgumentParser(description="Initialize a new Claude Code Skill")
    p.add_argument("name", help="Skill name (hyphen-case, max 64 chars)")
    p.add_argument("--path", default=".", help="Output root directory (default: current dir)")
    p.add_argument(
        "--components",
        default="scripts,references",
        help="Comma-separated subdirs to create (default: scripts,references). "
             "Valid: scripts, references, assets",
    )
    args = p.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        root.mkdir(parents=True)
    components = [c.strip() for c in args.components.split(",") if c.strip()]

    print(f"📂 Initializing skill '{args.name}' under {root}")
    skill_dir = init_skill(args.name, root, components)
    print(f"\n✅ Done: {skill_dir}")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md")
    print(f"  2. Add scripts/references/assets as needed")
    print(f"  3. Validate: python3 validate_skill.py {skill_dir}")
    print(f"  4. Package:  python3 package_skill.py {skill_dir}")


if __name__ == "__main__":
    main()
