#!/usr/bin/env python3
"""package_skill.py — 将一个 skill 目录打包为可分发的 .skill 文件

输入: $1 = skill 目录路径, $2 = 输出目录 (可选, 默认当前目录)
输出: <skill-name>.skill (一个标准 zip 压缩包)

打包前会自动调用 validate_skill.py 做校验，校验失败则中止打包。
"""

import os
import sys
import zipfile
from pathlib import Path

# 复用同目录下的 validate_skill.py
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from validate_skill import validate_skill  # noqa: E402


def package_skill(skill_dir: str, output_dir: str | None = None) -> Path | None:
    skill_path = Path(skill_dir).resolve()

    if not skill_path.exists():
        print(f"❌ Skill folder not found: {skill_path}", file=sys.stderr)
        return None
    if not skill_path.is_dir():
        print(f"❌ Path is not a directory: {skill_path}", file=sys.stderr)
        return None
    if not (skill_path / "SKILL.md").exists():
        print(f"❌ SKILL.md not found in {skill_path}", file=sys.stderr)
        return None

    # 1. Validate
    print("🔍 Validating skill...")
    result = validate_skill(str(skill_path))
    if not result["valid"]:
        print("❌ Validation failed:", file=sys.stderr)
        for err in result["errors"]:
            print(f"   • {err}", file=sys.stderr)
        return None
    if result.get("warnings"):
        for w in result["warnings"]:
            print(f"   ⚠ {w}")
    print(f"✅ Validation passed ({result['stats']['name']})\n")

    # 2. Determine output path
    out_root = Path(output_dir).resolve() if output_dir else Path.cwd()
    out_root.mkdir(parents=True, exist_ok=True)
    skill_file = out_root / f"{skill_path.name}.skill"

    # 3. Create zip
    print(f"📦 Packaging → {skill_file}")
    try:
        with zipfile.ZipFile(skill_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in skill_path.rglob("*"):
                if not path.is_file():
                    continue
                # 跳过常见垃圾
                if path.name in {".DS_Store"} or path.suffix in {".pyc"}:
                    continue
                if "__pycache__" in path.parts:
                    continue
                arcname = path.relative_to(skill_path.parent)
                zf.write(path, arcname)
                print(f"   + {arcname}")
    except Exception as e:
        print(f"❌ Failed to create .skill file: {e}", file=sys.stderr)
        return None

    size_kb = skill_file.stat().st_size / 1024
    print(f"\n✅ Packaged: {skill_file} ({size_kb:.1f} KB)")
    return skill_file


def main():
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <skill_directory> [output_directory]", file=sys.stderr)
        sys.exit(2)
    result = package_skill(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
