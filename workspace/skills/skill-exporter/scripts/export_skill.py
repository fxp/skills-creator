#!/usr/bin/env python3
"""export_skill.py — 将 Claude Code Skill 导出为其他 Agent 框架格式

用法:
  export_skill.py --format <格式> --session <session.json> --skill-dir <path> --output <path>
  export_skill.py --format all --session <session.json> --skill-dir <path> --output <path>

支持格式: openclaw, cursor, hermes, generic, all
"""

import argparse
import json
import os
import re
import shutil
import sys
import textwrap
from datetime import datetime, timezone

import yaml


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def load_session(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_skill_md(skill_dir: str) -> tuple[dict, str]:
    """返回 (frontmatter_dict, body_str)"""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        return {}, content

    frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    body = content[fm_match.end():]
    return frontmatter, body


def decisions_dict(session: dict) -> dict:
    return {d["topic"]: d["decision"] for d in session.get("decisions", [])}


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 导出器: OpenClaw
# ─────────────────────────────────────────────

def export_openclaw(session: dict, frontmatter: dict, body: str, skill_dir: str, output: str):
    """导出为 OpenClaw workspace 格式"""
    d = decisions_dict(session)
    name = session.get("skill_name", "unnamed")
    out = os.path.join(output, "openclaw")

    # SOUL.md — 角色定义
    soul = f"""# {name} Agent

## 核心身份

{d.get('task_description', '未定义任务')}

## 质量标准

{d.get('quality_criteria', '按照最佳实践执行')}

## 目标受众

{d.get('audience', '通用用户')}

## 边界

- {d.get('security', '遵循安全最佳实践')}
- {d.get('scope_exclusions', '无额外排除')}
"""
    write_file(os.path.join(out, "SOUL.md"), soul)

    # AGENTS.md — 工作流
    agents = f"""# {name} — 工作流

## Session Startup

1. Read SOUL.md
2. 开始执行以下工作流

## 工作流

{body}

## 边界情况

{d.get('edge_cases', '无特殊边界情况')}
"""
    write_file(os.path.join(out, "AGENTS.md"), agents)

    # TOOLS.md
    tools_list = frontmatter.get("allowed-tools", [])
    tools_mapping = {
        "Bash": "shell (exec)",
        "Read": "file_read",
        "Write": "file_write",
        "Edit": "file_edit",
        "WebSearch": "web_search",
        "WebFetch": "web_fetch",
        "Glob": "file_glob",
        "Grep": "file_grep",
    }
    tools_lines = "\n".join(
        f"- {tools_mapping.get(t, t)}" for t in tools_list
    )
    tools = f"""# TOOLS.md

## 可用工具

{tools_lines}

## 领域术语

{d.get('domain_vocabulary', '无特殊术语')}
"""
    write_file(os.path.join(out, "TOOLS.md"), tools)

    # 生成 SKILL.md inside skills/{name}/
    skill_md_content = f"""---
name: {name}
description: |
  {d.get('task_description', 'Specialized agent')}
---

{body}
"""
    write_file(os.path.join(out, "skills", name, "SKILL.md"), skill_md_content)

    # 复制 scripts/
    src_scripts = os.path.join(skill_dir, "scripts")
    if os.path.isdir(src_scripts):
        dst_scripts = os.path.join(out, "skills", name, "scripts")
        if os.path.exists(dst_scripts):
            shutil.rmtree(dst_scripts)
        shutil.copytree(src_scripts, dst_scripts)
        print(f"  ✓ {dst_scripts}/ (copied)")


# ─────────────────────────────────────────────
# 导出器: Cursor Rules
# ─────────────────────────────────────────────

def export_cursor(session: dict, frontmatter: dict, body: str, skill_dir: str, output: str):
    """导出为 .cursorrules 格式"""
    d = decisions_dict(session)
    name = session.get("skill_name", "unnamed")
    out = os.path.join(output, "cursor")

    # 将 scripts 逻辑描述为文字（Cursor 不支持独立脚本）
    scripts_note = ""
    src_scripts = os.path.join(skill_dir, "scripts")
    if os.path.isdir(src_scripts):
        script_files = [f for f in os.listdir(src_scripts) if not f.startswith(".")]
        if script_files:
            scripts_note = f"\n## 辅助脚本\n\n以下脚本应放在项目根目录的 scripts/ 下：\n"
            for sf in script_files:
                scripts_note += f"- `scripts/{sf}`\n"

    rules = f"""# {name}

You are a specialized assistant for: {d.get('task_description', 'the defined task')}.

## When to Activate

Trigger when the user says: {d.get('trigger', 'relevant keywords')}.

## Workflow

{body}

## Edge Cases

{d.get('edge_cases', 'Handle edge cases gracefully.')}

## Quality Criteria

{d.get('quality_criteria', 'Follow best practices.')}

## Constraints

- Security: {d.get('security', 'Follow security best practices.')}
- Out of scope: {d.get('scope_exclusions', 'N/A')}
{scripts_note}
## Examples

### Example 1
{d.get('example_1', 'N/A')}

### Example 2
{d.get('example_2', 'N/A')}
"""
    write_file(os.path.join(out, ".cursorrules"), rules)


# ─────────────────────────────────────────────
# 导出器: Hermes Agent
# ─────────────────────────────────────────────

def export_hermes(session: dict, frontmatter: dict, body: str, skill_dir: str, output: str):
    """导出为 Hermes Agent 格式"""
    d = decisions_dict(session)
    name = session.get("skill_name", "unnamed")
    out = os.path.join(output, "hermes")

    # agent.yaml
    tools_list = frontmatter.get("allowed-tools", [])
    hermes_tools = []
    tool_map = {
        "Bash": "shell", "Read": "file_read", "Write": "file_write",
        "WebSearch": "web_search", "WebFetch": "web_fetch",
    }
    for t in tools_list:
        hermes_tools.append(tool_map.get(t, t.lower()))

    agent_yaml = f"""# Hermes Agent Configuration
# Generated by Skills Creator on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

name: {name}
description: {d.get('task_description', 'Specialized agent')}

model:
  provider: openai-compatible
  name: your-model-here
  base_url: https://your-api-endpoint/v1

system_prompt: prompts/system.md

tools:
{chr(10).join(f'  - {t}' for t in hermes_tools)}

parameters:
  temperature: 0.7
  max_tokens: 4096
"""
    write_file(os.path.join(out, "agent.yaml"), agent_yaml)

    # system.md
    system = f"""# {name}

## Role

{d.get('task_description', 'You are a specialized assistant.')}

## Workflow

{body}

## Constraints

- Quality: {d.get('quality_criteria', 'Follow best practices.')}
- Security: {d.get('security', 'Follow security best practices.')}
- Exclusions: {d.get('scope_exclusions', 'N/A')}

## Edge Cases

{d.get('edge_cases', 'Handle gracefully.')}
"""
    write_file(os.path.join(out, "prompts", "system.md"), system)

    # examples/
    for key in ["example_1", "example_2"]:
        if key in d:
            example = f"""## Scenario

{d[key]}

## Expected Behavior

The agent should follow the workflow above and produce output matching the quality criteria.
"""
            write_file(os.path.join(out, "prompts", "examples", f"{key}.md"), example)

    # 复制 scripts/
    src_scripts = os.path.join(skill_dir, "scripts")
    if os.path.isdir(src_scripts):
        dst = os.path.join(out, "scripts")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src_scripts, dst)
        print(f"  ✓ {dst}/ (copied)")


