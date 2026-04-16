# Eval Generator — 测试用例生成器

从对话决策日志和生成的 SKILL.md 中提取测试场景，生成行为测试用例。

## 使用时机

在 EVAL 阶段，当 skill 已生成且专家批准后调用。

## 生成原则

### 测试什么
- **行为，不是语法** — 测试 skill 是否产出正确类型的输出，不是匹配特定字符串
- **覆盖对话中的例子** — 专家给的每个具体示例都应该成为测试
- **覆盖讨论的边界情况** — REFINEMENT 阶段发现的每个 edge case
- **测试错误处理** — 至少一个错误输入场景

### 测试数量
- 最少 5 个，最多 8 个
- 正常路径: 2-3 个（来自专家的例子）
- 边界情况: 2-3 个（来自 REFINEMENT 讨论）
- 错误处理: 1 个

## Eval Suite 格式

运行 `scripts/generate_evals.py` 生成 JSON：

```json
{
  "skill_name": "data-pipeline-monitor",
  "generated_at": "2026-04-16T10:30:00Z",
  "evals": [
    {
      "id": "eval-01",
      "name": "基本 DAG 状态检查",
      "category": "happy_path",
      "prompt": "检查我的数据管道状态",
      "context": "描述测试的前提条件和环境",
      "expected_behavior": [
        "应该调用 Airflow API",
        "应该报告 DAG 运行状态",
        "输出应包含 DAG 名称和执行时间"
      ],
      "unexpected_behavior": [
        "不应该修改任何 DAG 配置",
        "不应该重启失败的任务"
      ],
      "priority": "P0"
    }
  ]
}
```

### 字段说明

| 字段 | 必须 | 说明 |
|------|------|------|
| id | 是 | eval-01, eval-02, ... |
| name | 是 | 人类可读的测试名称 |
| category | 是 | happy_path / edge_case / error_handling |
| prompt | 是 | 发给 Claude 的提示词 |
| context | 否 | 测试前提条件描述 |
| expected_behavior | 是 | 预期行为列表（行为描述，不是精确字符串） |
| unexpected_behavior | 否 | 不应出现的行为 |
| priority | 是 | P0(必须通过) / P1(应该通过) / P2(最好通过) |

## 从决策到测试的映射

| 决策类型 | 测试类型 |
|----------|---------|
| example_1, example_2 | happy_path (P0) |
| edge_cases | edge_case (P0-P1) |
| quality_criteria | happy_path 的验证条件 |
| scope_exclusions | unexpected_behavior |
| security | error_handling (P0) |

## 输出

- 写入 `{skill_dir}/evals/eval-suite.json`
- 更新 session.json 的 `eval_path`
