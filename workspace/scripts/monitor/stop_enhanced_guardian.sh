#!/bin/bash
# 停止增强版智能超时监控卫士

echo "停止增强版智能超时监控卫士..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
PID_FILE="$WORKDIR/enhanced_timeout_guardian.pid"
LOG_FILE="$WORKDIR/enhanced_timeout_guardian.log"

if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "找到运行中的增强版监控卫士 (PID: $pid)"
        echo "正在停止..."
        
        # 优雅停止
        kill $pid
        sleep 2
        
        # 检查是否已停止
        if ps -p $pid > /dev/null 2>&1; then
            echo "进程仍在运行，强制停止..."
            kill -9 $pid
            sleep 1
        fi
        
        if ps -p $pid > /dev/null 2>&1; then
            echo "❌ 无法停止进程，请手动检查"
            exit 1
        else
            rm -f "$PID_FILE"
            echo "✅ 增强版监控卫士已停止"
            
            # 记录停止日志
            echo "$(date): 增强版监控卫士已手动停止 (原PID: $pid)" >> "$LOG_FILE"
        fi
    else
        echo "⚠️  PID文件存在但进程未运行，清理PID文件..."
        rm -f "$PID_FILE"
    fi
else
    echo "⏸️  增强版监控卫士未运行"
    
    # 检查是否有其他相关进程
    other_pids=$(ps aux | grep "enhanced_timeout_guardian" | grep -v grep | grep -v "stop_enhanced" | awk '{print $2}')
    if [ -n "$other_pids" ]; then
        echo "发现其他相关进程: $other_pids"
        read -p "是否停止这些进程? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            for other_pid in $other_pids; do
                echo "停止进程: $other_pid"
                kill $other_pid 2>/dev/null
            done
            echo "✅ 相关进程已停止"
        fi
    fi
fi

echo ""
echo "📊 状态检查:"
./check_enhanced_guardian.sh | head -20