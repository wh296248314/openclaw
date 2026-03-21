# ⚠️ 铁律：Gateway重启必须申请授权

### 涉及以下操作必须先申请授权！
- ❌ 修改 openclaw.json
- ❌ 重启 Gateway
- ❌ 删除文件或数据

### 正确流程：告知 → 等"同意" → 执行 → 汇报

---

# HEARTBEAT.md

## 主动学习检查

### 每次 Heartbeat 时执行：
1. 读取 `/home/pixiu/.openclaw/workspace/experts/product-xiaopi/self-improving/heartbeat-rules.md`
2. 检查上次运行状态
3. **主动学习任务**：
   - 随机抽取一个历史任务进行复盘
   - 检查是否有未完成的任务需要跟进
   - 回顾最近的MEMORY.md更新

### 复盘问题：
- 这个任务当时是怎么解决的？
- 有没有更好的方案？
- 有什么经验可以沉淀？

## Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/product-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/product-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK

---

## ⚠️ 重要：主动汇报原则

**断网、重启、重联时，必须主动回复皮休，不能等他来问！**

主动汇报内容：
- 网络断了 → 立即通知
- 服务重启了 → 立即通知
- 网络恢复了 → 立即通知
- 任务完成了 → 主动汇报

