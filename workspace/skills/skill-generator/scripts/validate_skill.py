#!/usr/bin/env python3
"""validate_skill.py — 验证生成的 SKILL.md 符合 Claude Code 规范

输入: skill 目录路径 (包含 SKILL.md)
输出: JSON 格式的验证结果 (stdout), 非零退出码表示失败
"""

import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required but not installed. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def validate_skill(skill_dir: str) -> dict:
    """验证 skill 目录结构和 SKILL.md 内容"""
    errors = []
    warnings = []

    skill_md = os.path.join(skill_dir, "SKILL.md")

    # 1. SKILL.md 存在性
    if not os.path.isfile(skill_md):
        errors.append("SKILL.md not found")
        return {"valid": False, "errors": errors, "warnings": warnings}

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. 解析 frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        errors.append("Missing or malformed YAML frontmatter (must start with --- and end with ---)")
        return {"valid": False, "errors": errors, "warnings": warnings}

    try:
        frontmatter = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return {"valid": False, "errors": errors, "warnings": warnings}

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter must be a YAML mapping")
        return {"valid": False, "errors": errors, "warnings": warnings}

    # 3. name 字段
    name = frontmatter.get("name")
    if not name:
        errors.append("Missing 'name' field in frontmatter")
    elif not re.match(r"^[a-z][a-z0-9-]*$", name):
        errors.append(f"name must be kebab-case (got: {name})")
    elif len(name) > 64:
        errors.append(f"name must be <= 64 chars (got: {len(name)})")

    # 4. description 字段
    desc = frontmatter.get("description")
    if not desc:
        errors.append("Missing 'description' field in frontmatter")
    elif len(desc.strip()) < 20:
        warnings.append("description is very short — may not trigger reliably")

    # 5. Body 长度
    body = content[fm_match.end():]
    lines = body.strip().split("\n")
    if len(lines) > 500:
        warnings.append(f"Body is {len(lines)} lines (recommended < 500)")

    # 6. 检查引用的文件是否存在
    ref_pattern = re.compile(r'\[.*?\]\(((?:scripts|references|assets)/[^\)]+)\)')
    for match in ref_pattern.finditer(body):
        ref_path = os.path.join(skill_dir, match.group(1))
        if not os.path.exists(ref_path):
            errors.append(f"Referenced file not found: {match.group(1)}")

    # 7. 检查目录完整性
    for subdir in ["scripts", "references", "assets"]:
        subdir_path = os.path.join(skill_dir, subdir)
        if os.path.isdir(subdir_path) and not os.listdir(subdir_path):
            warnings.append(f"Empty directory: {subdir}/")

    # 8. allowed-tools 验证
    allowed_tools = frontmatter.get("allowed-tools")
    if allowed_tools is not None:
        valid_tools = {
            "Bash", "Read", "Write", "Edit", "Glob", "Grep",
            "WebSearch", "WebFetch", "AskUserQuestion", "Agent",
            "TodoWrite", "NotebookEdit"
        }
        if isinstance(allowed_tools, list):
            for tool in allowed_tools:
                if tool not in valid_tools:
                    warnings.append(f"Unknown tool in allowed-tools: {tool}")

    # 9. 禁止文件检查
    forbidden = ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md"]
    for fname in forbidden:
        if os.path.isfile(os.path.join(skill_dir, fname)):
            errors.append(f"Forbidden file found: {fname}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "name": name,
            "body_lines": len(lines),
            "has_scripts": os.path.isdir(os.path.join(skill_dir, "scripts")),
            "has_references": os.path.isdir(os.path.join(skill_dir, "references")),
            "has_assets": os.path.isdir(os.path.join(skill_dir, "assets")),
        }
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <skill_directory>", file=sys.stderr)
        sys.exit(2)

    result = validate_skill(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["valid"] else 1)
