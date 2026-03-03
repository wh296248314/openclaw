#!/usr/bin/env python3
"""
智能超时监控卫士
监控任务执行时间，自动提醒超时任务
"""

import time
import threading
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TimeoutGuardian")

class TaskMonitor:
    """任务监控器"""
    
    def __init__(self, timeout_seconds: int = 60, max_updates: int = 3):
        """
        初始化任务监控器
        
        Args:
            timeout_seconds: 超时时间（秒）
            max_updates: 最大状态更新次数
        """
        self.timeout_seconds = timeout_seconds
        self.max_updates = max_updates
        self.active_tasks: Dict[str, Dict] = {}
        self.task_history: List[Dict] = []
        self.monitor_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 加载历史数据
        self.load_history()
    
    def start_task(self, task_id: str, task_name: str, description: str = "") -> str:
        """
        开始监控一个新任务
        
        Args:
            task_id: 任务ID
            task_name: 任务名称
            description: 任务描述
            
        Returns:
            任务ID
        """
        task_info = {
            "task_id": task_id,
            "task_name": task_name,
            "description": description,
            "start_time": datetime.now(),
            "last_update": datetime.now(),
            "status": "running",
            "update_count": 0,
            "estimated_completion": None,
            "timeout_warnings": 0
        }
        
        self.active_tasks[task_id] = task_info
        logger.info(f"开始监控任务: {task_name} (ID: {task_id})")
        
        # 保存到历史
        self.task_history.append({
            **task_info,
            "start_time": task_info["start_time"].isoformat()
        })
        self.save_history()
        
        return task_id
    
    def update_task(self, task_id: str, status: str = None, 
                   estimated_completion: str = None) -> bool:
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            estimated_completion: 预计完成时间
            
        Returns:
            是否成功更新
        """
        if task_id not in self.active_tasks:
            logger.warning(f"任务不存在: {task_id}")
            return False
        
        task = self.active_tasks[task_id]
        task["last_update"] = datetime.now()
        
        if status:
            task["status"] = status
        
        if estimated_completion:
            task["estimated_completion"] = estimated_completion
        
        task["update_count"] += 1
        
        logger.info(f"更新任务 {task['task_name']}: 状态={status}, 更新次数={task['update_count']}")
        return True
    
    def complete_task(self, task_id: str, result: str = "completed") -> bool:
        """
        标记任务完成
        
        Args:
            task_id: 任务ID
            result: 完成结果
            
        Returns:
            是否成功标记
        """
        if task_id not in self.active_tasks:
            logger.warning(f"任务不存在: {task_id}")
            return False
        
        task = self.active_tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end_time"] = datetime.now()
        task["duration"] = (task["end_time"] - task["start_time"]).total_seconds()
        
        # 更新历史记录
        for hist_task in self.task_history:
            if hist_task.get("task_id") == task_id and "end_time" not in hist_task:
                hist_task.update({
                    "status": "completed",
                    "result": result,
                    "end_time": task["end_time"].isoformat(),
                    "duration": task["duration"]
                })
        
        # 从活跃任务中移除
        del self.active_tasks[task_id]
        
        logger.info(f"任务完成: {task['task_name']}, 耗时: {task['duration']:.2f}秒")
        self.save_history()
        return True
    
    def check_timeouts(self):
        """检查所有任务是否超时"""
        now = datetime.now()
        timeout_tasks = []
        
        for task_id, task in list(self.active_tasks.items()):
            elapsed = (now - task["last_update"]).total_seconds()
            
            if elapsed > self.timeout_seconds:
                # 检查是否已达到最大更新次数
                if task["timeout_warnings"] < self.max_updates:
                    task["timeout_warnings"] += 1
                    timeout_tasks.append(task)
                    logger.warning(f"任务超时: {task['task_name']}, 已超时 {elapsed:.2f}秒")
        
        return timeout_tasks
    
    def get_timeout_alerts(self) -> List[Dict]:
        """
        获取超时提醒信息
        
        Returns:
            超时任务列表
        """
        timeout_tasks = self.check_timeouts()
        alerts = []
        
        for task in timeout_tasks:
            elapsed = (datetime.now() - task["last_update"]).total_seconds()
            alert = {
                "task_id": task["task_id"],
                "task_name": task["task_name"],
                "description": task.get("description", ""),
                "elapsed_seconds": elapsed,
                "timeout_warnings": task["timeout_warnings"],
                "max_warnings": self.max_updates,
                "status": task["status"],
                "estimated_completion": task.get("estimated_completion"),
                "alert_message": self._generate_alert_message(task, elapsed)
            }
            alerts.append(alert)
        
        return alerts
    
    def _generate_alert_message(self, task: Dict, elapsed: float) -> str:
        """生成提醒消息"""
        task_name = task["task_name"]
        elapsed_min = elapsed / 60
        
        if task["timeout_warnings"] == 1:
            return f"🚨 任务超时提醒 (第1次)\n任务: {task_name}\n已执行: {elapsed_min:.1f}分钟\n当前状态: {task['status']}\n预计完成: {task.get('estimated_completion', '未设置')}"
        elif task["timeout_warnings"] == 2:
            return f"⚠️ 任务超时提醒 (第2次)\n任务: {task_name}\n已执行: {elapsed_min:.1f}分钟\n请确认任务进度"
        else:
            return f"🔴 任务超时提醒 (第3次 - 最终)\n任务: {task_name}\n已执行: {elapsed_min:.1f}分钟\n需要立即关注！"
    
    def get_active_tasks(self) -> List[Dict]:
        """获取所有活跃任务"""
        return list(self.active_tasks.values())
    
    def get_task_stats(self) -> Dict:
        """获取任务统计信息"""
        now = datetime.now()
        stats = {
            "total_active": len(self.active_tasks),
            "total_timeout": len(self.check_timeouts()),
            "total_completed": len([t for t in self.task_history if t.get("status") == "completed"]),
            "avg_duration": 0,
            "timeout_rate": 0
        }
        
        # 计算平均耗时
        completed_tasks = [t for t in self.task_history if t.get("status") == "completed" and "duration" in t]
        if completed_tasks:
            stats["avg_duration"] = sum(t["duration"] for t in completed_tasks) / len(completed_tasks)
        
        # 计算超时率
        total_tasks = len(self.task_history)
        if total_tasks > 0:
            timeout_tasks = len([t for t in self.task_history if "timeout_warnings" in t and t["timeout_warnings"] > 0])
            stats["timeout_rate"] = (timeout_tasks / total_tasks) * 100
        
        return stats
    
    def save_history(self):
        """保存历史数据到文件"""
        try:
            history_file = "timeout_guardian_history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.task_history, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"历史数据已保存到: {history_file}")
        except Exception as e:
            logger.error(f"保存历史数据失败: {e}")
    
    def load_history(self):
        """从文件加载历史数据"""
        try:
            history_file = "timeout_guardian_history.json"
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.task_history = json.load(f)
                logger.info(f"从 {history_file} 加载了 {len(self.task_history)} 条历史记录")
        except Exception as e:
            logger.error(f"加载历史数据失败: {e}")
            self.task_history = []
    
    def start_monitoring(self, interval_seconds: int = 30):
        """启动监控线程"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            logger.warning("监控线程已在运行")
            return
        
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    alerts = self.get_timeout_alerts()
                    if alerts:
                        logger.info(f"发现 {len(alerts)} 个超时任务")
                        # 这里可以添加发送提醒的逻辑
                        for alert in alerts:
                            logger.warning(f"超时提醒: {alert['alert_message']}")
                    
                    time.sleep(interval_seconds)
                except Exception as e:
                    logger.error(f"监控循环错误: {e}")
                    time.sleep(interval_seconds)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info(f"监控线程已启动，检查间隔: {interval_seconds}秒")
    
    def stop_monitoring(self):
        """停止监控线程"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            logger.info("监控线程已停止")


class TimeoutGuardian:
    """智能超时监控卫士主类"""
    
    def __init__(self):
        self.monitor = TaskMonitor(timeout_seconds=60, max_updates=3)
        self.guardian_stats = {
            "start_time": datetime.now(),
            "total_alerts_sent": 0,
            "tasks_prevented": 0
        }
    
    def start(self):
        """启动卫士"""
        logger.info("🚀 启动智能超时监控卫士...")
        self.monitor.start_monitoring(interval_seconds=30)
        
        # 启动一个示例任务
        self.demo_task()
        
        logger.info("✅ 智能超时监控卫士已启动")
        logger.info(f"超时阈值: {self.monitor.timeout_seconds}秒")
        logger.info(f"最大提醒次数: {self.monitor.max_updates}")
    
    def demo_task(self):
        """演示任务"""
        task_id = self.monitor.start_task(
            task_id="demo_001",
            task_name="演示任务 - 数据处理",
            description="这是一个演示任务，用于展示超时监控功能"
        )
        
        # 模拟长时间运行的任务
        def run_demo_task():
            time.sleep(75)  # 75秒，会触发超时
            self.monitor.complete_task(task_id, "演示完成")
        
        threading.Thread(target=run_demo_task, daemon=True).start()
    
    def get_dashboard(self) -> str:
        """获取监控仪表板"""
        stats = self.monitor.get_task_stats()
        active_tasks = self.monitor.get_active_tasks()
        alerts = self.monitor.get_timeout_alerts()
        
        dashboard = f"""
