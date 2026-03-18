# HEARTBEAT.md

# 皮休重要规范提醒
- openclaw.json修改前必须申请"同意"
- Gateway重启必须申请"同意"
- 重启后立即汇报任务状态

# Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/development-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/development-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK

---

## ⚠️ 重要：主动汇报原则

**断网、重启、重联时，必须主动回复皮休，不能等他来问！**

主动汇报内容：
- 网络断了 → 立即通知
- 服务重启了 → 立即通知
- 网络恢复了 → 立即通知
- 任务完成了 → 主动汇报

