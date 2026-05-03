# Role Detection — 员工角色识别问题模板

不要直接问"你是什么职位？"——太正式。用任务/部门/工具三角度交叉问。

## 问题层次（按顺序）

### Layer 1：开放性接待
- "你好！能简单介绍一下你做什么吗？"
- "你在 {company_name} 的哪个团队？"

### Layer 2：任务确认（如果 Layer 1 模糊）
- "你日常最花时间的事是什么？"
- "上周做过什么让你觉得'又是这个'的任务？"

### Layer 3：工具确认（如果 Layer 2 仍模糊）
- "你常用什么工具？Salesforce？Notion？Excel？"
- "数据存在哪？你最常打开哪个软件？"

## 角色映射启发式

收到员工回答后，按关键词映射到 enterprise-roles.md 中的 10 个基线角色：

| 关键词信号 | 映射角色 |
|-----------|---------|
| pipeline / 客户 / quota / Salesforce / 报价 | sales-ops |
| 关账 / 凭证 / 对账 / P&L / 预算 | finance-analyst |
| 工单 / 客户 / 投诉 / Zendesk / 退款 | customer-support |
| 简历 / 面试 / JD / offer / Greenhouse | recruiting |
| 内容 / 投放 / 品牌 / SEO / GA4 | marketing-coordinator |
| PRD / roadmap / 用户访谈 / Linear | product-manager |
| 合同 / NDA / 合规 / 风险 | legal-ops |
| SQL / dashboard / 数据 / Snowflake | data-analyst |
| 邮件 / 会议 / 日历 / 待办 | productivity-assistant |

**含糊地带：** 当员工的角色不在基线 10 个中时，转入 `plugin-creator` 的 ROLE 阶段从零定义。

## 避免的话术

❌ "请填写以下信息：姓名、职位、部门..."（太像表单）
❌ "你属于哪个细分岗位？"（不是所有人想给自己贴标签）
❌ "我先帮你做一份能力测评"（员工反感）

✅ "你今天最想 AI 帮你解决什么？"（任务驱动）
✅ "你团队里有几个人？大家分工大概怎样？"（侧面了解）

## 多语言处理

中文员工先用中文，英文员工用英文。避免中英夹杂。例外：技术术语（如 PRD / SQL / OKR）保留原词。
