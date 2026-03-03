#!/usr/bin/env python3
"""
完整版增强监控卫士 - 修复所有语法错误
"""

import time
import threading
import json
import os
import sys
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
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
    """增强版任务监控器"""
    
    def __init__(self, config_file: str = None):
        # 默认配置
        self.config = {
            "timeout_thresholds": {
                "critical": 30,
                "high": 60,
                "medium": 120,
                "low": 300
            },
            "check_intervals": {
                "critical": 10,
                "high": 30,
                "medium": 60,
                "low": 120
            },
            "max_warnings": {
                "critical": 5,
                "high": 3,
                "medium": 2,
                "low": 1
            },
            "notification_channels": ["log", "desktop"],
            "enable_resource_monitoring": True,
            "data_retention_days": 30
        }
        
        # 加载自定义配置
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.task_history: List[Dict] = []
        self.monitor_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 加载历史数据
        self.load_history()
        
        logger.info("增强版任务监控器初始化完成")
    
    def load_config(self, config_file: str):
        """加载配置文件"""
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
            
            # 深度合并配置
            def deep_update(target, source):
                for key, value in source.items():
                    if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                        deep_update(target[key], value)
                    else:
                        target[key] = value
            
            deep_update(self.config, user_config)
            logger.info(f"配置文件已加载: {config_file}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
    
    def start_task(self, task_id: str, task_name: str, 
                   description: str = "", priority: str = "medium",
                   category: str = "custom", tags: List[str] = None,
                   dependencies: List[str] = None, estimated_duration: int = None) -> str:
        """开始监控一个新任务"""
        # 验证优先级
        if priority not in ["critical", "high", "medium", "low"]:
            logger.warning(f"无效的优先级: {priority}，使用默认值: medium")
            priority = "medium"
        
        # 获取资源使用基线
        resource_baseline = {}
        if self.config["enable_resource_monitoring"]:
            resource_baseline = self.get_system_resource_baseline()
        
        task_info = {
            "task_id": task_id,
            "task_name": task_name,
            "description": description,
            "priority": priority,
            "category": category,
            "tags": tags or [],
            "dependencies": dependencies or [],
            "estimated_duration": estimated_duration,
            "start_time": datetime.now(),
            "last_update": datetime.now(),
            "status": "running",
            "update_count": 0,
            "estimated_completion": None,
            "timeout_warnings": 0,
            "resource_baseline": resource_baseline,
            "current_resources": {},
            "performance_metrics": {
                "response_time": None,
                "throughput": None,
                "error_rate": None,
                "progress_percentage": 0
            }
        }
        
        self.active_tasks[task_id] = task_info
        
        log_msg = f"开始监控任务: {task_name} (ID: {task_id})"
        log_msg += f"\n  优先级: {priority}, 类别: {category}"
        if estimated_duration:
            log_msg += f", 预估耗时: {estimated_duration}秒"
        if tags:
            log_msg += f", 标签: {', '.join(tags)}"
        logger.info(log_msg)
        
        # 保存到历史
        self.save_task_to_history(task_info)
        
        return task_id
    
    def get_system_resource_baseline(self) -> Dict:
        """获取系统资源使用基线"""
        try:
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available_gb": psutil.virtual_memory().available / 1024 / 1024 / 1024
            }
        except Exception as e:
            logger.warning(f"获取资源基线失败: {e}")
            return {}
    
    def update_task(self, task_id: str, status: str = None,
                   estimated_completion: str = None,
                   performance_metrics: Dict = None,
                   progress_percentage: int = None) -> bool:
        """更新任务状态"""
        if task_id not in self.active_tasks:
            logger.warning(f"任务不存在: {task_id}")
            return False
        
        task = self.active_tasks[task_id]
        task["last_update"] = datetime.now()
        
        if status:
            task["status"] = status
        
        if estimated_completion:
            task["estimated_completion"] = estimated_completion
        
        if performance_metrics:
            task["performance_metrics"].update(performance_metrics)
        
        if progress_percentage is not None:
            task["performance_metrics"]["progress_percentage"] = progress_percentage
        
        # 更新资源使用
        if self.config["enable_resource_monitoring"]:
            task["current_resources"] = self.get_current_resource_usage()
        
        task["update_count"] += 1
        
        logger.debug(f"任务更新: {task_id}, 状态: {task['status']}, 进度: {task['performance_metrics']['progress_percentage']}%")
        return True
    
    def get_current_resource_usage(self) -> Dict:
        """获取当前资源使用情况"""
        try:
            process = psutil.Process()
            with process.oneshot():
                return {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_percent": process.cpu_percent(),
                    "memory_mb": process.memory_info().rss / 1024 / 1024,
                    "memory_percent": process.memory_percent(),
                    "threads": process.num_threads()
                }
        except Exception as e:
            logger.warning(f"获取资源使用失败: {e}")
            return {}
    
    def check_task_timeout(self, task_id: str) -> Tuple[bool, str, str]:
        """检查任务是否超时"""
        if task_id not in self.active_tasks:
            return False, "info", "任务不存在"
        
        task = self.active_tasks[task_id]
        priority = task.get("priority", "medium")
        
        # 获取对应优先级的超时阈值
        timeout_threshold = self.config["timeout_thresholds"].get(priority, 120)
        
        elapsed = (datetime.now() - task["start_time"]).total_seconds()
        
        # 如果有预估时间，使用预估时间作为参考
        estimated = task.get("estimated_duration")
        if estimated and elapsed > estimated * 1.5:  # 超过预估时间50%
            alert_level = "warning"
            alert_message = (
                f"[预估超时] 任务: {task['task_name']}\n"
                f"  已执行: {elapsed:.1f}秒 (预估: {estimated}秒)\n"
                f"  超时比例: {(elapsed/estimated*100):.1f}%"
            )
            return True, alert_level, alert_message
        
        if elapsed > timeout_threshold:
            # 检查是否超过最大警告次数
            max_warnings = self.config["max_warnings"].get(priority, 2)
            
            if task["timeout_warnings"] < max_warnings:
                task["timeout_warnings"] += 1
                
                # 根据超时严重程度确定告警级别
                if elapsed > timeout_threshold * 3:
                    alert_level = "critical"
                elif elapsed > timeout_threshold * 2:
                    alert_level = "error"
                else:
                    alert_level = "warning"
                
                # 生成详细的提醒消息
                progress = task["performance_metrics"].get("progress_percentage", 0)
                alert_message = (
                    f"[{alert_level.upper()}] 任务超时: {task['task_name']}\n"
                    f"  优先级: {priority}\n"
                    f"  已执行: {elapsed:.1f}秒 (阈值: {timeout_threshold}秒)\n"
                    f"  进度: {progress}%\n"
                    f"  警告次数: {task['timeout_warnings']}/{max_warnings}"
                )
                
                return True, alert_level, alert_message
        
        return False, "info", ""
    
    def complete_task(self, task_id: str, result: str = "完成", 
                     error_info: str = None, metrics: Dict = None) -> bool:
        """标记任务完成"""
        if task_id not in self.active_tasks:
            logger.warning(f"任务不存在: {task_id}")
            return False
        
        task = self.active_tasks[task_id]
        task["status"] = "completed" if not error_info else "failed"
        task["result"] = result
        task["error_info"] = error_info
        task["end_time"] = datetime.now()
        
        if metrics:
            task["performance_metrics"].update(metrics)
        
        # 计算持续时间
        duration = (task["end_time"] - task["start_time"]).total_seconds()
        task["duration"] = duration
        
        # 保存到历史
        self.save_task_to_history(task)
        
        # 从活跃任务中移除
        del self.active_tasks[task_id]
        
        status_emoji = "✅" if not error_info else "❌"
        logger.info(f"{status_emoji} 任务完成: {task['task_name']}, 耗时: {duration:.2f}秒, 结果: {result}")
        
        return True
    
    def save_task_to_history(self, task_info: Dict):
        """保存任务到历史记录"""
        # 转换datetime对象为字符串
        task_copy = task_info.copy()
        for key in ["start_time", "last_update", "end_time"]:
            if key in task_copy and isinstance(task_copy[key], datetime):
                task_copy[key] = task_copy[key].isoformat()
        
        self.task_history.append(task_copy)
        self.save_history()
    
    def load_history(self):
        """加载历史数据"""
        history_file = "/home/admin/openclaw/workspace/enhanced_timeout_guardian_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.task_history = json.load(f)
                logger.info(f"历史数据已加载: {len(self.task_history)} 条记录")
            except Exception as e:
                logger.error(f"加载历史数据失败: {e}")
                self.task_history = []
    
    def save_history(self):
        """保存历史数据"""
        history_file = "/home/admin/openclaw/workspace/enhanced_timeout_guardian_history.json"
        try:
            # 应用数据保留策略
            retention_days = self.config.get("data_retention_days", 30)
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            filtered_history = []
            for task in self.task_history:
                start_time_str = task.get("start_time")
                if start_time_str:
                    try:
                        task_date = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                        if task_date > cutoff_date:
                            filtered_history.append(task)
                    except:
                        filtered_history.append(task)
                else:
                    filtered_history.append(task)
            
            self.task_history = filtered_history
            
            with open(history_file, 'w') as f:
                json.dump(self.task_history, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"历史数据已保存: {len(self.task_history)} 条记录")
        except Exception as e:
            logger.error(f"保存历史数据失败: {e}")
    
    def start_monitoring(self):
        """启动监控线程"""
        if self.running:
            logger.warning("监控线程已在运行")
            return
        
        self.running = True
        
        def monitor_loop():
            """监控循环"""
            while self.running:
                try:
                    # 检查所有活跃任务
                    alerts = []
                    for task_id in list(self.active_tasks.keys()):
                        is_timeout, alert_level, alert_message = self.check_task_timeout(task_id)
                        if is_timeout:
                            alerts.append({
                                "task_id": task_id,
                                "alert_level": alert_level,
                                "alert_message": alert_message,
                                "task_info": self.active_tasks[task_id]
                            })
                    
                    # 处理提醒
                    if alerts:
                        for alert in alerts:
                            logger.warning(alert["alert_message"])
                    
                    # 动态调整检查间隔
                    check_interval = self.get_dynamic_check_interval()
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logger.error(f"监控循环错误: {e}")
                    time.sleep(30)
        
        # 启动任务监控线程
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("✅ 增强版监控卫士已启动")
        logger.info(f"  超时阈值: critical(30s), high(60s), medium(120s), low(300s)")
        logger.info(f"  检查间隔: 动态调整")
        logger.info(f"  最大提醒: critical(5次), high(3次), medium(2次), low(1次)")
    
    def get_dynamic_check_interval(self) -> int:
        """获取动态检查间隔"""
        if not self.active_tasks:
            return 60  # 无任务时检查间隔较长
        
        # 根据活跃任务的最高优先级调整检查间隔
        priority_intervals = {
            "critical": 10,
            "high": 30,
            "medium": 60,
            "low": 120
        }
        
        # 找到最高优先级的任务
        highest_priority = "low"
        for task in self.active_tasks.values():
            priority = task.get("priority", "medium")
            priority_values = {
                "critical": 4,
                "high": 3,
                "medium": 2,
                "low": 1
            }
            if priority_values.get(priority, 2) > priority_values.get(highest_priority, 1):
                highest_priority = priority
        
        return priority_intervals.get(highest_priority, 60)
    
    def stop_monitoring(self):
        """停止监控线程"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("监控线程已停止")
    
    def get_dashboard(self) -> str:
        """获取监控仪表板"""
        dashboard = []
        dashboard.append("=" * 80)
        dashboard.append("增强版智能超时监控卫士 - 实时仪表板")
        dashboard.append("=" * 80)
        
        # 活跃任务统计
        dashboard.append(f"\n📊 活跃任务: {len(self.active_tasks)} 个")
        
        if self.active_tasks:
            dashboard.append("-" * 40)
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                progress = task["performance_metrics"].get("progress_percentage", 0)
                priority = task["priority"]
                
                # 根据优先级选择图标
                if priority == "critical":
                    icon = "🔴"
                elif priority == "high":
                    icon = "🟠"
                elif priority == "medium":
                    icon = "🟡"
                else:
                    icon = "🟢"
                
                dashboard.append(f"{icon} {task['task_name']} (ID: {task_id})")
                dashboard.append(f"   优先级: {priority}, 状态: {task['status']}")
                dashboard.append(f"   已执行: {elapsed:.1f}秒, 进度: {progress}%")
                dashboard.append(f"   最后更新: {task['last_update'].strftime('%H:%M:%S')}")
        
        # 历史统计
        dashboard.append(f"\n📈 历史任务: {len(self.task_history)} 个")
        
        if self.task_history:
            completed = sum(1 for t in self.task_history if t.get("status") == "completed")
            failed = sum(1 for t in self.task_history if t.get("status") == "failed")
            timeout = sum(1 for t in self.task_history if t.get("status") == "timeout")
            
            total = len(self.task_history)
            success_rate = (completed / total * 100) if total > 0 else 0
            
            dashboard.append(f"  完成率: {success_rate:.1f}% ({completed}✅ {failed}❌ {timeout}⏰)")
        
        # 系统状态
        dashboard.append(f"\n🖥️  系统状态:")
        dashboard.append("-" * 40)
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            cpu_icon = "🟢" if cpu < 50 else "