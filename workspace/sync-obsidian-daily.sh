#!/bin/bash
# Obsidian Daily Sync Script
# Auto-commit and sync Obsidian workspace

echo "🔔 Obsidian 自动提交脚本启动 - $(date)"
echo "=========================================="

# Change to workspace directory
cd /home/admin/openclaw/workspace

# Check git status
echo "📊 检查 Git 状态..."
git status

# Add any untracked files
echo "📝 添加未跟踪文件..."
git add .

# Commit changes
COMMIT_MSG="Auto-commit: Obsidian daily sync - $(date '+%Y-%m-%d %H:%M')"
echo "💾 提交更改: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Try to push with timeout
echo "🚀 尝试推送到远程仓库..."
timeout 30 git push

if [ $? -eq 0 ]; then
    echo "✅ 推送成功!"
else
    echo "⚠️  推送超时或失败，将在下次尝试"
fi

echo "=========================================="
echo "🔔 Obsidian 自动提交脚本完成 - $(date)"