#!/usr/bin/env python3
"""
支持钉钉通知的增强版监控卫士 - 修复版
"""

import time
import threading
import json
import os
import psutil
from datetime import datetime, timedelta
import logging
from dingtalk_notifier import DingTalkNotifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EnhancedGuardianWithDingTalk")

class EnhancedGuardianWithDingTalk:
    """支持钉钉通知的增强版监控卫士"""
    
    def __init__(self, config_file=None):
        # 默认配置
        self.config = {
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
            "notification_channels": ["log", "dingtalk"],
            "dingtalk_config": {
                "webhook_url": os.environ.get("DINGTALK_WEBHOOK_URL", ""),
                "secret": os.environ.get("DINGTALK_SECRET", ""),
                "mention_users": []  # 需要@的用户手机号列表
            }
        }
        
        # 加载自定义配置
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        
        self.active_tasks = {}
        self.task_history = []
        self.running = False
        self.monitor_thread = None
        
        # 初始化钉钉通知器
        dingtalk_config = self.config["dingtalk_config"]
        self.dingtalk_notifier = DingTalkNotifier(
            dingtalk_config["webhook_url"],
            dingtalk_config["secret"]
        )
        
        logger.info("增强版监控卫士（钉钉通知版）初始化完成")
        
        # 检查钉钉通知是否可用
        if "dingtalk" in self.config["notification_channels"]:
            if self.dingtalk_notifier.enabled:
                logger.info("✅ 钉钉通知功能已启用")
            else:
                logger.warning("⚠️  钉钉通知功能已配置但未启用（缺少Webhook URL）")
    
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
            "estimated_time": estimated_time
        }
        
        self.active_tasks[task_id] = task_info
        
        # 发送任务开始通知（可选）
        if "dingtalk" in self.config["notification_channels"] and self.dingtalk_notifier.enabled:
            title = f"任务开始监控: {task_name}"
            message = f"任务 **{task_name}** 已开始监控\n优先级: {priority}\n预估时间: {estimated_time or '未设置'}秒"
            self.dingtalk_notifier.send_simple_message(title, message)
        
        logger.info(f"开始监控: {task_name} (优先级: {priority})")
        return task_id
    
    def update_task(self, task_id, progress=None):
        """更新任务进度"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["last_update"] = datetime.now()
            if progress is not None:
                self.active_tasks[task_id]["progress"] = progress
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
        
        # 发送任务完成通知
        if "dingtalk" in self.config["notification_channels"] and self.dingtalk_notifier.enabled:
            title = f"任务完成: {task['task_name']}"
            message = f"任务 **{task['task_name']}** 已完成\n耗时: {duration:.2f}秒\n结果: {result}"
            self.dingtalk_notifier.send_simple_message(title, message)
        
        self.task_history.append(task.copy())
        del self.active_tasks[task_id]
        
        logger.info(f"✅ 完成: {task['task_name']}, 耗时: {duration:.2f}秒, 结果: {result}")
        return True
    
    def check_timeouts(self):
        """检查超时任务并发送告警"""
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
                    alert_level = "critical"
                elif elapsed > timeout * 2:
                    alert_level = "error"
                else:
                    alert_level = "warning"
                
                # 记录日志告警
                alert_msg = f"[{alert_level.upper()}] {task['task_name']} 超时: {elapsed:.1f}s (阈值: {timeout}s)"
                alerts.append((task_id, alert_msg, alert_level, elapsed, timeout))
        
        return alerts
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                alerts = self.check_timeouts()
                
                # 处理告警
                for task_id, alert_msg, alert_level, elapsed, timeout in alerts:
                    logger.warning(alert_msg)
                    
                    # 发送钉钉通知
                    if "dingtalk" in self.config["notification_channels"] and self.dingtalk_notifier.enabled:
                        task = self.active_tasks[task_id]
                        success = self.dingtalk_notifier.send_task_timeout_alert(
                            task_name=task["task_name"],
                            elapsed_seconds=elapsed,
                            timeout_threshold=timeout,
                            alert_level=alert_level,
                            task_info=task
                        )
                        
                        if success:
                            logger.info(f"钉钉超时告警发送成功: {task['task_name']}")
                        else:
                            logger.warning(f"钉钉超时告警发送失败: {task['task_name']}")
                
                time.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                time.sleep(30)
    
    def start(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # 发送启动通知
        if "dingtalk" in self.config["notification_channels"] and self.dingtalk_notifier.enabled:
            title = "监控卫士启动通知"
            message = f"增强版智能超时监控卫士已启动\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.dingtalk_notifier.send_simple_message(title, message)
        
        logger.info("✅ 增强版监控卫士（钉钉通知版）已启动")
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        # 发送停止通知
        if "dingtalk" in self.config["notification_channels"] and self.dingtalk_notifier.enabled:
            title = "监控卫士停止通知"
            message = f"增强版智能超时监控卫士已停止\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.dingtalk_notifier.send_simple_message(title, message)
        
        logger.info("监控已停止")
    
    def get_dashboard(self):
        """获取仪表板"""
        lines = []
        lines.append("=" * 60)
        lines.append("增强版监控卫士（钉钉通知版） - 实时仪表板")
        lines.append("=" * 60)
        
        lines.append(f"\n📊 活跃任务: {len(self.active_tasks)} 个")
        if self.active_tasks:
            for task_id, task in self.active_tasks.items():
                elapsed = (datetime.now() - task["start_time"]).total_seconds()
                priority = task["priority"]
                icon = "🔴" if priority == "critical" else "🟠" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                lines.append(f"{icon} {task['task_name']} - {elapsed:.1f}s")
        
        lines.append(f"\n📈 历史任务: {len(self.task_history)} 个")
        if self.task_history:
            completed = sum(1 for t in self.task_history if t.get("status") == "completed")
            total = len(self.task_history)
            rate = (completed / total * 100) if total > 0 else 0
            lines.append(f"  完成率: {rate:.1f}% ({completed}/{total})")
        
        # 钉钉通知状态
        dingtalk_status = "✅ 已启用" if self.dingtalk_notifier.enabled else "⚠️  未配置"
        lines.append(f"\n📱 钉钉通知: {dingtalk_status}")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def test_dingtalk_integration():
    """测试钉钉通知集成"""
    print("🎯 测试钉钉通知集成功能")
    print("=" * 50)
    
    # 创建实例
    guardian = EnhancedGuardianWithDingTalk()
    
    # 检查钉钉配置
    webhook_url = guardian.config["dingtalk_config"]["webhook_url"]
    
    if webhook_url:
        print(f"✅ 找到钉钉Webhook配置")
        print(f"   通知渠道: {guardian.config['notification_channels']}")
    else:
        print("⚠️  未配置钉钉Webhook URL")
        print("   请设置环境变量:")
        print("   export DINGTALK_WEBHOOK_URL='你的Webhook URL'")
        print("   export DINGTALK_SECRET='你的加签密钥'（可选）")
    
    # 启动监控
    guardian.start()
    
    # 创建测试任务
    print("\n📝 创建测试任务:")
    test_tasks = [
        ("test_dingtalk_critical", "钉钉通知测试-关键任务", "critical", 25),
        ("test_dingtalk_high", "钉钉通知测试-重要任务", "high", 45)
    ]
    
    for task_id, name, priority, est in test_tasks:
        guardian.start_task(task_id, name, priority, est)
        icon = "🔴" if priority == "critical" else "🟠"
        print(f"{icon} {name} (优先级: {priority}, 预估: {est}秒)")
    
    print("\n🔄 监控中... 等待超时触发钉钉通知")
    print("按 Ctrl+C 停止测试")
    
    try:
        # 等待足够时间让任务超时
        for i in range(4):
            time.sleep(15)
            print(f"\n⏰ 第{i+1}次检查 ({datetime.now().strftime('%H:%M:%S')})")
            print(guardian.get_dashboard())
            
            # 模拟任务完成
            if i == 2:
                guardian.complete_task("test_dingtalk_critical", "测试完成")
                print("✅ 关键任务完成")
            elif i == 3:
                guardian.complete_task("test_dingtalk_high", "测试完成")
                print("✅ 重要任务完成")
                
    except KeyboardInterrupt:
        print("\n\n🛑 用户中断测试...")
    finally:
        guardian.stop()
        print("\n✅ 钉钉通知集成测试完成")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="测试钉钉通知集成")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表板")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    if args.test:
        test_dingtalk_integration()
    elif args.dashboard:
        guardian = EnhancedGuardianWithDingTalk(args.config)
        print(guardian.get_dashboard())
    else:
        print("增强版监控卫士（钉钉通知版）")
        print("使用说明:")
        print("  python3 enhanced_guardian_with_dingtalk_fixed.py --test    # 测试钉钉通知")
        print("  python3 enhanced_guardian_with_dingtalk_fixed.py --dashboard  # 显示仪表板")
        print("")
        print("环境变量配置:")
        print("  export DINGTALK_WEBHOOK_URL='你的钉钉机器人Webhook URL'")
        print("  export DINGTALK_SECRET='你的加签密钥'（可选）")
        print("")
        print("钉钉机器人创建步骤:")
        print("  1. 打开钉钉群 → 群设置 → 智能群助手")
        print("  2. 添加机器人 → 自定义机器人")
        print("  3. 设置机器人名称和安全设置")
        print("  4. 复制Webhook URL和加签密钥")
