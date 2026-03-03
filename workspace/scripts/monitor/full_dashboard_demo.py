#!/usr/bin/env python3
"""
完整仪表板演示 - 展示增强版所有功能
"""

import time
from enhanced_guardian_final import EnhancedGuardian
from datetime import datetime

def show_dashboard_with_details(guardian):
    """显示详细仪表板"""
    print("\n" + "=" * 70)
    print("增强版智能超时监控卫士 - 详细仪表板")
    print("=" * 70)
    
    # 获取系统信息
    import psutil
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    print(f"\n🖥️  系统状态:")
    print(f"  CPU使用率: {cpu:.1f}%")
    print(f"  内存使用: {memory.percent:.1f}% ({memory.available/1024/1024:.0f}MB 可用)")
    
    # 显示监控配置
    print(f"\n⚙️  监控配置:")
    config = guardian.config
    print(f"  超时阈值: critical({config['timeout_thresholds']['critical']}s), "
          f"high({config['timeout_thresholds']['high']}s), "
          f"medium({config['timeout_thresholds']['medium']}s), "
          f"low({config['timeout_thresholds']['low']}s)")
    
    print(f"  最大告警: critical({config['max_warnings']['critical']}次), "
          f"high({config['max_warnings']['high']}次), "
          f"medium({config['max_warnings']['medium']}次), "
          f"low({config['max_warnings']['low']}次)")
    
    # 显示仪表板
    print(guardian.get_dashboard())
    
    # 显示活跃任务详情
    if guardian.active_tasks:
        print("\n📋 活跃任务详情:")
        print("-" * 40)
        for task_id, task in guardian.active_tasks.items():
            elapsed = (datetime.now() - task["start_time"]).total_seconds()
            priority = task["priority"]
            timeout = config["timeout_thresholds"][priority]
            
            # 计算剩余时间
            remaining = max(0, timeout - elapsed)
            
            print(f"  • {task['task_name']}")
            print(f"    优先级: {priority}, 已执行: {elapsed:.1f}s, 剩余: {remaining:.1f}s")
            print(f"    警告次数: {task['timeout_warnings']}/{config['max_warnings'][priority]}")

def main():
    print("🎯 增强版监控卫士 - 完整仪表板演示")
    print("演示开始:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    # 创建监控实例
    guardian = EnhancedGuardian()
    guardian.start()
    
    # 第一阶段：创建任务并显示初始状态
    print("\n📝 第一阶段：创建监控任务")
    print("-" * 40)
    
    tasks = [
        ("task_urgent", "紧急漏洞修复", "critical", 25),
        ("task_important", "月度报告生成", "high", 50),
        ("task_normal", "用户数据导出", "medium", 100),
        ("task_background", "系统日志分析", "low", 200)
    ]
    
    for task_id, name, priority, est in tasks:
        guardian.start_task(task_id, name, priority, est)
        icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
        print(f"{icon} {name} - 优先级: {priority}, 预估: {est}秒")
    
    # 显示初始仪表板
    show_dashboard_with_details(guardian)
    
    # 第二阶段：模拟任务执行和更新
    print("\n\n📈 第二阶段：任务执行监控")
    print("-" * 40)
    print("模拟任务执行过程...")
    
    stages = [
        (10, "task_urgent", 40, "紧急漏洞修复进度40%"),
        (20, "task_important", 30, "月度报告生成进度30%"),
        (30, "task_urgent", None, "紧急漏洞修复完成"),
        (40, "task_normal", 50, "用户数据导出进度50%"),
        (50, "task_important", None, "月度报告生成完成"),
        (60, "task_normal", None, "用户数据导出完成"),
        (70, "task_background", None, "系统日志分析完成")
    ]
    
    for wait_time, task_id, progress, desc in stages:
        time.sleep(wait_time / 10)  # 加速演示
        
        if progress is not None:
            guardian.update_task(task_id, progress)
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - {desc}")
        else:
            guardian.complete_task(task_id, "任务完成")
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} - {desc}")
        
        # 每阶段显示仪表板
        if wait_time in [30, 60, 70]:
            show_dashboard_with_details(guardian)
    
    # 最终状态
    print("\n\n🎉 演示完成")
    print("=" * 70)
    show_dashboard_with_details(guardian)
    
    guardian.stop()
    print(f"\n演示结束: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
