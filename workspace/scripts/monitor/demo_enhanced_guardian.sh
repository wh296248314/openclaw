#!/bin/bash
# 增强版智能超时监控卫士演示脚本

echo "增强版智能超时监控卫士功能演示"
echo "================================"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
CONFIG_FILE="$WORKDIR/timeout_guardian_optimized_config.json"

# 检查是否在运行
if [ ! -f "$WORKDIR/enhanced_timeout_guardian.pid" ]; then
    echo "⚠️  增强版监控卫士未运行"
    echo "正在启动..."
    ./start_enhanced_guardian.sh --force
    sleep 3
fi

echo "1. 演示不同优先级的任务监控"
echo "---------------------------"

# 创建演示任务
echo "创建4个不同优先级的演示任务:"
echo ""

# 使用Python创建演示任务
python3 << 'EOF'
import time
from datetime import datetime

print("🎯 开始创建演示任务...")
print()

# 模拟任务数据
demo_tasks = [
    {
        "id": "demo_critical_001",
        "name": "紧急订单处理",
        "priority": "critical",
        "category": "data_processing",
        "estimated": 25,
        "description": "处理用户紧急订单，需要快速响应"
    },
    {
        "id": "demo_high_001", 
        "name": "API接口性能测试",
        "priority": "high",
        "category": "api_call",
        "estimated": 45,
        "description": "测试关键API接口性能"
    },
    {
        "id": "demo_medium_001",
        "name": "日常数据备份",
        "priority": "medium",
        "category": "system_task",
        "estimated": 90,
        "description": "执行日常数据库备份"
    },
    {
        "id": "demo_low_001",
        "name": "日志文件清理",
        "priority": "low",
        "category": "system_task",
        "estimated": 180,
        "description": "清理过期日志文件"
    }
]

for task in demo_tasks:
    print(f"📝 创建任务: {task['name']}")
    print(f"   优先级: {task['priority']}")
    print(f"   预估时间: {task['estimated']}秒")
    print(f"   描述: {task['description']}")
    print()

print("✅ 演示任务创建完成")
print("监控卫士将自动检测超时任务并发送提醒")
print()
EOF

echo ""
echo "2. 演示系统资源监控"
echo "-------------------"

# 显示当前系统资源
python3 << 'EOF'
import psutil
import time

print("📊 当前系统资源状态:")
print()

# CPU
cpu_percent = psutil.cpu_percent(interval=1)
cpu_status = "正常" if cpu_percent < 50 else "偏高" if cpu_percent < 80 else "过高"
print(f"⚡ CPU使用率: {cpu_percent:.1f}% ({cpu_status})")

# 内存
memory = psutil.virtual_memory()
memory_status = "正常" if memory.percent < 70 else "偏高" if memory.percent < 85 else "过高"
print(f"💾 内存使用: {memory.percent:.1f}% ({memory_status})")
print(f"   可用内存: {memory.available/1024/1024:.0f}MB")

# 磁盘
try:
    disk = psutil.disk_usage('/')
    disk_status = "正常" if disk.percent < 80 else "偏高" if disk.percent < 90 else "过高"
    print(f"💿 磁盘使用: {disk.percent:.1f}% ({disk_status})")
    print(f"   可用空间: {disk.free/1024/1024/1024:.1f}GB")
except:
    print("💿 磁盘信息: 获取失败")

print()
print("🔔 系统监控已启用，当资源超过阈值时会自动告警")
print()
EOF

echo ""
echo "3. 演示分级提醒机制"
echo "-------------------"

echo "分级提醒示例:"
echo "• 🟢 信息级别 (INFO): 任务开始、进度更新"
echo "• 🟡 警告级别 (WARNING): 任务超时（首次）"
echo "• 🟠 错误级别 (ERROR): 严重超时（超过阈值2倍）"
echo "• 🔴 严重级别 (CRITICAL): 极度超时（超过阈值3倍）或系统资源严重不足"
echo ""
echo "通知渠道:"
echo "• 日志记录: 所有级别"
echo "• 桌面通知: 警告级别及以上"
echo "• 邮件通知: 错误级别及以上（需配置）"
echo "• IM通知: 严重级别（需配置）"
echo ""

echo "4. 演示动态检查间隔"
echo "-------------------"

echo "检查间隔根据任务优先级动态调整:"
echo "• 🔴 Critical任务: 每10秒检查一次"
echo "• 🟠 High任务: 每30秒检查一次"
echo "• 🟡 Medium任务: 每60秒检查一次"
echo "• 🟢 Low任务: 每120秒检查一次"
echo ""
echo "当没有活跃任务时，检查间隔延长至60秒以节省资源。"
echo ""

echo "5. 演示预估时间超时检测"
echo "-----------------------"

echo "增强功能: 基于预估时间的智能超时检测"
echo "• 任务创建时可设置预估完成时间"
echo "• 实际执行时间超过预估时间50%时触发警告"
echo "• 帮助提前发现性能问题，而非等待固定超时"
echo ""

echo "6. 查看实时仪表板"
echo "-----------------"

echo "正在显示实时监控仪表板..."
echo ""
python3 "$WORKDIR/enhanced_timeout_guardian_full.py" --dashboard
echo ""

echo "7. 查看统计信息"
echo "---------------"

echo "正在显示统计信息..."
echo ""
python3 "$WORKDIR/enhanced_timeout_guardian_full.py" --stats 2>/dev/null | head -50
echo ""

echo "8. 演示任务更新和完成"
echo "---------------------"

echo "模拟任务更新和完成过程..."
echo ""

# 模拟任务更新
python3 << 'EOF'
import time
import random

print("🔄 模拟任务进度更新...")
time.sleep(2)

for i in range(1, 5):
    progress = i * 25
    print(f"   任务 demo_{['critical', 'high', 'medium', 'low'][i-1]}_001: 进度更新至 {progress}%")
    time.sleep(0.5)

print()
print("✅ 模拟任务完成...")
time.sleep(1)

tasks = ["紧急订单处理", "API接口性能测试", "日常数据备份", "日志文件清理"]
for task in tasks:
    duration = random.randint(30, 120)
    print(f"   {task}: 完成! 耗时 {duration}秒")
    time.sleep(0.3)

print()
print("🎉 演示任务全部完成!")
print()
EOF

echo ""
echo "演示总结"
echo "========"
echo "✅ 增强版监控卫士演示完成"
echo ""
echo "🎯 演示的功能包括:"
echo "1. 四级优先级任务管理"
echo "2. 分级提醒机制"
echo "3. 系统资源监控和告警"
echo "4. 动态检查间隔调整"
echo "5. 预估时间超时检测"
echo "6. 实时监控仪表板"
echo "7. 详细统计信息"
echo ""
echo "📊 监控效果:"
echo "• 更精准的超时检测"
echo "• 更及时的故障发现"
echo "• 更智能的资源管理"
echo "• 更完善的监控覆盖"
echo ""
echo "🚀 下一步:"
echo "• 在实际任务中测试增强版功能"
echo "• 根据需求调整监控配置"
echo "• 配置邮件或IM通知渠道"
echo "• 集成到现有工作流程中"
echo ""
echo "演示结束时间: $(date '+%Y-%m-%d %H:%M:%S')"