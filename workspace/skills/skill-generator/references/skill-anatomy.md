# Skill Anatomy — Claude Code Skill 编写规范

## 目录结构

```
skill-name/
├── SKILL.md              (必须) 元数据 + 指令
├── scripts/              (可选) 可执行脚本
├── references/           (可选) 参考文档
└── assets/               (可选) 输出资源
```

## SKILL.md 格式

### Frontmatter (YAML)

```yaml
---
name: skill-name              # 必须: kebab-case, <64字符
description: |                 # 必须: 触发条件写在这里
  一行概述 skill 做什么。
  触发场景：用户说"..."、"..."时使用。
allowed-tools:                 # 可选: 限制可用工具
  - Bash
  - Read
  - Write
  - WebSearch
---
```

**name 规则：** 小写、横杠分隔、不超过 64 字符。

**description 规则：** 这是唯一决定 skill 何时被触发的字段。必须：
- 第一行概述功能
- 包含具体的触发词和场景
- 中文 skill 需要中英双语触发词

**allowed-tools 常用选项：** Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Agent, TodoWrite

### Body (Markdown)

**原则：**
- 保持 < 500 行
- 只包含 Claude 不知道的信息
- 具体示例 > 抽象解释
- 引用 references/ 而不是复制内容

**推荐结构：**
1. 一句话说明这个 skill 做什么
2. 核心工作流（步骤序列）
3. 关键决策点和分支逻辑
4. Edge case 处理
5. 引用详细参考文件

## 自由度选择

| 场景 | 自由度 | 实现方式 |
|------|--------|---------|
| 多种有效方法 | 高 | 文字指引 |
| 有推荐模式但允许变化 | 中 | 伪代码 + 参数 |
| 操作脆弱、必须精确 | 低 | 具体脚本 |

## 渐进式加载

1. **元数据** (name + description) — 始终在上下文中 (~100词)
2. **SKILL.md body** — skill 触发时加载 (<5k词)
3. **bundled resources** — 按需加载 (无限制)

## 禁止创建的文件

- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- 任何非功能性的辅助文档

## Scripts 最佳实践

- Python 优先（跨平台）
- 脚本顶部注释：输入格式、输出格式、依赖
- 包含基本错误处理
- 可以不加载到上下文就执行
- 文件名 snake_case: `validate_output.py`

## References 最佳实践

- 一级深度引用（从 SKILL.md 直接链接）
- 大文件 (>10k词) 在 SKILL.md 中提供 grep 搜索模式
- 按领域/功能分文件，避免单个巨型参考文件
- 信息不要在 SKILL.md 和 references 之间重复
