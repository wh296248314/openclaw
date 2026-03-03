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
            
            cpu_icon = "🟢" if cpu < 50 else "🟡" if cpu < 80 else "🔴"
            memory_icon = "🟢" if memory.percent < 70 else "🟡" if memory.percent < 85 else "🔴"
            
            dashboard.append(f"{cpu_icon} CPU使用率: {cpu:.1f}%")
            dashboard.append(f"{memory_icon} 内存使用: {memory.percent:.1f}% ({memory.available/1024/1024:.0f}MB 可用)")
        except Exception as e:
            dashboard.append(f"系统状态获取失败: {e}")
        
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
            }
        }
        
        # 按优先级和类别统计
        for task in self.task_history:
            priority = task.get("priority", "medium")
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            
            category = task.get("category", "custom")
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
                "priority": "critical",
                "category": "data_processing",
                "estimated": 20
            },
            {
                "id": "demo_high_001", 
                "name": "API接口调用任务",
                "priority": "high",
                "category": "api_call",
                "estimated": 40
            },
            {
                "id": "demo_medium_001",
                "name": "普通系统维护任务",
                "priority": "medium",
                "category": "system_task",
                "estimated": 80
            },
            {
                "id": "demo_low_001",
                "name": "后台数据备份任务",
                "priority": "low",
                "category": "database",
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