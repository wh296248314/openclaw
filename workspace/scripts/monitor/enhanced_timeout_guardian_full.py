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
            elif cpu_percent > thresholds["cpu_warning"]:
                alerts.append({
                    "level": AlertLevel.WARNING.value,
                    "type": "cpu",
                    "message": f"CPU使用率过高: {cpu_percent}% (阈值: {thresholds['cpu_warning']}%)",
                    "value": cpu_percent
                })
            
            # 内存检查
            memory = psutil.virtual_memory()
            if memory.percent > thresholds["memory_critical"]:
                alerts.append({
                    "level": AlertLevel.CRITICAL.value,
                    "type": "memory",
                    "message": f"内存使用率严重过高: {memory.percent}% (可用: {memory.available/1024/1024:.1f}MB)",
                    "value": memory.percent
                })
            elif memory.percent > thresholds["memory_warning"]:
                alerts.append({
                    "level": AlertLevel.WARNING.value,
                    "type": "memory",
                    "message": f"内存使用率过高: {memory.percent}% (可用: {memory.available/1024/1024:.1f}MB)",
                    "value": memory.percent
                })
            
            # 磁盘检查（根分区）
            try:
                disk = psutil.disk_usage('/')
                if disk.percent > thresholds["disk_critical"]:
                    alerts.append({
                        "level": AlertLevel.CRITICAL.value,
                        "type": "disk",
                        "message": f"磁盘使用率严重过高: {disk.percent}% (可用: {disk.free/1024/1024/1024:.1f}GB)",
                        "value": disk.percent
                    })
                elif disk.percent > thresholds["disk_warning"]:
                    alerts.append({
                        "level": AlertLevel.WARNING.value,
                        "type": "disk",
                        "message": f"磁盘使用率过高: {disk.percent}% (可用: {disk.free/1024/1024/1024:.1f}GB)",
                        "value": disk.percent
                    })
            except Exception as e:
                logger.warning(f"磁盘检查失败: {e}")
        
        except Exception as e:
            logger.error(f"系统资源检查失败: {e}")
        
        return alerts
    
    def start_monitoring(self):
        """启动监控线程"""
        if self.running:
            logger.warning("监控线程已在运行")
            return
        
        self.running = True
        
        def task_monitor_loop():
            """任务监控循环"""
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
                        self.handle_alerts(alerts)
                    
                    # 动态调整检查间隔
                    check_interval = self.get_dynamic_check_interval()
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logger.error(f"任务监控循环错误: {e}")
                    time.sleep(30)
        
        def system_monitor_loop():
            """系统监控循环"""
            while self.running:
                try:
                    # 检查系统资源
                    system_alerts = self.check_system_resources()
                    
                    # 处理系统告警
                    if system_alerts:
                        for alert in system_alerts:
                            logger.warning(f"系统告警 [{alert['level'].upper()}]: {alert['message']}")
                            self.system_alerts.append({
                                **alert,
                                "timestamp": datetime.now().isoformat()
                            })
                    
                    # 系统监控间隔：60秒
                    time.sleep(60)
                    
                except Exception as e:
                    logger.error(f"系统监控循环错误: {e}")
                    time.sleep(60)
        
        # 启动任务监控线程
        self.monitor_thread = threading.Thread(target=task_monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # 启动系统监控线程
        self.system_monitor_thread = threading.Thread(target=system_monitor_loop, daemon=True)
        self.system_monitor_thread.start()
        
        logger.info("✅ 增强版监控卫士已启动")
        logger.info(f"  任务监控间隔: 动态调整")
        logger.info(f"  系统监控间隔: 60秒")
        logger.info(f"  启用资源监控: {self.config['enable_resource_monitoring']}")
    
    def get_dynamic_check_interval(self) -> int:
        """获取动态检查间隔"""
        if not self.active_tasks:
            return 60  # 无任务时检查间隔较长
        
        # 根据活跃任务的最高优先级调整检查间隔
        priority_intervals = {
            TaskPriority.CRITICAL.value: 10,
            TaskPriority.HIGH.value: 30,
            TaskPriority.MEDIUM.value: 60,
            TaskPriority.LOW.value: 120
        }
        
        # 找到最高优先级的任务
        highest_priority = TaskPriority.LOW.value
        for task in self.active_tasks.values():
            priority = task.get("priority", TaskPriority.MEDIUM.value)
            priority_values = {
                TaskPriority.CRITICAL.value: 4,
                TaskPriority.HIGH.value: 3,
                TaskPriority.MEDIUM.value: 2,
                TaskPriority.LOW.value: 1
            }
            if priority_values.get(priority, 2) > priority_values.get(highest_priority, 1):
                highest_priority = priority
        
        return priority_intervals.get(highest_priority, 60)
    
    def handle_alerts(self, alerts: List[Dict]):
        """处理提醒"""
        for alert in alerts:
            task_info = alert["task_info"]
            alert_level = alert["alert_level"]
            alert_message = alert["alert_message"]
            
            # 记录到日志
            logger.warning(alert_message)
            
            # 根据告警级别决定通知渠道
            channels = self.config["notification_channels"]
            
            if "desktop" in channels and alert_level in [AlertLevel.WARNING.value, AlertLevel.ERROR.value, AlertLevel.CRITICAL.value]:
                self.send_desktop_notification(alert_message)
            
            # 这里可以扩展为发送到其他渠道
            # 例如：邮件、企业微信、Slack等
    
    def send_desktop_notification(self, message: str):
        """发送桌面通知"""
        try:
            # 简化消息，避免通知过长
            lines = message.split('\n')
            summary = lines[0] if lines else "超时监控提醒"
            body = '\n'.join(lines[1:3]) if len(lines) > 1 else message
            
            # 使用notify-send发送桌面通知
            subprocess.run([
                'notify-send', 
                '-t', '10000',  # 显示10秒
                '-u', 'normal',
                summary,
                body[:200]  # 限制长度
            ], capture_output=True)
        except Exception as e:
            logger.debug(f"桌面通知发送失败: {e}")
    
    def stop_monitoring(self):
        """停止监控线程"""
        self.running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        if self.system_monitor_thread:
            self.system_monitor_thread.join(timeout=5)
        
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
                status_icon = "🟢" if progress < 50 else "🟡" if progress < 80 else "🔴"
                
                dashboard.append(f"{status_icon} {task['task_name']} (ID: {task_id})")
                dashboard.append(f"   优先级: {task['priority']}, 状态: {task['status']}")
                dashboard.append(f"   已执行: {elapsed:.1f}秒, 进度: {progress}%")
                dashboard.append(f"   最后更新: {task['last_update'].strftime('%H:%M:%S')}")
        
        # 系统状态
        dashboard.append(f"\n🖥️  系统状态:")
        dashboard.append("-" * 40)
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            cpu_icon = "🟢" if cpu < 50 else "🟡" if cpu < 80 else "🔴"
            memory_icon = "🟢" if memory.percent < 70 else "🟡" if memory.percent < 85 else "🔴"
            disk_icon = "🟢" if disk.percent < 80 else "🟡" if disk.percent < 90 else "🔴"
            
            dashboard.append(f"{cpu_icon} CPU使用率: {cpu:.1f}%")
            dashboard.append(f"{memory_icon} 内存使用: {memory.percent:.1f}% ({memory.available/1024/1024:.0f}MB 可用)")
            dashboard.append(f"{disk_icon} 磁盘使用: {disk.percent:.1f}% ({disk.free/1024/1024/1024:.1f}GB 可用)")
        except Exception as e:
            dashboard.append(f"系统状态获取失败: {e}")
        
        # 历史统计
        dashboard.append(f"\n📈 历史统计:")
        dashboard.append("-" * 40)
        if self.task_history:
            completed = sum(1 for t in self.task_history if t.get("status") == "completed")
            failed = sum(1 for t in self.task_history if t.get("status") == "failed")
            timeout = sum(1 for t in self.task_history if t.get("status") == "timeout")
            
            total = len(self.task_history)
            success_rate = (completed / total * 100) if total > 0 else 0
            
            dashboard.append(f"总任务数: {total}")
            dashboard.append(f"完成率: {success_rate:.1f}% ({completed}✅ {failed}❌ {timeout}⏰)")
        
        dashboard.append("\n" + "=" * 80)
        return '\n'.join(dashboard)
    
    def get_statistics(self) -> Dict:
        """获取详细统计信息"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "active_tasks": len(self.active_tasks),
            "total_history": len(self.task_history),
            "by_priority": {},
            "by_category": {},
            "performance": {
                "avg_duration": 0,
                "completion_rate": 0,
                "timeout_rate": 0
            },
            "system": {
                "cpu_percent": 0,
                "memory_percent": 0,
                "disk_percent": 0
            }
        }
        
        # 按优先级和类别统计
        for task in self.task_history:
            priority = task.get("priority", TaskPriority.MEDIUM.value)
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            
            category = task.get("category", TaskCategory.CUSTOM.value)
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # 计算性能指标
        completed_tasks = [t for t in self.task_history if t.get("status") == "completed"]
        if completed_tasks:
            total_duration = sum(t.get("duration", 0) for t in completed_tasks)
            stats["performance"]["avg_duration"] = total_duration / len(completed_tasks)
        
        if self.task_history:
            completed_count = len([t for t in self.task_history if t.get("status") == "completed"])
            timeout_count = len([t for t in self.task_history if t.get("status") == "timeout"])
            stats["performance"]["completion_rate"] = (completed_count / len(self.task_history)) * 100
            stats["performance"]["timeout_rate"] = (timeout_count / len(self.task_history)) * 100
        
        # 系统状态
        try:
            stats["system"]["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            stats["system"]["memory_percent"] = psutil.virtual_memory().percent
            stats["system"]["disk_percent"] = psutil.disk_usage('/').percent
        except:
            pass
        
        return stats


class EnhancedTimeoutGuardian:
    """增强版智能超时监控卫士主类"""
    
    def __init__(self, config_file: str = None):
        self.monitor = EnhancedTaskMonitor(config_file)
        self.running = False
    
    def start(self):
        """启动监控卫士"""
        if self.running:
            logger.warning("监控卫士已在运行")
            return
        
        self.monitor.start_monitoring()
        self.running = True
        
        logger.info("✅ 增强版智能超时监控卫士已启动")
        logger.info(f"  超时阈值: 分级管理 (critical:30s, high:60s, medium:120s, low:300s)")
        logger.info(f"  检查间隔: 动态调整 (基于任务优先级)")
        logger.info(f"  最大提醒: 分级限制 (critical:5次, high:3次, medium:2次, low:1次)")
        logger.info(f"  资源监控: {'启用' if self.monitor.config['enable_resource_monitoring'] else '禁用'}")
        logger.info(f"  系统监控: {'启用' if self.monitor.config['system_monitoring']['enable_cpu_monitoring'] else '禁用'}")
    
    def stop(self):
        """停止监控卫士"""
        self.monitor.stop_monitoring()
        self.running = False
        logger.info("增强版智能超时监控卫士已停止")
    
    def get_dashboard(self) -> str:
        """获取仪表板"""
        return self.monitor.get_dashboard()
    
    def demo_tasks(self):
        """演示任务"""
        logger.info("开始演示增强版监控功能...")
        
        # 演示不同优先级的任务
        tasks = [
            {
                "id": "demo_critical_001",
                "name": "关键数据处理任务",
                "priority": TaskPriority.CRITICAL.value,
                "category": TaskCategory.DATA_PROCESSING.value,
                "estimated": 20  # 预估20秒完成
            },
            {
                "id": "demo_high_001", 
                "name": "API接口调用任务",
                "priority": TaskPriority.HIGH.value,
                "category": TaskCategory.API_CALL.value,
                "estimated": 40
            },
            {
                "id": "demo_medium_001",
                "name": "普通系统维护任务",
                "priority": TaskPriority.MEDIUM.value,
                "category": TaskCategory.SYSTEM_TASK.value,
                "estimated": 80
            },
            {
                "id": "demo_low_001",
                "name": "后台数据备份任务",
                "priority": TaskPriority.LOW.value,
                "category": TaskCategory.DATABASE.value,
                "estimated": 150
            }
        ]
        
        task_ids = []
        for task in tasks:
            task_id = self.monitor.start_task(
                task_id=task["id"],
                task_name=task["name"],
                priority=task["priority"],
                category=task["category"],
                estimated_duration=task["estimated"],
                tags=["demo", "enhanced"]
            )
            task_ids.append(task_id)
        
        logger.info(f"已创建 {len(task_ids)} 个演示任务")
        
        # 模拟任务更新
        time.sleep(10)
        for i, task_id in enumerate(task_ids):
            progress = (i + 1) * 25  # 25%, 50%, 75%, 100%
            self.monitor.update_task(
                task_id=task_id,
                progress_percentage=progress,
                performance_metrics={"throughput": f"{i+1}MB/s"}
            )
        
        # 模拟任务完成
        time.sleep(5)
        for task_id in task_ids:
            self.monitor.complete_task(
                task_id=task_id,
                result="演示完成",
                metrics={"efficiency": "95%"}
            )
        
        logger.info("演示任务完成")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增强版智能超时监控卫士")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--demo", action="store_true", help="运行演示任务")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表板")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--status", action="store_true", help="显示状态")
    
    args = parser.parse_args()
    
    guardian = EnhancedTimeoutGuardian(args.config)
    
    if args.demo:
        guardian.start()
        guardian.demo_tasks()
        time.sleep(5)
        guardian.stop()
    elif args.dashboard:
        print(guardian.get_dashboard())
    elif args.stats:
        stats = guardian.monitor.get_statistics()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    elif args.status:
        print("增强版智能超时监控卫士")
        print(f"版本: 增强版 v1.0")
        print(f"配置: {args.config or '默认配置'}")
        print(f"历史任务: {len(guardian.monitor.task_history)}")
        print(f"活跃任务: {len(guardian.monitor.active_tasks)}")
    else:
        # 正常启动模式
        guardian.start()
        
        try:
            # 显示仪表板
            print("\n" + guardian.get_dashboard())
            
            # 保持运行
            print("\n监控中... 按 Ctrl+C 停止")
            print("命令提示:")
            print("  • 按 'd' 显示仪表板")
            print("  • 按 's' 显示统计信息")
            print("  • 按 'q' 退出")
            
            while True:
                try:
                    # 非阻塞读取输入
                    import select
                    if select.select([sys.stdin], [], [], 1)[0]:
                        cmd = sys.stdin.readline().strip().lower()
                        if cmd == 'd':
                            print("\n" + guardian.get_dashboard())
                        elif cmd == 's':
                            stats = guardian.monitor.get_statistics()
                            print("\n统计信息:")
                            print(json.dumps(stats, indent=2, ensure_ascii=False))
                        elif cmd == 'q':
                            break
                    
                    # 每分钟更新一次仪表板
                    time.sleep(60)
                    print("\n" + guardian.get_dashboard())
                    
                except KeyboardInterrupt:
                    break
                    
        except KeyboardInterrupt:
            print("\n接收到停止信号...")
        finally:
            guardian.stop()


if __name__ == "__main__":
    main()
