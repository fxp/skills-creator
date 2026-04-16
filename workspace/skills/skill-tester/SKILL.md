# Skill Tester — 自动测试运行器

执行 eval suite 中的测试用例，对比实际输出与预期行为，报告测试结果。

## 使用时机

在 TEST 阶段，当 eval suite 生成且专家确认后调用。

## 测试执行方式

### 方式 1: Claude Code CLI（推荐）

对每个 eval，用 Claude Code CLI 在 `--print` 模式下执行：

```bash
scripts/run_eval.sh <skill_dir> <eval_id> <prompt>
```

这会：
1. 将 skill 临时加载到 Claude Code
2. 发送 eval 的 prompt
3. 捕获输出
4. 保存到 `/tmp/skills-creator/test-results/{eval_id}.txt`

### 方式 2: 启发式验证（备选）

如果 Claude Code CLI 不可用，运行 `scripts/analyze_results.py` 的 dry-run 模式：
- 检查 SKILL.md 是否覆盖了 eval 的场景
- 验证 frontmatter 的触发词是否匹配 eval prompt
- 检查 edge case 是否在 SKILL.md 中有处理说明

## 测试流程

1. 读取 eval-suite.json
2. 按 priority 排序（P0 先跑）
3. 对每个 eval 执行测试
4. 收集结果
5. 运行 `scripts/analyze_results.py` 生成报告
6. 更新 session.json

## 结果格式

```json
{
  "eval_id": "eval-01",
  "status": "pass",
  "actual_output_summary": "成功获取了 3 个 DAG 的状态信息...",
  "expected_met": ["调用了 API", "报告了状态"],
  "expected_missed": [],
  "unexpected_found": [],
  "execution_time_s": 12.5,
  "suggested_fix": null
}
```

status 值: `pass` | `fail` | `error` | `skip`

## 报告方式

口头报告结果时遵循 summary-templates.md 中的模板。关键：
- 先说总数（X 通过，Y 失败）
- 逐个解释失败原因
- 对每个失败提出修复建议
