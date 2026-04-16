#!/usr/bin/env bash
# init_skill.sh — 创建 Skill 目录结构
# 输入: $1 = 输出根目录, $2 = skill 名称, $3+ = 可选组件 (scripts, references, assets)
# 输出: 创建目录结构，打印路径

set -euo pipefail

OUTPUT_ROOT="${1:-.}"
SKILL_NAME="${2:?Usage: init_skill.sh <output_root> <skill_name> [scripts] [references] [assets]}"

# 验证 skill 名称格式 (kebab-case)
if ! echo "$SKILL_NAME" | grep -qE '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'; then
    echo "ERROR: Skill name must be kebab-case (lowercase, hyphens only): $SKILL_NAME" >&2
    exit 1
fi

if [ ${#SKILL_NAME} -gt 64 ]; then
    echo "ERROR: Skill name must be <= 64 characters: $SKILL_NAME" >&2
    exit 1
fi

SKILL_DIR="$OUTPUT_ROOT/$SKILL_NAME"

# 创建基础目录
mkdir -p "$SKILL_DIR"

# 创建可选子目录
shift 2
for component in "$@"; do
    case "$component" in
        scripts|references|assets)
            mkdir -p "$SKILL_DIR/$component"
            ;;
        *)
            echo "WARNING: Unknown component '$component', skipping" >&2
            ;;
    esac
done

echo "$SKILL_DIR"
