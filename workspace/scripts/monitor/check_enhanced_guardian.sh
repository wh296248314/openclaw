#!/bin/bash
# 检查增强版智能超时监控卫士状态

echo "增强版智能超时监控卫士状态检查"
echo "================================"
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKDIR="/home/admin/openclaw/workspace"
PID_FILE="$WORKDIR/enhanced_timeout_guardian.pid"
LOG_FILE="$WORKDIR/enhanced_timeout_guardian.log"
CONFIG_FILE="$WORKDIR/timeout_guardian_optimized_config.json"
HISTORY_FILE="$WORKDIR/enhanced_timeout_guardian_history.json"

# 检查进程
echo "1. 进程状态:"
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p $pid > /dev/null 2>&1; then
        echo "   ✅ 正在运行 (PID: $pid)"
        
        # 检查运行时间
        start_time=$(ps -o lstart= -p $pid)
        echo "   🕐 启动时间: $start_time"
        
        # 检查内存使用
        memory=$(ps -o rss= -p $pid)
        memory_mb=$((memory / 1024))
        echo "   💾 内存使用: ${memory_mb}MB"
        
        # 检查CPU使用
        cpu=$(ps -o %cpu= -p $pid)
        echo "   ⚡ CPU使用: ${cpu}%"
    else
        echo "   ❌ PID文件存在但进程未运行"
        rm -f "$PID_FILE"
    fi
else
    echo "   ⏸️  未运行"
fi

# 检查配置文件
echo ""
echo "2. 配置文件:"
if [ -f "$CONFIG_FILE" ]; then
    config_size=$(du -h "$CONFIG_FILE" | cut -f1)
    echo "   ✅ 存在 ($config_size)"
    
    # 显示关键配置
    echo "   关键配置:"
    python3 -c "
import json
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
    
    # 超时阈值
    thresholds = config.get('monitoring_config', {}).get('timeout_thresholds', {})
    print(f'    超时阈值: critical({thresholds.get(\"critical\", 30)}s), high({thresholds.get(\"high\", 60)}s), medium({thresholds.get(\"medium\", 120)}s), low({thresholds.get(\"low\", 300)}s)')
    
    # 资源监控
    resource_monitoring = config.get('monitoring_config', {}).get('enable_resource_monitoring', False)
    print(f'    资源监控: {\"启用\" if resource_monitoring else \"禁用\"}')
    
    # 系统监控
    sys_monitoring = config.get('system_monitoring', {}).get('enable_cpu_monitoring', False)
    print(f'    系统监控: {\"启用\" if sys_monitoring else \"禁用\"}')
    
except Exception as e:
    print(f'    读取配置失败: {e}')
"
else
    echo "   ❌ 不存在"
fi

# 检查日志文件
echo ""
echo "3. 日志文件:"
if [ -f "$LOG_FILE" ]; then
    log_size=$(du -h "$LOG_FILE" | cut -f1)
    log_lines=$(wc -l < "$LOG_FILE")
    echo "   ✅ 存在 (${log_size}, ${log_lines}行)"
    
    # 显示最后5行日志
    if [ $log_lines -gt 0 ]; then
        echo "   最近日志:"
        tail -5 "$LOG_FILE" | sed 's/^/      /'
    fi
else
    echo "   ❌ 不存在"
fi

