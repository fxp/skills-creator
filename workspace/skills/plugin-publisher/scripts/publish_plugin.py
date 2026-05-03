#!/usr/bin/env python3
"""publish_plugin.py — 把 plugin 发布到企业 marketplace

用法:
  publish_plugin.py <plugin_dir>
      --marketplace <marketplace.json>
      [--target local|git|zip]
      [--marketplace-dir <dir>]
      [--push]                          # git target only
      [--approve]                       # 批准 pending/ 中的 plugin

副作用:
  - 校验 plugin
  - 在 marketplace.json 的 plugins 数组中插入或更新条目
  - target=local: 复制 plugin 到 marketplace-dir
  - target=git: --push 时执行 git add/commit/push
  - target=zip: 输出 dist/<name>.zip + 不修改 marketplace
"""

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
# 复用 plugin-creator/scripts/validate_plugin
SIBLING = SCRIPT_DIR.parent.parent / "plugin-creator" / "scripts"
sys.path.insert(0, str(SIBLING))
try:
    from validate_plugin import validate_plugin  # type: ignore
except ImportError:
    print("ERROR: cannot import validate_plugin", file=sys.stderr)
    sys.exit(2)


def load_or_init_marketplace(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "name": "company-marketplace",
        "owner": {"name": "Your Org"},
        "plugins": [],
    }


def upsert_plugin(marketplace: dict, entry: dict) -> str:
    """Insert or update a plugin entry. Returns 'inserted' or 'updated'."""
    plugins = marketplace.setdefault("plugins", [])
    for i, p in enumerate(plugins):
        if p.get("name") == entry["name"]:
            plugins[i] = entry
            return "updated"
    plugins.append(entry)
    return "inserted"


def append_changelog(marketplace_dir: Path, plugin_name: str, version: str, action: str):
    cl = marketplace_dir / "changelog.md"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    line = f"- **{plugin_name}** v{version} {action}\n"
    if cl.exists():
        # Insert under today's heading or create one
        content = cl.read_text(encoding="utf-8")
        heading = f"## {today}"
        if heading in content:
            content = content.replace(heading, f"{heading}\n{line.rstrip()}")
        else:
            content = f"{heading}\n{line}\n" + content
    else:
        content = f"# Changelog\n\n## {today}\n{line}"
    cl.write_text(content, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Publish a plugin to enterprise marketplace")
    p.add_argument("plugin_dir", help="Path to the plugin directory")
    p.add_argument("--marketplace", required=True, help="Path to marketplace.json")
    p.add_argument("--target", choices=["local", "git", "zip"], default="local")
    p.add_argument("--marketplace-dir", help="Directory where local target copies plugin")
    p.add_argument("--push", action="store_true", help="git push after commit (target=git)")
    p.add_argument("--approve", action="store_true", help="Move from pending/ to published")
    args = p.parse_args()

    plugin_path = Path(args.plugin_dir).resolve()
    marketplace_path = Path(args.marketplace).resolve()
    marketplace_dir = Path(args.marketplace_dir).resolve() if args.marketplace_dir else marketplace_path.parent

    # 1. validate
    print(f"🔍 Validating {plugin_path.name}...")
    result = validate_plugin(plugin_path)
    if not result["valid"]:
        print("❌ Validation failed:")
        for e in result["errors"]:
            print(f"   • {e}")
        sys.exit(1)
    print(f"✅ Valid ({len(result['stats']['skills'])} skills, {result['stats']['commands']} commands)")

    # 2. read manifest
    manifest = json.loads((plugin_path / ".claude-plugin" / "plugin.json").read_text())
    name = manifest["name"]
    version = manifest.get("version", "0.1.0")

    # 3. copy / package
    if args.target == "local":
        dest = marketplace_dir / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(plugin_path, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        source_value = f"./{name}"
        print(f"📂 Copied → {dest}")
    elif args.target == "zip":
        dist = marketplace_dir / "dist"
        dist.mkdir(parents=True, exist_ok=True)
        zip_path = dist / f"{name}-{version}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in plugin_path.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    zf.write(path, path.relative_to(plugin_path.parent))
        source_value = str(zip_path.relative_to(marketplace_dir))
        print(f"📦 Packaged → {zip_path}")
    else:  # git
        source_value = f"./{name}"
        # caller is expected to have plugin already in the git workspace
        if args.push:
            subprocess.run(["git", "add", str(plugin_path)], cwd=marketplace_dir, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Publish {name} v{version}"],
                cwd=marketplace_dir,
                check=True,
            )
            subprocess.run(["git", "push"], cwd=marketplace_dir, check=True)
            print("📤 Pushed to git remote")

    # 4. update marketplace.json
    marketplace = load_or_init_marketplace(marketplace_path)
    entry = {
        "name": name,
        "source": source_value,
        "description": manifest.get("description", ""),
        "version": version,
        "author": manifest.get("author", {"name": "Unknown"}),
    }
    action = upsert_plugin(marketplace, entry)
    marketplace_path.write_text(
        json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"📝 marketplace.json {action}: {name}")

    # 5. changelog
    append_changelog(marketplace_dir, name, version, "发布" if action == "inserted" else "更新")
    print("✅ Done")


if __name__ == "__main__":
    main()
