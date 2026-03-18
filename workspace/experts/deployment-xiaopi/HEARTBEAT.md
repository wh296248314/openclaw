# HEARTBEAT.md

## 核心规范提醒

⚠️ **openclaw.json 修改必须向皮休申请，只有回复"同意"才能执行**  
⚠️ **gateway 重启必须向皮休申请，只有回复"同意"才能等待5秒自动重启**  
⚠️ **每日 12:00 自动备份 openclaw.json**

## 主动学习机制

**目标**: 每天主动学习之前的事情，做好记忆回顾加强印象管理

### 每日主动学习任务

1. **回顾昨日记忆**
   - 读取 memory/YYYY-MM-DD.md（昨天）
   - 回顾重要决策和任务

2. **检查未完成任务**
   - 查看 memory/ 中是否有遗留任务
   - 主动推进待处理事项

3. **反思与总结**
   - 思考今日工作是否有改进空间
   - 记录学习心得到 self-improving/

4. **主动汇报意识**
   - 当有新进展时主动汇报（不等询问）
   - 发现问题主动报告

### 触发条件

每次心跳时检查：
- 是否有重要事项需要主动汇报
- 是否有未完成的任务需要跟进
- 是否有新知识需要学习

## Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/deployment-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/deployment-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK
