#!/usr/bin/env python3
"""
智能超时监控卫士 - 命令行界面
"""

import sys
import time
import argparse
from timeout_guardian import TimeoutGuardian, TaskMonitor
from datetime import datetime

def show_banner():
    """显示横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║      🛡️ 智能超时监控卫士 - 命令行界面 v1.0         ║
    ║          随时守护你的任务，永不超时！               ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def start_monitoring(args):
    """启动监控"""
    guardian = TimeoutGuardian()
    
    print("🚀 启动智能超时监控卫士...")
    guardian.start()
    
    try:
        while True:
            print("\n" + guardian.get_dashboard())
            print("\n命令: [s]状态 [q]退出 [t]测试任务")
            cmd = input("> ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 's':
                print(guardian.get_dashboard())
            elif cmd == 't':
                # 创建测试任务
                task_id = f"test_{int(time.time())}"
                guardian.monitor.start_task(
                    task_id=task_id,
                    task_name="手动测试任务",
                    description="用户手动创建的测试任务"
                )
                print(f"✅ 已创建测试任务: {task_id}")
            elif cmd == 'h':
                show_help()
            else:
                print("❓ 未知命令，输入 'h' 查看帮助")
                
    except KeyboardInterrupt:
        print("\n\n接收到停止信号...")
    finally:
        guardian.stop()
        print("✅ 监控已停止")

def show_stats(args):
    """显示统计信息"""
    monitor = TaskMonitor()
    monitor.load_history()
    
    stats = monitor.get_task_stats()
    print("\n📊 任务统计信息:")
    print(f"   活跃任务: {stats['total_active']}个")
    print(f"   超时任务: {stats['total_timeout']}个")
    print(f"   已完成: {stats['total_completed']}个")
    print(f"   平均耗时: {stats['avg_duration']:.2f}秒")
    print(f"   超时率: {stats['timeout_rate']:.1f}%")
    
    # 显示最近任务
    print("\n🕐 最近任务:")
    recent_tasks = monitor.task_history[-5:] if monitor.task_history else []
    for task in reversed(recent_tasks):
        task_name = task.get('task_name', '未知任务')
        status = task.get('status', 'unknown')
        start_time = task.get('start_time', '未知时间')
        
        status_icon = "✅" if status == "completed" else "🔄" if status == "running" else "❓"
        print(f"   {status_icon} {task_name} - {status} ({start_time})")

def create_task(args):
    """创建新任务"""
    monitor = TaskMonitor()
    
    task_name = input("任务名称: ").strip()
    if not task_name:
        print("❌ 任务名称不能为空")
        return
    
    description = input("任务描述 (可选): ").strip()
    
    task_id = f"manual_{int(time.time())}"
    monitor.start_task(task_id, task_name, description)
    
    print(f"✅ 任务已创建:")
    print(f"   ID: {task_id}")
    print(f"   名称: {task_name}")
    print(f"   描述: {description}")
    print(f"   开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def show_help():
    """显示帮助信息"""
    help_text = """
可用命令:
  start       启动监控卫士
  stats       显示统计信息
  task        创建新任务
  help        显示此帮助信息
  version     显示版本信息

监控设置:
  • 超时阈值: 60秒
  • 最大提醒次数: 3次
  • 检查间隔: 30秒

在监控模式下:
  s - 显示状态仪表板
  t - 创建测试任务
  q - 退出监控
  h - 显示帮助
    """
    print(help_text)

def show_version():
    """显示版本信息"""
    version_info = """
智能超时监控卫士 v1.0
作者: 皮休 (Pixiu)
创建时间: 2026-03-03
功能: 任务超时监控与自动提醒
配置: 60秒超时阈值，最多3次提醒
    """
    print(version_info)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='智能超时监控卫士')
    parser.add_argument('command', nargs='?', default='start', 
                       help='命令: start, stats, task, help, version')
    
    args = parser.parse_args()
    
    show_banner()
    
    if args.command == 'start':
        start_monitoring(args)
    elif args.command == 'stats':
        show_stats(args)
    elif args.command == 'task':
        create_task(args)
    elif args.command == 'help':
        show_help()
    elif args.command == 'version':
        show_version()
    else:
        print(f"❌ 未知命令: {args.command}")
        print("使用 'help' 查看可用命令")

if __name__ == "__main__":
    main()