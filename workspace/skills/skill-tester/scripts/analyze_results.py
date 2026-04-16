#!/usr/bin/env python3
"""analyze_results.py — 分析测试结果，与预期行为对比

输入: $1 = eval-suite.json 路径, $2 = test-results 目录 (可选, 默认 /tmp/skills-creator/test-results)
输出: JSON 格式的分析报告 (stdout)

两种模式:
- 实际测试分析: 有 test-results 目录时，比对实际输出与预期
- 启发式分析 (dry-run): 没有 test-results 时，基于 SKILL.md 内容做静态分析
"""

import json
import os
import re
import sys


def analyze_results(eval_suite_path: str, results_dir: str) -> dict:
    """分析测试结果"""

    with open(eval_suite_path, "r", encoding="utf-8") as f:
        suite = json.load(f)

    results = []
    total_pass = 0
    total_fail = 0
    total_error = 0

    for eval_item in suite["evals"]:
        eval_id = eval_item["id"]
        result_file = os.path.join(results_dir, f"{eval_id}.txt")
        timing_file = os.path.join(results_dir, f"{eval_id}.time")

        if not os.path.isfile(result_file):
            results.append({
                "eval_id": eval_id,
                "name": eval_item["name"],
                "status": "skip",
                "reason": "No output file found",
                "suggested_fix": None
            })
            continue

        with open(result_file, "r", encoding="utf-8") as f:
            actual_output = f.read()

        # 读取执行时间
        execution_time = None
        if os.path.isfile(timing_file):
            with open(timing_file, "r") as f:
                try:
                    execution_time = float(f.read().strip())
                except ValueError:
                    pass

        # 检查是否有执行错误
        if actual_output.startswith("ERROR:") or '{"status": "error"' in actual_output:
            total_error += 1
            results.append({
                "eval_id": eval_id,
                "name": eval_item["name"],
                "status": "error",
                "actual_output_summary": actual_output[:200],
                "execution_time_s": execution_time,
                "suggested_fix": "检查 Claude Code CLI 配置和 skill 路径"
            })
            continue

        # 检查预期行为
        expected = eval_item.get("expected_behavior", [])
        unexpected = eval_item.get("unexpected_behavior", [])

        expected_met = []
        expected_missed = []
        unexpected_found = []

        for exp in expected:
            # 简单的关键词匹配（实际使用时可以更智能）
            keywords = extract_keywords(exp)
            if any(kw.lower() in actual_output.lower() for kw in keywords):
                expected_met.append(exp)
            else:
                expected_missed.append(exp)

        for unexp in unexpected:
            keywords = extract_keywords(unexp)
            if any(kw.lower() in actual_output.lower() for kw in keywords):
                unexpected_found.append(unexp)

        # 判断通过/失败
        if not expected_missed and not unexpected_found:
            status = "pass"
            total_pass += 1
            suggested_fix = None
        else:
            status = "fail"
            total_fail += 1
            fixes = []
            if expected_missed:
                fixes.append(f"缺少预期行为: {'; '.join(expected_missed)}")
            if unexpected_found:
                fixes.append(f"出现不期望的行为: {'; '.join(unexpected_found)}")
            suggested_fix = " | ".join(fixes)

        results.append({
            "eval_id": eval_id,
            "name": eval_item["name"],
            "status": status,
            "actual_output_summary": actual_output[:300],
            "expected_met": expected_met,
            "expected_missed": expected_missed,
            "unexpected_found": unexpected_found,
            "execution_time_s": execution_time,
            "suggested_fix": suggested_fix
        })

    report = {
        "skill_name": suite["skill_name"],
        "total": len(suite["evals"]),
        "pass": total_pass,
        "fail": total_fail,
        "error": total_error,
        "skip": len(suite["evals"]) - total_pass - total_fail - total_error,
        "all_passed": total_fail == 0 and total_error == 0,
        "results": results
    }

    return report


def extract_keywords(text: str) -> list:
    """从行为描述中提取关键词"""
    # 去掉常见的前缀词
    text = re.sub(r'^(应该|应|不应该|不应|should|must|不能|不要)\s*', '', text)
    # 提取有意义的词（中文或英文）
    words = re.findall(r'[\w\u4e00-\u9fff]{2,}', text)
    return words[:5]  # 最多 5 个关键词


def dry_run_analyze(eval_suite_path: str, skill_md_path: str) -> dict:
    """启发式分析（无实际测试结果时）"""

    with open(eval_suite_path, "r", encoding="utf-8") as f:
        suite = json.load(f)

    with open(skill_md_path, "r", encoding="utf-8") as f:
        skill_content = f.read().lower()

    results = []
    for eval_item in suite["evals"]:
        # 检查 SKILL.md 是否覆盖了 eval 的关键词
        keywords = extract_keywords(eval_item.get("prompt", ""))
        coverage = sum(1 for kw in keywords if kw.lower() in skill_content) / max(len(keywords), 1)

        status = "pass" if coverage >= 0.5 else "fail"
        results.append({
            "eval_id": eval_item["id"],
            "name": eval_item["name"],
            "status": status,
            "mode": "dry_run",
            "keyword_coverage": f"{coverage:.0%}",
            "suggested_fix": None if status == "pass" else f"SKILL.md 可能未覆盖此场景的关键词"
        })

    total_pass = sum(1 for r in results if r["status"] == "pass")
    return {
        "skill_name": suite["skill_name"],
        "mode": "dry_run",
        "total": len(results),
        "pass": total_pass,
        "fail": len(results) - total_pass,
        "results": results
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_results.py <eval-suite.json> [test-results-dir]", file=sys.stderr)
        print("       analyze_results.py --dry-run <eval-suite.json> <SKILL.md>", file=sys.stderr)
        sys.exit(2)

    if sys.argv[1] == "--dry-run":
        if len(sys.argv) != 4:
            print("Usage: analyze_results.py --dry-run <eval-suite.json> <SKILL.md>", file=sys.stderr)
            sys.exit(2)
        report = dry_run_analyze(sys.argv[2], sys.argv[3])
    else:
        results_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/skills-creator/test-results"
        report = analyze_results(sys.argv[1], results_dir)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if report.get("all_passed", report["fail"] == 0) else 1)
