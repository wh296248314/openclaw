#!/bin/bash
# 设置Git自动同步定时任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_SYNC_SCRIPT="$SCRIPT_DIR/auto-git-sync.sh"
CRON_LOG="$SCRIPT_DIR/../logs/git-cron.log"

# 创建日志目录
mkdir -p "$(dirname "$CRON_LOG")"

echo "🔄 设置OpenClaw Git自动同步定时任务"
echo "======================================"

# 检查脚本是否存在
if [ ! -f "$AUTO_SYNC_SCRIPT" ]; then
    echo "❌ 自动同步脚本不存在: $AUTO_SYNC_SCRIPT"
    exit 1
fi

echo "✅ 找到自动同步脚本: $AUTO_SYNC_SCRIPT"

# 创建crontab配置
CRON_JOB="*/30 * * * * $AUTO_SYNC_SCRIPT >> $CRON_LOG 2>&1"
CRON_JOB_DAILY="0 2 * * * $AUTO_SYNC_SCRIPT --force >> $CRON_LOG 2>&1"

echo ""
echo "📋 建议的定时任务:"
echo "1. 每30分钟同步一次:"
echo "   $CRON_JOB"
echo ""
echo "2. 每天凌晨2点强制同步:"
echo "   $CRON_JOB_DAILY"
echo ""

# 检查当前crontab
echo "🔍 当前crontab内容:"
crontab -l 2>/dev/null || echo "暂无crontab配置"
echo ""

# 询问用户是否要添加
read -p "是否添加定时任务？(y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 备份现有crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).bak 2>/dev/null || true
    
    # 添加新任务
    (crontab -l 2>/dev/null | grep -v "$AUTO_SYNC_SCRIPT"; echo "$CRON_JOB") | crontab -
    
    echo "✅ 定时任务已添加"
    echo "   每30分钟自动同步一次"
    
    # 显示更新后的crontab
    echo ""
    echo "📋 更新后的crontab:"
    crontab -l
else
    echo "⚠️  跳过添加定时任务"
    echo "   你可以手动添加:"
    echo "   crontab -e"
    echo "   然后添加: $CRON_JOB"
fi

echo ""
echo "🎯 设置完成！"
echo "   手动测试: $AUTO_SYNC_SCRIPT"
echo "   查看日志: tail -f $CRON_LOG"
