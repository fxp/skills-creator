#!/usr/bin/env bash
# run_suite.sh — 运行整个 eval suite
# 输入: $1 = skill 目录 (包含 evals/eval-suite.json)
# 输出: 所有测试结果在 /tmp/skills-creator/test-results/

set -euo pipefail

SKILL_DIR="${1:?Usage: run_suite.sh <skill_dir>}"
EVAL_SUITE="$SKILL_DIR/evals/eval-suite.json"

if [ ! -f "$EVAL_SUITE" ]; then
    echo "ERROR: eval-suite.json not found at $EVAL_SUITE" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="/tmp/skills-creator/test-results"
mkdir -p "$RESULTS_DIR"

# 清理旧结果
rm -f "$RESULTS_DIR"/eval-*.txt "$RESULTS_DIR"/eval-*.time

# 解析 eval suite 并逐个运行
TOTAL=$(python3 -c "import json; d=json.load(open('$EVAL_SUITE')); print(len(d['evals']))")
echo "Running $TOTAL evals for $(python3 -c "import json; d=json.load(open('$EVAL_SUITE')); print(d['skill_name'])")"
echo "========================================="

for i in $(seq 0 $((TOTAL - 1))); do
    EVAL_ID=$(python3 -c "import json; d=json.load(open('$EVAL_SUITE')); print(d['evals'][$i]['id'])")
    EVAL_NAME=$(python3 -c "import json; d=json.load(open('$EVAL_SUITE')); print(d['evals'][$i]['name'])")
    EVAL_PROMPT=$(python3 -c "import json; d=json.load(open('$EVAL_SUITE')); print(d['evals'][$i]['prompt'])")

    echo ""
    echo "[$((i+1))/$TOTAL] $EVAL_NAME ($EVAL_ID)"
    echo "-----------------------------------------"

    if "$SCRIPT_DIR/run_eval.sh" "$SKILL_DIR" "$EVAL_ID" "$EVAL_PROMPT"; then
        echo "  → Completed"
    else
        echo "  → Error during execution"
    fi
done

echo ""
echo "========================================="
echo "Suite complete. Results in $RESULTS_DIR/"
echo "Run analyze_results.py to generate the report."
