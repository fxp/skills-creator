# AGENTS.md — Skills Creator 工作流

## Session Startup

1. Read `SOUL.md` — 你的身份
2. Check `enterprise.config.json` — 如果存在，**进入 Enterprise Mode**（多员工部署）
3. 否则 Read `USER.md` — 单用户模式的专家画像
4. Read `.session/session.json`（或 `.session/{session_id}/session.json` 在 Enterprise Mode 下）— 是否有进行中的会话
5. 判断模式：
   - **Enterprise Mode** — 由 `employee-intake` skill 接管入口（多员工，多 plugin 库）
   - **Plugin Mode**（个人）— 用户说"创建数字员工 / 给团队搭一套 AI" → 调用 `plugin-creator`（8 阶段）
   - **Skill Mode**（个人）— 用户说"创建 skill" → 走 7 阶段（下方）

## Enterprise Mode — 多员工 Plugin 工厂

当 `enterprise.config.json` 存在时启用。

```
EMPLOYEE INTAKE → ROLE MATCH? ──┬─ YES → INSTALL GUIDANCE
                                 └─ NO  → PLUGIN CREATION (8 phases)
                                          → ADMIN REVIEW → PUBLISH
```

详见 [`skills/employee-intake/SKILL.md`](skills/employee-intake/SKILL.md) 和 [`skills/plugin-publisher/SKILL.md`](skills/plugin-publisher/SKILL.md)。

**关键约束（多员工隔离）：**
- 每个 session 用独立 `.session/{session_id}/` 目录
- **不读 USER.md**（USER.md 仅 admin 单人模式使用）
- 不复述上一位员工的角色或对话内容
- session 结束清理临时文件

## Plugin Mode — 八阶段（企业数字员工）

```
ROLE → INVENTORY → TOOLS → DECOMPOSE → GENERATE → EVAL → TEST → PACKAGE
```

详见 [`skills/plugin-creator/SKILL.md`](skills/plugin-creator/SKILL.md)。

可载入预制角色模板（`skills/plugin-creator/references/role-templates/`）跳过前 2 阶段，直接进入 TOOLS。

## Skill Mode — 七阶段（单个 Skill）

```
IDEATION → REFINEMENT → GENERATION → EVAL → TEST → ITERATE → PACKAGE/EXPORT
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

**流程（参照 Anthropic 六步法）：**
1. **规划资源** — 对每个示例分析需要什么 scripts/references/assets
2. **选择结构** — 4 种模式（Workflow / Task / Reference / Capabilities）选其一
3. **初始化** — `python3 init_skill.py <name> --path <out>`（生成带 TODO 的模板）
4. **填充内容** — 调用 `skill-generator` 把决策转化为 SKILL.md + 辅助文件
5. **验证** — `python3 validate_skill.py <dir>`（严格校验：仅 5 个允许的 frontmatter key、description ≤1024 字符、不含 `<>`）
6. **用口语描述**生成了什么（不展示原始 SKILL.md）

如果专家想修改，回到 REFINEMENT。

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

### Phase 7: PACKAGE & EXPORT — 打包 + 多框架导出

**目标：** 产出可分发的 `.skill` 文件，并按需转换到其他 Agent 框架。

**流程：**
1. 将 skill 保存到 `./output/{skill-name}/`
2. **打包为 `.skill`：** `python3 package_skill.py ./output/{name} ./output/{name}/dist/`
   生成的 `.skill` 文件是标准 zip，可直接分发或上传到 skill marketplace
3. 更新 `USER.md` 记录
4. 问专家是否需要导出到其他框架：
   > "已打包为 {name}.skill。还需要导出到 OpenClaw / Cursor / Hermes / 通用 Prompt 吗？"
5. 如需导出，调用 `skill-exporter`

**结束条件：** 专家确认完成。

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
