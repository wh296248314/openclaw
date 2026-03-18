#!/bin/bash
# Gateway Auto-Restart & Monitor
# 功能：
# 1. 网络重连时自动检查并重启Gateway
# 2. 断网断连时自动监测并重启
# 3. 记录重启原因

LOGFILE="/home/pixiu/.openclaw/logs/gateway-monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

# 检查网络连接
check_network() {
    if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
        return 0  # 网络正常
    else
        return 1  # 网络断开
    fi
}

# 获取重启原因
get_restart_reason() {
    local reason="未知原因"
    
    if ! check_network; then
        reason="网络断开"
    fi
    
    # 检查systemd日志中的原因
    if systemctl --user show openclaw-gateway --property=Result 2>/dev/null | grep -q "core"; then
        reason="服务崩溃"
    elif systemctl --user show openclaw-gateway --property=ActiveState 2>/dev/null | grep -q "failed"; then
        reason="服务失败"
    elif [ -f /var/log/syslog ]; then
        reason=$(grep -i "openclaw" /var/log/syslog 2>/dev/null | tail -1 | awk '{print $5,$6,$7}')
        [ -z "$reason" ] && reason="系统事件触发"
    fi
    
    echo "$reason"
}

# 检查gateway是否运行
check_gateway() {
    if systemctl --user is-active --quiet openclaw-gateway; then
        log "Gateway is running"
        return 0
    else
        reason=$(get_restart_reason)
        log "Gateway is NOT running, starting... Reason: $reason"
        systemctl --user start openclaw-gateway
        sleep 2
        if systemctl --user is-active --quiet openclaw-gateway; then
            log "Gateway started successfully after: $reason"
            return 0
        else
            log "Gateway failed to start. Reason: $reason"
            return 1
        fi
    fi
}

# 主动监测模式
monitor_loop() {
    local consecutive_failures=0
    local max_check=3
    
    while true; do
        if ! check_network; then
            log "Network disconnected, waiting for reconnect..."
            consecutive_failures=0
            sleep 10
            continue
        fi
        
        if ! systemctl --user is-active --quiet openclaw-gateway; then
            consecutive_failures=$((consecutive_failures + 1))
            reason=$(get_restart_reason)
            log "Gateway down detected (check #$consecutive_failures). Reason: $reason"
            
            if [ $consecutive_failures -ge 2 ]; then
                log "Attempting restart due to: $reason"
                systemctl --user restart openclaw-gateway
                sleep 5
                consecutive_failures=0
            fi
        else
            if [ $consecutive_failures -gt 0 ]; then
                log "Gateway recovered"
                consecutive_failures=0
            fi
        fi
        
        sleep 30
    done
}

# 主逻辑
log "=== Gateway monitor started ==="

case "${1:-check}" in
    monitor)
        monitor_loop
        ;;
    check|*)
        check_gateway
        ;;
esac
