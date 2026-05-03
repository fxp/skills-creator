#!/usr/bin/env python3
"""validate_plugin.py — 校验 Claude Code Plugin 目录

输入: plugin 目录路径
输出: JSON 结果 (stdout)，非零退出码表示失败

校验:
  1. .claude-plugin/plugin.json 存在且字段合规
  2. skills/* 每个子目录都有合法 SKILL.md（递归调用 validate_skill）
  3. commands/*.md 有 frontmatter
  4. .mcp.json 是合法 JSON
"""

import json
import os
import re
import sys
from pathlib import Path

# 复用 skill-generator 的 validate_skill
SCRIPT_DIR = Path(__file__).resolve().parent
SIBLING = SCRIPT_DIR.parent.parent / "skill-generator" / "scripts"
sys.path.insert(0, str(SIBLING))
try:
    from validate_skill import validate_skill  # type: ignore
except ImportError:
    print("ERROR: cannot import validate_skill from skill-generator/scripts/", file=sys.stderr)
    sys.exit(2)


PLUGIN_ALLOWED_KEYS = {
    "name", "description", "version", "author",
    "homepage", "repository", "license", "keywords",
}


def validate_manifest(path: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    if not path.exists():
        return [f"Missing {path}"], []
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"Invalid JSON in {path.name}: {e}"], []

    if not isinstance(m, dict):
        return [f"{path.name} must be a JSON object"], []

    unexpected = set(m.keys()) - PLUGIN_ALLOWED_KEYS
    if unexpected:
        errors.append(f"Unexpected plugin.json key(s): {', '.join(sorted(unexpected))}")

    name = m.get("name", "")
    if not name:
        errors.append("plugin.json missing 'name'")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"plugin name must be hyphen-case: {name}")
    elif name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append(f"plugin name has invalid hyphen pattern: {name}")
    elif len(name) > 64:
        errors.append(f"plugin name too long ({len(name)} chars)")

    desc = m.get("description", "")
    if not desc:
        errors.append("plugin.json missing 'description'")
    elif len(desc) > 1024:
        errors.append(f"description too long ({len(desc)} chars, max 1024)")
    elif "<" in desc or ">" in desc:
        errors.append("description cannot contain < or >")

    author = m.get("author")
    if author and not (isinstance(author, dict) and "name" in author):
        warnings.append("'author' should be {\"name\": \"...\"}")

    return errors, warnings


def validate_command(path: Path) -> list[str]:
    errors = []
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        errors.append(f"{path.name}: missing YAML frontmatter")
        return errors
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        errors.append(f"{path.name}: malformed frontmatter")
    return errors


def validate_plugin(plugin_dir: Path) -> dict:
    errors, warnings = [], []
    skill_results = {}

    plugin_dir = Path(plugin_dir).resolve()
    if not plugin_dir.is_dir():
        return {"valid": False, "errors": [f"Not a directory: {plugin_dir}"]}

    # 1. manifest
    errs, warns = validate_manifest(plugin_dir / ".claude-plugin" / "plugin.json")
    errors.extend(errs)
    warnings.extend(warns)

    # 2. skills/
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for sub in sorted(skills_dir.iterdir()):
            if not sub.is_dir() or sub.name.startswith("_") or sub.name.startswith("."):
                continue
            r = validate_skill(str(sub))
            skill_results[sub.name] = r
            for e in r["errors"]:
                errors.append(f"skills/{sub.name}: {e}")
            for w in r["warnings"]:
                warnings.append(f"skills/{sub.name}: {w}")

    if not skill_results:
        warnings.append("Plugin contains no skills/ — is this intentional?")

    # 3. commands/
    commands_dir = plugin_dir / "commands"
    cmd_count = 0
    if commands_dir.is_dir():
        for cmd_file in commands_dir.glob("*.md"):
            cmd_count += 1
            errors.extend(validate_command(cmd_file))

    # 4. .mcp.json
    mcp_path = plugin_dir / ".mcp.json"
    if mcp_path.exists():
        try:
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
            if not isinstance(mcp, dict) or "mcpServers" not in mcp:
                warnings.append(".mcp.json should contain top-level 'mcpServers' key")
        except json.JSONDecodeError as e:
            errors.append(f".mcp.json invalid: {e}")

    # 5. README
    if not (plugin_dir / "README.md").exists():
        warnings.append("Missing README.md")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "plugin": plugin_dir.name,
            "skills": list(skill_results.keys()),
            "commands": cmd_count,
            "has_mcp": mcp_path.exists(),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_plugin.py <plugin_directory>", file=sys.stderr)
        sys.exit(2)
    result = validate_plugin(Path(sys.argv[1]))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["valid"] else 1)
