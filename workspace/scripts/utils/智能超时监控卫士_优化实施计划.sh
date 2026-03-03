#!/bin/bash
# 智能超时监控卫士优化实施计划

echo "================================================"
echo "智能超时监控卫士优化实施计划"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"

# 创建优化工作目录
OPTIMIZE_DIR="/home/admin/openclaw/workspace/监控卫士优化_$(date +%Y%m%d_%H%M)"
mkdir -p "$OPTIMIZE_DIR"
cd "$OPTIMIZE_DIR"

echo "工作目录: $(pwd)"
echo ""

echo "第一阶段：基础优化（立即实施）"
echo "--------------------------------"

# 1. 创建增强版监控卫士
cat > enhanced_timeout_guardian.py << 'EOF'
#!/usr/bin/env python3
"""
增强版智能超时监控卫士
添加优先级管理、分级提醒、扩展监控数据
"""

import time
import threading
import json
import os
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
    
    def load_config(self, config_file: str):
        """加载配置文件"""
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
            self.config.update(user_config)
            logger.info(f"配置文件已加载: {config_file}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
    
    def start_task(self, task_id: str, task_name: str, 
                   description: str = "", priority: str = TaskPriority.MEDIUM.value,
                   category: str = TaskCategory.CUSTOM.value, tags: List[str] = None,
                   dependencies: List[str] = None) -> str:
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
            
        Returns:
            任务ID
        """
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
                "error_rate": None
            }
        }
        
        self.active_tasks[task_id] = task_info
        logger.info(f"开始监控任务: {task_name} (ID: {task_id}, 优先级: {priority})")
        
        # 保存到历史
        self.save_task_to_history(task_info)
        
        return task_id
    
    def get_system_resource_baseline(self) -> Dict:
        """获取系统资源使用基线"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_io": psutil.disk_io_counters()._asdict() if hasattr(psutil, 'disk_io_counters') else {},
                "network_io": psutil.net_io_counters()._asdict() if hasattr(psutil, 'net_io_counters') else {}
            }
        except Exception as e:
            logger.warning(f"获取资源基线失败: {e}")
            return {}
    
    def update_task(self, task_id: str, status: str = None,
                   estimated_completion: str = None,
                   performance_metrics: Dict = None) -> bool:
        """
        更新任务状态（增强版）
        
        Args:
            task_id: 任务ID
            status: 新状态
            estimated_completion: 预计完成时间
            performance_metrics: 性能指标
            
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
        
        # 更新资源使用（如果启用）
        if self.config["enable_resource_monitoring"]:
            task["current_resources"] = self.get_current_resource_usage()
        
        task["update_count"] += 1
        
        logger.debug(f"任务更新: {task_id}, 状态: {task['status']}")
        return True
    
    def get_current_resource_usage(self) -> Dict:
        """获取当前资源使用情况"""
        try:
            process = psutil.Process()
            return {
                "cpu_percent": process.cpu_percent(),
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "threads": process.num_threads(),
                "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0
            }
        except Exception as e:
            logger.warning(f"获取资源使用失败: {e}")
            return {}
    
    def check_timeout(self, task_id: str) -> Tuple[bool, str]:
        """
        检查任务是否超时（增强版）
        
        Args:
            task_id: 任务ID
            
        Returns:
            (是否超时, 提醒消息)
        """
        if task_id not in self.active_tasks:
            return False, "任务不存在"
        
        task = self.active_tasks[task_id]
        priority = task.get("priority", TaskPriority.MEDIUM.value)
        
        # 获取对应优先级的超时阈值
        timeout_threshold = self.config["timeout_thresholds"].get(
            priority, 
            self.config["timeout_thresholds"][TaskPriority.MEDIUM.value]
        )
        
        elapsed = (datetime.now() - task["start_time"]).total_seconds()
        
        if elapsed > timeout_threshold:
            # 检查是否超过最大警告次数
            max_warnings = self.config["max_warnings"].get(
                priority,
                self.config["max_warnings"][TaskPriority.MEDIUM.value]
            )
            
            if task["timeout_warnings"] < max_warnings:
                task["timeout_warnings"] += 1
                
                # 生成分级提醒消息
                alert_level = "WARNING"
                if elapsed > timeout_threshold * 2:
                    alert_level = "ERROR"
                elif elapsed > timeout_threshold * 3:
                    alert_level = "CRITICAL"
                
                alert_message = (
                    f"[{alert_level}] 任务超时: {task['task_name']}\n"
                    f"  优先级: {priority}\n"
                    f"  已超时: {elapsed:.1f}秒 (阈值: {timeout_threshold}秒)\n"
                    f"  警告次数: {task['timeout_warnings']}/{max_warnings}\n"
                    f"  资源使用: CPU {task.get('current_resources', {}).get('cpu_percent', 'N/A')}%"
                )
                
                return True, alert_message
        
        return False, ""
    
    def complete_task(self, task_id: str, result: str = "完成", 
                     error_info: str = None) -> bool:
        """
        标记任务完成（增强版）
        
        Args:
            task_id: 任务ID
            result: 任务结果
            error_info: 错误信息（如果有）
            
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
        
        # 计算持续时间
        duration = (task["end_time"] - task["start_time"]).total_seconds()
        task["duration"] = duration
        
        # 保存到历史
        self.save_task_to_history(task)
        
        # 从活跃任务中移除
        del self.active_tasks[task_id]
        
        logger.info(f"任务完成: {task['task_name']}, 耗时: {duration:.2f}秒")
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
        history_file = "enhanced_timeout_guardian_history.json"
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
        history_file = "enhanced_timeout_guardian_history.json"
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
    
    def start_monitoring(self, interval_seconds: int = None):
        """
        启动监控线程（增强版）
        
        Args:
            interval_seconds: 检查间隔秒数，如果为None则根据配置决定
        """
        if self.running:
            logger.warning("监控线程已在运行")
            return
        
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    # 检查所有活跃任务
                    alerts = []
                    for task_id in list(self.active_tasks.keys()):
                        is_timeout, alert_message = self.check_timeout(task_id)
                        if is_timeout:
                            alerts.append({
                                "task_id": task_id,
                                "alert_message": alert_message,
                                "task_info": self.active_tasks[task_id]
                            })
                    
                    # 处理提醒
                    if alerts:
                        self.handle_alerts(alerts)
                    
                    # 动态调整检查间隔
                    check_interval = interval_seconds or self.get_dynamic_check_interval()
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logger.error(f"监控循环错误: {e}")
                    time.sleep(30)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        actual_interval = interval_seconds or self.get_dynamic_check_interval()
        logger.info(f"增强版监控线程已启动，动态检查间隔: {actual_interval}秒")
    
    def get_dynamic_check_interval(self) -> int:
        """获取动态检查间隔"""
        # 根据活跃任务数量和优先级动态调整
        if not self.active_tasks:
            return 60  # 无任务时检查间隔较长
        
        # 计算平均优先级
        priority_weights = {
            TaskPriority.CRITICAL.value: 4,
            TaskPriority.HIGH.value: 3,
            TaskPriority.MEDIUM.value: 2,
            TaskPriority.LOW.value: 1
        }
        
        total_weight = 0
        for task in self.active_tasks.values():
            priority = task.get("priority", TaskPriority.MEDIUM.value)
            total_weight += priority_weights.get(priority, 2)
        
        avg_weight = total_weight / len(self.active_tasks)
        
        # 根据平均权重调整检查间隔
        if avg_weight >= 3.5:  # 高优先级任务多
            return 10
        elif avg_weight >= 2.5:
            return 30
        else:
            return 60
    
    def handle_alerts(self, alerts: List[Dict]):
        """处理提醒（可扩展为发送通知）"""
        for alert in alerts:
            logger.warning(alert["alert_message"])
            
            # 这里可以扩展为发送到不同渠道
            # 例如：发送桌面通知、邮件、企业微信等
            
            task_info = alert["task_info"]
            priority = task_info.get("priority", TaskPriority.MEDIUM.value)
            
            # 根据优先级决定通知渠道
            if priority == TaskPriority.CRITICAL.value:
                # 关键任务：所有渠道
                self.send_desktop_notification(alert["alert_message"])
                # self.send_email_notification(alert["alert_message"])
                # self.send_im_notification(alert["alert_message"])
            elif priority == TaskPriority.HIGH.value:
                # 高优先级：桌面通知
                self.send_desktop_notification(alert["alert_message"])
    
    def send_desktop_notification(self, message: str):
        """发送桌面通知（示例）"""
        try:
            # 这里可以使用notify-send或其他桌面通知工具
            os.system(f'notify-send "超时监控提醒" "{message}"')
        except:
            pass  # 桌面通知失败时不中断主流程
    
    def stop_monitoring(self):
        """停止监控线程"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            logger.info("监控线程已停止")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = {
            "active_tasks": len(self.active_tasks),
            "total_history": len(self.task_history),
            "by_priority": {},
            "by_category": {},
            "performance": {
                "avg_duration": 0,
                "completion_rate": 0,
                "timeout_rate": 0
            }
        }
        
        # 按优先级统计
        for task in self.task_history:
            priority = task.get("priority", TaskPriority.MEDIUM.value)
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            
            category = task.get("category", TaskCategory.CUSTOM.value)
            stats["by_category"][category] =