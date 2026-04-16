# Example Skills — 优秀 Skill 参考

以下是 3 个不同复杂度的优秀 skill 示例，供生成时参考风格和结构。

## 示例 1: 简单 Skill（无 scripts/references）

```yaml
---
name: code-review-helper
description: |
  帮助做代码审查，检查常见问题并给出改进建议。
  触发场景：用户说"review this"、"代码审查"、"帮我看看这段代码"时使用。
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

```markdown
# Code Review Helper

审查代码时关注以下维度，按优先级排列：

1. **安全性** — SQL注入、XSS、硬编码密钥
2. **正确性** — 逻辑错误、边界条件、空值处理
3. **可读性** — 命名、函数长度、注释必要性
4. **性能** — N+1查询、不必要的循环、内存泄漏

每个问题给出：位置、问题描述、建议修复、严重程度(P0-P2)。
```

**要点：** 简单任务不需要 scripts 或 references。description 包含了中英文触发词。

## 示例 2: 中等复杂度（有 scripts）

```
data-pipeline-monitor/
├── SKILL.md
└── scripts/
    └── check_dag_status.py
```

```yaml
---
name: data-pipeline-monitor
description: |
  监控 Airflow DAG 运行状态，检测失败和延迟。
  触发场景：用户说"check pipeline"、"DAG status"、"管道状态"、
  "有没有失败的任务"时使用。
allowed-tools:
  - Bash
  - Read
  - Write
---
```

```markdown
# Data Pipeline Monitor

## 工作流

1. 运行 `scripts/check_dag_status.py` 获取 DAG 状态
2. 分析结果，识别失败和延迟
3. 生成状态报告

## 状态判断

- **健康**: 所有 DAG 最近一次运行成功，执行时间在均值 2 倍标准差内
- **警告**: 执行时间超常但成功完成
- **失败**: 最近一次运行失败或超时

## 输出格式

Markdown 表格：DAG名称 | 上次状态 | 执行时间 | 趋势
```

**要点：** 确定性操作（API 调用）放在 script 里。SKILL.md 只包含决策逻辑。

## 示例 3: 复杂 Skill（完整结构）

```
tripgen/
├── SKILL.md
├── scripts/
│   ├── get_location.py
│   ├── generate_map.py
│   └── save_history.py
└── references/
    └── (省略)
```

```yaml
---
name: tripgen
description: |
  家庭出行规划 Agent — 根据天气、家庭成员构成、装备和实时进展，
  动态生成并更新一日游计划。
  触发场景：用户说"今天去哪玩"、"帮我规划出行"、"带孩子去哪好"、
  "周末亲子活动推荐"、"我们已经到了XX"等进展更新。
  只要涉及家庭出行规划、景点推荐、位置更新或实时进展汇报，就应调用此 skill。
allowed-tools:
  - Bash
  - WebSearch
  - WebFetch
  - Read
  - Write
  - AskUserQuestion
---
```

**要点：**
- description 非常详尽，列出了所有可能的触发场景
- 多个 scripts 各司其职
- allowed-tools 列表精确匹配需要的工具
- 中文 skill 用中文写 description 和 body

## 生成时的选择指南

| 任务复杂度 | 结构 |
|-----------|------|
| 纯文本指引，无外部依赖 | 只有 SKILL.md |
| 有 API 调用或精确操作 | SKILL.md + scripts/ |
| 需要领域知识参考 | SKILL.md + references/ |
| 复杂多步骤工作流 | SKILL.md + scripts/ + references/ |
| 需要模板或资源 | 加上 assets/ |
