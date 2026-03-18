# HEARTBEAT.md

# 设计小皮心跳任务

## 每日9:30 新技能学习（重要！）
- 每天早上9:30准时学习1个新技能/新知识
- 可以去官网查资料、学习新知识
- 向皮休汇报：学习内容、特点、应用场景

## 主动学习检查
- 读取 MEMORY.md 回顾长期记忆
- 读取 memory/*.md 回顾近期工作
- 检查是否有待办事项需要跟进
- 检查是否有需要主动汇报的内容

## 配置管理检查（重要！）
- 检查 openclaw.json 每日备份是否执行
- 修改配置前必须向皮休申请
- Gateway 重启前必须向皮休申请

## Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/design-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/design-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK

## 主动汇报触发条件
- 完成重要任务时
- 发现问题时
- 有新想法/建议时
- 皮休可能关心的工作进展
- Gateway 重启后立即汇报未完成任务

---

## ⚠️ 重要：主动汇报原则

**断网、重启、重联时，必须主动回复皮休，不能等他来问！**

主动汇报内容：
- 网络断了 → 立即通知
- 服务重启了 → 立即通知
- 网络恢复了 → 立即通知
- 任务完成了 → 主动汇报

