#!/usr/bin/env python3
"""init_plugin.py — 创建 Claude Code Plugin 骨架

用法:
  init_plugin.py <plugin-name> --path <output-root>
                                [--description "..."]
                                [--author "Your Org"]
                                [--version 1.0.0]
                                [--skills skill1,skill2,skill3]
                                [--commands cmd1,cmd2]
                                [--mcp slack,notion]

输出: 创建 <output-root>/<plugin-name>/ 目录，含 .claude-plugin/plugin.json + 子目录
"""

import argparse
import json
import re
import sys
from pathlib import Path


PLUGIN_JSON_TEMPLATE = {
    "name": "",
    "description": "",
    "version": "0.1.0",
    "author": {"name": "Your Org"},
}

README_TEMPLATE = """# {title}

{description}

## Skills

{skill_list}

## Commands

{command_list}

## Setup

1. Install via `/plugin install {name}` or place under `~/.claude/plugins/{name}/`
2. {mcp_setup_note}
3. `/reload-plugins` to activate

## Usage

Skills auto-trigger based on context. Commands are explicit:

```
{command_examples}
```
"""


# Common MCP server templates
MCP_TEMPLATES = {
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {"SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"},
    },
    "notion": {
        "command": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env": {"NOTION_TOKEN": "${NOTION_TOKEN}"},
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"},
    },
    "linear": {
        "command": "npx",
        "args": ["-y", "@tacticlaunch/mcp-linear"],
        "env": {"LINEAR_API_KEY": "${LINEAR_API_KEY}"},
    },
}


def kebab_check(name: str) -> str | None:
    if not re.match(r"^[a-z0-9-]+$", name):
        return "name must be hyphen-case (lowercase letters/digits/hyphens only)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return "name cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return f"name too long ({len(name)} chars). Maximum 64."
    return None


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path}")


def init_plugin(args) -> Path:
    err = kebab_check(args.name)
    if err:
        sys.exit(f"❌ {err}: {args.name}")

    root = Path(args.path).resolve()
    plugin_dir = root / args.name
    if plugin_dir.exists():
        sys.exit(f"❌ Already exists: {plugin_dir}")

    plugin_dir.mkdir(parents=True)

    # 1. plugin.json
    manifest = dict(PLUGIN_JSON_TEMPLATE)
    manifest["name"] = args.name
    manifest["description"] = args.description or f"Digital employee plugin: {args.name}"
    manifest["version"] = args.version
    manifest["author"] = {"name": args.author}
    write(
        plugin_dir / ".claude-plugin" / "plugin.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )

    # 2. skills/ 子目录骨架
    skills = [s.strip() for s in (args.skills or "").split(",") if s.strip()]
    for skill in skills:
        if kebab_check(skill):
            print(f"  ⚠ Skipped invalid skill name: {skill}", file=sys.stderr)
            continue
        skill_md = f"""---
name: {skill}
description: |
  [TODO: One sentence on what this skill does, plus specific triggers.
  Max 1024 characters. No < or >.]
---

# {' '.join(w.capitalize() for w in skill.split('-'))}

[TODO: Implement using one of the 4 structural patterns
 (Workflow / Task / Reference / Capabilities).
 See ../../skill-generator/references/skill-anatomy.md]
"""
        write(plugin_dir / "skills" / skill / "SKILL.md", skill_md)

    # 3. commands/
    commands = [c.strip() for c in (args.commands or "").split(",") if c.strip()]
    for cmd in commands:
        if kebab_check(cmd):
            continue
        cmd_md = f"""---
description: [TODO: What this command does]
---

[TODO: Steps to execute. Reference skills inside this plugin
 like: "Use the {{skill-name}} skill to ..."
]
"""
        write(plugin_dir / "commands" / f"{cmd}.md", cmd_md)

    # 4. .mcp.json
    mcps = [m.strip() for m in (args.mcp or "").split(",") if m.strip()]
    if mcps:
        mcp_config = {"mcpServers": {}}
        for m in mcps:
            if m in MCP_TEMPLATES:
                mcp_config["mcpServers"][m] = MCP_TEMPLATES[m]
            else:
                # Generic placeholder
                mcp_config["mcpServers"][m] = {
                    "command": "npx",
                    "args": ["-y", f"@example/mcp-server-{m}"],
                    "env": {f"{m.upper()}_TOKEN": f"${{{m.upper()}_TOKEN}}"},
                }
        write(
            plugin_dir / ".mcp.json",
            json.dumps(mcp_config, indent=2) + "\n",
        )

    # 5. README.md
    skill_list = "\n".join(f"- `{s}`" for s in skills) or "(none yet)"
    command_list = "\n".join(f"- `/{args.name}:{c}`" for c in commands) or "(none yet)"
    cmd_examples = "\n".join(f"/{args.name}:{c}" for c in commands[:3]) or f"# (auto-trigger by saying things related to {args.name})"
    mcp_note = (
        f"Set environment variables: {', '.join(f'{m.upper()}_TOKEN' for m in mcps)}"
        if mcps else "No external services required"
    )
    write(
        plugin_dir / "README.md",
        README_TEMPLATE.format(
            title=" ".join(w.capitalize() for w in args.name.split("-")),
            description=manifest["description"],
            skill_list=skill_list,
            command_list=command_list,
            mcp_setup_note=mcp_note,
            command_examples=cmd_examples,
            name=args.name,
        ),
    )

    return plugin_dir


def main():
    p = argparse.ArgumentParser(description="Initialize a Claude Code Plugin")
    p.add_argument("name", help="Plugin name (hyphen-case)")
    p.add_argument("--path", default=".", help="Output root (default: current dir)")
    p.add_argument("--description", default="", help="Plugin description")
    p.add_argument("--author", default="Your Org", help="Author name")
    p.add_argument("--version", default="0.1.0", help="Initial version")
    p.add_argument("--skills", default="", help="Comma-separated skill names")
    p.add_argument("--commands", default="", help="Comma-separated command names")
    p.add_argument("--mcp", default="", help="Comma-separated MCP servers (slack, notion, github, linear, ...)")
    args = p.parse_args()

    print(f"📦 Initializing plugin '{args.name}' under {Path(args.path).resolve()}")
    plugin_dir = init_plugin(args)
    print(f"\n✅ Created: {plugin_dir}")
    print("\nNext steps:")
    print(f"  1. Edit each skills/*/SKILL.md TODO")
    print(f"  2. Edit each commands/*.md TODO")
    print(f"  3. Validate: python3 validate_plugin.py {plugin_dir}")
    print(f"  4. Package:  python3 package_plugin.py {plugin_dir}")


if __name__ == "__main__":
    main()
