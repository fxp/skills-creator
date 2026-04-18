# Examples — 真实生成产物

这里存放 Skills Creator Agent 真实运行产生的完整输出。每个示例包含：

- 原始**决策日志** (`session.json`) — 对话中萃取的 12 个决策维度
- 生成的 **Claude Code Skill** — SKILL.md + scripts + references
- 自动生成的 **测试套件** — `evals/eval-suite.json`
- **4 种框架导出** — OpenClaw / Cursor / Hermes / Generic

---

## 📦 commit-message-enhancer

**场景：** 后端开发者想要一个帮助写 Conventional Commits 规范 commit message 的 skill。

**从对话到成品：** 12 轮决策 → 1 个 Claude Code Skill (3 文件) + 8 个 eval 测试 + 4 种框架导出 = **17 个文件**

### 目录导览

```
commit-message-enhancer/
├── session.json                            # 对话决策日志（溯源）
├── SKILL.md                                # Claude Code skill 主文件
├── scripts/read_diff.sh                    # 读取 git diff + 敏感信息检测
├── references/glossary.md                  # 领域术语表
├── evals/eval-suite.json                   # 8 个自动生成的测试
└── exports/                                # 多框架导出
    ├── cursor/.cursorrules                 # Cursor IDE 规则
    ├── generic/PROMPT.md                   # 通用 LLM prompt
    ├── hermes/
    │   ├── agent.yaml
    │   ├── prompts/system.md
    │   ├── prompts/examples/*.md
    │   └── scripts/read_diff.sh
    └── openclaw/
        ├── SOUL.md                         # 角色定义
        ├── AGENTS.md                       # 工作流
        ├── TOOLS.md                        # 工具映射
        └── skills/commit-message-enhancer/
            ├── SKILL.md
            └── scripts/read_diff.sh
```

### 对话脚本（摘录）

完整 7 阶段对话见 [`commit-message-enhancer/transcript.md`](./commit-message-enhancer/transcript.md)。

### 真实验证结果

| 验证项 | 结果 |
|--------|------|
| `validate_skill.py` 格式校验 | ✅ valid, 0 errors, 0 warnings |
| Eval dry-run 分析 | ✅ 8/8 通过, 关键词覆盖 100% |
| 真实 git repo 正常 diff 测试 | ✅ 正确输出 `staged_files` + `diff_stats` |
| 真实 git repo 含假 API key 测试 | ✅ **成功捕获 `sk-...` 密钥，标记 `has_sensitive: true`** |
| 真实 git repo 空 diff 测试 | ✅ 返回 `{"empty": true}` 提示 |

---

## 复现这个示例

在本地运行完整的生成链路：

```bash
# 1. 写入决策日志
cp examples/commit-message-enhancer/session.json /tmp/skills-creator/session.json

# 2. 初始化 skill 目录
workspace/skills/skill-generator/scripts/init_skill.sh ./my-output commit-message-enhancer scripts references

# 3. 验证
python3 workspace/skills/skill-generator/scripts/validate_skill.py ./my-output/commit-message-enhancer

# 4. 生成 evals
python3 workspace/skills/eval-generator/scripts/generate_evals.py \
  /tmp/skills-creator/session.json \
  ./my-output/commit-message-enhancer

# 5. 多框架导出
python3 workspace/skills/skill-exporter/scripts/export_skill.py \
  --format all \
  --session /tmp/skills-creator/session.json \
  --skill-dir ./my-output/commit-message-enhancer \
  --output ./my-output/commit-message-enhancer/exports
```

或者通过 OpenClaw 语音对话自然生成（推荐）。
