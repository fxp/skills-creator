#!/usr/bin/env bash
# run_eval.sh — 用 Claude Code CLI 运行单个 eval
# 输入: $1 = skill 目录, $2 = eval ID, $3 = prompt
# 输出: 测试输出写入 /tmp/skills-creator/test-results/{eval_id}.txt

set -euo pipefail

SKILL_DIR="${1:?Usage: run_eval.sh <skill_dir> <eval_id> <prompt>}"
EVAL_ID="${2:?Missing eval_id}"
PROMPT="${3:?Missing prompt}"

RESULTS_DIR="/tmp/skills-creator/test-results"
mkdir -p "$RESULTS_DIR"

OUTPUT_FILE="$RESULTS_DIR/${EVAL_ID}.txt"
TIMING_FILE="$RESULTS_DIR/${EVAL_ID}.time"

echo "Running eval: $EVAL_ID"
echo "Prompt: $PROMPT"
echo "---"

# 检查 claude CLI 是否可用
if ! command -v claude &>/dev/null; then
    echo "ERROR: claude CLI not found. Install Claude Code first." >&2
    echo '{"status": "error", "reason": "claude CLI not available"}' > "$OUTPUT_FILE"
    exit 1
fi

# 记录开始时间
START_TIME=$(date +%s)

# 运行 Claude Code 并捕获输出
# --print: 非交互模式，直接输出结果
# --permission-mode bypassPermissions: 跳过权限确认（测试环境）
claude --print \
    --permission-mode bypassPermissions \
    --prompt "You have a skill installed at $SKILL_DIR. Use it to handle this request: $PROMPT" \
    > "$OUTPUT_FILE" 2>&1 || true

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "$DURATION" > "$TIMING_FILE"
echo "Done in ${DURATION}s → $OUTPUT_FILE"
