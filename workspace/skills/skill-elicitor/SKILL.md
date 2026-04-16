# Skill Elicitor — 对话引导引擎

通过结构化的苏格拉底式对话，从领域专家身上提取创建高质量 Claude Code Skill 所需的全部信息。

## 使用时机

在 IDEATION 和 REFINEMENT 阶段，你是主要的对话驱动者。根据当前阶段和已收集的信息，选择下一个最有价值的问题。

## 对话策略

### 关键原则
1. **一次一个问题** — 语音对话的铁律
2. **具体优于抽象** — "能举个例子吗" > "能详细说说吗"
3. **追问 > 新话题** — 深挖一个点比广泛覆盖更有价值
4. **确认术语** — 遇到可能的专业术语，立即确认含义

### IDEATION 阶段问题流

按优先级从上到下，每轮选一个问：

1. **任务探索** — "你有什么重复性的任务，希望 Claude 能帮你自动化？" / "What repetitive task would you like Claude to handle for you?"
2. **触发条件** — "你一般什么时候/什么情况下会做这个？" / "When or under what circumstances do you typically do this?"
3. **具体示例** — "能给我走一遍吗？就像你现在要做这个任务一样。" / "Can you walk me through it, as if you were doing it right now?"
4. **输出形态** — "做完之后结果是什么样的？谁会用这个结果？" / "What does the output look like? Who uses it?"
5. **第二个示例** — "能再给我一个不同的例子吗？最好是情况不太一样的。" / "Can you give me a different example? Ideally one where the situation is a bit different."
6. **命名** — "如果给这个 skill 起个名字，你会叫它什么？" / "If you were to name this skill, what would you call it?"

### REFINEMENT 阶段问题流

1. **边界情况** — "如果输入是空的，或者格式不对，会怎样？" / "What happens if the input is empty or malformed?"
2. **排除条件** — "有没有什么情况看起来能用，但其实不该用？" / "Are there situations where this seems applicable but actually isn't?"
3. **质量标准** — "你怎么判断结果好不好？什么样的结果算差的？" / "How do you judge if the result is good? What would a bad result look like?"
4. **领域词汇** — "这里面有没有什么行话或专业术语我需要知道的？" / "Are there any jargon or domain-specific terms I should know?"
5. **工具依赖** — "这个任务需要用到什么工具、API 或系统？" / "What tools, APIs, or systems does this task depend on?"
6. **安全考虑** — "有没有什么安全方面的红线？比如不能碰的数据、不能做的操作？" / "Are there any security red lines? Data you can't touch, operations you can't perform?"
7. **频率和规模** — "这个任务你多久做一次？每次大概处理多少数据？" / "How often do you do this? How much data do you typically handle each time?"

### 摘要确认（REFINEMENT 结束时）

用以下模板做口头摘要，等专家确认：

**中文模板：**
> "好的，让我确认一下我的理解。你需要一个 skill 来 {task_description}。它在 {trigger_conditions} 时启动。核心步骤是 {core_steps}。输出是 {output_format}，给 {audience} 用。需要注意的边界情况有：{edge_cases}。需要用到 {tools_apis}。对吗？有什么要补充或修改的？"

**English template:**
> "Let me confirm my understanding. You need a skill that {task_description}. It triggers when {trigger_conditions}. The core steps are {core_steps}. It outputs {output_format} for {audience}. Edge cases to handle: {edge_cases}. It depends on {tools_apis}. Is that right? Anything to add or change?"

## 决策记录

每当专家确认一个决策，记录到 session.json 的 decisions 数组：

```python
# 使用 scripts 目录下的工具更新 session
# decision topics: task_description, trigger, example_1, example_2,
#   output_format, audience, edge_cases, quality_criteria,
#   domain_vocabulary, tools_apis, security, scope_exclusions
```

## 追问技巧

当专家的回答太笼统时：
- "能具体一点吗？比如上次你做这个任务的时候……"
- "你说的 X 具体是指什么？"
- "有没有真实的例子？"

当专家说"就这些了"但你觉得信息不够时：
- "还有一个方面我想确认一下……"
- "关于 X，如果遇到 Y 的情况会怎样？"

当专家偏离主题时：
- "这很有意思。让我们先把 [当前话题] 聊完，然后再来讨论这个。"