╔══════════════════════════════════════════════════╗
║          🛡️ 智能超时监控卫士 - 仪表板           ║
╠══════════════════════════════════════════════════╣
║ 📊 统计信息                                      ║
║   • 活跃任务: {stats['total_active']}个          ║
║   • 超时任务: {stats['total_timeout']}个         ║
║   • 已完成: {stats['total_completed']}个         ║
║   • 平均耗时: {stats['avg_duration']:.2f}秒     ║
║   • 超时率: {stats['timeout_rate']:.1f}%        ║
╠══════════════════════════════════════════════════╣
║ ⚠️ 超时提醒 ({len(alerts)}个)                    ║
"""
        
        for i, alert in enumerate(alerts, 1):
            dashboard += f"║   {i}. {alert['task_name']} - {alert['elapsed_seconds']:.1f}秒\n"
        
        dashboard += "╠══════════════════════════════════════════════════╣\n"
        dashboard += "║ 🔄 活跃任务 ({len(active_tasks)}个)                    ║\n"
        
        for i, task in enumerate(active_tasks, 1):
            elapsed = (datetime.now() - task["start_time"]).total_seconds()
            dashboard += f"║   {i}. {task['task_name']} - {elapsed:.1f}秒\n"
        
        dashboard += "╚══════════════════════════════════════════════════╝\n"
        
        return dashboard
    
    def stop(self):
        """停止卫士"""
        logger.info("🛑 停止智能超时监控卫士...")
        self.monitor.stop_monitoring()
        logger.info("✅ 智能超时监控卫士已停止")


def main():
    """主函数"""
    guardian = TimeoutGuardian()
    
    try:
        guardian.start()
        
        # 显示仪表板
        print("\n" + guardian.get_dashboard())
        
        # 保持运行
        print("监控中... 按 Ctrl+C 停止")
        while True:
            time.sleep(60)
            # 每分钟更新一次仪表板
            print("\n" + guardian.get_dashboard())
            
    except KeyboardInterrupt:
        print("\n接收到停止信号...")
    finally:
        guardian.stop()


if __name__ == "__main__":
    main()