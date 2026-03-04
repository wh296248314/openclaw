#!/usr/bin/env python3
"""
监控卫士增强版 - 包含改进功能
1. 任务清理功能（自动清理已完成或过期的任务）
2. 任务优先级排序显示
3. 任务搜索和过滤功能
4. 可配置超时检测机制
"""

import time
import threading
import json
import os
import re
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/admin/openclaw/workspace/logs/guardian_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GuardianEnhanced")

# 单例实例
_instance = None
_lock = threading.Lock()

def get_guardian():
    """获取单例实例"""
    global _instance
    with _lock:
        if _instance is None:
            _instance = EnhancedGuardian()
        return _instance

class EnhancedGuardian:
    """监控卫士增强版"""
    
    def __init__(self):
        self.data_file = "/home/admin/openclaw/workspace/data/guardian_tasks.json"
        self.config_file = "/home/admin/openclaw/workspace/configs/guardian_config.json"
        self.tasks: Dict[str, Dict] = self._load_tasks()
        self.config = self._load_config()
        self.running = False
        self.thread = None
        
        logger.info("监控卫士增强版初始化完成")
        logger.info(f"加载了 {len(self.tasks)} 个任务")
        logger.info(f"配置: 超时={self.config['timeout_seconds']}秒, 保留天数={self.config['keep_completed_days']}")
    
    def _load_tasks(self) -> Dict:
        """加载任务数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载任务失败: {e}")
        return {}
    
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "timeout_seconds": 120,  # 默认2分钟
            "keep_completed_days": 7,  # 保留7天
            "auto_cleanup": True,  # 自动清理
            "priority_order": ["critical", "high", "medium", "low"]  # 优先级顺序
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
        
        return default_config
    
    def _save_tasks(self) -> bool:
        """保存任务数据"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False
    
    def _save_config(self) -> bool:
        """保存配置"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def start_task(self, task_id: str, name: str, priority: str = "medium") -> bool:
        """开始任务"""
        if task_id in self.tasks:
            logger.warning(f"任务已存在: {task_id}")
            return False
        
        if priority not in self.config["priority_order"]:
            priority = "medium"
        
        self.tasks[task_id] = {
            "name": name,
            "priority": priority,
            "start": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "status": "running",
            "progress": 0,
            "created": datetime.now().isoformat()
        }
        
        self._save_tasks()
        logger.info(f"开始监控: {name} (优先级: {priority})")
        return True
    
    def update_task(self, task_id: str, progress: int) -> bool:
        """更新任务"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id]["last_update"] = datetime.now().isoformat()
        self.tasks[task_id]["progress"] = progress
        self._save_tasks()
        return True
    
    def complete_task(self, task_id: str, result: str = "完成") -> bool:
        """完成任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task["status"] = "completed"
        task["result"] = result
        task["end"] = datetime.now().isoformat()
        task["completed"] = datetime.now().isoformat()
        
        self._save_tasks()
        logger.info(f"完成: {task['name']} - {result}")
        return True
    
    def search_tasks(self, query: str) -> List[Dict]:
        """搜索任务"""
        results = []
        query_lower = query.lower()
        
        for task_id, task in self.tasks.items():
            # 搜索任务ID
            if query_lower in task_id.lower():
                results.append({"id": task_id, **task})
                continue
            
            # 搜索任务名称
            if query_lower in task.get("name", "").lower():
                results.append({"id": task_id, **task})
                continue
            
            # 搜索任务结果
            if "result" in task and query_lower in task["result"].lower():
                results.append({"id": task_id, **task})
                continue
        
        return results
    
    def filter_tasks(self, **filters) -> List[Dict]:
        """过滤任务"""
        results = []
        
        for task_id, task in self.tasks.items():
            match = True
            
            for key, value in filters.items():
                if key == "status":
                    if task.get("status") != value:
                        match = False
                        break
                elif key == "priority":
                    if task.get("priority") != value:
                        match = False
                        break
                elif key == "min_progress":
                    if task.get("progress", 0) < value:
                        match = False
                        break
                elif key == "max_progress":
                    if task.get("progress", 0) > value:
                        match = False
                        break
                elif key == "days_old":
                    if "created" in task:
                        created = datetime.fromisoformat(task["created"])
                        days_old = (datetime.now() - created).days
                        if days_old > value:
                            match = False
                            break
            
            if match:
                results.append({"id": task_id, **task})
        
        return results
    
    def cleanup_tasks(self, force: bool = False) -> Dict[str, int]:
        """清理任务"""
        if not self.config["auto_cleanup"] and not force:
            return {"skipped": 0, "removed": 0}
        
        removed = 0
        now = datetime.now()
        keep_days = self.config["keep_completed_days"]
        
        tasks_to_remove = []
        
        for task_id, task in self.tasks.items():
            # 清理已完成且过期的任务
            if task.get("status") == "completed":
                # 检查完成时间（优先使用completed字段，其次使用end字段）
                completed_time = None
                if "completed" in task:
                    completed_time = datetime.fromisoformat(task["completed"])
                elif "end" in task:
                    completed_time = datetime.fromisoformat(task["end"])
                
                if completed_time:
                    days_since_completion = (now - completed_time).days
                    
                    if days_since_completion > keep_days:
                        tasks_to_remove.append(task_id)
                        removed += 1
        
        # 移除任务
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
        
        if removed > 0:
            self._save_tasks()
            logger.info(f"清理了 {removed} 个已完成且超过{keep_days}天的任务")
        
        return {"skipped": len(tasks_to_remove) - removed, "removed": removed}
    
    def update_config(self, **kwargs) -> bool:
        """更新配置"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self._save_config()
        logger.info(f"配置已更新: {kwargs}")
        return True
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                now = datetime.now()
                timeout_seconds = self.config["timeout_seconds"]
                
                for task_id, task in list(self.tasks.items()):
                    if task.get("status") != "running":
                        continue
                    
                    # 检查超时
                    start = datetime.fromisoformat(task["start"])
                    elapsed = (now - start).total_seconds()
                    
                    if elapsed > timeout_seconds:
                        logger.warning(f"超时: {task['name']} ({elapsed:.1f}s > {timeout_seconds}s)")
                        # 可以在这里添加超时处理逻辑，如自动标记为失败
                
                # 自动清理
                if self.config["auto_cleanup"]:
                    self.cleanup_tasks()
                
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
    
    def get_status(self, sort_by_priority: bool = True) -> str:
        """获取状态（按优先级排序）"""
        lines = []
        lines.append("=" * 60)
        lines.append("监控卫士增强版 - 状态")
        lines.append("=" * 60)
        
        running = [{"id": tid, **t} for tid, t in self.tasks.items() if t.get("status") == "running"]
        completed = [{"id": tid, **t} for tid, t in self.tasks.items() if t.get("status") == "completed"]
        
        lines.append(f"运行中: {len(running)} 个")
        lines.append(f"已完成: {len(completed)} 个")
        lines.append(f"配置: 超时={self.config['timeout_seconds']}秒, 保留={self.config['keep_completed_days']}天")
        
        if running:
            # 按优先级排序
            if sort_by_priority:
                priority_order = self.config["priority_order"]
                running.sort(key=lambda x: priority_order.index(x.get("priority", "medium")) 
                            if x.get("priority") in priority_order else len(priority_order))
            
            lines.append("\n运行中任务 (按优先级排序):")
            now = datetime.now()
            for task in running:
                start = datetime.fromisoformat(task["start"])
                elapsed = (now - start).total_seconds()
                priority = task.get("priority", "medium")
                lines.append(f"  • [{priority.upper():8}] {task['name']}")
                lines.append(f"     进度: {task.get('progress', 0)}%, 运行: {elapsed:.1f}s, ID: {task['id']}")
        
        if completed:
            lines.append(f"\n已完成任务 (最近{self.config['keep_completed_days']}天):")
            now = datetime.now()
            recent_completed = []
            
            for task in completed:
                if "completed" in task:
                    completed_time = datetime.fromisoformat(task["completed"])
                    days_old = (now - completed_time).days
                    if days_old <= self.config["keep_completed_days"]:
                        recent_completed.append(task)
            
            if recent_completed:
                for task in recent_completed[-5:]:  # 显示最近5个
                    completed_time = datetime.fromisoformat(task["completed"])
                    days_ago = (now - completed_time).days
                    hours_ago = (now - completed_time).seconds // 3600
                    
                    if days_ago > 0:
                        time_str = f"{days_ago}天前"
                    elif hours_ago > 0:
                        time_str = f"{hours_ago}小时前"
                    else:
                        time_str = "刚刚"
                    
                    lines.append(f"  • {task['name']} - {task.get('result', '完成')} ({time_str})")
            else:
                lines.append("  (无最近完成的任务)")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
    
    def get_tasks_by_priority(self) -> Dict[str, List[Dict]]:
        """按优先级分组获取任务"""
        grouped = {priority: [] for priority in self.config["priority_order"]}
        grouped["other"] = []
        
        for task_id, task in self.tasks.items():
            priority = task.get("priority", "medium")
            if priority in grouped:
                grouped[priority].append({"id": task_id, **task})
            else:
                grouped["other"].append({"id": task_id, **task})
        
        return grouped

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="监控卫士增强版")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--start", nargs=3, metavar=("ID", "NAME", "PRIORITY"), help="启动任务")
    parser.add_argument("--update", nargs=2, metavar=("ID", "PROGRESS"), help="更新任务")
    parser.add_argument("--complete", nargs=2, metavar=("ID", "RESULT"), help="完成任务")
    parser.add_argument("--search", metavar="QUERY", help="搜索任务")
    parser.add_argument("--filter", metavar="FILTER", help="过滤任务 (格式: status=running,priority=high)")
    parser.add_argument("--cleanup", action="store_true", help="清理已完成且过期的任务")
    parser.add_argument("--config", metavar="KEY=VALUE", help="更新配置 (格式: timeout_seconds=300)")
    parser.add_argument("--list-priority", action="store_true", help="按优先级列出任务")
    
    args = parser.parse_args()
    
    guardian = get_guardian()
    
    if args.status:
        print(guardian.get_status())
    
    elif args.start:
        task_id, name, priority = args.start
        if guardian.start_task(task_id, name, priority):
            print(f"✅ 任务启动: {name} (优先级: {priority})")
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
    
    elif args.search:
        results = guardian.search_tasks(args.search)
        if results:
            print(f"🔍 找到 {len(results)} 个匹配任务:")
            for task in results:
                print(f"  • {task['name']} (ID: {task['id']}, 状态: {task.get('status', 'unknown')})")
        else:
            print("🔍 未找到匹配任务")
    
    elif args.filter:
        filters = {}
        for filter_str in args.filter.split(","):
            if "=" in filter_str:
                key, value = filter_str.split("=", 1)
                if key in ["min_progress", "max_progress", "days_old"]:
                    filters[key] = int(value)
                else:
                    filters[key] = value
        
        results = guardian.filter_tasks(**filters)
        if results:
            print(f"🔍 找到 {len(results)} 个匹配任务:")
            for task in results:
                print(f"  • {task['name']} (ID: {task['id']}, 状态: {task.get('status', 'unknown')})")
        else:
            print("🔍 未找到匹配任务")
    
    elif args.cleanup:
        result = guardian.cleanup_tasks(force=True)
        print(f"🧹 清理完成: 移除了 {result['removed']} 个任务, 跳过了 {result['skipped']} 个")
    
    elif args.config:
        if "=" in args.config:
            key, value = args.config.split("=", 1)
            # 尝试转换数值
            if value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                value = float(value)
            elif value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            
            if guardian.update_config(**{key: value}):
                print(f"⚙️ 配置已更新: {key}={value}")
            else:
                print("❌ 配置更新失败")
    
    elif args.list_priority:
        grouped = guardian.get_tasks_by_priority()
        print("📊 按优先级分组任务:")
        for priority, tasks in grouped.items():
            if tasks:
                print(f"\n[{priority.upper()}]: {len(tasks)} 个任务")
                for task in tasks:
                    status = task.get("status", "unknown")
                    progress = task.get("progress", 0)
                    print(f"  • {task['name']} (状态: {status}, 进度: {progress}%)")
    
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