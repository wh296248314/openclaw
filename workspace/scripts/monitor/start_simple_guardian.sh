#!/bin/bash
echo "启动简化版增强监控卫士..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

WORKDIR="/home/admin/openclaw/workspace"
LOG_FILE="$WORKDIR/enhanced_guardian_runtime.log"
PID_FILE="$WORKDIR/enhanced_guardian_runtime.pid"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ 监控卫士已在运行 (PID: $pid)"
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

# 启动简化版监控卫士
echo "启动监控进程..."
cd "$WORKDIR"

# 使用简化版代码启动后台进程
python3 << 'EOF_PYTHON' > "$LOG_FILE" 2>&1 &
import time
import threading
from enhanced_guardian_final import EnhancedGuardian
from datetime import datetime

guardian = EnhancedGuardian()
guardian.start()

print(f"✅ 增强版监控卫士已启动 ({datetime.now().strftime('%H:%M:%S')})")
print(f"   超时阈值: critical(30s), high(60s), medium(120s), low(300s)")
print(f"   运行时间: 09:00-19:00")

# 保持运行
try:
    while True:
        time.sleep(60)
        # 每分钟记录一次心跳
        print(f"💓 监控运行中 ({datetime.now().strftime('%H:%M:%S')})")
except KeyboardInterrupt:
    guardian.stop()
    print("监控已停止")
EOF_PYTHON

SIMPLE_PID=$!
echo $SIMPLE_PID > "$PID_FILE"

sleep 2

if ps -p $SIMPLE_PID > /dev/null 2>&1; then
    echo "✅ 简化版增强监控卫士启动成功 (PID: $SIMPLE_PID)"
    echo "📋 监控配置:"
    echo "  • 超时阈值: critical(30s), high(60s), medium(120s), low(300s)"
    echo "  • 检查间隔: 动态调整"
    echo "  • 最大告警: critical(5次), high(3次), medium(2次), low(1次)"
    echo ""
    echo "📊 使用命令:"
    echo "  • 查看状态: ps aux | grep enhanced_guardian"
    echo "  • 查看日志: tail -f $LOG_FILE"
    echo "  • 停止监控: kill $SIMPLE_PID"
    echo "  • 仪表板: python3 enhanced_guardian_final.py --dashboard"
else
    echo "❌ 启动失败"
    echo "请检查日志: $LOG_FILE"
    exit 1
fi
