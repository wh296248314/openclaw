#!/usr/bin/env python3
"""
监控卫士简化修复版 - 先解决核心问题
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
        logging.FileHandler('/home/admin/openclaw/workspace/logs/guardian_simple.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GuardianSimple")

# 单例实例
_instance = None
_instance_lock = threading.Lock()

def get_guardian():
    """获取单例实例"""
    global _instance
    with _instance_lock:
        if _instance is None:
            _instance = SimpleGuardian()
        return _instance

class SimpleGuardian:
    """简化版监控卫士（只修复核心问题）"""
    
    def __init__(self):
        self.data_file = "/home/admin/openclaw/workspace/data/monitor/simple_tasks.json"
        self.active_tasks = self._load_tasks()
        self.running = False
        self.thread = None
        
        logger.info("简化版监控卫士初始化完成")
        logger.info(f"加载了 {len(self.active_tasks)} 个任务")
    
    def _load_tasks(self):
        """加载任务数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_tasks(self):
        """保存任务数据"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.active_tasks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存任务失败: {e}")
            return False
    
    def start_task(self, task_id, task_name, priority="medium"):
        """开始监控任务"""
        if task_id in self.active_tasks:
            logger.warning(f"任务已存在: {task_id}")
            return False
        
        self.active_tasks[task_id] = {
            "name": task_name,
            "priority": priority,
            "start_time": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "status": "running"
        }
        
        self._save_tasks()
        logger.info(f"开始监控: {task_name}")
        return True
    
    def update_task(self, task_id, progress=None):
        """更新任务"""
        if task_id not in self.active_tasks:
            return False
        
        self.active_tasks[task_id]["last_update"] = datetime.now().isoformat()
        if progress is not None:
            self.active_tasks[task_id]["progress"] = progress
        
        self._save_tasks()
        return True
    
    def complete_task(self, task_id, result="完成"):
        """完成任务"""
        if task_id not in self.active_tasks:
            return False
        
        task = self.active_tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end_time"] = datetime.now().isoformat()
        
        self._save_tasks()
        logger.info(f"完成: {task['name']}")
        return True
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                current_time = datetime.now()
                alerts = []
                
                for task_id, task in list(self.active_tasks.items()):
                    if task.get("status") != "running":
                        continue
                    
                    # 检查超时
                    start_time = datetime.fromisoformat(task["start_time"])
                    elapsed = (current_time - start_time).total_seconds()
                    
                    # 简单超时检查
                    timeout = 120  # 默认2分钟
                    if elapsed > timeout:
                        alerts.append(f"超时: {task['name']} ({elapsed:.1f}s)")
                
                # 处理告警
                for alert in alerts:
                    logger.warning(alert)
                
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                time.sleep(30)
    
    def start(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()
        logger.info("监控已启动")
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("监控已停止")
    
    def get_status(self):
        """获取状态"""
        lines = []
        lines.append("=" * 50)
        lines.append("简化版监控卫士状态")
        lines.append("=" * 50)
        
        running_tasks = [t for t in self.active_tasks.values() if t.get("status") == "running"]
        completed_tasks = [t for t in self.active_tasks.values() if t.get("status") == "completed"]
        
        lines.append(f"运行中: {len(running_tasks)} 个")
        lines.append(f"已完成: {len(completed_tasks)} 个")
        
        if running_tasks:
            lines.append("\n运行中任务:")
            for task in running_tasks:
                start_time = datetime.fromisoformat(task["start_time"])
                elapsed = (datetime.now() - start_time).total_seconds()
                lines.append(f"  • {task['name']} ({elapsed:.1f}s)")
        
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--dashboard", action="store_true", help="显示状态")
    parser.add_argument("--start", help="启动任务，格式: id:名称:优先级")
    parser.add_argument("--complete", help="完成任务，格式: id:结果")
    
    args = parser.parse_args()
    
    guardian = get_guardian()
    
    if args.start:
        task_id, name, priority = args.start.split(":")
        guardian.start_task(task_id, name, priority)
        print(f"✅ 任务启动: {name}")
    
    elif args.complete:
        task_id, result = args.complete.split(":")
        guardian.complete_task(task_id, result)
        print(f"✅ 任务完成: {task_id}")
    
    elif args.dashboard:
        print(guardian.get_status())
    
    else:
        guardian.start()
        try:
            print(guardian.get_status())
            print("\n监控中...按Ctrl+C停止")
            while True:
                time.sleep(60)
                print("\n" + guardian.get_status())
        except KeyboardInterrupt:
            print("\n停止中...")
        finally:
            guardian.stop()

if __name__ == "__main__":
    main()
