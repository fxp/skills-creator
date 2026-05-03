#!/usr/bin/env bash
# install.sh — Plugin Studio 企业部署一键安装脚本
#
# 用法:
#   sudo bash install.sh [--target-dir /opt/plugin-studio] [--gateway-bind lan]
#
# 功能:
#   1. 检查依赖（OpenClaw, Python 3.10+, PyYAML）
#   2. 把 workspace 拷贝到目标目录
#   3. 注册 OpenClaw agent (skills-creator)
#   4. 创建 enterprise.config.json（从模板）
#   5. 初始化空的 marketplace.json
#   6. 启动 OpenClaw Gateway

set -euo pipefail

# ─── 默认参数 ───
TARGET_DIR="/opt/plugin-studio"
GATEWAY_BIND="lan"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# ─── 解析参数 ───
while [[ $# -gt 0 ]]; do
    case $1 in
        --target-dir) TARGET_DIR="$2"; shift 2 ;;
        --gateway-bind) GATEWAY_BIND="$2"; shift 2 ;;
        -h|--help)
            grep '^#' "$0" | sed 's/^# \?//'
            exit 0 ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

echo "🦞 Plugin Studio Enterprise Installer"
echo "   Target: $TARGET_DIR"
echo "   Gateway bind: $GATEWAY_BIND"
echo ""

# ─── 1. 依赖检查 ───
echo "[1/6] 检查依赖..."

if ! command -v openclaw &>/dev/null; then
    echo "❌ openclaw not found. Install:"
    echo "   npm install -g openclaw"
    echo "   或 pnpm add -g openclaw"
    exit 1
fi
echo "   ✓ OpenClaw $(openclaw --version | head -1)"

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 not found"
    exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "   ✓ Python $PY_VERSION"

if ! python3 -c 'import yaml' 2>/dev/null; then
    echo "   Installing PyYAML..."
    pip3 install pyyaml --break-system-packages 2>/dev/null || pip3 install --user pyyaml
fi
echo "   ✓ PyYAML"

# ─── 2. 拷贝 workspace ───
echo ""
echo "[2/6] 部署 workspace 到 $TARGET_DIR..."

if [ -d "$TARGET_DIR" ]; then
    echo "   ⚠ 目录已存在，备份至 $TARGET_DIR.bak.$(date +%s)"
    mv "$TARGET_DIR" "$TARGET_DIR.bak.$(date +%s)"
fi

mkdir -p "$TARGET_DIR"
cp -r "$REPO_ROOT/workspace/." "$TARGET_DIR/"
echo "   ✓ workspace copied"

# ─── 3. 写入 enterprise.config.json ───
echo ""
echo "[3/6] 配置 enterprise.config.json..."

if [ ! -f "$TARGET_DIR/enterprise.config.json" ]; then
    cp "$SCRIPT_DIR/config.example.json" "$TARGET_DIR/enterprise.config.json"
    echo "   ✓ 已创建 $TARGET_DIR/enterprise.config.json"
    echo "   ⚠ 部署后请编辑该文件填入公司信息"
else
    echo "   ✓ 已存在"
fi

# ─── 4. 初始化 marketplace ───
echo ""
echo "[4/6] 初始化 marketplace..."

mkdir -p "$TARGET_DIR/marketplace"
if [ ! -f "$TARGET_DIR/marketplace/marketplace.json" ]; then
    cp "$SCRIPT_DIR/marketplace.example.json" "$TARGET_DIR/marketplace/marketplace.json"
fi
echo "   ✓ marketplace at $TARGET_DIR/marketplace/"

# ─── 5. 注册 OpenClaw agent ───
echo ""
echo "[5/6] 注册 OpenClaw agent 'plugin-studio'..."

openclaw agents add plugin-studio --workspace "$TARGET_DIR" --non-interactive 2>&1 | tail -5 || true
echo "   ✓ agent registered"

# ─── 6. 启动指引 ───
echo ""
echo "[6/6] 启动指引"
echo ""
echo "✅ 安装完成。下一步："
echo ""
echo "1. 编辑 $TARGET_DIR/enterprise.config.json 填入公司名、admins、Slack webhook 等"
echo ""
echo "2. 配置 LLM API key（建议 OpenAI 兼容端点）："
echo "   export OPENAI_API_KEY=your-key"
echo "   export OPENAI_BASE_URL=https://your-llm-endpoint/v1"
echo ""
echo "3. 启动 Gateway："
echo "   openclaw gateway --bind $GATEWAY_BIND"
echo ""
echo "4. 员工可通过以下方式接入："
echo "   - Web UI:    http://<server>:29533/<basePath>"
echo "   - 终端:       openclaw tui"
echo "   - Telegram:  openclaw channels add telegram"
echo "   - 飞书/钉钉等: 见 OpenClaw 文档"
echo ""
echo "📚 完整部署指南: $REPO_ROOT/enterprise/README.md"
