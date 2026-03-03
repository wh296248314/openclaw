#!/bin/bash
# 启动智能超时监控卫士

WORKDIR="/home/admin/openclaw/workspace"
LOG_FILE="$WORKDIR/timeout_guardian.log"
PID_FILE="$WORKDIR/timeout_guardian.pid"

# 检查是否在运行时间内 (09:00-19:00)
current_hour=$(date +%H)
if [ $current_hour -lt 9 ] || [ $current_hour -ge 19 ]; then
    echo "$(date): 非运行时间 (09:00-19:00)，当前时间: $(date +%H:%M)" >> "$LOG_FILE"
    exit 0
fi

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "$(date): 监控卫士已在运行 (PID: $pid)" >> "$LOG_FILE"
        exit 0
    fi
fi

# 启动监控卫士
echo "$(date): 启动智能超时监控卫士..." >> "$LOG_FILE"
cd "$WORKDIR"
nohup python3 timeout_guardian.py >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

echo "$(date): 监控卫士已启动 (PID: $!)" >> "$LOG_FILE"
