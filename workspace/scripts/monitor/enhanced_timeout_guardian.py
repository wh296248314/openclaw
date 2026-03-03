#!/usr/bin/env python3
"""
增强版智能超时监控卫士
支持优先级管理、分级提醒、资源监控
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
from enum import Enum
import subprocess

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

class TaskPriority(Enum):
    """任务优先级枚举"""
    CRITICAL = "critical"    # 关键任务，30秒超时
    HIGH = "high"           # 高优先级，60秒超时  
    MEDIUM = "medium"       # 中优先级，120秒超时
    LOW = "low"             # 低优先级，300秒超时

class TaskCategory(Enum):
    """任务类别枚举"""
    DATA_PROCESSING = "data_processing"
    API_CALL = "api_call"
    SYSTEM_TASK = "system_task"
    NETWORK = "network"
    DATABASE = "database"
    CUSTOM = "custom"

class AlertLevel(Enum):
    """告警级别枚举"""
    INFO = "info"           # 信息级别
    WARNING = "warning"     # 警告级别
    ERROR = "error"         # 错误级别
    CRITICAL = "critical"   # 严重级别

class EnhancedTaskMonitor:
    """增强版任务监控器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化增强版任务监控器
        
        Args:
            config_file: 配置文件路径
        """
        # 默认配置
        self.config = {
            "timeout_thresholds": {
                TaskPriority.CRITICAL.value: 30,
                TaskPriority.HIGH.value: 60,
                TaskPriority.MEDIUM.value: 120,
                TaskPriority.LOW.value: 300
            },
            "check_intervals": {
                TaskPriority.CRITICAL.value: 10,
                TaskPriority.HIGH.value: 30,
                TaskPriority.MEDIUM.value: 60,
                TaskPriority.LOW.value: 120
            },
            "max_warnings": {
                TaskPriority.CRITICAL.value: 5,
                TaskPriority.HIGH.value: 3,
                TaskPriority.MEDIUM.value: 2,
                TaskPriority.LOW.value: 1
            },
            "notification_channels": ["log", "desktop"],
            "enable_resource_monitoring": True,
            "data_retention_days": 30,
            "enable_performance_metrics": True,
            "system_monitoring": {
                "enable_cpu_monitoring": True,
                "enable_memory_monitoring": True,
                "enable_disk_monitoring": True,
                "enable_network_monitoring": True,
                "thresholds": {
                    "cpu_warning": 80,
                    "cpu_critical": 95,
                    "memory_warning": 85,
                    "memory_critical": 95,
                    "disk_warning": 90,
                    "disk_critical": 98
                }
            }
        }
        
        # 加载自定义配置
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.task_history: List[Dict] = []
        self.system_alerts: List[Dict] = []
        self.monitor_thread: Optional[threading.Thread] = None
        self.system_monitor_thread: Optional[threading.Thread] = None
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
                   description: str = "", priority: str = TaskPriority.MEDIUM.value,
                   category: str = TaskCategory.CUSTOM.value, tags: List[str] = None,
                   dependencies: List[str] = None, estimated_duration: int = None) -> str:
        """
        开始监控一个新任务（增强版）
        
        Args:
            task_id: 任务ID
            task_name: 任务名称
            description: 任务描述
            priority: 任务优先级
            category: 任务类别
            tags: 任务标签
            dependencies: 依赖任务列表
            estimated_duration: 预估持续时间（秒）
            
        Returns:
            任务ID
        """
        # 验证优先级
        if priority not in [p.value for p in TaskPriority]:
            logger.warning(f"无效的优先级: {priority}，使用默认值: {TaskPriority.MEDIUM.value}")
            priority = TaskPriority.MEDIUM.value
        
        # 获取资源使用基线（如果启用资源监控）
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
            },
            "metadata": {
                "created_by": os.environ.get('USER', 'unknown'),
                "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown'
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
                "memory_available_gb": psutil.virtual_memory().available / 1024 / 1024 / 1024,
                "disk_usage": {},
                "network_io": psutil.net_io_counters()._asdict() if hasattr(psutil, 'net_io_counters') else {}
            }
        except Exception as e:
            logger.warning(f"获取资源基线失败: {e}")
            return {}
    
    def update_task(self, task_id: str, status: str = None,
                   estimated_completion: str = None,
                   performance_metrics: Dict = None,
                   progress_percentage: int = None) -> bool:
        """
        更新任务状态（增强版）
        
        Args:
            task_id: 任务ID
            status: 新状态
            estimated_completion: 预计完成时间
            performance_metrics: 性能指标
            progress_percentage: 进度百分比
            
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
        
        if performance_metrics:
            task["performance_metrics"].update(performance_metrics)
        
        if progress_percentage is not None:
            task["performance_metrics"]["progress_percentage"] = progress_percentage
        
        # 更新资源使用（如果启用）
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
                    "threads": process.num_threads(),
                    "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0,
                    "io_counters": process.io_counters()._asdict() if hasattr(process, 'io_counters') else {}
                }
        except Exception as e:
            logger.warning(f"获取资源使用失败: {e}")
            return {}
    
    def check_task_timeout(self, task_id: str) -> Tuple[bool, str, str]:
        """
        检查任务是否超时（增强版）
        
        Args:
            task_id: 任务ID
            
        Returns:
            (是否超时, 告警级别, 提醒消息)
        """
        if task_id not in self.active_tasks:
            return False, AlertLevel.INFO.value, "任务不存在"
        
        task = self.active_tasks[task_id]
        priority = task.get("priority", TaskPriority.MEDIUM.value)
        
        # 获取对应优先级的超时阈值
        timeout_threshold = self.config["timeout_thresholds"].get(
            priority, 
            self.config["timeout_thresholds"][TaskPriority.MEDIUM.value]
        )
        
        elapsed = (datetime.now() - task["start_time"]).total_seconds()
        
        # 如果有预估时间，使用预估时间作为参考
        estimated = task.get("estimated_duration")
        if estimated and elapsed > estimated * 1.5:  # 超过预估时间50%
            alert_level = AlertLevel.WARNING.value
            alert_message = (
                f"[预估超时] 任务: {task['task_name']}\n"
                f"  已执行: {elapsed:.1f}秒 (预估: {estimated}秒)\n"
                f"  超时比例: {(elapsed/estimated*100):.1f}%"
            )
            return True, alert_level, alert_message
        
        if elapsed > timeout_threshold:
            # 检查是否超过最大警告次数
            max_warnings = self.config["max_warnings"].get(
                priority,
                self.config["max_warnings"][TaskPriority.MEDIUM.value]
            )
            
            if task["timeout_warnings"] < max_warnings:
                task["timeout_warnings"] += 1
                
                # 根据超时严重程度确定告警级别
                if elapsed > timeout_threshold * 3:
                    alert_level = AlertLevel.CRITICAL.value
                elif elapsed > timeout_threshold * 2:
                    alert_level = AlertLevel.ERROR.value
                else:
                    alert_level = AlertLevel.WARNING.value
                
                # 生成详细的提醒消息
                progress = task["performance_metrics"].get("progress_percentage", 0)
                alert_message = (
                    f"[{alert_level.upper()}] 任务超时: {task['task_name']}\n"
                    f"  优先级: {priority}\n"
                    f"  已执行: {elapsed:.1f}秒 (阈值: {timeout_threshold}秒)\n"
                    f"  进度: {progress}%\n"
                    f"  警告次数: {task['timeout_warnings']}/{max_warnings}\n"
                    f"  资源使用: CPU {task.get('current_resources', {}).get('cpu_percent', 'N/A')}%"
                )
                
                return True, alert_level, alert_message
        
        return False, AlertLevel.INFO.value, ""
    
    def complete_task(self, task_id: str, result: str = "完成", 
                     error_info: str = None, metrics: Dict = None) -> bool:
        """
        标记任务完成（增强版）
        
        Args:
            task_id: 任务ID
            result: 任务结果
            error_info: 错误信息（如果有）
            metrics: 最终指标
            
        Returns:
            是否成功完成
        """
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
        
        # 计算性能评分
        estimated = task.get("estimated_duration")
        if estimated:
            efficiency = (estimated / duration * 100) if duration > 0 else 100
            task["efficiency_score"] = min(efficiency, 100)
        
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
    
    def check_system_resources(self):
        """检查系统资源"""
        if not self.config.get("system_monitoring", {}).get("enable_cpu_monitoring", True):
            return []
        
        alerts = []
        thresholds = self.config["system_monitoring"]["thresholds"]
        
        try:
            # CPU检查
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > thresholds["cpu_critical"]:
                alerts.append({
                    "level": AlertLevel.CRITICAL.value,
                    "type": "cpu",
                    "message": f"CPU使用率严重过高: {cpu_percent}% (阈值: {thresholds['cpu_critical']}%)",
                    "value": cpu_percent
                })
            elif cpu_percent > thresholds["cpu_warning"]:
                alerts.append({
                    "level": AlertLevel.WARNING.value,
                    "type": "cpu",
                    "message": f"CPU使用率过高: