#!/bin/bash
# 清理临时文件
# 用法: bash scripts/cleanup_temp.sh

WORKSPACE="/home/pixiu/.openclaw/workspace"

echo "🧹 开始清理临时文件..."

# 清理Python缓存
find $WORKSPACE -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✅ 清理Python缓存"

# 清理node_modules
find $WORKSPACE -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null
echo "✅ 清理node_modules"

# 清理日志文件
find $WORKSPACE -type f -name "*.log" -delete 2>/dev/null
echo "✅ 清理日志文件"

# 清理临时文件
find $WORKSPACE -type f -name "*.tmp" -delete 2>/dev/null
find $WORKSPACE -type f -name "*.swp" -delete 2>/dev/null
find $WORKSPACE -type f -name "*~" -delete 2>/dev/null
echo "✅ 清理临时文件"

# 清理系统文件
find $WORKSPACE -type f -name ".DS_Store" -delete 2>/dev/null
find $WORKSPACE -type f -name "Thumbs.db" -delete 2>/dev/null
echo "✅ 清理系统文件"

echo "✨ 清理完成！"
