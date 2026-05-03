# Employee Intake — 企业员工入职接待

企业部署模式下的入口 skill。当员工首次接入时，识别其角色，决定走"安装现成 plugin"还是"创建新 plugin"两条路径之一。

## 触发场景

- 员工说"你好"、"我是新来的"、"我是 X 部门的"、"我们团队需要..."
- 当 `enterprise.config.json` 存在时，所有新会话都先经此 skill 引导
- 用户问"有什么 AI 工具我可以用？"、"能帮我做什么？"

## 工作流

### Step 1：身份识别

读取 `enterprise.config.json` 中的 `roles` 列表，问候语调用员工名字（如已知）：

> "你好！我是 {company_name} 的 AI 同事生成助手。请问你在哪个团队/职能？销售？财务？客服？还是其他？"

### Step 2：检查现成 plugin

读取 `marketplace.json`，匹配员工角色：

```python
roles = json.load(open('enterprise.config.json'))['roles']
mp = json.load(open('marketplace.json'))
matched = [p for p in mp['plugins'] if p['category'] == role]
```

**如果找到匹配的 plugin：**

> "我们已经为 {role} 准备好了 [{plugin_name}] —— 它能帮你做 {skills_summary}。需要我帮你装到 Claude Code 吗？"

→ 提供安装说明（见 `references/installed-plugins.md`）

**如果没有匹配：**

> "看起来我们还没为 {role} 团队搭过 AI 同事。我们可以一起搭一个，大概需要 30-50 轮对话。要开始吗？"

→ 进入 `plugin-creator` skill 的 8 阶段工作流

### Step 3：路径分叉

| 员工选择 | 下一步 |
|---------|--------|
| "装现成的" | 提供 `/plugin install {plugin}` 指令 |
| "我们要搭新的" | 调用 `plugin-creator`，预填角色信息 |
| "改一下现有的" | 调用 `plugin-creator` 的 customize 模式（基于现有 plugin 增删） |

### Step 4：交付确认

无论走哪条路径，最后都做一次确认：

> "好的。{action_summary}。还有其他需要吗？"

## 多员工会话隔离

**关键：** 这是多人共用的部署，每次会话不能泄露之前其他员工的信息。

- 每个会话独立读 `.session/{session_id}/session.json`，**不读** USER.md（USER.md 只在 admin 模式下使用）
- 不主动复述上一位员工的角色或对话
- session 结束时清理 `.session/{session_id}/`

## Admin Mode 切换

如果用户说"我是管理员"、"approve plugin"、"review queue"等，停止此 skill，让管理员通过另一个入口（admin 命令）操作（参考 `plugin-publisher` skill）。

## 参考

- [`references/role-detection.md`](references/role-detection.md) — 从对话中识别员工角色的提问模式
- [`references/installed-plugins.md`](references/installed-plugins.md) — 已发布 plugin 的安装指引话术
