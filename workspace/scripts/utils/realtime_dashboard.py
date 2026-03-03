#!/usr/bin/env python3
"""
实时监控仪表板演示
"""

import time
from enhanced_guardian_final import EnhancedGuardian
from datetime import datetime

def main():
    print("🎯 增强版监控卫士 - 实时监控演示")
    print("开始时间:", datetime.now().strftime("%H:%M:%S"))
    print("=" * 60)
    
    # 创建监控实例
    guardian = EnhancedGuardian()
    guardian.start()
    
    # 创建不同类型的任务
    print("\n📝 创建监控任务:")
    print("-" * 40)
    
    tasks = [
        ("task_critical_001", "SCRM数据同步", "critical", 30),
        ("task_high_001", "API性能测试", "high", 60),
        ("task_medium_001", "数据库备份", "medium", 120),
        ("task_low_001", "日志归档", "low", 300)
    ]
    
    for task_id, name, priority, est in tasks:
        guardian.start_task(task_id, name, priority, est)
        icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
        print(f"{icon} {name} (优先级: {priority}, 预估: {est}秒)")
    
    print("\n🔄 开始实时监控...")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    
    try:
        # 实时更新仪表板
        for i in range(6):
            time.sleep(10)  # 每10秒更新一次
            
            print(f"\n⏰ 第{i+1}次更新 ({datetime.now().strftime('%H:%M:%S')})")
            print(guardian.get_dashboard())
            
            # 模拟任务进度更新
            if i == 1:
                guardian.update_task("task_critical_001", progress=50)
                print("  更新: SCRM数据同步 进度 50%")
            elif i == 2:
                guardian.complete_task("task_critical_001", "同步完成")
                print("  完成: SCRM数据同步")
            elif i == 3:
                guardian.update_task("task_high_001", progress=75)
                guardian.complete_task("task_medium_001", "备份完成")
                print("  更新: API性能测试 进度 75%")
                print("  完成: 数据库备份")
            elif i == 4:
                guardian.complete_task("task_high_001", "测试完成")
                print("  完成: API性能测试")
            elif i == 5:
                guardian.complete_task("task_low_001", "归档完成")
                print("  完成: 日志归档")
                
    except KeyboardInterrupt:
        print("\n\n🛑 用户中断...")
    finally:
        guardian.stop()
        print("\n✅ 演示结束")
        print("最终统计:")
        print(guardian.get_dashboard())

if __name__ == "__main__":
    main()
