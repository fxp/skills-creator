# Plugin Publisher — 发布到企业 marketplace

把 `plugin-creator` 生成的 plugin 加入企业内部 marketplace.json，并按需推送到 git / 文件系统 / 网盘。

## 触发场景

- plugin-creator 完成 PACKAGE 阶段后自动调用
- Admin 说"发布"、"publish"、"上架 plugin"、"加到 marketplace"

## 工作流

### Step 1：审核状态判断

读取 `enterprise.config.json` 中的 `approval_required`：

| 配置 | 行为 |
|------|------|
| `false` | 直接发布 |
| `true` | 进入待审核队列（写入 `pending/`），通知 admin |

### Step 2：发布

调用 `scripts/publish_plugin.py`：

```bash
python3 scripts/publish_plugin.py <plugin_dir> \
    --marketplace marketplace.json \
    --target {git|local|zip} \
    [--push]
```

会：
1. 校验 plugin（`validate_plugin.py`）
2. 把条目加入 marketplace.json 的 `plugins` 数组
3. 复制 plugin 到 marketplace 目录或推到 git
4. 更新 plugin 的 `version` 字段（如未指定）

### Step 3：通知

按 `enterprise.config.json` 的 `notification_channels` 推送：

- Slack：发到指定频道
- 邮件：发给该 plugin 的目标 role 团队成员
- 钉钉/飞书：群通知

### Step 4：员工通告

把发布信息写入 `marketplace/changelog.md`：

```markdown
## 2026-05-03

- **sales-ops** v1.0.0 发布。包含 4 个 skill。Slack #sales-ops 频道已通告。
```

## 审核流程

如果 `approval_required: true`：

1. plugin 写入 `pending/{plugin_name}/`
2. 通知所有 admin（`enterprise.config.json.admins` 列表）
3. Admin 通过命令审核：

```bash
# 列出待审 plugin
ls workspace/marketplace/pending/

# 查看
python3 scripts/review_plugin.py workspace/marketplace/pending/sales-ops

# 批准
python3 scripts/publish_plugin.py workspace/marketplace/pending/sales-ops --approve
```

## 安全约束

- 发布前必须通过 validate_plugin.py
- plugin 中不应包含明文凭证（脚本扫描 `*-token` `*-key` 等）
- description 中不能含有员工个人信息（隐私扫描）

## 参考

- [`scripts/publish_plugin.py`](scripts/publish_plugin.py) — 发布脚本
