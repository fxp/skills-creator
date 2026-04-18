# Commit Message 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| 约定式提交 | Conventional Commits | 行业标准的 commit message 规范 (conventionalcommits.org) |
| 作用域 | scope | commit 影响的代码范围，通常是模块名 |
| 破坏性变更 | breaking change | 会破坏向后兼容的修改，需用 `BREAKING CHANGE:` 标注 |
| 暂存区 | staged area | `git add` 后尚未 commit 的变更 |
| 祈使语气 | imperative mood | "add X" 而非 "added X" 或 "adds X" |

## Type 参考

- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 只改文档
- `style`: 格式化（不影响代码含义）
- `refactor`: 重构（行为不变）
- `test`: 增加或修改测试
- `chore`: 构建/依赖/配置改动
