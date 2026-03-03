#!/bin/bash
# 监控卫士半小时观察脚本

WORKDIR="/home/admin/openclaw/workspace"
LOG_FILE="$WORKDIR/complete_guardian.log"
MONITOR_LOG="$WORKDIR/guardian_monitor_$(date +%Y%m%d_%H%M%S).log"

echo "🔍 监控卫士半小时观察日志" > "$MONITOR_LOG"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$MONITOR_LOG"
echo "观察时长: 30分钟" >> "$MONITOR_LOG"
echo "======================================" >> "$MONITOR_LOG"

# 初始状态
echo "" >> "$MONITOR_LOG"
echo "📊 初始状态 (T+0):" >> "$MONITOR_LOG"
python3 "$WORKDIR/complete_guardian_main.py" --dashboard 2>&1 | tail -50 >> "$MONITOR_LOG"

# 每5分钟检查一次，共6次
for i in {1..6}; do
    sleep 300  # 5分钟
    
    echo "" >> "$MONITOR_LOG"
    echo "📊 检查点 $i/6 (T+$((i*5))分钟):" >> "$MONITOR_LOG"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$MONITOR_LOG"
    
    # 检查进程状态
    if [ -f "$WORKDIR/complete_guardian.pid" ]; then
        pid=$(cat "$WORKDIR/complete_guardian.pid")
        if ps -p $pid > /dev/null 2>&1; then
            echo "✅ 监控进程运行正常 (PID: $pid)" >> "$MONITOR_LOG"
        else
            echo "❌ 监控进程已停止" >> "$MONITOR_LOG"
        fi
    else
        echo "⚠️  PID文件不存在" >> "$MONITOR_LOG"
    fi
    
    # 获取仪表板
    python3 "$WORKDIR/complete_guardian_main.py" --dashboard 2>&1 | tail -50 >> "$MONITOR_LOG"
    
    # 检查最近日志中的告警
    echo "" >> "$MONITOR_LOG"
    echo "⚠️  最近5分钟告警:" >> "$MONITOR_LOG"
    tail -100 "$LOG_FILE" 2>/dev/null | grep -E "(WARNING|ERROR|CRITICAL)" | tail -10 >> "$MONITOR_LOG" || echo "无告警" >> "$MONITOR_LOG"
    
    # 检查系统资源
    echo "" >> "$MONITOR_LOG"
    echo "🖥️  系统资源状态:" >> "$MONITOR_LOG"
    echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%" >> "$MONITOR_LOG"
    echo "内存: $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}')" >> "$MONITOR_LOG"
    echo "磁盘: $(df -h / | awk 'NR==2{print $5}')" >> "$MONITOR_LOG"
done

echo "" >> "$MONITOR_LOG"
echo "======================================" >> "$MONITOR_LOG"
echo "观察结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$MONITOR_LOG"
echo "总观察时长: 30分钟" >> "$MONITOR_LOG"

# 生成总结报告
echo "" >> "$MONITOR_LOG"
echo "📈 观察总结:" >> "$MONITOR_LOG"
echo "1. 进程稳定性: $(grep -c "运行正常" "$MONITOR_LOG")/6 次检查正常" >> "$MONITOR_LOG"
echo "2. 告警数量: $(grep -c "WARNING\|ERROR\|CRITICAL" "$MONITOR_LOG") 次" >> "$MONITOR_LOG"
echo "3. 系统资源: 平均CPU $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%, 内存 $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}')" >> "$MONITOR_LOG"

echo "✅ 监控观察完成，日志保存到: $MONITOR_LOG"
