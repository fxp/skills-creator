#!/usr/bin/env python3
"""package_plugin.py — 把 plugin 目录打包为可分发的 zip + marketplace.json snippet

用法:
  package_plugin.py <plugin_dir> [output_dir]

输出:
  - <plugin-name>.zip
  - marketplace-snippet.json  (可粘到现有 marketplace.json 的 plugins 数组里)
"""

import json
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from validate_plugin import validate_plugin  # noqa: E402


def package(plugin_dir: Path, out_dir: Path | None = None) -> Path | None:
    plugin_dir = plugin_dir.resolve()
    out_dir = (out_dir or Path.cwd()).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. validate
    print("🔍 Validating plugin...")
    result = validate_plugin(plugin_dir)
    if not result["valid"]:
        print("❌ Validation failed:", file=sys.stderr)
        for e in result["errors"]:
            print(f"   • {e}", file=sys.stderr)
        return None
    for w in result.get("warnings", []):
        print(f"   ⚠ {w}")
    print(f"✅ Valid ({len(result['stats']['skills'])} skills, {result['stats']['commands']} commands)\n")

    # 2. zip
    name = plugin_dir.name
    zip_path = out_dir / f"{name}.zip"
    print(f"📦 Packaging → {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in plugin_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.name in {".DS_Store"} or path.suffix == ".pyc":
                continue
            if "__pycache__" in path.parts:
                continue
            arcname = path.relative_to(plugin_dir.parent)
            zf.write(path, arcname)
    size_kb = zip_path.stat().st_size / 1024
    print(f"   ✓ {zip_path} ({size_kb:.1f} KB)")

    # 3. marketplace snippet
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    snippet = {
        "name": manifest["name"],
        "source": f"./{name}",
        "description": manifest.get("description", ""),
        "author": manifest.get("author", {"name": "Unknown"}),
    }
    if "version" in manifest:
        snippet["version"] = manifest["version"]
    snippet_path = out_dir / "marketplace-snippet.json"
    snippet_path.write_text(json.dumps(snippet, indent=2, ensure_ascii=False) + "\n")
    print(f"   ✓ {snippet_path} (paste into your marketplace.json plugins array)")

    return zip_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: package_plugin.py <plugin_dir> [output_dir]", file=sys.stderr)
        sys.exit(2)
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    res = package(Path(sys.argv[1]), out)
    sys.exit(0 if res else 1)
