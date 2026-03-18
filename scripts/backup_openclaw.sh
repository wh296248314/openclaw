#!/bin/bash
# openclaw.json 每日备份脚本
# 用法: 每天晚上12点自动执行，或手动执行

BACKUP_DIR="/home/pixiu/.openclaw"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "📦 开始备份 openclaw.json ..."

# 创建备份目录
mkdir -p "$BACKUP_DIR/backups"

# 备份 openclaw.json
if [ -f "$BACKUP_DIR/openclaw.json" ]; then
    cp "$BACKUP_DIR/openclaw.json" "$BACKUP_DIR/backups/openclaw.json.bak_$TIMESTAMP"
    echo "✅ 备份成功: openclaw.json.bak_$TIMESTAMP"
    
    # 保留最近30天的备份，删除旧的
    find "$BACKUP_DIR/backups" -name "openclaw.json.bak_*" -mtime +30 -delete
    echo "✅ 已清理30天前的旧备份"
else
    echo "❌ openclaw.json 不存在"
fi

echo "✨ 备份完成！"
