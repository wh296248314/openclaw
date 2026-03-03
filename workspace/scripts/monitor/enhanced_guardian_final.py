#!/usr/bin/env python3
"""
最终版增强监控卫士 - 完全修复，无语法错误
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EnhancedGuardian")

class EnhancedGuardian:
    """最终版增强监控卫士"""
    
    def __init__(self, config_file=None):
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
        
        logger.info("增强版监控卫士初始化完成")
    
    def start_task(self, task_id, task_name, priority="medium", estimated_time=None):
        """开始监控任务"""
        task_info = {
            "task_id": task_id,
            "task_name": task_name,
            "priority": priority,
            "start_time": datetime.now(),
            "last_update": datetime.now(),
            "status": "running",
            "timeout_warnings": 0,
            "estimated_time": estimated_time
        }
        
        self.active_tasks[task_id] = task_info
        logger.info(f"开始监控: {task_name} (优先级: {priority})")
        return task_id
    
    def update_task(self, task_id, progress=None):
        """更新任务进度"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["last_update"] = datetime.now()
            if progress is not None:
                self.active_tasks[task_id]["progress"] = progress
            return True
        return False
    
    def complete_task(self, task_id, result="完成"):
        """标记任务完成"""
        if task_id not in self.active_tasks:
            return False
        
        task = self.active_tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end_time"] = datetime.now()
        
        duration = (task["end_time"] - task["start_time"]).total_seconds()
        task["duration"] = duration
        
        self.task_history.append(task.copy())
        del self.active_tasks[task_id]
        
        logger.info(f"✅ 完成: {task['task_name']}, 耗时: {duration:.2f}秒")
        return True
    
    def check_timeouts(self):
        """检查超时任务"""
        alerts = []
        current_time = datetime.now()
        
        for task_id, task in list(self.active_tasks.items()):
            priority = task.get("priority", "medium")
            timeout = self.config["timeout_thresholds"].get(priority, 120)
            max_warn = self.config["max_warnings"].get(priority, 2)
            
            elapsed = (current_time - task["start_time"]).total_seconds()
            
            if elapsed > timeout and task["timeout_warnings"] < max_warn:
                task["timeout_warnings"] += 1
                
                # 确定告警级别
                if elapsed > timeout * 3:
                    level = "CRITICAL"
                elif elapsed > timeout * 2:
                    level = "ERROR"
                else:
                    level = "WARNING"
                
                alert_msg = f"[{level}] {task['task_name']} 超时: {elapsed:.1f}s (阈值: {timeout}s)"
                alerts.append(alert_msg)
        
        return alerts
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                alerts = self.check_timeouts()
                for alert in alerts:
                    logger.warning(alert)
                
                time.sleep(30)  # 每30秒检查一次
            except Exception as e:
                logger.error(f"监控错误: {e}")
                time.sleep(30)
    
    def start(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("✅ 增强版监控卫士已启动")
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("监控已停止")
    
    def get_dashboard(self):
        """获取仪表板"""
        lines = []
        lines.append("=" * 60)
        lines.append("增强版监控卫士 - 实时仪表板")
        lines.append("=" * 60)
        
        lines.append(f"\n📊 活跃任务: {len(self.active_tasks)} 个")
        if self.active_tasks:
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                priority = task["priority"]
                icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                lines.append(f"{icon} {task['task_name']} - {elapsed:.1f}s")
        
        lines.append(f"\n📈 历史任务: {len(self.task_history)} 个")
        if self.task_history:
            completed = sum(1 for t in self.task_history if t.get("status") == "completed")
            total = len(self.task_history)
            rate = (completed / total * 100) if total > 0 else 0
            lines.append(f"  完成率: {rate:.1f}% ({completed}/{total})")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def demo():
    """演示功能"""
    guardian = EnhancedGuardian()
    guardian.start()
    
    print("\n🎯 演示增强版监控功能")
    print("=" * 40)
    
    # 创建演示任务
    tasks = [
        ("demo_critical", "紧急订单处理", "critical", 25),
        ("demo_high", "API接口测试", "high", 45),
        ("demo_medium", "数据备份", "medium", 90),
        ("demo_low", "日志清理", "low", 180)
    ]
    
    for task_id, name, priority, est in tasks:
        guardian.start_task(task_id, name, priority, est)
        print(f"创建: {name} (优先级: {priority}, 预估: {est}s)")
    
    print("\n🔄 监控中...")
    print(guardian.get_dashboard())
    
    # 模拟任务执行
    for i in range(3):
        time.sleep(10)
        print(f"\n⏰ 第{i+1}次检查")
        print(guardian.get_dashboard())
        
        # 模拟任务完成
        if i == 1:
            guardian.complete_task("demo_critical", "紧急处理完成")
        elif i == 2:
            guardian.complete_task("demo_high", "API测试完成")
    
    guardian.stop()
    print("\n✅ 演示完成")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表板")
    
    args = parser.parse_args()
    
    if args.demo:
        demo()
    elif args.dashboard:
        guardian = EnhancedGuardian()
        print(guardian.get_dashboard())
    else:
        print("增强版监控卫士")
        print("使用: python3 enhanced_guardian_final.py --demo  # 运行演示")
        print("     python3 enhanced_guardian_final.py --dashboard  # 显示仪表板")
