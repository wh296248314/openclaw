#!/bin/bash
# 启动修复版监控卫士

echo "🚀 启动修复版监控卫士..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
LOG_DIR="$WORKDIR/logs"
DATA_DIR="$WORKDIR/data/monitor"
PID_FILE="$WORKDIR/complete_guardian.pid"
CONFIG_FILE="$WORKDIR/configs/timeout_guardian_optimized_config.json"

# 创建必要的目录
mkdir -p "$LOG_DIR"
mkdir -p "$DATA_DIR"

echo "📁 目录检查:"
echo "  工作目录: $WORKDIR"
echo "  日志目录: $LOG_DIR"
echo "  数据目录: $DATA_DIR"
echo "  配置文件: $CONFIG_FILE"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ 监控卫士已在运行 (PID: $pid)"
        echo "   使用以下命令查看状态:"
        echo "   python3 scripts/monitor/complete_guardian_fixed.py --dashboard"
        exit 0
    else
        echo "⚠️  发现旧的PID文件，但进程不存在，清理..."
        rm -f "$PID_FILE"
    fi
fi

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在，创建默认配置..."
    cat > "$CONFIG_FILE" << 'CONFIG_EOF'
{
  "monitoring_config": {
    "timeout_thresholds": {
      "critical": 30,
      "high": 60,
      "medium": 120,
      "low": 300
    },
    "max_warnings": {
      "critical": 5,
      "high": 3,
      "medium": 2,
      "low": 1
    },
    "stuck_thresholds": {
      "critical": 15,
      "high": 30,
      "medium": 60,
      "low": 120
    },
    "notification_channels": ["log"],
    "enable_resource_monitoring": true,
    "data_retention_days": 30,
    "enable_performance_metrics": true,
    "heartbeat_interval": 60
  },
  "system_monitoring": {
    "enable_cpu_monitoring": true,
    "enable_memory_monitoring": true,
    "enable_disk_monitoring": true,
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
CONFIG_EOF
    echo "✅ 默认配置文件已创建"
fi

# 启动修复版监控卫士
echo ""
echo "🚀 启动监控进程..."
cd "$WORKDIR"

# 使用nohup在后台运行
nohup python3 scripts/monitor/complete_guardian_fixed.py > "$LOG_DIR/guardian_fixed.log" 2>&1 &
GUARDIAN_PID=$!

# 等待启动
sleep 3

# 检查是否启动成功
if ps -p $GUARDIAN_PID > /dev/null 2>&1; then
    echo "✅ 修复版监控卫士启动成功 (PID: $GUARDIAN_PID)"
    echo ""
    echo "📋 修复版功能摘要:"
    echo "  ✅ 单例模式 - 全局唯一实例"
    echo "  ✅ 任务持久化 - 重启不丢任务"
    echo "  ✅ PID文件管理 - 正确创建和维护"
    echo "  ✅ 僵死检测 - 检测卡住的任务"
    echo "  ✅ 心跳机制 - 定期保存状态"
    echo "  ✅ 数据清理 - 自动清理过期数据"
    echo ""
    echo "📊 使用命令:"
    echo "  • 查看仪表板: python3 scripts/monitor/complete_guardian_fixed.py --dashboard"
    echo "  • 启动任务: python3 scripts/monitor/complete_guardian_fixed.py --start-task ID 名称 优先级"
    echo "  • 更新任务: python3 scripts/monitor/complete_guardian_fixed.py --update-task ID 进度"
    echo "  • 完成任务: python3 scripts/monitor/complete_guardian_fixed.py --complete-task ID 结果"
    echo "  • 列出任务: python3 scripts/monitor/complete_guardian_fixed.py --list-tasks"
    echo "  • 查看日志: tail -f $LOG_DIR/guardian_fixed.log"
    echo "  • 停止监控: kill $GUARDIAN_PID"
    echo ""
    echo "🎯 立即测试:"
    echo "  1. 查看状态: python3 scripts/monitor/complete_guardian_fixed.py --dashboard"
    echo "  2. 创建测试任务: python3 scripts/monitor/complete_guardian_fixed.py --start-task test1 '测试任务' critical"
    echo "  3. 等待30秒查看超时告警"
    echo "  4. 更新任务: python3 scripts/monitor/complete_guardian_fixed.py --update-task test1 50"
    echo "  5. 完成任务: python3 scripts/monitor/complete_guardian_fixed.py --complete-task test1 '测试完成'"
    echo ""
    echo "📁 数据文件位置:"
    echo "  • 活跃任务: $DATA_DIR/active_tasks.json"
    echo "  • 历史任务: $DATA_DIR/task_history.json"
    echo "  • 系统告警: $DATA_DIR/system_alerts.json"
    echo "  • PID文件: $PID_FILE"
else
    echo "❌ 监控卫士启动失败"
    echo "请检查日志: $LOG_DIR/guardian_fixed.log"
    exit 1
fi

echo ""
echo "⏰ 启动完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🎯 修复版监控卫士已就绪！"