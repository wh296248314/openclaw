# ⚠️ 铁律：Gateway重启必须申请授权

### 涉及以下操作必须先申请授权！
- ❌ 修改 openclaw.json
- ❌ 重启 Gateway
- ❌ 删除文件或数据

### 正确流程：告知 → 等"同意" → 执行 → 汇报

---

# HEARTBEAT.md

# Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/audit-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/audit-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK

---

## ⚠️ 重要：主动汇报原则

**断网、重启、重联时，必须主动回复皮休，不能等他来问！**

主动汇报内容：
- 网络断了 → 立即通知
- 服务重启了 → 立即通知
- 网络恢复了 → 立即通知
- 任务完成了 → 主动汇报

---

## 📝 Memory 同步机制（重要对话结论自动同步）

**必须立即同步的触发场景：**

1. **每次 reset 前** → 同步本次会话的重要结论到 memory/YYYY-MM-DD.md
2. **任务完成后** → 立即同步任务结论、决策、产出到 memory
3. **重要配置变更后** → 立即同步变更内容到 memory（如 openclaw.json、skill 配置等）

**同步格式要求：**
```markdown
## [时间] 重要结论同步

### 任务/事件
- 结论/决策/变更内容
- 负责人：xxx
- 影响范围：xxx
```

**同步位置：**
- 日常记录 → `memory/YYYY-MM-DD.md`
- 重要决策 → `MEMORY.md`（长期记忆）
- 配置变更 → `memory/YYYY-MM-DD.md` + 同步更新相关配置文件

