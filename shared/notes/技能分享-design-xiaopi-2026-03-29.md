# 技能分享 - design-xiaopi

## 技能名称
Coding Agent（编码智能体）

## 技能特点
1. **多智能体支持**：支持 Codex、Claude Code、Pi 等多种编码智能体，可根据任务需求灵活选择
2. **背景任务执行**：支持后台模式运行，通过 PTY 终端保持交互能力，适合长时间构建任务
3. **工作目录隔离**：使用 workdir 参数将智能体聚焦在特定目录，避免读取无关文件
4. **并行任务能力**：通过 git worktree 可并行处理多个 PR 或 issue，显著提升效率
5. **进度通知机制**：支持完成时自动触发系统事件通知，无需轮询等待

## 应用场景
- **构建新功能/应用**：需要创建新项目或复杂功能时，委托给编码智能体处理
- **代码审查**：批量审查多个 PR，可并行启动多个审查进程
- **重构大型代码库**：需要全面修改但又担心出错的场景
- **迭代开发**：需要多次文件探索和修改的复杂任务
- **快速修复**：使用 git worktree 并行修复多个 issue

## 核心命令示例

```bash
# 快速执行（Claude Code）
claude --permission-mode bypassPermissions --print 'Your task'

# 背景执行（Codex，需 PTY）
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build a REST API'"

# PR 审查（并行）
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86'"
```

## 关键要点
- Codex/Pi/OpenCode 需要 `pty:true`，Claude Code 使用 `--print --permission-mode bypassPermissions`
- Codex 必须在 git 仓库中运行，可用 `mktemp -d && git init` 创建临时仓库
- 长时间任务添加完成通知：`openclaw system event --text "Done" --mode now`

## 学习资源
- OpenClaw Coding Agent Skill: `~/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md`
- ClawHub: https://clawhub.com
