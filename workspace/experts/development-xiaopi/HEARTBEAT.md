# HEARTBEAT.md

# 皮休重要规范提醒
- openclaw.json修改前必须申请"同意"
- Gateway重启必须申请"同意"
- 重启后立即汇报任务状态

# Self-Improving Check
- Read /home/pixiu/.openclaw/workspace/experts/development-xiaopi/self-improving/heartbeat-rules.md
- Use /home/pixiu/.openclaw/workspace/experts/development-xiaopi/self-improving/heartbeat-state.md for last-run markers
- If no file inside self-improving/ changed since last review, return HEARTBEAT_OK
