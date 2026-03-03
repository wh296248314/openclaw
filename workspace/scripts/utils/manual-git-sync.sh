#!/bin/bash
# OpenClaw手动Git同步脚本

set -e

OPENCLAW_DIR="/home/admin/openclaw"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_SYNC_SCRIPT="$SCRIPT_DIR/auto-git-sync.sh"

echo "🔄 OpenClaw手动Git同步"
echo "======================"

cd "$OPENCLAW_DIR"

# 显示当前状态
echo "📊 当前Git状态:"
git status --short

echo ""
echo "📝 最近提交:"
git log --oneline -3

echo ""
# 询问用户操作
echo "请选择操作:"
echo "1. 只提交本地更改"
echo "2. 提交并推送到GitHub"
echo "3. 拉取最新代码"
echo "4. 运行完整自动同步"
echo "5. 查看同步日志"
read -p "选择 (1-5): " choice

case $choice in
    1)
        echo "📝 提交本地更改..."
        git add -A
        read -p "请输入提交消息: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="手动提交: $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        git commit -m "$commit_msg"
        echo "✅ 本地提交完成"
        ;;
    2)
        echo "🚀 提交并推送..."
        git add -A
        read -p "请输入提交消息: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="手动提交: $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        git commit -m "$commit_msg"
        git push origin main
        echo "✅ 提交并推送完成"
        ;;
    3)
        echo "📥 拉取最新代码..."
        git pull origin main
        echo "✅ 拉取完成"
        ;;
    4)
        echo "🔄 运行完整自动同步..."
        "$AUTO_SYNC_SCRIPT"
        ;;
    5)
        echo "📋 查看同步日志..."
        tail -50 "$SCRIPT_DIR/../logs/git-sync.log" 2>/dev/null || echo "暂无日志"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎯 操作完成！"
