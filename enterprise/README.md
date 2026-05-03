# Plugin Studio — 企业部署版

把 Skills Creator 升级为**企业级 AI 同事生成工厂**。员工对着它说话，它产出针对该员工角色的 Claude Code Plugin。

## 适用场景

| 场景 | 受众 |
|------|------|
| 公司刚开始用 Claude Code，想给每个职能配一个 AI 同事 | HR / IT |
| 已有一些 plugin，新员工入职后自助选装 | 任何团队 |
| 现有 plugin 不够用，员工自己描述需求扩展 | 业务团队 |

## 架构

```
┌──────────────────────────────────────────────┐
│ 员工 (任意频道)                                │
│   Slack / Telegram / Web UI / 飞书 / 终端    │
└──────────────────┬───────────────────────────┘
                   │ 对话
                   ▼
┌──────────────────────────────────────────────┐
│ OpenClaw Gateway                             │
│  ┌────────────────────────────────────────┐  │
│  │ Plugin Studio Agent                    │  │
│  │   employee-intake → 角色识别            │  │
│  │   ├─ 已有 plugin → 安装指引             │  │
│  │   └─ 没 plugin → plugin-creator        │  │
│  │      （8 阶段对话生成）                 │  │
│  │   plugin-publisher → 加入 marketplace  │  │
│  └────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────┘
                   │ 写入
                   ▼
┌──────────────────────────────────────────────┐
│ Marketplace (公司内部 git / 文件系统)          │
│   marketplace.json · plugins/* · changelog   │
└──────────────────────────────────────────────┘
```

## 部署

### 一行命令

```bash
git clone https://github.com/fxp/skills-creator.git
cd skills-creator
sudo bash enterprise/install.sh --target-dir /opt/plugin-studio
```

### 配置公司信息

编辑 `/opt/plugin-studio/enterprise.config.json`：

```json
{
  "company_name": "Acme Corp",
  "approval_required": true,
  "admins": ["alice@acme.com"],
  "marketplace": { "type": "git", "git_remote": "git@github.com:acme/ai-plugins.git" },
  "notification_channels": { "slack_webhook": "https://hooks.slack.com/..." }
}
```

### 配置 LLM

```bash
export OPENAI_API_KEY=your-key
export OPENAI_BASE_URL=https://your-endpoint/v1
```

支持任何 OpenAI-compatible 端点：BigModel、DeepSeek、Azure OpenAI、Together、本地 LM Studio。

### 启动

```bash
openclaw gateway --bind lan
```

服务起在 0.0.0.0:29533。员工通过 Web UI 或对接的频道（Slack/Telegram/飞书）即可使用。

## 员工使用流

```
员工：你好，我是新来的销售。

Agent：欢迎！我们已经为销售团队准备好了 AI 同事 sales-ops。
       它能帮你做：客户调研、会前 brief、pipeline 健康检查、
       竞品 battlecard 维护、每周报告。

       要装到你的 Claude Code 吗？只需要一行命令：
       /plugin marketplace add git.acme.com/ai-plugins
       /plugin install sales-ops

员工：装一下。

Agent：好的。装好后试一句"调研一下 X 公司"应该会自动响应。
       用一段时间后欢迎反馈。
```

如果是新角色（没有现成 plugin）：

```
员工：你好，我们刚成立 RevOps 团队。

Agent：RevOps —— 我们还没准备过这个角色。我们花 30-50 分钟一起搭一个？

员工：好。

Agent：先来定使命：你们 RevOps 团队最关键的产出是什么？...
       ⌐ 30 轮对话 ⌐
       已生成 revops 数字员工：5 个 skill + 1 个 weekly command。
       提交给管理员审核了，预计今天会发布到 marketplace。
```

## 管理员工作流

```bash
# 列出待审核 plugin
ls /opt/plugin-studio/marketplace/pending/

# 查看详情
python3 /opt/plugin-studio/skills/plugin-creator/scripts/validate_plugin.py \
    /opt/plugin-studio/marketplace/pending/revops

# 批准发布
python3 /opt/plugin-studio/skills/plugin-publisher/scripts/publish_plugin.py \
    /opt/plugin-studio/marketplace/pending/revops \
    --marketplace /opt/plugin-studio/marketplace/marketplace.json \
    --target git --push --approve
```

发布会同时：
- 写入 `marketplace.json` 的 `plugins` 数组
- 更新 `marketplace/changelog.md`
- 通过 Slack/邮件通告对应团队

## 安全考量

- **隔离会话**：每个员工对话独立，不复述其他员工的输入
- **审核机制**：默认 `approval_required: true`，新生成的 plugin 必须管理员批准才发布
- **凭证扫描**：`publish_plugin.py` 会扫描明文 token / API key
- **隐私扫描**：description 不允许员工 PII

## 维护

### 升级到新版

```bash
cd /opt/plugin-studio
git pull
# (workspace 内核心 skill 会更新，但 enterprise.config.json 和 marketplace 保留)
```

### 备份

```bash
tar -czf plugin-studio-backup-$(date +%F).tar.gz /opt/plugin-studio
```

### 卸载

```bash
openclaw agents delete plugin-studio
rm -rf /opt/plugin-studio
```

## 常见问题

**Q：员工生成的 plugin 质量怎么保证？**
A：默认开启 admin 审核。每个 plugin 还会自动跑 eval suite，validate_plugin 会拦截格式问题。

**Q：可以脱敏不让员工看到其他员工的对话吗？**
A：默认就是隔离的。每个 session 独立，agent 不读 USER.md（USER.md 仅 admin 模式使用）。

**Q：怎么对接公司现有的 SSO？**
A：通过 OpenClaw 的 channel 层。Slack/Teams/飞书 channel 已经天然带 SSO 身份。

**Q：plugin 被员工跑出 bug 怎么办？**
A：所有 plugin 都有版本号。在 marketplace.json 里把 version 回滚一个号即可。

## 技术细节

- 依赖 OpenClaw 2026.3+
- Python 3.10+
- 任意 OpenAI-compatible LLM 端点
- marketplace 可放本地、git、对象存储
- 单机可服务 50-100 员工；更多需要多实例 + 负载均衡（OpenClaw 支持）

## 完整示例

参考 [`examples/sales-ops-plugin/`](../examples/sales-ops-plugin/) 看一个由 Plugin Studio 生成的真实数字员工 plugin。
