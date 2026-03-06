#!/usr/bin/env python3
"""
增强版cron任务更新工具
支持从QQ Bot切换到钉钉，并验证配置
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional

class CronUpdater:
    def __init__(self, cron_file: str, dry_run: bool = False, verbose: bool = False):
        self.cron_file = cron_file
        self.dry_run = dry_run
        self.verbose = verbose
        self.backup_file = None
        
        # 要更新的任务配置
        self.tasks_to_update = [
            {
                "id": "2b2f4073-542c-4139-b60e-89c033ee8310",
                "name": "系统唤醒准备",
                "schedule": "每天 08:00",
                "new_delivery": {
                    "mode": "announce",
                    "channel": "dingtalk-connector",
                    "to": "manager7367"
                }
            },
            {
                "id": "770e4abf-cb35-448d-94b1-9d6f06ecb259",
                "name": "每日早安问候",
                "schedule": "每天 08:30",
                "new_delivery": {
                    "mode": "announce",
                    "channel": "dingtalk-connector",
                    "to": "manager7367"
                }
            },
            {
                "id": "d4345282-580f-420b-a9ad-4ca789140231",
                "name": "早上9点问候",
                "schedule": "每天 09:00",
                "new_delivery": {
                    "mode": "announce",
                    "channel": "dingtalk-connector",
                    "to": "manager7367"
                }
            }
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def validate_config(self, data: Dict) -> bool:
        """验证配置文件结构"""
        if "version" not in data:
            self.log("配置文件缺少version字段", "ERROR")
            return False
        
        if "jobs" not in data:
            self.log("配置文件缺少jobs字段", "ERROR")
            return False
        
        if not isinstance(data["jobs"], list):
            self.log("jobs字段必须是列表", "ERROR")
            return False
        
        self.log(f"配置文件验证通过，包含 {len(data['jobs'])} 个任务")
        return True
    
    def create_backup(self) -> bool:
        """备份原文件"""
        if not os.path.exists(self.cron_file):
            self.log(f"配置文件不存在: {self.cron_file}", "ERROR")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_file = f"{self.cron_file}.backup.{timestamp}"
        
        try:
            with open(self.cron_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log(f"已创建备份: {self.backup_file}")
            return True
        except Exception as e:
            self.log(f"备份失败: {e}", "ERROR")
            return False
    
    def update_tasks(self, data: Dict) -> int:
        """更新任务配置"""
        updated_count = 0
        not_found_tasks = []
        
        for task_config in self.tasks_to_update:
            task_id = task_config["id"]
            task_found = False
            
            for job in data.get("jobs", []):
                if job.get("id") == task_id:
                    task_found = True
                    
                    # 检查当前配置
                    current_channel = job.get("delivery", {}).get("channel", "")
                    current_to = job.get("delivery", {}).get("to", "")
                    
                    if (current_channel == "dingtalk-connector" and 
                        current_to == "manager7367"):
                        self.log(f"任务 '{task_config['name']}' 已配置为钉钉，跳过更新", "WARNING")
                        continue
                    
                    # 更新配置
                    if self.verbose:
                        self.log(f"更新任务: {task_config['name']} ({task_id})")
                        self.log(f"  时间: {task_config['schedule']}")
                        self.log(f"  新配置: 钉钉 -> manager7367")
                    
                    job["delivery"] = task_config["new_delivery"]
                    
                    # 重置错误状态
                    if "state" in job:
                        job["state"]["lastStatus"] = "pending"
                        job["state"]["lastRunStatus"] = "pending"
                        job["state"]["lastError"] = None
                        job["state"]["consecutiveErrors"] = 0
                    
                    updated_count += 1
                    break
            
            if not task_found:
                not_found_tasks.append(task_config["name"])
        
        # 报告未找到的任务
        if not_found_tasks:
            self.log(f"未找到以下任务: {', '.join(not_found_tasks)}", "WARNING")
        
        return updated_count
    
    def save_config(self, data: Dict) -> bool:
        """保存更新后的配置"""
        if self.dry_run:
            self.log("Dry run模式，不保存文件")
            self.log("更新后的配置预览:", "INFO")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return True
        
        try:
            with open(self.cron_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.log(f"配置已保存到: {self.cron_file}")
            return True
        except Exception as e:
            self.log(f"保存配置失败: {e}", "ERROR")
            return False
    
    def run(self) -> bool:
        """执行更新"""
        self.log("开始更新cron任务配置")
        
        # 1. 备份文件
        if not self.create_backup():
            return False
        
        # 2. 读取配置文件
        try:
            with open(self.cron_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.log(f"读取配置文件失败: {e}", "ERROR")
            return False
        
        # 3. 验证配置
        if not self.validate_config(data):
            return False
        
        # 4. 更新任务
        updated_count = self.update_tasks(data)
        
        # 5. 保存配置
        if not self.save_config(data):
            return False
        
        # 6. 输出结果
        self.log(f"✅ 成功更新 {updated_count}/{len(self.tasks_to_update)} 个任务")
        
        if updated_count > 0:
            self.log("\n📋 更新摘要:")
            for task in self.tasks_to_update:
                self.log(f"  • {task['name']} ({task['schedule']}) -> 钉钉 (manager7367)")
        
        if updated_count == len(self.tasks_to_update):
            self.log("\n🎉 所有任务更新成功！")
        else:
            self.log(f"\n⚠️  部分任务未更新，请检查配置")
        
        self.log(f"\n💾 备份文件: {self.backup_file}")
        self.log("🔄 需要重启OpenClaw Gateway使配置生效")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="更新OpenClaw cron任务到钉钉")
    parser.add_argument("--cron-file", default="/home/admin/.openclaw/cron/jobs.json",
                       help="cron配置文件路径")
    parser.add_argument("--dry-run", action="store_true",
                       help="模拟运行，不实际修改文件")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细输出")
    
    args = parser.parse_args()
    
    updater = CronUpdater(
        cron_file=args.cron_file,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    success = updater.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()