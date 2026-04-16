# Question Bank — 完整问题语料库

## IDEATION 阶段

### 任务发现
- 你有什么重复性的任务，希望 Claude 能帮你自动化？
- 你日常工作中有没有什么事情每次都要花很多时间，但其实步骤差不多？
- 如果 Claude 能帮你做一件事，你最想它做什么？
- What repetitive task would you like Claude to handle for you?
- Is there something in your daily work that takes a lot of time but follows similar steps each time?

### 触发条件
- 你一般什么时候/什么情况下会做这个？
- 是什么事件或信号让你知道"该做这个了"？
- 是定期做的，还是某个事件触发的？
- When do you typically do this task?
- What event or signal tells you "it's time to do this"?

### 具体示例（第一个）
- 能给我走一遍吗？就像你现在要做这个任务一样。
- 从头到尾，一步一步地说说你怎么做的。
- 你打开什么工具/文件/页面？第一步做什么？
- Can you walk me through it step by step?
- What tools do you open first? What's step one?

### 输出形态
- 做完之后结果是什么样的？
- 结果是一个文件？一条消息？一个图表？
- 谁会用这个结果？他们用来做什么？
- What does the final output look like?
- Who consumes this output and what do they do with it?

### 第二个示例
- 能再给我一个不同的例子吗？最好是情况不太一样的。
- 有没有一个比较棘手的案例？
- 有没有你曾经做砸了或者花了特别久的一次？
- Can you give me a different example, ideally an unusual one?
- Was there ever a time this task went wrong or took unusually long?

### 命名
- 如果给这个工具起个名字，你会叫它什么？
- 你和同事怎么称呼这个任务？
- If you were naming this tool, what would you call it?

## REFINEMENT 阶段

### 边界情况
- 如果输入是空的，该怎么办？
- 如果数据格式不对呢？
- 如果数据量特别大/特别小会有问题吗？
- 有没有遇到过让你措手不及的情况？
- What if the input is empty or malformed?
- Have you ever encountered a case that caught you off guard?

### 排除条件
- 有没有什么情况看起来能用，但其实不该用这个 skill？
- 什么时候应该用人工而不是自动化？
- Are there situations where this seems applicable but actually shouldn't be used?

### 质量标准
- 你怎么判断结果好不好？
- 什么样的结果你会觉得"不对"需要重做？
- 有没有一个最低标准——低于这个就不能接受？
- How do you judge if the output is good?
- What would make you say "this needs to be redone"?

### 领域词汇
- 这里面有没有什么行话？
- [某个术语] 具体是什么意思？在你们这个领域怎么理解？
- 有没有缩写或简称我需要知道的？
- Are there domain-specific terms I should know?

### 工具和依赖
- 这个任务需要用到什么工具或系统？
- 需要访问什么 API 或数据源？
- 需要什么权限？
- What tools, APIs, or data sources does this depend on?

### 安全
- 有没有不能碰的数据？
- 有没有不能做的操作（比如删除、发送到外部）？
- 这里面有没有敏感信息需要特别处理？
- Are there any data or operations that are off-limits?

### 频率和规模
- 这个任务你多久做一次？
- 每次大概处理多少数据/文件/记录？
- 有峰值的时候吗？
- How often do you do this? What's the typical data volume?

### 协作
- 这个任务是你一个人做，还是有其他人参与？
- 结果需要别人审核吗？
- Is this a solo task or does it involve collaboration?

## 追问模板

### 回答太笼统
- "能再具体一点吗？比如上次你做这个的时候……"
- "你说的 {term} 具体是指什么？"
- "有没有一个真实的案例？"

### 信息可能不足
- "还有一个方面我想确认一下……"
- "关于 {topic}，如果遇到 {scenario} 会怎样？"
- "你刚才提到的 {point}，有没有例外情况？"

### 偏离主题
- "这很有意思。我们先把 {current_topic} 聊完，然后再来讨论这个。"
- "记下了。让我们先回到 {current_topic}。"

### STT 纠错
- "我听到你说 {term}——是 {clarification} 的意思吗？"
- "你说的是 {option_a} 还是 {option_b}？语音有时候不太清楚。"
- "I heard {term} — did you mean {clarification}?"
