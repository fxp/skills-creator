# Summary Templates — 阶段摘要模板

## IDEATION → REFINEMENT 摘要

### 中文
> 好的，让我梳理一下。你想要一个 skill 来帮你 {task_description}。
> 通常在 {trigger_conditions} 的时候用到。
> 你给了我两个例子：一个是 {example_1_brief}，另一个是 {example_2_brief}。
> 输出是 {output_format}，给 {audience} 用。
> 接下来我想深入了解一些边界情况和细节。准备好了吗？

### English
> Let me summarize what I've got so far. You want a skill that {task_description}.
> You typically need it when {trigger_conditions}.
> You gave me two examples: {example_1_brief} and {example_2_brief}.
> The output is {output_format}, used by {audience}.
> Next, I'd like to dig into edge cases and details. Ready?

## REFINEMENT → GENERATION 摘要（最重要的摘要）

### 中文
> 好的，让我做一个完整的确认。
>
> **任务：** {task_description}
> **触发条件：** {trigger_conditions}
> **核心步骤：** {core_steps}
> **输出：** {output_format}，给 {audience}
> **需要的工具：** {tools_apis}
> **边界情况：** {edge_cases}
> **质量标准：** {quality_criteria}
> **安全考虑：** {security_notes}
>
> 对吗？有什么要补充或修改的？确认之后我就开始生成了。

### English
> Let me do a complete confirmation.
>
> **Task:** {task_description}
> **Triggers:** {trigger_conditions}
> **Core steps:** {core_steps}
> **Output:** {output_format} for {audience}
> **Tools needed:** {tools_apis}
> **Edge cases:** {edge_cases}
> **Quality criteria:** {quality_criteria}
> **Security:** {security_notes}
>
> Does that cover it? Anything to add or change? Once confirmed, I'll start generating.

## GENERATION → EVAL 摘要

### 中文
> Skill 生成好了！叫 "{skill_name}"。
> 它会在 {triggers} 时自动启动。
> 具体做这些事：{steps_overview}。
> 我已经验证了格式没问题。
> 接下来我要为它生成测试用例。你准备好了吗？

### English
> The skill is ready! It's called "{skill_name}".
> It triggers on {triggers}.
> Here's what it does: {steps_overview}.
> Format validation passed.
> Now I'll generate test cases for it. Ready?

## EVAL → TEST 摘要

### 中文
> 我准备了 {n} 个测试用例：
> {for each: "第 {i} 个：{name} — {brief_description}"}
> 覆盖了 {n_happy} 个正常路径和 {n_edge} 个边界情况。
> 你觉得还需要加什么测试吗？没有的话我就开始跑了。

### English
> I've prepared {n} test cases:
> {for each: "{i}. {name} — {brief_description}"}
> Covering {n_happy} happy paths and {n_edge} edge cases.
> Want to add any tests? If not, I'll start running them.

## TEST 结果报告

### 全部通过 — 中文
> 好消息！{n} 个测试全部通过了。Skill 准备好了，要 ship 吗？

### 部分失败 — 中文
> {n_total} 个测试跑完了。{n_pass} 个通过，{n_fail} 个失败。
> 失败的是：
> {for each failed: "- {name}：{failure_reason}"}
> 我分析了一下，{fix_proposal}。要修复吗？

### 全部通过 — English
> Good news! All {n} tests passed. The skill is ready. Ship it?

### 部分失败 — English
> {n_total} tests completed. {n_pass} passed, {n_fail} failed.
> Failures:
> {for each failed: "- {name}: {failure_reason}"}
> My analysis: {fix_proposal}. Shall I fix it?

## 完成摘要

### 中文
> Skill "{skill_name}" 创建完成！
> {n_tests} 个测试全部通过，经过了 {iteration_count} 轮迭代。
> 输出在 output/{skill_name}/ 目录下。
> 你可以把它复制到 ~/.claude/skills/{skill_name}/ 来使用。
> 还有其他 skill 想创建吗？

### English
> Skill "{skill_name}" is complete!
> All {n_tests} tests passed after {iteration_count} iteration(s).
> Output is in output/{skill_name}/.
> Copy it to ~/.claude/skills/{skill_name}/ to use it.
> Want to create another skill?
