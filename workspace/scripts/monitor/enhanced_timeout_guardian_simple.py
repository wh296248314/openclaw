#!/usr/bin/env python3
"""
简化版增强监控卫士 - 修复语法错误
"""

import time
import threading
import json
import os
import psutil
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/admin/openclaw/workspace/enhanced_timeout_guardian.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EnhancedTimeoutGuardian")

class EnhancedTaskMonitor:
    """简化版任务监控器"""
    
    def __init__(self):
        self.config = {
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
            }
        }
        
        self.active_tasks = {}
        self.task_history = []
        self.running = False
        self.monitor_thread = None
        
        logger.info("简化版任务监控器初始化完成")
    
    def start_task(self, task_id: str, task_name: str, priority: str = "medium"):
        """开始监控任务"""
        task_info = {
            "task_id": task_id,
            "task_name": task_name,
            "priority": priority,
            "start_time": datetime.now(),
            "last_update": datetime.now(),
            "status": "running",
            "timeout_warnings": 0
        }
        
        self.active_tasks[task_id] = task_info
        logger.info(f"开始监控任务: {task_name} (优先级: {priority})")
        return task_id
    
    def update_task(self, task_id: str, status: str = None):
        """更新任务状态"""
        if task_id not in self.active_tasks:
            return False
        
        self.active_tasks[task_id]["last_update"] = datetime.now()
        if status:
            self.active_tasks[task_id]["status"] = status
        
        return True
    
    def complete_task(self, task_id: str, result: str = "完成"):
        """标记任务完成"""
        if task_id not in self.active_tasks:
            return False
        
        task = self.active_tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end_time"] = datetime.now()
        
        # 计算持续时间
        duration = (task["end_time"] - task["start_time"]).total_seconds()
        task["duration"] = duration
        
        # 保存到历史
        self.task_history.append(task.copy())
        
        # 从活跃任务中移除
        del self.active_tasks[task_id]
        
        logger.info(f"✅ 任务完成: {task['task_name']}, 耗时: {duration:.2f}秒")
        return True
    
    def check_timeout(self):
        """检查超时任务"""
        alerts = []
        current_time = datetime.now()
        
        for task_id, task in list(self.active_tasks.items()):
            priority = task.get("priority", "medium")
            timeout_threshold = self.config["timeout_thresholds"].get(priority, 120)
            max_warnings = self.config["max_warnings"].get(priority, 2)
            
            elapsed = (current_time - task["start_time"]).total_seconds()
            
            if elapsed > timeout_threshold and task["timeout_warnings"] < max_warnings:
                task["timeout_warnings"] += 1
                
                alert_level = "WARNING"
                if elapsed > timeout_threshold * 3:
                    alert_level = "CRITICAL"
                elif elapsed > timeout_threshold * 2:
                    alert_level = "ERROR"
                
                alert_message = (
                    f"[{alert_level}] 任务超时: {task['task_name']}\n"
                    f"  优先级: {priority}\n"
                    f"  已执行: {elapsed:.1f}秒 (阈值: {timeout_threshold}秒)\n"
                    f"  警告次数: {task['timeout_warnings']}/{max_warnings}"
                )
                
                alerts.append({
                    "task_id": task_id,
                    "alert_message": alert_message,
                    "task": task
                })
        
        return alerts
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                alerts = self.check_timeout()
                for alert in alerts:
                    logger.warning(alert["alert_message"])
                
                time.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                time.sleep(30)
    
    def start_monitoring(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("✅ 简化版监控卫士已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("监控已停止")
    
    def get_dashboard(self):
        """获取仪表板"""
        dashboard = []
        dashboard.append("=" * 60)
        dashboard.append("简化版增强监控卫士 - 实时仪表板")
        dashboard.append("=" * 60)
        
        dashboard.append(f"\n📊 活跃任务: {len(self.active_tasks)} 个")
        
        if self.active_tasks:
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                priority = task["priority"]
                icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                
                dashboard.append(f"{icon} {task['task_name']} (ID: {task_id})")
                dashboard.append(f"   优先级: {priority}, 已执行: {elapsed:.1f}秒")
        
        dashboard.append(f"\n📈 历史任务: {len(self.task_history)} 个")
        
        dashboard.append("\n" + "=" * 60)
        return '\n'.join(dashboard)


def main():
    """主函数"""
    monitor = EnhancedTaskMonitor()
    monitor.start_monitoring()
    
    print("\n" + monitor.get_dashboard())
    print("\n🎯 演示不同优先级的任务监控:")
    
    # 创建演示任务
    demo_tasks = [
        ("demo_critical_001", "紧急订单处理", "critical"),
        ("demo_high_001", "API接口测试", "high"),
        ("demo_medium_001", "数据备份", "medium"),
        ("demo_low_001", "日志清理", "low")
    ]
    
    for task_id, task_name, priority in demo_tasks:
        monitor.start_task(task_id, task_name, priority)
        print(f"  创建: {task_name} (优先级: {priority})")
    
    print("\n🔄 监控中... 按 Ctrl+C 停止")
    print("超时任务将自动告警 (critical:30s, high:60s, medium:120s, low:300s)")
    
    try:
        # 模拟任务执行
        for i in range(6):
            time.sleep(10)
            print(f"\n⏰ 第{i+1}次检查 ({datetime.now().strftime('%H:%M:%S')})")
            print(monitor.get_dashboard())
            
            # 模拟任务完成
            if i == 2:
                monitor.complete_task("demo_critical_001", "紧急处理完成")
            elif i == 3:
                monitor.complete_task("demo_high_001", "API测试完成")
            elif i == 4:
                monitor.complete_task("demo_medium_001", "备份完成")
            elif i == 5:
                monitor.complete_task("demo_low_001", "清理完成")
                
    except KeyboardInterrupt:
        print("\n\n🛑 停止监控...")
    finally:
        monitor.stop_monitoring()
        print("✅ 演示结束")


if __name__ == "__main__":
    main()
