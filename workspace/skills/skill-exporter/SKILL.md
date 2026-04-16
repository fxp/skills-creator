# Skill Exporter — 多框架导出器

将已生成的 Claude Code Skill 导出为其他 Agent 框架的格式。

## 使用时机

在 skill 创建完成后（Phase 6 ITERATE 通过或专家说 "ship it"），询问专家：
> "Skill 创建完成！除了 Claude Code 格式，你还需要导出到其他 Agent 框架吗？
> 支持的格式：OpenClaw、Cursor Rules、Hermes Agent、通用 Prompt。"

## 支持的导出格式

| 格式 | 输出文件 | 适用框架 |
|------|---------|---------|
| `claude-code` | `SKILL.md` + scripts/ + references/ | Claude Code (默认，已生成) |
| `openclaw` | `SOUL.md` + `AGENTS.md` + skills/ | OpenClaw Agent |
| `cursor` | `.cursorrules` | Cursor IDE |
| `hermes` | `agent.yaml` + prompts/ | Hermes Agent (Nous Research) |
| `generic` | `PROMPT.md` | 任何支持 system prompt 的 LLM/Agent |

## 导出流程

1. 读取 session.json 中的决策日志
2. 读取已生成的 Claude Code SKILL.md 作为源
3. 运行 `scripts/export_skill.py --format <格式> --session <session.json> --skill-dir <path> --output <path>`
4. 输出到 `{output_dir}/exports/{format}/`

## 格式说明

详见 `references/export-formats.md`

## 多格式批量导出

专家可以说"全部导出"，此时对所有格式各生成一份：

```bash
python3 scripts/export_skill.py --format all \
    --session /tmp/skills-creator/session.json \
    --skill-dir ./output/{name}/ \
    --output ./output/{name}/exports/
```
