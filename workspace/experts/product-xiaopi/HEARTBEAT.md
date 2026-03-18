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
