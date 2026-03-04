#!/bin/bash
# Git 重试推送脚本
# 在网络问题期间自动重试推送提交

echo "🔄 Git 重试推送脚本启动 - $(date)"
echo "=========================================="

# 切换到工作目录
cd /home/admin/openclaw/workspace

# 检查待推送提交数量
PENDING_COMMITS=$(git log --oneline origin/main..HEAD | wc -l)
echo "📊 当前状态: $PENDING_COMMITS 个提交待推送"

if [ $PENDING_COMMITS -eq 0 ]; then
    echo "✅ 无待推送提交，脚本退出"
    exit 0
fi

# 尝试推送（使用较短超时）
echo "🚀 尝试推送提交..."
timeout 15 git push

if [ $? -eq 0 ]; then
    echo "✅ 推送成功!"
    
    # 更新队列文件状态
    if [ -f "git-commit-queue.json" ]; then
        echo "📝 更新队列文件状态..."
        sed -i 's/"status": "pending"/"status": "completed"/' git-commit-queue.json
        sed -i "s/\"pending_commits\": [0-9]*/\"pending_commits\": 0/" git-commit-queue.json
        echo "✅ 队列文件已更新"
    fi
    
    # 记录成功日志
    echo "$(date): 成功推送 $PENDING_COMMITS 个提交" >> logs/git-sync.log
else
    echo "⚠️  推送失败或超时"
    
    # 记录失败日志
    echo "$(date): 推送失败，仍有 $PENDING_COMMITS 个提交待推送" >> logs/git-sync.log
    
    # 检查是否需要创建备份
    if [ $PENDING_COMMITS -ge 5 ]; then
        echo "💾 创建本地备份..."
        BACKUP_DIR="backups/git-commits/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        
        # 备份提交信息
        git log --oneline -$PENDING_COMMITS > "$BACKUP_DIR/commits.txt"
        git diff HEAD~$PENDING_COMMITS HEAD > "$BACKUP_DIR/changes.diff"
        
        echo "✅ 备份已保存到: $BACKUP_DIR"
        echo "$(date): 创建备份到 $BACKUP_DIR" >> logs/git-sync.log
    fi
fi

echo "=========================================="
echo "🔄 Git 重试推送脚本完成 - $(date)"