# ─────────────────────────────────────────────
# 导出器: Generic Prompt
# ─────────────────────────────────────────────

def export_generic(session: dict, frontmatter: dict, body: str, skill_dir: str, output: str):
    """导出为通用 PROMPT.md 格式"""
    d = decisions_dict(session)
    name = session.get("skill_name", "unnamed")
    out = os.path.join(output, "generic")

    # Strip references links from body (lines like "参见 references/xxx.md")
    clean_body = re.sub(r'(?m)^.*参见\s+references/\S+.*\n?', '', body)

    prompt = f"""# {name}

## 角色

{d.get('task_description', '你是一个专业助手。')}

## 触发条件

{d.get('trigger', '当用户请求相关任务时')}

## 工作流

{clean_body}

## 边界情况

{d.get('edge_cases', '优雅地处理异常情况。')}

## 质量标准

{d.get('quality_criteria', '遵循最佳实践。')}

## 约束

- 安全: {d.get('security', '遵循安全最佳实践。')}
- 排除范围: {d.get('scope_exclusions', '无')}

## 领域术语

{d.get('domain_vocabulary', '无特殊术语。')}

## 示例

### 示例 1
{d.get('example_1', '无')}

### 示例 2
{d.get('example_2', '无')}
"""
    write_file(os.path.join(out, "PROMPT.md"), prompt)


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

EXPORTERS = {
    "openclaw": export_openclaw,
    "cursor": export_cursor,
    "hermes": export_hermes,
    "generic": export_generic,
}


def main():
    parser = argparse.ArgumentParser(description="Export Claude Code Skill to other agent frameworks")
    parser.add_argument("--format", required=True, choices=list(EXPORTERS.keys()) + ["all"],
                        help="Target format (or 'all' for all formats)")
    parser.add_argument("--session", required=True, help="Path to session.json")
    parser.add_argument("--skill-dir", required=True, help="Path to the generated skill directory")
    parser.add_argument("--output", required=True, help="Output directory for exports")
    args = parser.parse_args()

    session = load_session(args.session)
    frontmatter, body = load_skill_md(args.skill_dir)

    formats = list(EXPORTERS.keys()) if args.format == "all" else [args.format]

    print(f"Exporting skill '{session.get('skill_name', '?')}' to: {', '.join(formats)}")
    print(f"Output: {args.output}")
    print()

    for fmt in formats:
        print(f"[{fmt}]")
        EXPORTERS[fmt](session, frontmatter, body, args.skill_dir, args.output)
        print()

    # 生成汇总
    summary = {
        "skill_name": session.get("skill_name"),
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "formats": formats,
        "output_dir": args.output,
    }
    summary_path = os.path.join(args.output, "export-summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
