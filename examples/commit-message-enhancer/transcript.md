# 对话脚本 — commit-message-enhancer

以下是一个模拟的完整对话脚本，展示 Skills Creator Agent 如何通过 7 阶段对话引导专家创建一个规范的 commit message 生成器。

> 每一轮对话都会写入 `session.json` 的 `decisions` 数组。真正的 agent 用 LLM 判断阶段转换时机；这个脚本是人工标注了阶段的演示版本。

---

## Phase 1 — IDEATION

**Agent:** 你好！我是你的 Skill 创建顾问。有什么重复性的任务，你希望 Claude 能帮你自动化？

**专家:** 我每天提交代码的时候，都要花时间写规范的 commit message。团队用 Conventional Commits，但我经常忘记 type，或者写得太啰嗦。

**Agent:** 懂了。所以是一个帮你从 git diff 自动生成 commit message 的工具？

**专家:** 对。我希望它能看懂我改了什么，自动推断 type 和 scope。

**Agent:** 能给我一个最近的具体例子吗？上一次你写 commit 是什么情况？

**专家:** 昨天我改了 `auth/login.py` 和 `auth/tokens.py`，加了个 JWT refresh token 的逻辑。我写的是 `feat(auth): add JWT refresh token support`。

**Agent:** 很好。"type(scope): description" 这个格式。那输出给谁用？你自己？

**专家:** 我自己，但 commit 会被团队其他人看到，也会进 release notes。

**Agent:** 再来一个不同的例子？最好是不同类型的。

**专家:** 上周修了个 `payment.py` 里的浮点数精度 bug，我写的是 `fix(payment): correct floating-point precision in amount calculation`。

> ✓ 转换条件满足：收集了 2 个具体示例 + 任务描述

---

## Phase 2 — REFINEMENT

**Agent:** 让我挑战几个边界情况。如果你什么都没 `git add`，暂存区是空的，会怎样？

**专家:** 应该提示我先 add 文件。

**Agent:** 如果改动特别大，比如 1000 行 diff 怎么办？一条 commit message 肯定说不清。

**专家:** ……对，那种情况应该建议我拆成多个 commit。

**Agent:** 如果我只跑了 prettier 格式化代码，Agent 会不会误判成 feat？

**专家:** 不行，那应该是 `style` 或 `chore`。

**Agent:** 怎么判断生成的 message 好不好？比如什么样的是"坏"的？

**专家:** description 如果不是祈使句（比如写成 "added X"）就不对。超过 72 个字符也不行。type 必须是 Conventional Commits 规定的 7 种之一。

**Agent:** 这里面有没有术语我要记一下？

**专家:** Conventional Commits, scope, breaking change, staged diff, imperative mood。

**Agent:** 安全方面呢？如果 diff 里不小心有 API key？

**专家:** ……好问题。那绝对不能把 key 写进 commit message 里。Agent 应该检测到然后**拒绝生成**，提醒我先撤回那个变更。

**Agent:** 还有一个我想确认一下——这个 skill 要不要自动执行 `git commit`？

**专家:** 不要。只给建议，我自己确认后再提交。如果是已经 push 的 commit 更不能碰，rewrite 历史很危险。

**Agent:** 好，让我完整确认一下我的理解：

> 你需要一个 skill 来分析 git staged diff，生成符合 Conventional Commits 规范的消息。它在你说"帮我写 commit"时触发。核心步骤是：读 diff → 推断 type/scope → 生成祈使句 description。输出是 `type(scope): description\n\n[body]` 格式。边界情况：空 diff、超大 diff、纯格式化、混合改动。需要用 git CLI。安全约束：检测密钥，拒绝生成含敏感信息的 message，不自动执行 commit，不处理已 push 历史。
>
> 对吗？还有什么要补充或修改的？

**专家:** 完美，就这样。

> ✓ 转换条件满足：专家确认摘要，进入 GENERATION

---

## Phase 3 — GENERATION

**Agent:** 好，我开始生成了。

（调用 `skill-generator`，生成 SKILL.md + `scripts/read_diff.sh` + `references/glossary.md`）

**Agent:** 生成了一个叫 `commit-message-enhancer` 的 skill。它会在你说"帮我写 commit"、"生成提交信息"时启动。核心工作流是：

1. 运行 `read_diff.sh` 读取 staged changes 并检测敏感信息
2. 按照 type 推断表选择 feat/fix/docs/style/refactor/test/chore
3. 从文件路径推断 scope
4. 生成 ≤72 字符的祈使句 description

如果检测到疑似 API key（比如 `sk-...`、`AKIA...`），会拒绝生成并警告你。

你觉得这个描述准确吗？

**专家:** 准确。

> ✓ 专家批准，进入 EVAL

---

## Phase 4 — EVAL

**Agent:** 我根据我们的对话生成了 8 个测试：

- **P0** `eval-01` happy_path — JWT refresh token 场景（来自你的例子 1）
- **P0** `eval-02` happy_path — payment precision 场景（来自你的例子 2）
- **P0** `eval-03` happy_path — 触发词验证
- **P1** `eval-04` edge_case — 空 diff
- **P1** `eval-05` edge_case — 超大 diff (>1000 行)
- **P1** `eval-06` edge_case — 纯格式化改动
- **P0** `eval-07` error_handling — 无效输入
- **P0** `eval-08` edge_case — **安全约束**（含密钥的 diff）

有什么测试场景我遗漏了？

**专家:** 挺全面的，跑吧。

> ✓ 进入 TEST

---

## Phase 5 — TEST

**Agent:** 跑完了。**8 个全部通过**。

启发式分析：所有 eval 的关键词在 SKILL.md 中覆盖率均为 100%。

我还在真实 git repo 上跑了脚本：
- 正常 diff → 正确返回文件列表和统计
- 含假 API key 的 diff → **成功捕获 `sk-...` 并标记为敏感**
- 空 diff → 返回 `{"empty": true}` 提示

Skill 准备好了。要 ship it 吗？还是想导出到其他 Agent 框架？

> ✓ 全部通过，进入 EXPORT

---

## Phase 6 (跳过 ITERATE)

所有测试通过，不需要迭代。

---

## Phase 7 — EXPORT

**Agent:** 除了 Claude Code 格式，还需要导出到哪些框架？

**专家:** 全部都要。

**Agent:** （调用 `skill-exporter --format all`）

已导出 4 种格式，共 17 个文件：

- `exports/openclaw/` — 完整 OpenClaw workspace (SOUL + AGENTS + TOOLS + skills)
- `exports/cursor/.cursorrules` — 单文件 Cursor 规则
- `exports/hermes/` — Hermes agent.yaml + prompts + scripts
- `exports/generic/PROMPT.md` — 通用 LLM system prompt

全部就绪，你可以把任意一份复制到对应的框架里用。

> ✓ 流程结束

---

## 耗时统计

| 阶段 | 大致轮次 |
|------|---------|
| IDEATION | 6 轮对话 |
| REFINEMENT | 6 轮对话 |
| GENERATION | 1 轮确认 |
| EVAL | 1 轮确认 |
| TEST | 自动执行 |
| EXPORT | 1 轮确认 |
| **总计** | **约 15 轮对话，纯语音约 12-15 分钟** |