# 检查历史记录
echo ""
echo "4. 历史记录:"
if [ -f "$HISTORY_FILE" ]; then
    history_count=$(python3 -c "
import json
try:
    with open('$HISTORY_FILE', 'r') as f:
        history = json.load(f)
    print(f'   ✅ {len(history)} 个任务记录')
    
    # 统计信息
    if history:
        completed = sum(1 for t in history if t.get('status') == 'completed')
        failed = sum(1 for t in history if t.get('status') == 'failed')
        timeout = sum(1 for t in history if t.get('status') == 'timeout')
        
        total = len(history)
        success_rate = (completed / total * 100) if total > 0 else 0
        
        print(f'     完成率: {success_rate:.1f}% ({completed}✅ {failed}❌ {timeout}⏰)')
        
        # 按优先级统计
        priorities = {}
        for task in history:
            priority = task.get('priority', 'medium')
            priorities[priority] = priorities.get(priority, 0) + 1
        
        if priorities:
            print(f'     优先级分布:')
            for priority, count in priorities.items():
                print(f'       {priority}: {count}个')
        
except Exception as e:
    print(f'   ❌ 读取失败: {e}')
")
else
    echo "   ⏸️  无历史记录"
fi

# 检查系统资源
echo ""
echo "5. 系统资源状态:"
python3 -c "
import psutil
import json

try:
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_status = '🟢' if cpu_percent < 50 else '🟡' if cpu_percent < 80 else '🔴'
    print(f'   {cpu_status} CPU使用率: {cpu_percent:.1f}%')
    
    # 内存
    memory = psutil.virtual_memory()
    memory_status = '🟢' if memory.percent < 70 else '🟡' if memory.percent < 85 else '🔴'
    print(f'   {memory_status} 内存使用: {memory.percent:.1f}% ({memory.available/1024/1024:.0f}MB 可用)')
    
    # 磁盘
    try:
        disk = psutil.disk_usage('/')
        disk_status = '🟢' if disk.percent < 80 else '🟡' if disk.percent < 90 else '🔴'
        print(f'   {disk_status} 磁盘使用: {disk.percent:.1f}% ({disk.free/1024/1024/1024:.1f}GB 可用)')
    except:
        print('   ⚠️  磁盘信息获取失败')
    
    # 加载配置检查阈值
    try:
        with open('$CONFIG_FILE', 'r') as f:
            config = json.load(f)
        
        thresholds = config.get('system_monitoring', {}).get('thresholds', {})
        if thresholds:
            print(f'   告警阈值:')
            print(f'     CPU警告: {thresholds.get(\"cpu_warning\", 80)}%, 严重: {thresholds.get(\"cpu_critical\", 95)}%')
            print(f'     内存警告: {thresholds.get(\"memory_warning\", 85)}%, 严重: {thresholds.get(\"memory_critical\", 95)}%')
            print(f'     磁盘警告: {thresholds.get(\"disk_warning\", 90)}%, 严重: {thresholds.get(\"disk_critical\", 98)}%')
    except:
        print('   告警阈值: 使用默认值')
        
except Exception as e:
    print(f'   ❌ 系统资源检查失败: {e}')
"

# 检查Python依赖
echo ""
echo "6. Python依赖:"
python3 -c "
try:
    import psutil
    print('   ✅ psutil: 已安装')
except ImportError:
    print('   ❌ psutil: 未安装 (运行: pip3 install psutil)')

try:
    import json
    print('   ✅ json: 已安装')
except ImportError:
    print('   ❌ json: 未安装')
"

# 运行时间检查
echo ""
echo "7. 运行时间配置:"
current_hour=$(date +%H)
if [ $current_hour -ge 9 ] && [ $current_hour -lt 19 ]; then
    echo "   ✅ 在运行时间内 (09:00-19:00)"
    echo "     当前时间: $(date +%H:%M)"
else
    echo "   ⏸️  非运行时间 (09:00-19:00)"
    echo "     当前时间: $(date +%H:%M)"
fi

# 显示cron配置
echo ""
echo "8. 自动启动配置:"
cron_count=$(crontab -l 2>/dev/null | grep -c "start_enhanced_guardian")
if [ $cron_count -gt 0 ]; then
    echo "   ✅ 已配置自动启动"
    crontab -l 2>/dev/null | grep "start_enhanced_guardian" | sed 's/^/     /'
else
    echo "   ⚠️  未配置自动启动"
    echo "     建议配置: */5 9-18 * * * $WORKDIR/start_enhanced_guardian.sh"
fi

echo ""
echo "=" * 50
echo "📊 使用命令汇总:"
echo "  • 启动: ./start_enhanced_guardian.sh"
echo "  • 停止: ./stop_enhanced_guardian.sh"
echo "  • 演示: ./demo_enhanced_guardian.sh"
echo "  • 仪表板: python3 enhanced_timeout_guardian_full.py --dashboard"
echo "  • 统计: python3 enhanced_timeout_guardian_full.py --stats"
echo ""
echo "🎯 增强版功能:"
echo "  • 四级优先级管理 (critical/high/medium/low)"
echo "  • 分级提醒机制 (warning/error/critical)"
echo "  • 系统资源监控 (CPU/内存/磁盘)"
echo "  • 动态检查间隔 (基于任务负载)"
echo "  • 预估时间超时检测"
echo ""
echo "⏰ 下次检查: $(date -d '+5 minutes' '+%H:%M')"