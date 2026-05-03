# Plugin Creator — 企业数字员工 Plugin 生成器

将一段角色访谈转化为完整的 Claude Code Plugin —— 包含 `.claude-plugin/plugin.json`、若干 SKILL.md、commands、可选的 MCP server 配置 —— 作为一个**完整的数字员工**交付。

## 使用时机

当用户说"创建数字员工"、"生成 plugin"、"为 [角色] 团队搭一套 AI"、"build a plugin"、"create a digital employee"时启动。

与 `skill-creator`（生成单个 skill）的区别：

| 维度 | Skills Creator | Plugins Creator |
|------|---------------|-----------------|
| 输入 | 一位专家、一个任务 | 一个角色、5-7 个核心任务 |
| 输出 | 1 个 SKILL.md + 脚本 | 1 个完整 plugin（多个 skills + commands + 清单）|
| 对话长度 | 12-15 轮 | 30-50 轮（分多个会话）|
| 分发 | `.skill` 单文件 | git repo / marketplace |

## 八阶段工作流

```
ROLE → INVENTORY → TOOLS → DECOMPOSE → GENERATE → EVAL → TEST → PACKAGE
```

### Phase 1：ROLE — 角色定义

确定要构建的数字员工角色。

**关键问题：**
- "你想为哪个职能/团队搭这个数字员工？销售运营？财务分析？客服？招聘？还是其他？"
- "这个角色的人，每天上班的第一件事和最后一件事通常是什么？"
- "如果这个数字员工只能做好一件事，你最希望它能解决什么问题？"
- "这个角色的产出会被谁消费？写给老板看？给客户？给同事？"

参考 `references/enterprise-roles.md` 中的 10 个基线角色画像。

**转换条件：** 角色名、所属职能、3-5 句话的核心使命描述都已确认。

### Phase 2：INVENTORY — 任务盘点

列出这个角色每天/每周/每月做的所有具体任务。

**关键问题：**
- "我们一项项过：这个岗位每天都要做哪些事？哪怕是觉得很琐碎的也说。"
- "周一早上的例行公事是什么？"
- "月底会突然忙起来做什么？"
- "做哪些任务最痛苦/最容易出错？"

**目标：** 收集 8-15 个候选任务，最终筛选出 5-7 个核心任务进入 plugin。

**转换条件：** 任务清单完整，每个任务有 1-2 句话描述。

### Phase 3：TOOLS — 工具发现

确定数字员工需要接入的企业系统。

**关键问题：**
- "你们团队日常用什么工具？Slack？Notion？Salesforce？"
- "数据存在哪里？数据库？Google Sheets？还是某个 SaaS？"
- "需要写到外部的话，权限谁掌握？"

参考 `references/tool-catalog.md` 中的常见工具与对应 MCP server / API 集成模式。

**转换条件：** 每个核心任务的工具依赖都已明确，并标记需要 `.mcp.json` 还是仅 `Bash` + 脚本。

### Phase 4：DECOMPOSE — 技能分解

将每个核心任务转化为一个独立的 SKILL.md。

**对每个任务：**
1. 是否能独立成 skill？还是几个任务需要合并？
2. 是否需要 `commands/`（明确的 slash command 入口，如 `/sales-ops:weekly-report`）？
3. 共享的 references 是什么？（统一的术语表、模板库、领域知识）
4. 工具组合是什么？（allowed-tools 清单）

**转换条件：** 5-7 个独立 skill 的边界已划清，共享 references 已识别。

### Phase 5：GENERATE — 批量生成

**流程：**

1. 用 `scripts/init_plugin.py <plugin-name> --role <role>` 创建 plugin 骨架，包含：
   - `.claude-plugin/plugin.json`（清单）
   - `skills/`（每个 skill 一个子目录）
   - `commands/`（每个明确入口一个 .md）
   - `README.md`（角色说明）
2. 对每个 skill，复用 `skill-generator`（Phase 3 of skills-creator workflow）逐一生成
3. 共享内容（术语表、模板）放在 `skills/_shared/references/`

**转换条件：** 所有文件生成完毕，`validate_plugin.py` 通过。

### Phase 6-7：EVAL + TEST — 测试套件

每个 skill 各自跑 `eval-generator` + `skill-tester`。
**额外增加跨技能工作流测试**：例如 "/sales-ops:weekly-report 调用了 prospect-research 和 pipeline-review 两个 skill 后，输出格式正确"。

### Phase 8：PACKAGE — 打包分发

```bash
python3 scripts/package_plugin.py ./my-plugin
```

输出：
- `my-plugin/` 完整 plugin 目录（可作为 git repo 推送）
- `my-plugin.zip` 单文件分发包
- `marketplace-snippet.json` 一段可粘贴到 marketplace.json 的 plugins 数组项

## 角色模板（快速启动）

不想从零开始？参考 `references/role-templates/`：

- `sales-ops.json` — 销售运营 Associate（5 个 skill）
- `finance-analyst.json` — 财务分析师（6 个 skill）
- `customer-support.json` — 客服专员（5 个 skill）
- `recruiting.json` — 招聘专员（4 个 skill）

把模板载入 session.json 后跳过 ROLE/INVENTORY，直接进入 TOOLS 阶段做企业定制。

## 参考文件

- [`references/plugin-anatomy.md`](references/plugin-anatomy.md) — Anthropic plugin 规范
- [`references/enterprise-roles.md`](references/enterprise-roles.md) — 10 个基线企业角色
- [`references/tool-catalog.md`](references/tool-catalog.md) — 常见企业系统集成模式
- [`references/role-templates/`](references/role-templates/) — 预制的角色技能包
