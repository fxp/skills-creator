# Tool Catalog — 企业系统集成模式

按职能列出常见企业工具，及其在 plugin 中的集成方式。

## 沟通与协作

| 工具 | 集成方式 |
|------|---------|
| Slack | MCP server (`@modelcontextprotocol/server-slack`) 或 Slack Web API + Bash |
| Microsoft Teams | Graph API + Bash |
| 飞书 / Lark | 飞书 SDK + MCP |
| 钉钉 | DingTalk OpenAPI |
| 企业微信 | WeCom API |
| Discord | Webhook 或 Discord.py |

## 文档与知识

| 工具 | 集成方式 |
|------|---------|
| Notion | MCP server (`@notionhq/notion-mcp-server`) |
| Google Workspace (Docs/Sheets) | Google MCP / Workspace API |
| Microsoft 365 | Graph API |
| Confluence | Atlassian REST API |
| Box / Dropbox | 各家 SDK |

## CRM / 销售

| 工具 | 集成方式 |
|------|---------|
| Salesforce | Salesforce REST API + Bash |
| HubSpot | HubSpot MCP |
| Close | Close API |
| Pipedrive | Pipedrive API |

## 客服 / 支持

| 工具 | 集成方式 |
|------|---------|
| Intercom | Intercom API |
| Zendesk | Zendesk API |
| Freshdesk | Freshdesk API |

## 项目 / 工单

| 工具 | 集成方式 |
|------|---------|
| Linear | Linear MCP / GraphQL |
| Jira | Atlassian MCP |
| Asana | Asana API |
| Monday | Monday API |
| ClickUp | ClickUp API |

## 数据 / BI

| 工具 | 集成方式 |
|------|---------|
| Snowflake | Snowflake Connector + Bash |
| BigQuery | `bq` CLI |
| Databricks | Databricks API |
| Hex | Hex API |
| Amplitude | Amplitude Export API |
| Looker | Looker SDK |

## 财务 / HR

| 工具 | 集成方式 |
|------|---------|
| QuickBooks | QB API |
| Xero | Xero API |
| Workday | Workday Web Services |
| Greenhouse | Greenhouse API |
| Lever | Lever API |

## 中国本土生态

| 工具 | 集成方式 |
|------|---------|
| 腾讯文档 / 腾讯会议 | 各家开放平台 API |
| 阿里云盘 / 钉钉文档 | 阿里开放平台 |
| 字节系（飞书 / 巨量引擎）| 字节开放 API |
| 高德 / 百度地图 | 各家开发者平台 |
| 微信生态 | 微信开放平台 |

## 在 plugin 中的体现

### 方式 1：`.mcp.json` 配置

适用于有现成 MCP server 的工具：

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": { "NOTION_TOKEN": "${NOTION_TOKEN}" }
    }
  }
}
```

### 方式 2：`scripts/` 调 API

适用于无现成 MCP 的工具：

```bash
# scripts/post_to_slack.sh
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -d "channel=$1&text=$2"
```

skill 在 `allowed-tools` 加 `Bash`，并在 SKILL.md 中说明何时调用脚本。

### 方式 3：commands 显式调用

对必须由人触发的危险/外部操作（发邮件、改 CRM 状态），优先做成 command 而非 auto-trigger 的 skill：

```markdown
# commands/post-update.md
---
description: 发送本周更新到团队 Slack
---

调用 scripts/post_to_slack.sh 把本周生成的 weekly-report.md 内容贴到 #sales-ops 频道。
```

## 选用决策树

```
任务需要外部系统？
├─ 否 → 不需要 .mcp.json，用 Bash + 本地文件
└─ 是 → 该工具有 MCP server？
        ├─ 是 → 用 .mcp.json
        └─ 否 → scripts/ 调 API
```
