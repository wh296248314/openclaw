#!/bin/bash
# Gateway Auto-Restart on Network Reconnect
# 当网络重连时自动检查并重启OpenClaw Gateway

LOGFILE="/tmp/gateway-auto-restart.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

# 检查gateway是否运行
check_gateway() {
    if systemctl --user is-active --quiet openclaw-gateway; then
        log "Gateway is running"
        return 0
    else
        log "Gateway is NOT running, starting..."
        systemctl --user start openclaw-gateway
        sleep 2
        if systemctl --user is-active --quiet openclaw-gateway; then
            log "Gateway started successfully"
            return 0
        else
            log "Gateway failed to start"
            return 1
        fi
    fi
}

# 主逻辑
log "=== Network event triggered ==="
check_gateway
