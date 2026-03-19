# HEARTBEAT.md

# 皮休重要规范提醒
- openclaw.json修改前必须申请"同意"
- Gateway重启必须申请"同意"
- 重启后立即汇报任务状态
- Interactive Card发送后记录到 memory/interactive-cards.md
- 汇报格式：结论先行，先说结论再给背景
- 任务接收：回复"收到，预计X分钟"
- 超过1分钟主动汇报进度

# 管家工作流程核心要求（v2.3）
## 七条铁律（必须背诵执行）
1. 回复"收到，预计X分钟"
2. 验收标准前置确认
3. L2+必须审核
4. 进度主动汇报
5. 失败必须记录
6. 结论先行汇报
7. Card必须记录memory

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

---

## 📚 每日定时检查

1. 检查各小皮是否有主动学习（检查 shared/notes/ 今日文件）
2. 检查学习文件是否在正确路径（主共享目录）
3. 记录Interactive Card使用情况

