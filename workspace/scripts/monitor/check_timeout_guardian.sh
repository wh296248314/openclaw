#!/bin/bash
# 检查智能超时监控卫士状态

WORKDIR="/home/admin/openclaw/workspace"
PID_FILE="$WORKDIR/timeout_guardian.pid"
LOG_FILE="$WORKDIR/timeout_guardian.log"
STATE_FILE="$WORKDIR/timeout_monitor_state.json"

echo "智能超时监控卫士状态检查"
echo "=========================="

# 检查进程
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ 运行状态: 正在运行 (PID: $pid)"
        
        # 检查运行时间
        start_time=$(ps -o lstart= -p $pid)
        echo "🕐 启动时间: $start_time"
        
        # 检查内存使用
        memory=$(ps -o rss= -p $pid)
        memory_mb=$((memory / 1024))
        echo "💾 内存使用: ${memory_mb}MB"
    else
        echo "❌ 运行状态: PID文件存在但进程未运行"
        rm -f "$PID_FILE"
    fi
else
    echo "⏸️  运行状态: 未运行"
fi

# 检查日志
if [ -f "$LOG_FILE" ]; then
    log_size=$(du -h "$LOG_FILE" | cut -f1)
    log_lines=$(wc -l < "$LOG_FILE")
    echo "📝 日志文件: $LOG_FILE (${log_size}, ${log_lines}行)"
    
    # 显示最后5行日志
    echo "最近日志:"
    tail -5 "$LOG_FILE" | sed 's/^/  /'
else
    echo "📝 日志文件: 不存在"
fi

# 检查状态文件
if [ -f "$STATE_FILE" ]; then
    state_size=$(du -h "$STATE_FILE" | cut -f1)
    echo "⚙️  状态文件: $STATE_FILE (${state_size})"
    
    # 显示状态信息
    echo "监控配置:"
    python3 -c "
import json
try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
    for key, value in state.items():
        print(f'  {key}: {value}')
except:
    print('  无法读取状态文件')
"
else
    echo "⚙️  状态文件: 不存在"
fi

# 检查历史记录
HISTORY_FILE="$WORKDIR/timeout_guardian_history.json"
if [ -f "$HISTORY_FILE" ]; then
    history_count=$(python3 -c "
import json
try:
    with open('$HISTORY_FILE', 'r') as f:
        history = json.load(f)
    print(len(history))
except:
    print('0')
")
    echo "📊 历史记录: ${history_count}个任务"
fi

# 检查cron配置
cron_count=$(crontab -l 2>/dev/null | grep -c "start_timeout_guardian")
echo "⏰ Cron配置: $cron_count个定时任务"

echo ""
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "运行时间范围: 09:00-19:00"
