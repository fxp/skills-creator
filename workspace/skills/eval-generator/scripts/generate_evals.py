#!/usr/bin/env python3
"""generate_evals.py — 从 session.json 生成 eval suite

输入: $1 = session.json 路径, $2 = skill 目录路径
输出: 在 skill 目录下创建 evals/eval-suite.json
"""

import json
import os
import sys
from datetime import datetime, timezone


def generate_evals(session_path: str, skill_dir: str) -> dict:
    """从 session 决策生成 eval 用例"""

    with open(session_path, "r", encoding="utf-8") as f:
        session = json.load(f)

    decisions = {d["topic"]: d["decision"] for d in session.get("decisions", [])}
    skill_name = session.get("skill_name", "unknown-skill")
    language = session.get("language", "en")

    evals = []
    eval_id = 0

    # 1. 从具体示例生成 happy path 测试
    for key in ["example_1", "example_2", "example_3"]:
        if key in decisions:
            eval_id += 1
            example = decisions[key]
            evals.append({
                "id": f"eval-{eval_id:02d}",
                "name": f"示例场景: {example[:50]}..." if language == "zh" else f"Example scenario: {example[:50]}...",
                "category": "happy_path",
                "prompt": extract_prompt_from_example(example, decisions),
                "context": example,
                "expected_behavior": build_expected_behavior(decisions),
                "unexpected_behavior": build_unexpected_behavior(decisions),
                "priority": "P0"
            })

    # 2. 从触发条件生成触发测试
    if "trigger" in decisions:
        eval_id += 1
        evals.append({
            "id": f"eval-{eval_id:02d}",
            "name": "触发条件验证" if language == "zh" else "Trigger validation",
            "category": "happy_path",
            "prompt": decisions["trigger"],
            "context": f"验证 skill 在正确条件下触发",
            "expected_behavior": [
                f"应正确识别为 {skill_name} 的使用场景",
                "应按照核心工作流执行"
            ],
            "priority": "P0"
        })

    # 3. 从边界情况生成 edge case 测试
    if "edge_cases" in decisions:
        edge_cases = decisions["edge_cases"]
        if isinstance(edge_cases, str):
            edge_cases = [e.strip() for e in edge_cases.split(";") if e.strip()]
        for ec in edge_cases[:3]:  # 最多 3 个边界测试
            eval_id += 1
            evals.append({
                "id": f"eval-{eval_id:02d}",
                "name": f"边界: {ec[:40]}" if language == "zh" else f"Edge: {ec[:40]}",
                "category": "edge_case",
                "prompt": build_edge_case_prompt(ec, decisions),
                "context": ec,
                "expected_behavior": ["应优雅地处理此边界情况", "不应崩溃或产生错误输出"],
                "priority": "P1"
            })

    # 4. 错误处理测试
    eval_id += 1
    evals.append({
        "id": f"eval-{eval_id:02d}",
        "name": "错误输入处理" if language == "zh" else "Error input handling",
        "category": "error_handling",
        "prompt": build_error_prompt(decisions),
        "context": "测试对无效/空输入的处理",
        "expected_behavior": [
            "应给出有意义的错误提示",
            "不应崩溃或产生不可预期的副作用"
        ],
        "unexpected_behavior": [
            "不应静默失败",
            "不应产生部分/损坏的输出"
        ],
        "priority": "P0"
    })

    # 5. 安全相关测试（如果有安全约束）
    if "security" in decisions:
        eval_id += 1
        evals.append({
            "id": f"eval-{eval_id:02d}",
            "name": "安全约束验证" if language == "zh" else "Security constraint check",
            "category": "edge_case",
            "prompt": build_security_prompt(decisions),
            "context": decisions["security"],
            "expected_behavior": ["应遵守安全约束", "不应执行被禁止的操作"],
            "unexpected_behavior": extract_security_violations(decisions),
            "priority": "P0"
        })

    suite = {
        "skill_name": skill_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_evals": len(evals),
        "evals": evals
    }

    # 写入文件
    evals_dir = os.path.join(skill_dir, "evals")
    os.makedirs(evals_dir, exist_ok=True)
    output_path = os.path.join(evals_dir, "eval-suite.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(suite, f, indent=2, ensure_ascii=False)

    return suite


def extract_prompt_from_example(example: str, decisions: dict) -> str:
    """从示例描述提取可用的提示词"""
    # 简化版：使用示例的前 100 个字符作为 prompt 基础
    trigger = decisions.get("trigger", "")
    if trigger:
        return trigger
    return example[:100]


def build_expected_behavior(decisions: dict) -> list:
    """从决策构建预期行为列表"""
    behaviors = []
    if "output_format" in decisions:
        behaviors.append(f"输出应为: {decisions['output_format']}")
    if "quality_criteria" in decisions:
        behaviors.append(f"质量标准: {decisions['quality_criteria']}")
    if not behaviors:
        behaviors.append("应产出有意义的输出")
    return behaviors


def build_unexpected_behavior(decisions: dict) -> list:
    """从决策构建不期望的行为列表"""
    unexpected = []
    if "scope_exclusions" in decisions:
        unexpected.append(f"不应: {decisions['scope_exclusions']}")
    return unexpected


def build_edge_case_prompt(edge_case: str, decisions: dict) -> str:
    """为边界情况构建测试 prompt"""
    task = decisions.get("task_description", "执行任务")
    return f"{task}（场景: {edge_case}）"


def build_error_prompt(decisions: dict) -> str:
    """构建错误输入的测试 prompt"""
    task = decisions.get("task_description", "处理数据")
    return f"{task}（输入为空或格式无效）"


def build_security_prompt(decisions: dict) -> str:
    """构建安全测试的 prompt"""
    task = decisions.get("task_description", "执行任务")
    security = decisions.get("security", "")
    return f"{task}（尝试触及安全边界: {security[:50]}）"


def extract_security_violations(decisions: dict) -> list:
    """提取安全违规行为列表"""
    security = decisions.get("security", "")
    if security:
        return [f"不应违反: {security}"]
    return []


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generate_evals.py <session.json> <skill_directory>", file=sys.stderr)
        sys.exit(2)

    result = generate_evals(sys.argv[1], sys.argv[2])
    print(f"Generated {result['total_evals']} evals → {sys.argv[2]}/evals/eval-suite.json")
