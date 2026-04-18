#!/usr/bin/env bash
# read_diff.sh — 读取 git staged diff，检测敏感信息
# 输出: JSON { staged_files, diff_stats, has_sensitive, sensitive_warnings }
set -euo pipefail

# 检查是否在 git repo 中
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo '{"error":"Not a git repository"}' >&2
    exit 1
fi

# 获取 staged 文件列表
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")
if [ -z "$STAGED_FILES" ]; then
    echo '{"error":"No staged changes. Run `git add` first.","empty":true}'
    exit 0
fi

# 获取 diff 统计
STATS=$(git diff --cached --stat 2>/dev/null | tail -1 || echo "")

# 检测敏感信息
DIFF_CONTENT=$(git diff --cached 2>/dev/null)
SENSITIVE_PATTERNS='(sk-[A-Za-z0-9]{20,}|api[_-]?key["'\'']?\s*[:=]\s*["'\''][A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[A-Za-z0-9]{36})'
SENSITIVE_MATCHES=$(echo "$DIFF_CONTENT" | grep -E "$SENSITIVE_PATTERNS" | head -3 || true)

# 输出 JSON
python3 -c "
import json, sys
files = '''$STAGED_FILES'''.strip().split('\n')
stats = '''$STATS'''.strip()
sensitive = '''$SENSITIVE_MATCHES'''.strip()
print(json.dumps({
    'staged_files': files,
    'file_count': len(files),
    'diff_stats': stats,
    'has_sensitive': bool(sensitive),
    'sensitive_warnings': sensitive.split('\n') if sensitive else []
}, ensure_ascii=False, indent=2))
"
