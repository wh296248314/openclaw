#!/bin/bash
# 智能超时监控卫士自动启动配置脚本
# 配置为每天上午9点-19点自动启动

echo "================================================"
echo "智能超时监控卫士自动启动配置"
echo "时间范围: 每天 09:00 - 19:00"
echo "================================================"

# 创建监控卫士启动脚本
cat > /home/admin/openclaw/workspace/start_timeout_guardian.sh << 'EOF'
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
EOF

chmod +x /home/admin/openclaw/workspace/start_timeout_guardian.sh

# 创建停止脚本
cat > /home/admin/openclaw/workspace/stop_timeout_guardian.sh << 'EOF'
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
EOF

chmod +x /home/admin/openclaw/workspace/stop_timeout_guardian.sh

# 创建状态检查脚本
cat > /home/admin/openclaw/workspace/check_timeout_guardian.sh << 'EOF'
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
EOF

chmod +x /home/admin/openclaw/workspace/check_timeout_guardian.sh

# 配置cron定时任务
echo "配置cron定时任务..."
CRON_JOB="*/5 9-18 * * * /home/admin/openclaw/workspace/start_timeout_guardian.sh"
CRON_JOB2="0 19 * * * /home/admin/openclaw/workspace/stop_timeout_guardian.sh"

# 添加到当前用户的crontab
(crontab -l 2>/dev/null | grep -v "start_timeout_guardian\|stop_timeout_guardian"; echo "$CRON_JOB"; echo "$CRON_JOB2") | crontab -

# 创建每日清理任务（凌晨清理日志）
CRON_CLEAN="0 2 * * * find /home/admin/openclaw/workspace -name \"timeout_guardian.log.*\" -mtime +7 -delete"
(crontab -l 2>/dev/null | grep -v "timeout_guardian.log"; echo "$CRON_CLEAN") | crontab -

echo "Cron配置完成:"
crontab -l | grep timeout_guardian

# 立即测试启动（如果在运行时间内）
current_hour=$(date +%H)
if [ $current_hour -ge 9 ] && [ $current_hour -lt 19 ]; then
    echo "当前时间在运行范围内，立即启动监控卫士..."
    /home/admin/openclaw/workspace/start_timeout_guardian.sh
    sleep 2
fi

# 显示配置完成信息
echo ""
echo "✅ 配置完成!"
echo ""
echo "📋 创建的脚本:"
echo "  • start_timeout_guardian.sh    - 启动脚本"
echo "  • stop_timeout_guardian.sh     - 停止脚本"
echo "  • check_timeout_guardian.sh    - 状态检查脚本"
echo ""
echo "⏰ 定时任务配置:"
echo "  • 每5分钟 09:00-18:55 检查并启动"
echo "  • 每天 19:00 停止监控卫士"
echo "  • 每天 02:00 清理旧日志"
echo ""
echo "📊 使用命令:"
echo "  • 手动启动: ./start_timeout_guardian.sh"
echo "  • 手动停止: ./stop_timeout_guardian.sh"
echo "  • 检查状态: ./check_timeout_guardian.sh"
echo ""
echo "📝 日志文件: /home/admin/openclaw/workspace/timeout_guardian.log"
echo ""
echo "🔧 监控卫士将在每天 09:00-19:00 自动运行"