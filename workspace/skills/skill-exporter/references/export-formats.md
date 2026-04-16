# Export Formats — 各框架格式规范

## 1. Claude Code (默认)

已由 skill-generator 生成，无需额外导出。

```
skill-name/
├── SKILL.md          (frontmatter: name, description, allowed-tools)
├── scripts/
├── references/
└── assets/
```

## 2. OpenClaw Agent

OpenClaw 用 workspace 文件组织 agent：

```
openclaw-export/
├── SOUL.md           (角色定义 — 从 task_description + quality_criteria 生成)
├── AGENTS.md         (工作流指令 — 从 SKILL.md body 转换)
├── TOOLS.md          (工具配置 — 从 allowed-tools 映射)
└── skills/
    └── {name}/
        └── SKILL.md  (OpenClaw skill 格式 — 比 Claude Code 更简洁)
```

**映射规则：**
- SOUL.md ← task_description + quality_criteria + audience
- AGENTS.md ← SKILL.md body（工作流步骤）
- TOOLS.md ← allowed-tools 映射到 OpenClaw 工具名
- skills/ ← scripts/ 保持不变，references/ 内容合并到 AGENTS.md

## 3. Cursor Rules

Cursor 用 `.cursorrules` 文件（纯文本 system prompt）：

```
.cursorrules          (单文件，所有指令合并)
```

**映射规则：**
- 开头：角色定义（从 task_description）
- 中间：工作流步骤（从 SKILL.md body，去掉 frontmatter）
- 结尾：约束和边界情况（从 edge_cases + security + scope_exclusions）
- 无 scripts/ 支持 — 脚本逻辑转为文字指令

## 4. Hermes Agent

Hermes 用 YAML 配置 + prompts 目录：

```
hermes-export/
├── agent.yaml        (agent 配置：name, model, tools, system_prompt 路径)
└── prompts/
    ├── system.md     (system prompt — 角色 + 工作流)
    └── examples/     (few-shot 示例 — 从 example_1, example_2 生成)
```

**映射规则：**
- agent.yaml ← name + model(glm-4-plus) + tools(从 allowed-tools 映射)
- system.md ← SOUL 角色 + SKILL.md body 合并
- examples/ ← session.json 中的 example_1, example_2 转为 few-shot 格式

## 5. Generic Prompt

纯 Markdown 格式，可直接粘贴到任何 LLM 的 system prompt：

```
PROMPT.md             (单文件，结构化 Markdown)
```

**结构：**
```markdown
# {skill_name}

## 角色
{从 task_description 生成}

## 触发条件
{从 trigger 生成}

## 工作流
{从 SKILL.md body 提取}

## 边界情况
{从 edge_cases 生成}

## 质量标准
{从 quality_criteria 生成}

## 约束
{从 security + scope_exclusions 生成}

## 示例
### 示例 1
{从 example_1 生成}
### 示例 2
{从 example_2 生成}
```
