#!/bin/bash
# OpenClaw Issue #32400 监控脚本
# 监控: https://github.com/openclaw/openclaw/issues/32400

ISSUE_URL="https://api.github.com/repos/openclaw/openclaw/issues/32400"
LOG_FILE="/home/admin/openclaw/workspace/issue-32400-monitor.log"
STATE_FILE="/home/admin/openclaw/workspace/issue-32400-state.json"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_issue() {
    log "检查Issue #32400状态..."
    
    # 使用curl获取issue信息
    response=$(curl -s -H "Accept: application/vnd.github.v3+json" "$ISSUE_URL" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        log "错误: 无法连接到GitHub API"
        return 1
    fi
    
    # 解析JSON响应
    title=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('title', ''))")
    state=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('state', ''))")
    updated_at=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('updated_at', ''))")
    comments=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('comments', 0))")
    
    # 读取上次状态
    if [ -f "$STATE_FILE" ]; then
        last_updated=$(cat "$STATE_FILE" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('updated_at', ''))" 2>/dev/null)
        last_comments=$(cat "$STATE_FILE" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('comments', 0))" 2>/dev/null)
    else
        last_updated=""
        last_comments=0
    fi
    
    # 保存当前状态
    echo "$response" > "$STATE_FILE"
    
    # 检查是否有更新
    if [ "$updated_at" != "$last_updated" ]; then
        log "📢 Issue已更新!"
        log "标题: $title"
        log "状态: $state"
        log "更新时间: $updated_at"
        log "评论数: $comments"
        log "链接: https://github.com/openclaw/openclaw/issues/32400"
        
        # 如果有新评论
        if [ "$comments" -gt "$last_comments" ]; then
            log "💬 有新评论: 增加了$((comments - last_comments))条"
        fi
        
        # 如果状态改变
        if [ "$state" == "closed" ]; then
            log "🎉 Issue已关闭! 问题可能已修复"
            log "建议检查OpenClaw新版本"
        fi
    else
        log "状态未变化: $title (状态: $state, 评论: $comments)"
    fi
    
    log "检查完成"
    echo ""
}

# 主循环
log "开始监控OpenClaw Issue #32400"
log "问题: Control UI hangs when WebSocket disconnects during long streaming responses"
log "按Ctrl+C停止监控"

while true; do
    check_issue
    # 每30分钟检查一次
    sleep 1800
done