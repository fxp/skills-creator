# Installed Plugins — 已发布 plugin 的员工安装话术

当员工的角色匹配到现成 plugin 时，提供清晰的安装指引。

## 标准应答模板

> "好消息——你的角色我们已经准备好了 AI 同事 **{plugin_name}**。它能帮你：
>
> - {skill_1_description}
> - {skill_2_description}
> - {skill_3_description}
>
> 需要安装到你的 Claude Code 吗？只需要一行命令。"

## 安装命令

根据公司部署的 marketplace 来源生成不同的安装指令：

### 公司内部 Git marketplace

```
/plugin marketplace add https://git.{company}.com/ai-plugins
/plugin install {plugin_name}@{company}-marketplace
```

### 公司内部文件系统

```
/plugin install {plugin_name} --plugin-dir /shared/ai-plugins/{plugin_name}
```

### 远程 zip 包

```
curl -L https://files.{company}.com/plugins/{plugin_name}.zip -o /tmp/{plugin_name}.zip
unzip /tmp/{plugin_name}.zip -d ~/.claude/plugins/
/reload-plugins
```

## 安装后验证

> "装好了。试一句：'帮我 {sample_task}' —— 应该会自动触发 {skill_name}。如果没反应，可以用 `/{plugin_name}:{command}` 显式调用。"

## 升级/反馈引导

> "用了一段时间后，如果发现：
>
> - 某个 skill 不够用 → 跟我说哪里不准，可以做小改进
> - 缺少某个常用任务 → 我们可以新增一个 skill
> - 整体跑偏 → 提交反馈给管理员评审"

引导员工把反馈写到 `enterprise.config.json` 中的 `feedback_endpoint`（如果配置了）。

## 多 plugin 推荐

有时一个员工的角色覆盖多个 plugin（如"业务发展" = sales-ops + marketing）。推荐方式：

> "你的工作横跨销售和市场。建议同时装：
>
> 1. **sales-ops** —— 客户调研、pipeline 管理
> 2. **marketing-coordinator** —— 内容生产、活动复盘
>
> 两个一起装吗？"
