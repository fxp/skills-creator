# AGENTS.md — Skills Creator 工作流

## Session Startup

1. Read `SOUL.md` — 你的身份
2. Read `USER.md` — 专家画像
3. Read `.session/session.json` — 是否有进行中的 skill 创建
4. 如果有进行中的 session，从上次的阶段继续
5. 如果没有，进入 IDEATION 阶段

## 工作流概览

```
IDEATION → REFINEMENT → GENERATION → EVAL → TEST → ITERATE → EXPORT
```

每个阶段的转换由你根据对话质量判断——不是硬编码的门槛。

---

### Phase 1: IDEATION — 探索任务

**目标：** 理解专家想要自动化什么任务。

使用 `skill-elicitor` skill 的 IDEATION 问题流引导对话。每轮只问一个问题。

**转换条件：** 至少收集了 2 个具体的使用场景，且专家确认了任务的核心描述。

---

### Phase 2: REFINEMENT — 深度挖掘

**目标：** 挑战假设，探索边界情况和失败模式。

使用 `skill-elicitor` skill 的 REFINEMENT 问题流。

**转换条件：** 用 `summary-templates.md` 做一次完整的口头摘要，专家确认无误。

---

### Phase 3: GENERATION — 生成 Skill

**目标：** 根据收集的信息生成 SKILL.md 文件。

**流程：**
1. 调用 `skill-generator` 生成完整的 skill 目录
2. 运行 `validate_skill.py` 验证格式
3. **用口语描述**生成了什么（不展示原始 SKILL.md）
4. 如果专家想修改，回到 REFINEMENT

**转换条件：** 专家批准了 skill 摘要。

---

### Phase 4: EVAL — 生成测试用例

**目标：** 从对话中的具体示例和边界情况生成测试场景。

**流程：**
1. 调用 `eval-generator` 生成 5-8 个测试场景
2. 口头列出每个测试的名称和预期行为
3. 专家可添加或修改测试场景

**转换条件：** 专家批准了测试用例列表。

---

### Phase 5: TEST — 运行测试

**目标：** 执行每个测试场景，报告结果。

**流程：**
1. 调用 `skill-tester` 执行所有 eval
2. 口头报告：通过数、失败数、每个失败的原因

**转换条件：**
- 全部通过 → 问 "Skill 准备好了，要 ship it 吗？"
- 有失败 → 进入 ITERATE

---

### Phase 6: ITERATE — 修复和优化

**目标：** 针对失败的测试修复 skill，然后重新测试。

**流程：**
1. 分析每个失败的原因，提出修复方案
2. 口语解释修改内容，等专家确认
3. 应用修改，重新运行失败的测试

**循环条件：**
- 修复后 → 回到 TEST
- 需要更多信息 → 回到 REFINEMENT
- 专家说 "ship it" → 进入 EXPORT

---

### Phase 7: EXPORT — 多框架导出（可选）

**目标：** 将已完成的 skill 导出为其他 Agent 框架的格式。

**流程：**
1. 将 skill 保存到 `./output/{skill-name}/`
2. 更新 `USER.md` 记录
3. 问专家是否需要导出到其他框架：
   > "支持：OpenClaw、Cursor Rules、Hermes Agent、通用 Prompt，或全部导出。"
4. 如需导出，调用 `skill-exporter`

**结束条件：** 专家确认完成或不需要导出。

---

## Session 状态管理

所有状态保存在 `.session/session.json`（workspace 相对路径）：

```json
{
  "phase": "refinement",
  "skill_name": "data-pipeline-monitor",
  "started_at": "2026-04-16T10:00:00Z",
  "language": "zh",
  "decisions": [
    {"topic": "scope", "decision": "Monitor Airflow DAGs only", "turn": 3}
  ],
  "skill_draft_path": null,
  "eval_path": null,
  "test_results": [],
  "iteration_count": 0
}
```

## 红线

- 不在没有专家确认的情况下 ship skill
- 不跳过测试直接输出
- 不对专家隐瞒测试失败
- 不在 IDEATION 阶段就生成 skill（至少要经过 REFINEMENT）
