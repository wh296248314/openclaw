#!/usr/bin/env python3
"""
监控卫士最终修复版 - 最小可用版本
只解决核心问题，代码干净无错误
"""

import time
import threading
import json
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/admin/openclaw/workspace/logs/guardian_final.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GuardianFinal")

# 单例实例
_instance = None
_lock = threading.Lock()

def get_guardian():
    """获取单例实例"""
    global _instance
    with _lock:
        if _instance is None:
            _instance = Guardian()
        return _instance

class Guardian:
    """监控卫士最终修复版"""
    
    def __init__(self):
        self.data_file = "/home/admin/openclaw/workspace/data/guardian_tasks.json"
        self.tasks = self._load_tasks()
        self.running = False
        self.thread = None
        
        logger.info("监控卫士初始化完成")
        logger.info(f"加载了 {len(self.tasks)} 个任务")
    
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
                json.dump(self.tasks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False
    
    def start_task(self, task_id, name, priority="medium"):
        """开始任务"""
        if task_id in self.tasks:
            logger.warning(f"任务已存在: {task_id}")
            return False
        
        self.tasks[task_id] = {
            "name": name,
            "priority": priority,
            "start": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "status": "running",
            "progress": 0
        }
        
        self._save_tasks()
        logger.info(f"开始监控: {name}")
        return True
    
    def update_task(self, task_id, progress):
        """更新任务"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id]["last_update"] = datetime.now().isoformat()
        self.tasks[task_id]["progress"] = progress
        self._save_tasks()
        return True
    
    def complete_task(self, task_id, result="完成"):
        """完成任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end"] = datetime.now().isoformat()
        
        self._save_tasks()
        logger.info(f"完成: {task['name']}")
        return True
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                now = datetime.now()
                for task_id, task in list(self.tasks.items()):
                    if task.get("status") != "running":
                        continue
                    
                    # 检查超时（简单版）
                    start = datetime.fromisoformat(task["start"])
                    elapsed = (now - start).total_seconds()
                    
                    # 超时阈值
                    timeout = 120  # 默认2分钟
                    if elapsed > timeout:
                        logger.warning(f"超时: {task['name']} ({elapsed:.1f}s)")
                
                time.sleep(30)
            except Exception as e:
                logger.error(f"监控错误: {e}")
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
        lines.append("监控卫士最终修复版 - 状态")
        lines.append("=" * 50)
        
        running = [t for t in self.tasks.values() if t.get("status") == "running"]
        completed = [t for t in self.tasks.values() if t.get("status") == "completed"]
        
        lines.append(f"运行中: {len(running)} 个")
        lines.append(f"已完成: {len(completed)} 个")
        
        if running:
            lines.append("\n运行中任务:")
            now = datetime.now()
            for task in running:
                start = datetime.fromisoformat(task["start"])
                elapsed = (now - start).total_seconds()
                lines.append(f"  • {task['name']} ({elapsed:.1f}s, 进度: {task.get('progress', 0)}%)")
        
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--start", nargs=3, metavar=("ID", "NAME", "PRIORITY"), help="启动任务")
    parser.add_argument("--update", nargs=2, metavar=("ID", "PROGRESS"), help="更新任务")
    parser.add_argument("--complete", nargs=2, metavar=("ID", "RESULT"), help="完成任务")
    
    args = parser.parse_args()
    
    guardian = get_guardian()
    
    if args.status:
        print(guardian.get_status())
    
    elif args.start:
        task_id, name, priority = args.start
        if guardian.start_task(task_id, name, priority):
            print(f"✅ 任务启动: {name}")
        else:
            print("❌ 任务启动失败")
    
    elif args.update:
        task_id, progress = args.update
        if guardian.update_task(task_id, int(progress)):
            print(f"✅ 任务更新: {task_id} → {progress}%")
        else:
            print("❌ 任务更新失败")
    
    elif args.complete:
        task_id, result = args.complete
        if guardian.complete_task(task_id, result):
            print(f"✅ 任务完成: {task_id}")
        else:
            print("❌ 任务完成失败")
    
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