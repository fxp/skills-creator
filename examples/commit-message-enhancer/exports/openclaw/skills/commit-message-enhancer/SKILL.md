---
name: commit-message-enhancer
description: |
  分析 git diff 并生成符合 Conventional Commits 规范的 commit message（中英双语），包括类型标签、范围、简洁的描述和可选的详细说明
---


# Commit Message Enhancer

分析 git 暂存区变更，生成规范的 Conventional Commits 消息。

## 核心工作流

1. **读取 diff** — 运行 `scripts/read_diff.sh` 获取 staged changes
2. **推断 type** — 基于改动性质判断（见下表）
3. **推断 scope** — 从修改的路径提取
4. **生成 description** — 祈使句，≤72 字符
5. **展示建议** — 返回候选消息让用户确认

## Type 推断规则

| 改动性质 | Type |
|---------|------|
| 新功能、新接口 | `feat` |
| Bug 修复 | `fix` |
| 仅改文档/注释 | `docs` |
| 仅格式化（prettier/black） | `style` |
| 重构（行为不变） | `refactor` |
| 仅改/加测试 | `test` |
| 构建/依赖/配置 | `chore` |

## Scope 推断

从 diff 的文件路径提取最相关的目录或模块名：
- `auth/login.py` + `auth/tokens.py` → scope: `auth`
- `components/Button.tsx` → scope: `components`
- 根目录或多模块改动 → 省略 scope

## 输出格式

```
<type>(<scope>): <description>

[optional body]

[optional BREAKING CHANGE footer]
```

## 边界情况

- **空 diff**：提示"暂存区无变更，先 `git add` 再试"
- **超大 diff (>1000 行)**：分解为多个 commit 建议
- **混合改动（代码+文档+测试）**：建议用户分成多个 commit

## 安全约束

- 检查 diff 中是否含有疑似密钥（匹配 `[A-Za-z0-9]{32,}`、`sk-`、`api_key` 等）
- 如发现敏感信息，**拒绝生成并提醒用户**，不要把敏感串写进 message
- 不自动执行 `git commit`，只输出建议
- 不处理已 push 的历史

## 领域术语

见 `references/glossary.md`

