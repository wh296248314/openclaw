#!/bin/bash

# 备份原文件
BACKUP_FILE="/home/admin/.openclaw/cron/jobs.json.backup.$(date +%Y%m%d_%H%M%S)"
cp /home/admin/.openclaw/cron/jobs.json "$BACKUP_FILE"
echo "已创建备份: $BACKUP_FILE"

# 使用sed直接替换配置
echo "正在更新cron任务配置..."

# 更新系统唤醒准备任务 (ID: 2b2f4073-542c-4139-b60e-89c033ee8310)
sed -i 's/"channel": "qqbot"/"channel": "dingtalk-connector",\n        "to": "manager7367"/g' /home/admin/.openclaw/cron/jobs.json

# 重置错误状态
sed -i 's/"lastError": "Delivering to QQ Bot requires target"/"lastError": null/g' /home/admin/.openclaw/cron/jobs.json
sed -i 's/"lastStatus": "error"/"lastStatus": "pending"/g' /home/admin/.openclaw/cron/jobs.json
sed -i 's/"lastRunStatus": "error"/"lastRunStatus": "pending"/g' /home/admin/.openclaw/cron/jobs.json
sed -i 's/"consecutiveErrors": [0-9]*/"consecutiveErrors": 0/g' /home/admin/.openclaw/cron/jobs.json

echo "✅ 配置更新完成！"
echo ""
echo "更新后的配置："
echo "1. 系统唤醒准备 (08:00) -> 钉钉通道 (manager7367)"
echo "2. 每日早安问候 (08:30) -> 钉钉通道 (manager7367)"
echo "3. 早上9点问候 (09:00) -> 钉钉通道 (manager7367)"
echo ""
echo "需要重启OpenClaw Gateway使配置生效："