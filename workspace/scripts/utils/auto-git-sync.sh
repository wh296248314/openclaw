#!/bin/bash
# OpenClaw自动Git同步脚本
# 每天自动提交更改并推送到GitHub

set -e

WORKSPACE_DIR="/home/admin/openclaw/workspace"
OPENCLAW_DIR="/home/admin/openclaw"
LOG_FILE="$WORKSPACE_DIR/logs/git-sync.log"
MAX_LOG_SIZE=10485760  # 10MB

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# 清理过大的日志文件
cleanup_log() {
    if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt $MAX_LOG_SIZE ]; then
        log "📁 日志文件过大，清理..."
        tail -1000 "$LOG_FILE" > "$LOG_FILE.tmp"
        mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "✅ 日志已清理"
    fi
}

# 检查Git状态
check_git_status() {
    cd "$OPENCLAW_DIR"
    
    # 检查是否有未提交的更改
    if git status --porcelain | grep -q .; then
        log "📝 检测到未提交的更改"
        return 0
    else
        log "✅ 没有未提交的更改"
        return 1
    fi
}

# 自动提交更改
auto_commit() {
    cd "$OPENCLAW_DIR"
    
    log "🚀 开始自动提交..."
    
    # 添加所有更改
    git add -A
    
    # 获取更改统计
    changed_files=$(git status --porcelain | wc -l)
    
    # 生成提交消息
    commit_msg="自动同步: $(date '+%Y-%m-%d %H:%M:%S')
    
变更统计:
- 更改文件: $changed_files 个
- 时间: $(date '+%Y年%m月%d日 %H:%M')
- 触发: 定时任务"

    # 提交更改
    git commit -m "$commit_msg"
    
    log "✅ 本地提交完成: $changed_files 个文件"
}

# 推送到GitHub
push_to_github() {
    cd "$OPENCLAW_DIR"
    
    log "📤 推送到GitHub..."
    
    # 尝试推送
    if git push origin main; then
        log "✅ 推送成功"
        return 0
    else
        log "⚠️  推送失败，尝试拉取最新代码..."
        
        # 先拉取最新代码
        if git pull --rebase origin main; then
            log "✅ 拉取成功，重新推送..."
            if git push origin main; then
                log "✅ 推送成功"
                return 0
            else
                log "❌ 推送仍然失败"
                return 1
            fi
        else
            log "❌ 拉取失败，需要手动处理"
            return 1
        fi
    fi
}

# 生成同步报告
generate_report() {
    cd "$OPENCLAW_DIR"
    
    local report_file="$WORKSPACE_DIR/logs/git-sync-report-$(date '+%Y%m%d_%H%M%S').txt"
    
    {
        echo "OpenClaw Git同步报告"
        echo "======================"
        echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        # Git状态
        echo "📊 Git状态:"
        git status --short
        echo ""
        
        # 最近提交
        echo "📝 最近提交:"
        git log --oneline -5
        echo ""
        
        # 文件统计
        echo "📁 文件统计:"
        echo "工作空间文件数: $(find "$WORKSPACE_DIR" -type f | wc -l)"
        echo "Git跟踪文件数: $(git ls-files | wc -l)"
        
    } > "$report_file"
    
    log "📋 同步报告已生成: $report_file"
}

# 主函数
main() {
    log "🔄 OpenClaw Git同步开始"
    log "工作目录: $OPENCLAW_DIR"
    
    # 清理日志
    cleanup_log
    
    # 检查Git状态
    if check_git_status; then
        # 有更改，执行自动提交
        auto_commit
        
        # 推送到GitHub
        if push_to_github; then
            log "🎉 同步成功完成"
        else
            log "⚠️  同步完成但有警告"
        fi
    else
        log "💤 没有更改，跳过同步"
    fi
    
    # 生成报告
    generate_report
    
    log "✅ Git同步流程结束"
    echo ""
}

# 执行主函数
main "$@"
