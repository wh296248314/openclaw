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
        print(f"版本: