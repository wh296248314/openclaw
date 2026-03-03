#!/bin/bash
# 启动增强版智能超时监控卫士

echo "启动增强版智能超时监控卫士..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
CONFIG_FILE="$WORKDIR/timeout_guardian_optimized_config.json"
LOG_FILE="$WORKDIR/enhanced_timeout_guardian.log"
PID_FILE="$WORKDIR/enhanced_timeout_guardian.pid"

# 检查是否在运行时间内 (09:00-19:00)
current_hour=$(date +%H)
if [ $current_hour -lt 9 ] || [ $current_hour -ge 19 ]; then
    echo "⚠️  非运行时间 (09:00-19:00)，当前时间: $(date +%H:%M)"
    echo "如需强制启动，请使用: ./start_enhanced_guardian.sh --force"
    
    if [ "$1" != "--force" ]; then
        exit 0
    else
        echo "强制启动模式..."
    fi
fi

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ 增强版监控卫士已在运行 (PID: $pid)"
        echo "使用以下命令查看状态:"
        echo "  ./check_enhanced_guardian.sh"
        echo "  tail -f $LOG_FILE"
        exit 0
    else
        echo "⚠️  PID文件存在但进程未运行，清理PID文件..."
        rm -f "$PID_FILE"
    fi
fi

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在，使用默认配置..."
    cat > "$CONFIG_FILE" << 'EOF'
{
  "monitoring_config": {
    "timeout_thresholds": {
      "critical": 30,
      "high": 60,
      "medium": 120,
      "low": 300
    },
    "check_intervals": {
      "critical": 10,
      "high": 30,
      "medium": 60,
      "low": 120
    },
    "max_warnings": {
      "critical": 5,
      "high": 3,
      "medium": 2,
      "low": 1
    },
    "notification_channels": ["log", "desktop"],
    "enable_resource_monitoring": true,
    "data_retention_days": 30,
    "enable_performance_metrics": true,
    "enable_trend_analysis": true
  },
  "system_monitoring": {
    "enable_cpu_monitoring": true,
    "enable_memory_monitoring": true,
    "enable_disk_monitoring": true,
    "enable_network_monitoring": true,
    "thresholds": {
      "cpu_warning": 80,
      "cpu_critical": 95,
      "memory_warning": 85,
      "memory_critical": 95,
      "disk_warning": 90,
      "disk_critical": 98
    }
  }
}
EOF
    echo "✅ 默认配置文件已创建: $CONFIG_FILE"
fi

# 检查Python依赖
echo "检查Python依赖..."
python3 -c "import psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装psutil库..."
    pip3 install psutil --quiet
    if [ $? -eq 0 ]; then
        echo "✅ psutil库安装成功"
    else
        echo "❌ psutil库安装失败，尝试使用apt安装..."
        sudo apt install -y python3-psutil 2>/dev/null || echo "⚠️  请手动安装: sudo apt install python3-psutil"
    fi
else
    echo "✅ Python依赖检查通过"
fi

# 启动增强版监控卫士
echo "启动增强版监控卫士..."
cd "$WORKDIR"

# 备份旧日志
if [ -f "$LOG_FILE" ]; then
    log_size=$(du -h "$LOG_FILE" | cut -f1)
    if [ $(echo "$log_size" | grep -o '[0-9]*') -gt 10 ]; then
        backup_file="${LOG_FILE}.backup_$(date +%Y%m%d_%H%M%S)"
        cp "$LOG_FILE" "$backup_file"
        echo "📁 日志文件已备份: $backup_file"
        > "$LOG_FILE"  # 清空日志文件
    fi
fi

# 启动进程
nohup python3 enhanced_timeout_guardian_full.py --config "$CONFIG_FILE" >> "$LOG_FILE" 2>&1 &
ENHANCED_PID=$!

# 等待启动
sleep 3

# 检查是否启动成功
if ps -p $ENHANCED_PID > /dev/null 2>&1; then
    echo $ENHANCED_PID > "$PID_FILE"
    echo "✅ 增强版监控卫士启动成功 (PID: $ENHANCED_PID)"
    echo ""
    echo "📋 监控配置:"
    echo "  • 超时阈值: critical(30s), high(60s), medium(120s), low(300s)"
    echo "  • 检查间隔: 动态调整 (基于任务优先级)"
    echo "  • 资源监控: 启用 (CPU、内存、磁盘)"
    echo "  • 系统监控: 启用 (阈值告警)"
    echo ""
    echo "📊 使用命令:"
    echo "  • 查看状态: ./check_enhanced_guardian.sh"
    echo "  • 查看日志: tail -f $LOG_FILE"
    echo "  • 停止服务: ./stop_enhanced_guardian.sh"
    echo "  • 演示功能: ./demo_enhanced_guardian.sh"
    echo ""
    echo "🖥️  实时仪表板:"
    echo "  运行: python3 enhanced_timeout_guardian_full.py --dashboard"
    echo ""
    echo "⏰ 运行时间: 每天 09:00 - 19:00"
else
    echo "❌ 增强版监控卫士启动失败"
    echo "请检查日志: $LOG_FILE"
    exit 1
fi

# 显示最后几行日志
echo "最近日志:"
tail -10 "$LOG_FILE" | sed 's/^/  /'

echo ""
echo "🎯 增强版功能已启用!"
echo "   优先级管理、分级提醒、资源监控、系统告警"