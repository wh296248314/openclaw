#!/bin/bash
# 档案馆GitHub自动同步脚本
# 用法: sync_archives_github.sh [commit_message]
# 建议: 每次产出物提交后自动执行

ARCHIVES_DIR="$HOME/.openclaw/workspace/archives"
cd "$ARCHIVES_DIR"

# 提交消息（默认自动生成）
if [ -z "$1" ]; then
    COMMIT_MSG="docs: 归档更新 - $(date +'%Y-%m-%d %H:%M')"
else
    COMMIT_MSG="$1"
fi

echo "📦 档案馆 GitHub 同步"
echo "================================"

# 检查是否有变更
if git diff --quiet && git diff --cached --quiet; then
    echo "⚪ 没有变更需要提交"
    exit 0
fi

# 添加所有变更
git add .

# 提交
git commit -m "$COMMIT_MSG"

# 显示提交内容
echo ""
echo "📝 已提交:"
git log -1 --oneline

# 推送到远程（如果配置了）
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [ -n "$REMOTE" ] && [ "$REMOTE" != "(no remote)" ]; then
    echo ""
    echo "🚀 推送到远程..."
    if git push origin master 2>/dev/null; then
        echo "✅ 推送成功"
    else
        echo "⚠️ 推送失败（可能需要手动解决冲突）"
    fi
else
    echo "⚠️ 未配置远程仓库，请手动推送"
fi

echo ""
echo "✅ 同步完成！"
