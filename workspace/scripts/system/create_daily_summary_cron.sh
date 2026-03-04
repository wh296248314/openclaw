#!/bin/bash
# 创建每日总结cron任务

set -e

WORKSPACE="/home/admin/openclaw/workspace"
CRON_JOBS_FILE="$HOME/.openclaw/cron/jobs.json"
BACKUP_FILE="${CRON_JOBS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

echo "🔧 创建每日总结cron任务"
echo "工作空间: $WORKSPACE"

# 备份原文件
if [ -f "$CRON_JOBS_FILE" ]; then
    cp "$CRON_JOBS_FILE" "$BACKUP_FILE"
    echo "✅ 已备份原cron文件: $BACKUP_FILE"
fi

# 检查是否已存在每日总结任务
if grep -q "每日总结" "$CRON_JOBS_FILE" 2>/dev/null; then
    echo "⚠️  每日总结任务已存在，跳过创建"
    exit 0
fi

# 创建新的cron任务配置
NEW_CRON_TASK=$(cat <<EOF
{
  "id": "$(uuidgen)",
  "agentId": "main",
  "name": "每日总结 - 21:00",
  "enabled": true,
  "createdAtMs": $(date +%s%3N),
  "updatedAtMs": $(date +%s%3N),
  "schedule": {
    "kind": "cron",
    "expr": "0 21 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "📊 **每日总结时间**\n\n现在是21:00，开始生成今日工作总结报告。\n\n请执行以下命令生成总结：\n\`\`\`bash\ncd /home/admin/openclaw/workspace && python3 scripts/system/daily_summary.py\n\`\`\`\n\n总结报告将保存到：\n- \`memory/summary_YYYY-MM-DD.json\` (JSON格式)\n- \`memory/summary_YYYY-MM-DD.txt\` (文本格式)\n\n记得查看今日完成的任务和明日计划建议！"
  },
  "state": {
    "nextRunAtMs": $(date -d "today 21:00" +%s%3N),
    "lastRunAtMs": 0,
    "lastStatus": "pending",
    "lastDurationMs": 0
  }
}
EOF
)

echo "📝 新cron任务配置："
echo "$NEW_CRON_TASK" | python3 -m json.tool

# 添加到cron文件
if [ -f "$CRON_JOBS_FILE" ]; then
    # 使用Python处理JSON文件
    python3 -c "
import json
import sys

try:
    with open('$CRON_JOBS_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_task = json.loads('''$NEW_CRON_TASK''')
    
    # 添加到jobs数组
    data['jobs'].append(new_task)
    
    # 保存文件
    with open('$CRON_JOBS_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print('✅ 每日总结cron任务已添加到文件')
    
except Exception as e:
    print(f'❌ 添加cron任务失败: {e}')
    sys.exit(1)
"
else
    echo "❌ cron文件不存在: $CRON_JOBS_FILE"
    exit 1
fi

echo ""
echo "🎉 每日总结机制设置完成！"
echo "📅 任务将在每天21:00自动执行"
echo "📁 总结文件将保存到 memory/summary_*.{json,txt}"
echo ""
echo "🔍 验证设置："
echo "1. 查看cron任务: cat $CRON_JOBS_FILE | grep -A5 -B5 '每日总结'"
echo "2. 手动测试: python3 $WORKSPACE/scripts/system/daily_summary.py"
echo "3. 检查日志: tail -f $WORKSPACE/logs/system/daily_summary.log"