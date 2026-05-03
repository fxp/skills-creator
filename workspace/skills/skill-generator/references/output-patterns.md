# Output Patterns — 输出格式模式

当 skill 需要产出一致、高质量的输出时，使用以下模式之一。

## 1. Template Pattern（模板模式）

提供输出格式模板。根据需求严格度选择措辞。

**严格要求（API 响应、数据格式）：**

```markdown
## 报告结构

ALWAYS use this exact template structure:

# [标题]

## 摘要
[一段话概述核心发现]

## 关键发现
- 发现 1（含支撑数据）
- 发现 2（含支撑数据）

## 建议
1. 具体可执行的建议
2. 具体可执行的建议
```

**灵活引导（允许根据上下文调整）：**

```markdown
## 报告结构

这是一个合理的默认格式，但请根据上下文判断：

# [标题]
## 摘要
## 关键发现
[根据发现适配章节]
## 建议
[根据具体场景定制]
```

## 2. Examples Pattern（示例模式）

当输出质量依赖看到示例时，提供 input/output 对：

```markdown
## Commit message 格式

按以下示例生成 commit message：

**示例 1：**
Input: 添加了 JWT 认证
Output:
\`\`\`
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
\`\`\`

**示例 2：**
Input: 修复报表日期显示错误
Output:
\`\`\`
fix(reports): correct date formatting in timezone conversion
\`\`\`

Follow this style: type(scope): brief description, then detailed explanation.
```

示例比描述更能让 Claude 理解期望的风格和细节程度。

## 3. Schema Pattern（模式模式）

当输出必须可机器解析时，提供 JSON Schema 或类似规约：

```markdown
## 输出格式

输出必须为 JSON，符合以下 schema：

\`\`\`json
{
  "status": "pass" | "fail" | "error",
  "issues": [{"file": string, "line": int, "message": string}],
  "score": float  // 0.0 - 1.0
}
\`\`\`

不允许任何 markdown 包裹，必须为纯 JSON。
```

## 选用建议

| 输出类型 | 推荐 |
|---------|------|
| 文档/报告（人类阅读） | Template + Examples |
| 短消息（commit、PR title） | Examples |
| 机器可解析（JSON/YAML） | Schema |
| 创意内容 | 灵活引导 + Examples |
