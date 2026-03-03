#!/usr/bin/env python3
"""
钉钉通知模块 - 为增强版监控卫士添加钉钉通知功能
"""

import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger("DingTalkNotifier")

class DingTalkNotifier:
    """钉钉通知器"""
    
    def __init__(self, webhook_url: str = None, secret: str = None):
        """
        初始化钉钉通知器
        
        Args:
            webhook_url: 钉钉机器人Webhook URL
            secret: 钉钉机器人加签密钥（可选）
        """
        self.webhook_url = webhook_url
        self.secret = secret
        self.enabled = bool(webhook_url)
        
        if self.enabled:
            logger.info("钉钉通知器初始化完成")
        else:
            logger.warning("钉钉通知器未配置Webhook URL，通知功能禁用")
    
    def send_alert(self, title: str, message: str, alert_level: str = "warning",
                  task_info: Dict = None, mention_users: List[str] = None) -> bool:
        """
        发送告警通知到钉钉
        
        Args:
            title: 通知标题
            message: 通知内容
            alert_level: 告警级别 (info/warning/error/critical)
            task_info: 任务信息（可选）
            mention_users: 需要@的用户列表（可选）
            
        Returns:
            是否发送成功
        """
        if not self.enabled or not self.webhook_url:
            logger.warning("钉钉通知未启用或未配置Webhook URL")
            return False
        
        try:
            # 根据告警级别选择消息格式
            if alert_level == "critical":
                msg_type = "严重告警"
                color = "#FF0000"  # 红色
            elif alert_level == "error":
                msg_type = "错误告警"
                color = "#FF6B35"  # 橙色
            elif alert_level == "warning":
                msg_type = "警告提醒"
                color = "#FFC300"  # 黄色
            else:
                msg_type = "信息通知"
                color = "#1890FF"  # 蓝色
            
            # 构建markdown消息
            markdown_content = f"## {msg_type}: {title}\n\n"
            markdown_content += f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            markdown_content += f"**内容**: {message}\n\n"
            
            if task_info:
                markdown_content += "**任务详情**:\n"
                markdown_content += f"- 任务名称: {task_info.get('task_name', '未知')}\n"
                markdown_content += f"- 任务ID: {task_info.get('task_id', '未知')}\n"
                markdown_content += f"- 优先级: {task_info.get('priority', '未知')}\n"
                if 'start_time' in task_info:
                    markdown_content += f"- 开始时间: {task_info['start_time']}\n"
            
            # 构建@消息
            at_content = {
                "at": {
                    "atMobiles": mention_users or [],
                    "isAtAll": False
                }
            }
            
            # 构建完整消息
            dingtalk_msg = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"{msg_type}: {title}",
                    "text": markdown_content
                },
                "at": at_content["at"]
            }
            
            # 如果有加签密钥，需要计算签名
            headers = {
                "Content-Type": "application/json"
            }
            
            # 发送请求
            response = requests.post(
                self.webhook_url,
                data=json.dumps(dingtalk_msg),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    logger.info(f"钉钉通知发送成功: {title}")
                    return True
                else:
                    logger.error(f"钉钉通知发送失败: {result.get('errmsg')}")
                    return False
            else:
                logger.error(f"钉钉通知HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"钉钉通知发送异常: {e}")
            return False
    
    def send_simple_message(self, title: str, content: str) -> bool:
        """发送简单文本消息"""
        return self.send_alert(title, content, "info")
    
    def send_task_timeout_alert(self, task_name: str, elapsed_seconds: float,
                               timeout_threshold: float, alert_level: str,
                               task_info: Dict = None) -> bool:
        """发送任务超时告警"""
        title = f"任务超时告警: {task_name}"
        
        # 构建详细消息
        message_lines = []
        message_lines.append(f"任务 **{task_name}** 已超时")
        message_lines.append(f"已执行时间: {elapsed_seconds:.1f}秒")
        message_lines.append(f"超时阈值: {timeout_threshold}秒")
        message_lines.append(f"超时比例: {(elapsed_seconds/timeout_threshold*100):.1f}%")
        message_lines.append(f"告警级别: {alert_level.upper()}")
        
        message = "\n".join(message_lines)
        
        return self.send_alert(title, message, alert_level, task_info)
    
    def send_system_alert(self, alert_type: str, value: float, threshold: float,
                         alert_level: str) -> bool:
        """发送系统资源告警"""
        title = f"系统资源告警: {alert_type}"
        
        # 根据类型构建消息
        if alert_type == "cpu":
            resource_name = "CPU使用率"
            unit = "%"
        elif alert_type == "memory":
            resource_name = "内存使用率"
            unit = "%"
        elif alert_type == "disk":
            resource_name = "磁盘使用率"
            unit = "%"
        else:
            resource_name = alert_type
            unit = ""
        
        message_lines = []
        message_lines.append(f"**{resource_name}** 超过阈值")
        message_lines.append(f"当前值: {value}{unit}")
        message_lines.append(f"阈值: {threshold}{unit}")
        message_lines.append(f"超出比例: {((value-threshold)/threshold*100):.1f}%")
        message_lines.append(f"告警级别: {alert_level.upper()}")
        
        message = "\n".join(message_lines)
        
        return self.send_alert(title, message, alert_level)


# 测试函数
def test_dingtalk():
    """测试钉钉通知功能"""
    import os
    
    # 从环境变量获取配置
    webhook_url = os.environ.get("DINGTALK_WEBHOOK_URL")
    secret = os.environ.get("DINGTALK_SECRET")
    
    if not webhook_url:
        print("⚠️  未设置钉钉Webhook URL，使用模拟测试")
        print("请设置环境变量: export DINGTALK_WEBHOOK_URL='你的Webhook URL'")
        
        # 模拟测试
        notifier = DingTalkNotifier()
        print("✅ 钉钉通知器初始化完成（模拟模式）")
        
        # 模拟发送测试消息
        print("\n📝 模拟发送测试消息:")
        print("1. 任务超时告警")
        print("2. 系统资源告警")
        print("3. 简单通知")
        
        return True
    else:
        print(f"✅ 找到钉钉Webhook配置")
        notifier = DingTalkNotifier(webhook_url, secret)
        
        # 发送测试消息
        print("发送测试消息...")
        success = notifier.send_simple_message(
            "监控卫士测试通知",
            "增强版智能超时监控卫士钉钉通知功能测试成功！\n时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        if success:
            print("✅ 钉钉测试通知发送成功")
        else:
            print("❌ 钉钉测试通知发送失败")
        
        return success


if __name__ == "__main__":
    test_dingtalk()
