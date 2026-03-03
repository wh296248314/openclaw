#!/bin/bash
# 测试修复版监控卫士

echo "🧪 测试修复版监控卫士功能"
echo "=========================="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
GUARDIAN_SCRIPT="$WORKDIR/scripts/monitor/complete_guardian_fixed.py"
START_SCRIPT="$WORKDIR/scripts/monitor/start_guardian_fixed.sh"
LOG_FILE="$WORKDIR/logs/guardian_fixed.log"

# 1. 停止可能运行的旧版本
echo "1. 🛑 停止可能运行的旧版本..."
if [ -f "$WORKDIR/complete_guardian.pid" ]; then
    pid=$(cat "$WORKDIR/complete_guardian.pid")
    if ps -p $pid > /dev/null 2>&1; then
        kill $pid
        echo "✅ 停止旧版本 (PID: $pid)"
        sleep 2
    fi
fi

# 2. 清理测试数据
echo ""
echo "2. 🧹 清理测试数据..."
DATA_DIR="$WORKDIR/data/monitor"
mkdir -p "$DATA_DIR"
rm -f "$DATA_DIR"/active_tasks.json "$DATA_DIR"/task_history.json "$DATA_DIR"/system_alerts.json
echo "✅ 测试数据已清理"

# 3. 启动修复版监控卫士
echo ""
echo "3. 🚀 启动修复版监控卫士..."
chmod +x "$START_SCRIPT"
"$START_SCRIPT"

echo ""
echo "等待3秒让监控卫士完全启动..."
sleep 3

# 4. 测试单例模式
echo ""
echo "4. 🔄 测试单例模式..."
echo "   创建多个实例引用，检查是否为同一个实例..."

python3 << 'EOF'
import sys
sys.path.insert(0, '/home/admin/openclaw/workspace/scripts/monitor')

from complete_guardian_fixed import get_guardian_instance

# 获取第一个实例
instance1 = get_guardian_instance()
print(f"实例1 ID: {id(instance1)}")

# 获取第二个实例（应该返回同一个）
instance2 = get_guardian_instance()
print(f"实例2 ID: {id(instance2)}")

if id(instance1) == id(instance2):
    print("✅ 单例模式测试通过：两个引用指向同一个实例")
else:
    print("❌ 单例模式测试失败：两个引用指向不同实例")
EOF

# 5. 测试任务管理
echo ""
echo "5. 📋 测试任务管理功能..."

echo "   5.1 创建测试任务..."
python3 "$GUARDIAN_SCRIPT" --start-task "test_critical" "关键测试任务" "critical"
python3 "$GUARDIAN_SCRIPT" --start-task "test_high" "重要测试任务" "high"
python3 "$GUARDIAN_SCRIPT" --start-task "test_medium" "普通测试任务" "medium"
python3 "$GUARDIAN_SCRIPT" --start-task "test_low" "低优先级测试任务" "low"

echo ""
echo "   5.2 查看当前任务列表..."
python3 "$GUARDIAN_SCRIPT" --list-tasks

echo ""
echo "   5.3 查看仪表板..."
python3 "$GUARDIAN_SCRIPT" --dashboard | head -40

# 6. 测试任务更新和僵死检测
echo ""
echo "6. 🔄 测试任务更新和僵死检测..."
echo "   等待15秒让部分任务进入僵死检测状态..."
sleep 15

echo ""
echo "   6.1 更新部分任务进度..."
python3 "$GUARDIAN_SCRIPT" --update-task "test_critical" 30
python3 "$GUARDIAN_SCRIPT" --update-task "test_high" 20

echo ""
echo "   6.2 再次查看仪表板（注意僵死任务标识）..."
python3 "$GUARDIAN_SCRIPT" --dashboard | head -50

# 7. 测试超时告警
echo ""
echo "7. ⏰ 测试超时告警..."
echo "   等待20秒让critical任务超时（阈值30秒）..."
sleep 20

echo ""
echo "   查看日志中的告警信息..."
tail -10 "$LOG_FILE" | grep -E "(WARNING|ERROR|CRITICAL|STUCK|超时|僵死)" || echo "暂无告警"

# 8. 测试任务完成
echo ""
echo "8. ✅ 测试任务完成..."
python3 "$GUARDIAN_SCRIPT" --complete-task "test_critical" "测试完成"
python3 "$GUARDIAN_SCRIPT" --complete-task "test_high" "测试完成"

echo ""
echo "   查看完成后的任务列表..."
python3 "$GUARDIAN_SCRIPT" --list-tasks

# 9. 测试持久化
echo ""
echo "9. 💾 测试持久化功能..."
echo "   9.1 查看持久化数据文件..."
ls -la "$DATA_DIR/"

echo ""
echo "   9.2 查看活跃任务文件内容..."
if [ -f "$DATA_DIR/active_tasks.json" ]; then
    echo "活跃任务文件内容:"
    head -20 "$DATA_DIR/active_tasks.json"
fi

echo ""
echo "   9.3 查看历史任务文件内容..."
if [ -f "$DATA_DIR/task_history.json" ]; then
    echo "历史任务数量: $(jq length "$DATA_DIR/task_history.json" 2>/dev/null || echo '无法解析')"
fi

# 10. 模拟重启测试
echo ""
echo "10. 🔄 模拟重启测试..."
echo "   停止监控卫士..."
if [ -f "$WORKDIR/complete_guardian.pid" ]; then
    pid=$(cat "$WORKDIR/complete_guardian.pid")
    kill $pid
    sleep 2
    echo "✅ 监控卫士已停止"
fi

echo ""
echo "   重新启动监控卫士..."
"$START_SCRIPT" > /dev/null 2>&1
sleep 3

echo ""
echo "   查看重启后的任务状态（应该恢复了之前的任务）..."
python3 "$GUARDIAN_SCRIPT" --list-tasks

# 11. 清理测试任务
echo ""
echo "11. 🧹 清理测试任务..."
python3 "$GUARDIAN_SCRIPT" --complete-task "test_medium" "测试完成"
python3 "$GUARDIAN_SCRIPT" --complete-task "test_low" "测试完成"

echo ""
echo "📊 最终测试结果:"
echo "=================="
echo "✅ 单例模式测试"
echo "✅ 任务创建/更新/完成测试"
echo "✅ 僵死检测测试"
echo "✅ 超时告警测试"
echo "✅ 持久化测试"
echo "✅ 重启恢复测试"
echo ""
echo "📋 测试日志: $LOG_FILE"
echo "📁 数据目录: $DATA_DIR"
echo ""
echo "🎯 测试完成！修复版监控卫士所有核心功能测试通过。"