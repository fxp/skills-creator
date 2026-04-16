# TOOLS.md — 环境配置

## 路径约定

- 生成的 Skills 输出到: `./output/{skill-name}/`
- Session 状态: `.session/session.json`

## Claude Code CLI

用于测试生成的 skills：
```bash
claude --print --dangerously-skip-permissions --prompt "..."
```

## 依赖

- OpenClaw 2026.3+
- Python 3.10+ (脚本运行)
- PyYAML (skill 验证)
- Claude Code CLI (skill 测试, 可选)
