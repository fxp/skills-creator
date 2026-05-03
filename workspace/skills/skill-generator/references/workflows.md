# Workflow Patterns — 工作流模式

生成 skill 的 SKILL.md body 时，根据任务的复杂度选用以下模式之一。

## 1. Sequential Workflow（顺序工作流）

**适用：** 任务有清晰的步骤序列。

在 SKILL.md 开头给一个总览，然后逐步展开：

```markdown
## 工作流总览

执行此任务包含以下步骤：

1. 分析输入（运行 analyze.py）
2. 创建配置（编辑 config.json）
3. 验证配置（运行 validate.py）
4. 执行操作（运行 execute.py）
5. 检查输出（运行 verify.py）
```

## 2. Conditional Workflow（条件工作流）

**适用：** 任务有分支逻辑，根据输入类型走不同路径。

```markdown
## 工作流

1. 判断操作类型：
   - **创建新内容** → 走 "创建工作流"
   - **编辑已有内容** → 走 "编辑工作流"

2. **创建工作流：** ...步骤...
3. **编辑工作流：** ...步骤...
```

## 3. Decision Tree（决策树）

**适用：** 多个判断点，每个判断点有多个分支。

```markdown
## 决策树

输入数据格式判断：
- CSV → 调用 read_csv.py
- JSON → 调用 read_json.py
- Excel → 调用 read_xlsx.py
- 其他 → 报错并提示支持的格式
```

## 选用建议

| 场景 | 推荐 |
|------|------|
| 步骤固定，无分支 | Sequential |
| 一两个分支 | Conditional |
| 三个以上判断点 | Decision Tree |
| 任务非线性、多入口 | 改用 Task-Based 结构（见 skill-anatomy.md）|
