#!/bin/bash
# 归档旧文件
# 用法: bash scripts/archive_old.sh [天数] [目标目录]
# 默认：30天前，移动到 archive/

DAYS=${1:-30}
WORKSPACE="/home/pixiu/.openclaw/workspace"
ARCHIVE_DIR="${2:-$WORKSPACE/shared/archive}"

echo "📦 开始归档旧文件（超过${DAYS}天）..."

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 移动旧文件
count=$(find $WORKSPACE -type f -mtime +$DAYS ! -path "$ARCHIVE_DIR/*" | wc -l)

if [ $count -eq 0 ]; then
    echo "✅ 没有需要归档的文件"
else
    find $WORKSPACE -type f -mtime +$DAYS ! -path "$ARCHIVE_DIR/*" -exec mv {} "$ARCHIVE_DIR/" \; 2>/dev/null
    echo "✅ 已归档 $count 个文件到 $ARCHIVE_DIR"
fi

echo "✨ 归档完成！"
