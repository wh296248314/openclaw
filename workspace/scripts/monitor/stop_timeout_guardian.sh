#!/bin/bash
# 停止智能超时监控卫士

WORKDIR="/home/admin/openclaw/workspace"
PID_FILE="$WORKDIR/timeout_guardian.pid"
LOG_FILE="$WORKDIR/timeout_guardian.log"

if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "$(date): 停止监控卫士 (PID: $pid)" >> "$LOG_FILE"
        kill $pid
        sleep 2
        if ps -p $pid > /dev/null 2>&1; then
            kill -9 $pid
            echo "$(date): 强制停止监控卫士" >> "$LOG_FILE"
        fi
    fi
    rm -f "$PID_FILE"
    echo "$(date): 监控卫士已停止" >> "$LOG_FILE"
else
    echo "$(date): 监控卫士未运行" >> "$LOG_FILE"
fi
