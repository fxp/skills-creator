# Plugin Anatomy — Claude Code Plugin 规范

参照 [Anthropic 官方 plugin 规范](https://code.claude.com/docs/en/plugins)。

## 目录结构

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 必需：plugin 清单
├── .mcp.json                # 可选：MCP server 配置
├── skills/                  # 自动触发的 skills
│   └── skill-name/
│       └── SKILL.md
├── commands/                # 显式 slash commands
│   └── command-name.md
├── agents/                  # 可选：自定义 subagents
├── hooks/                   # 可选：事件钩子
│   └── hooks.json
├── monitors/                # 可选：后台监控
│   └── monitors.json
├── settings.json            # 可选：默认设置
└── README.md                # 角色说明文档
```

**关键规则：** 只有 `plugin.json` 在 `.claude-plugin/` 内；其他目录都在 plugin 根目录。

## plugin.json 清单

**最简清单：**

```json
{
  "name": "sales-ops",
  "description": "Digital Sales Ops Associate — pipeline review, prospect research, weekly reports.",
  "version": "1.0.0",
  "author": { "name": "Your Org" }
}
```

**完整字段：**

| 字段 | 类型 | 用途 |
|------|------|------|
| `name` | string | 唯一标识，作为 skill 命名空间（如 `/sales-ops:prospect-research`）|
| `description` | string | plugin 管理器/marketplace 中显示 |
| `version` | string | 可选；省略时用 git commit SHA |
| `author` | object | `{ "name": "..." }` |
| `homepage` | string | 文档链接 |
| `repository` | string | git repo URL |
| `license` | string | 许可证 |
| `keywords` | array | 搜索 tags |

## 命名空间

plugin 名作为 skill 的前缀：

| 文件 | 调用方式 |
|------|---------|
| `skills/prospect-research/SKILL.md` | 自动触发，namespace `sales-ops:prospect-research` |
| `commands/weekly-report.md` | `/sales-ops:weekly-report` |

## Commands 格式

`commands/weekly-report.md`：

```markdown
---
description: 生成每周销售运营报告
---

执行以下步骤：

1. 调用 prospect-research skill 拉取本周新增 prospect
2. 调用 pipeline-review skill 评估 deal 状态
3. 按照 references/report-template.md 格式合并输出
```

Commands 是显式入口，比 skill 更"硬"（用户主动 `/cmd` 触发）。

## Marketplace 清单

**marketplace.json**（用于发布 plugin 集合）：

```json
{
  "name": "my-org-plugins",
  "owner": { "name": "My Org" },
  "plugins": [
    {
      "name": "sales-ops",
      "source": "./sales-ops",
      "description": "Sales Ops digital employee",
      "category": "sales"
    }
  ]
}
```

`source` 可以是：
- 本地路径：`"./plugin-dir"`
- 外部 git：`{"source": "url", "url": "https://...", "sha": "..."}`
- Git 子目录：`{"source": "git-subdir", "url": "...", "path": "...", "ref": "main"}`

## 安装与触发

```bash
# 本地测试
claude --plugin-dir ./my-plugin

# 从 marketplace 安装
/plugin install plugin-name

# 重新加载
/reload-plugins
```

## 与单个 Skill 的对比

| 维度 | 单 Skill | Plugin |
|------|---------|--------|
| 文件 | 1 个 SKILL.md | plugin.json + N skills + commands |
| 分发 | `.skill` zip | git repo / marketplace |
| 命名空间 | 无 | `plugin-name:skill-name` |
| 入口 | 自动触发 | 自动 + 显式 commands |
| 适用 | 个人/项目 | 团队/组织/企业 |
