#!/usr/bin/env python3
"""
功能完整的增强版监控卫士主程序
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
        logging.FileHandler('/home/admin/openclaw/workspace/complete_guardian.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CompleteGuardian")

class CompleteGuardian:
    """功能完整的增强版监控卫士"""
    
    def __init__(self, config_file=None):
        # 加载配置
        self.config = self.load_config(config_file)
        self.active_tasks = {}
        self.task_history = []
        self.system_alerts = []
        self.running = False
        self.monitor_thread = None
        self.system_monitor_thread = None
        
        logger.info("功能完整的增强版监控卫士初始化完成")
        logger.info(f"超时阈值: critical({self.config['timeout_thresholds']['critical']}s), "
                   f"high({self.config['timeout_thresholds']['high']}s), "
                   f"medium({self.config['timeout_thresholds']['medium']}s), "
                   f"low({self.config['timeout_thresholds']['low']}s)")
    
    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
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
            },
            "notification_channels": ["log"],
            "enable_resource_monitoring": True,
            "data_retention_days": 30,
            "enable_performance_metrics": True,
            "system_monitoring": {
                "enable_cpu_monitoring": True,
                "enable_memory_monitoring": True,
                "enable_disk_monitoring": True,
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
        
        if config_file and os.path.exists(config_file):
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
                
                deep_update(default_config, user_config)
                logger.info(f"配置文件已加载: {config_file}")
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        
        return default_config
    
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
            "estimated_time": estimated_time,
            "performance_metrics": {
                "progress": 0,
                "start_resources": self.get_system_resources()
            }
        }
        
        self.active_tasks[task_id] = task_info
        logger.info(f"开始监控: {task_name} (优先级: {priority})")
        return task_id
    
    def get_system_resources(self):
        """获取系统资源状态"""
        try:
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available_gb": psutil.virtual_memory().available / 1024 / 1024 / 1024,
                "disk_usage": psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else 0
            }
        except Exception as e:
            logger.warning(f"获取系统资源失败: {e}")
            return {}
    
    def update_task(self, task_id, progress=None):
        """更新任务进度"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["last_update"] = datetime.now()
            if progress is not None:
                self.active_tasks[task_id]["performance_metrics"]["progress"] = progress
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
        
        # 计算资源使用变化
        end_resources = self.get_system_resources()
        start_resources = task["performance_metrics"]["start_resources"]
        
        if start_resources and end_resources:
            task["performance_metrics"]["resource_delta"] = {
                "cpu_change": end_resources.get("cpu_percent", 0) - start_resources.get("cpu_percent", 0),
                "memory_change": end_resources.get("memory_percent", 0) - start_resources.get("memory_percent", 0)
            }
        
        self.task_history.append(task.copy())
        del self.active_tasks[task_id]
        
        logger.info(f"✅ 完成: {task['task_name']}, 耗时: {duration:.2f}秒, 结果: {result}")
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
                    alert_level = "CRITICAL"
                elif elapsed > timeout * 2:
                    alert_level = "ERROR"
                else:
                    alert_level = "WARNING"
                
                alert_msg = f"[{alert_level}] {task['task_name']} 超时: {elapsed:.1f}s (阈值: {timeout}s)"
                alerts.append((task_id, alert_msg, alert_level.lower(), elapsed, timeout))
        
        return alerts
    
    def check_system_resources(self):
        """检查系统资源"""
        alerts = []
        
        if not self.config["system_monitoring"]["enable_cpu_monitoring"]:
            return alerts
        
        thresholds = self.config["system_monitoring"]["thresholds"]
        
        try:
            # CPU检查
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > thresholds["cpu_critical"]:
                alerts.append(("system", "cpu", "critical", cpu_percent, thresholds["cpu_critical"]))
            elif cpu_percent > thresholds["cpu_warning"]:
                alerts.append(("system", "cpu", "warning", cpu_percent, thresholds["cpu_warning"]))
            
            # 内存检查
            memory = psutil.virtual_memory()
            if memory.percent > thresholds["memory_critical"]:
                alerts.append(("system", "memory", "critical", memory.percent, thresholds["memory_critical"]))
            elif memory.percent > thresholds["memory_warning"]:
                alerts.append(("system", "memory", "warning", memory.percent, thresholds["memory_warning"]))
            
            # 磁盘检查
            disk = psutil.disk_usage('/')
            if disk.percent > thresholds["disk_critical"]:
                alerts.append(("system", "disk", "critical", disk.percent, thresholds["disk_critical"]))
            elif disk.percent > thresholds["disk_warning"]:
                alerts.append(("system", "disk", "warning", disk.percent, thresholds["disk_warning"]))
                
        except Exception as e:
            logger.error(f"系统资源检查失败: {e}")
        
        return alerts
    
    def task_monitor_loop(self):
        """任务监控循环"""
        while self.running:
            try:
                # 检查任务超时
                task_alerts = self.check_timeouts()
                for task_id, alert_msg, alert_level, elapsed, timeout in task_alerts:
                    logger.warning(alert_msg)
                
                time.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"任务监控循环错误: {e}")
                time.sleep(30)
    
    def system_monitor_loop(self):
        """系统监控循环"""
        while self.running:
            try:
                # 检查系统资源
                system_alerts = self.check_system_resources()
                for system_type, resource_type, alert_level, current_value, threshold in system_alerts:
                    alert_msg = f"[{alert_level.upper()}] 系统资源告警: {resource_type} {current_value:.1f}% (阈值: {threshold}%)"
                    logger.warning(alert_msg)
                    self.system_alerts.append({
                        "type": resource_type,
                        "level": alert_level,
                        "value": current_value,
                        "threshold": threshold,
                        "timestamp": datetime.now().isoformat()
                    })
                
                time.sleep(60)  # 每60秒检查一次
                
            except Exception as e:
                logger.error(f"系统监控循环错误: {e}")
                time.sleep(60)
    
    def start(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        
        # 启动任务监控线程
        self.monitor_thread = threading.Thread(target=self.task_monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # 启动系统监控线程
        if self.config["system_monitoring"]["enable_cpu_monitoring"]:
            self.system_monitor_thread = threading.Thread(target=self.system_monitor_loop, daemon=True)
            self.system_monitor_thread.start()
            logger.info("✅ 系统资源监控已启用")
        
        logger.info("✅ 功能完整的增强版监控卫士已启动")
    
    def stop(self):
        """停止监控"""
        self.running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        if self.system_monitor_thread:
            self.system_monitor_thread.join(timeout=5)
        
        logger.info("监控已停止")
    
    def get_dashboard(self):
        """获取仪表板"""
        lines = []
        lines.append("=" * 70)
        lines.append("功能完整的增强版监控卫士 - 实时仪表板")
        lines.append("=" * 70)
        
        # 系统状态
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            cpu_icon = "🟢" if cpu < 50 else "🟡" if cpu < 80 else "🔴"
            memory_icon = "🟢" if memory.percent < 70 else "🟡" if memory.percent < 85 else "🔴"
            disk_icon = "🟢" if disk.percent < 80 else "🟡" if disk.percent < 90 else "🔴"
            
            lines.append(f"\n🖥️  系统状态:")
            lines.append(f"{cpu_icon} CPU: {cpu:.1f}%")
            lines.append(f"{memory_icon} 内存: {memory.percent:.1f}% ({memory.available/1024/1024:.0f}MB 可用)")
            lines.append(f"{disk_icon} 磁盘: {disk.percent:.1f}% ({disk.free/1024/1024/1024:.1f}GB 可用)")
        except:
            lines.append("\n🖥️  系统状态: 获取失败")
        
        # 任务状态
        lines.append(f"\n📊 任务状态:")
        lines.append(f"  活跃任务: {len(self.active_tasks)} 个")
        lines.append(f"  历史任务: {len(self.task_history)} 个")
        
        if self.active_tasks:
            lines.append("\n📋 活跃任务列表:")
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                priority = task["priority"]
                progress = task["performance_metrics"]["progress"]
                icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                
                lines.append(f"{icon} {task['task_name']}")
                lines.append(f"   优先级: {priority}, 已执行: {elapsed:.1f}s, 进度: {progress}%")
        
        # 系统告警
        if self.system_alerts:
            recent_alerts = self.system_alerts[-5:]  # 最近5个告警
            lines.append(f"\n⚠️  最近系统告警: {len(recent_alerts)} 个")
            for alert in recent_alerts:
                icon = "🔴" if alert["level"] == "critical" else "🟡" if alert["level"] == "warning" else "🟢"
                lines.append(f"{icon} {alert['type']}: {alert['value']:.1f}% (阈值: {alert['threshold']}%)")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="/home/admin/openclaw/workspace/timeout_guardian_optimized_config.json")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表板")
    
    args = parser.parse_args()
    
    guardian = CompleteGuardian(args.config)
    
    if args.dashboard:
        print(guardian.get_dashboard())
    else:
        guardian.start()
        
        try:
            print("\n" + guardian.get_dashboard())
            print("\n监控中... 按 Ctrl+C 停止")
            
            while True:
                time.sleep(60)
                print("\n" + guardian.get_dashboard())
                
        except KeyboardInterrupt:
            print("\n接收到停止信号...")
        finally:
            guardian.stop()


if __name__ == "__main__":
    main()
