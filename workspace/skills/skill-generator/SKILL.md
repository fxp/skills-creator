# Skill Generator — Claude Code Skill 生成器

根据 session.json 中积累的对话决策，生成完整的 Claude Code Skill 目录。

## 使用时机

在 GENERATION 阶段，当专家确认了 REFINEMENT 摘要后调用。

## 生成流程

### Step 1: 读取决策日志

从 `/tmp/skills-creator/session.json` 读取所有 decisions。

### Step 2: 确定 Skill 结构

根据决策内容判断需要哪些组件：

| 条件 | 创建 |
|------|------|
| 任务有确定的步骤序列 | `scripts/` 下的脚本 |
| 需要领域知识或 API 文档 | `references/` 下的参考文件 |
| 需要模板或资源文件 | `assets/` 下的资源 |
| 简单任务 | 只需 SKILL.md |

### Step 3: 生成 SKILL.md

**Frontmatter 规则：**
```yaml
---
name: {kebab-case, 从 skill_name 决策获取}
description: |
  {从 task_description 决策生成，一行概述}
  {从 trigger 决策生成触发场景描述}
  {确保包含具体的触发词和场景}
allowed-tools:
  - {根据 tools_apis 决策选择}
---
```

**description 字段是最重要的** — 它决定了 skill 何时被触发。必须包含：
1. 一句话概述 skill 做什么
2. 具体的触发场景和关键词
3. 中英双语触发词（如果专家使用中文）

**Body 规则：**
- 保持在 500 行以内
- 先写核心工作流（步骤序列）
- 用具体示例而非抽象解释
- 引用 references/ 下的文件而不是复制内容
- 包含 edge case 处理说明

### Step 4: 生成辅助文件

**scripts/ — 当任务有确定步骤时：**
- Python 优先（跨平台）
- 每个脚本有明确的单一职责
- 包含基本的错误处理
- 在脚本顶部注释输入/输出格式

**references/ — 当需要领域知识时：**
- 从对话中提取的领域词汇表
- API 文档摘要
- 具体的示例和模板

### Step 5: 验证

运行 `scripts/validate_skill.py` 检查：
- frontmatter 格式正确
- name 是 kebab-case
- description 非空且包含触发信息
- 引用的文件都存在
- SKILL.md 行数 < 500

### Step 6: 输出

1. 创建目录: `{workspace}/output/{skill-name}/`
2. 写入所有文件
3. 更新 session.json 的 `skill_draft_path`

## 质量标准

参照 `references/skill-anatomy.md` 中的最佳实践。关键原则：

1. **简洁优先** — Claude 已经很聪明，只提供它不知道的信息
2. **适当的自由度** — 脆弱操作用脚本，灵活操作用文字指引
3. **渐进式加载** — SKILL.md 是入口，details 在 references/ 里
4. **不要多余文件** — 没有 README、CHANGELOG、安装指南

## 参考文件

- `references/skill-anatomy.md` — Skill 编写规范和最佳实践
- `references/example-skills.md` — 3 个优秀 skill 示例供参考
