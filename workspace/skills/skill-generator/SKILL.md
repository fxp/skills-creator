# Skill Generator — Claude Code Skill 生成器

根据 session.json 中积累的对话决策，生成完整的 Claude Code Skill 目录。

## 使用时机

在 GENERATION 阶段，当专家确认了 REFINEMENT 摘要后调用。

## 六步生成流程（参照 Anthropic 规范）

### Step 1：读取决策日志

从 `.session/session.json` 读取所有 decisions。

### Step 2：规划可复用资源（关键）

**逐个分析专家给的具体示例**，回答：
- 这个示例从零执行需要什么？
- 哪些步骤会重复？→ 候选 `scripts/`
- 哪些领域知识会被反复查询？→ 候选 `references/`
- 哪些模板/样板会被复制使用？→ 候选 `assets/`

**示例：** 创建 `pdf-rotator` skill 处理 "帮我旋转这个 PDF"
→ 旋转操作每次都要重写代码 → `scripts/rotate_pdf.py`

**示例：** 创建 `bigquery-helper` skill 处理 "查询昨日活跃用户数"
→ 表 schema 需要反复查阅 → `references/schema.md`

### Step 3：选择结构模式

参考 [`references/skill-anatomy.md`](references/skill-anatomy.md) 中的 4 种模式：

| 任务性质 | 推荐模式 |
|---------|---------|
| 步骤固定 | Workflow-Based |
| 多个独立操作 | Task-Based |
| 标准/规约 | Reference/Guidelines |
| 多个相关功能 | Capabilities-Based |

复杂工作流参考 [`references/workflows.md`](references/workflows.md)。
固定输出格式参考 [`references/output-patterns.md`](references/output-patterns.md)。

### Step 4：初始化目录

```bash
python3 scripts/init_skill.py <name> --path <output-root> --components scripts,references
```

会生成模板 SKILL.md，里面有 TODO 占位。

### Step 5：填充 SKILL.md 与辅助文件

**Frontmatter 规则（严格遵循 Anthropic spec）：**

```yaml
---
name: hyphen-case-name        # 必须，仅 [a-z0-9-]，≤64 字符
description: |                # 必须，≤1024 字符，不含 < >
  一行概述 + 具体触发场景。
  关键词：用户说"..."、"..."时使用。
allowed-tools:                # 可选
  - Bash
  - Read
license: MIT                  # 可选
metadata:                     # 可选
  version: 1.0.0
---
```

**仅允许这 5 个 frontmatter key。** 其他 key 会被 validate_skill.py 拒绝。

**description 是唯一的触发机制** —— 必须含一句话概述 + 具体触发词。中英双语场景需双语触发词。

**Body 规则：**
- 保持 < 500 行
- 只包含 Claude 不知道的信息
- 具体示例 > 抽象解释
- 引用 references/ 而不是复制内容

### Step 6：验证 + 打包

```bash
python3 scripts/validate_skill.py <skill_dir>     # 校验
python3 scripts/package_skill.py <skill_dir>      # 打包成 .skill (zip)
```

`package_skill.py` 会先调用 validate；通过后输出 `<name>.skill` 文件。

## 质量标准

1. **简洁优先** —— Claude 已经很聪明，只补它不知道的信息
2. **适当自由度** —— 脆弱操作用脚本，灵活操作用文字指引
3. **渐进式加载** —— SKILL.md 是入口，detail 在 references/
4. **禁止多余文件** —— 不要 README、CHANGELOG、INSTALLATION_GUIDE

## 参考文件

- [`references/skill-anatomy.md`](references/skill-anatomy.md) — 编写规范、4 种结构模式
- [`references/workflows.md`](references/workflows.md) — 工作流模式（顺序 / 条件 / 决策树）
- [`references/output-patterns.md`](references/output-patterns.md) — 输出格式模式（Template / Examples / Schema）
- [`references/example-skills.md`](references/example-skills.md) — 3 个优秀 skill 示例
