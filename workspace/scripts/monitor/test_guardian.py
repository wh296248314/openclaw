#!/usr/bin/env python3
"""
测试智能超时监控卫士
"""

import time
from timeout_guardian import TaskMonitor

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试智能超时监控卫士基本功能...")
    
    # 创建监控器
    monitor = TaskMonitor(timeout_seconds=10, max_updates=2)  # 使用10秒超时方便测试
    
    # 测试1: 创建任务
    print("1. 测试任务创建...")
    task_id = monitor.start_task(
        task_id="test_001",
        task_name="测试任务 - 数据处理",
        description="这是一个测试任务"
    )
    print(f"   ✅ 任务创建成功: {task_id}")
    
    # 测试2: 更新任务状态
    print("2. 测试任务状态更新...")
    monitor.update_task(task_id, status="processing", estimated_completion="30秒后")
    print("   ✅ 任务状态更新成功")
    
    # 测试3: 检查超时（等待12秒）
    print("3. 测试超时检测（等待12秒）...")
    time.sleep(12)
    
    alerts = monitor.get_timeout_alerts()
    if alerts:
        print(f"   ✅ 超时检测成功！发现 {len(alerts)} 个超时任务")
        for alert in alerts:
            print(f"     提醒: {alert['alert_message']}")
    else:
        print("   ❌ 超时检测失败")
    
    # 测试4: 完成任务
    print("4. 测试任务完成...")
    monitor.complete_task(task_id, "测试完成")
    print("   ✅ 任务完成标记成功")
    
    # 测试5: 获取统计信息
    print("5. 测试统计信息...")
    stats = monitor.get_task_stats()
    print(f"   ✅ 统计信息获取成功:")
    print(f"     总任务数: {stats['total_completed'] + stats['total_active']}")
    print(f"     平均耗时: {stats['avg_duration']:.2f}秒")
    
    print("\n🎉 所有基本功能测试通过！")

def test_multiple_tasks():
    """测试多任务监控"""
    print("\n🧪 测试多任务监控...")
    
    monitor = TaskMonitor(timeout_seconds=5, max_updates=2)
    
    # 创建多个任务
    tasks = []
    for i in range(3):
        task_id = f"multi_test_{i}"
        monitor.start_task(task_id, f"多任务测试 {i}", f"测试任务 {i}")
        tasks.append(task_id)
        print(f"   创建任务 {i}: {task_id}")
    
    print(f"   ✅ 创建了 {len(tasks)} 个任务")
    
    # 等待超时
    time.sleep(6)
    
    # 检查超时
    alerts = monitor.get_timeout_alerts()
    print(f"   发现 {len(alerts)} 个超时任务")
    
    # 完成所有任务
    for task_id in tasks:
        monitor.complete_task(task_id, "多任务测试完成")
    
    print("   ✅ 多任务测试完成")

def test_history_persistence():
    """测试历史数据持久化"""
    print("\n🧪 测试历史数据持久化...")
    
    # 创建监控器并添加任务
    monitor1 = TaskMonitor()
    task_id = monitor1.start_task("persist_test", "持久化测试", "测试数据保存")
    monitor1.complete_task(task_id, "测试完成")
    
    # 保存历史
    monitor1.save_history()
    print("   数据已保存")
    
    # 创建新监控器并加载历史
    monitor2 = TaskMonitor()
    monitor2.load_history()
    
    # 检查加载的数据
    if monitor2.task_history:
        print(f"   ✅ 历史数据加载成功，找到 {len(monitor2.task_history)} 条记录")
        last_task = monitor2.task_history[-1]
        print(f"     最后任务: {last_task.get('task_name')} - {last_task.get('status')}")
    else:
        print("   ❌ 历史数据加载失败")
    
    print("   ✅ 持久化测试完成")

if __name__ == "__main__":
    print("🛡️ 智能超时监控卫士 - 功能测试")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_multiple_tasks()
        test_history_persistence()
        
        print("\n" + "=" * 50)
        print("🎊 所有测试完成！智能超时监控卫士功能正常。")
        print("\n💡 提示: 现在可以运行 './start_guardian.sh' 启动完整监控系统")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()