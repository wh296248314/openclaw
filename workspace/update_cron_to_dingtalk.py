#!/usr/bin/env python3
"""
更新cron任务从QQ Bot切换到钉钉
"""

import json
import os
from datetime import datetime

# 配置文件路径
cron_file = "/home/admin/.openclaw/cron/jobs.json"
backup_file = f"{cron_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# 要更新的任务ID和名称
tasks_to_update = [
    {
        "id": "2b2f4073-542c-4139-b60e-89c033ee8310",
        "name": "系统唤醒准备",
        "new_delivery": {
            "mode": "announce",
            "channel": "dingtalk-connector",
            "to": "manager7367"
        }
    },
    {
        "id": "770e4abf-cb35-448d-94b1-9d6f06ecb259",
        "name": "每日早安问候",
        "new_delivery": {
            "mode": "announce",
            "channel": "dingtalk-connector",
            "to": "manager7367"
        }
    },
    {
        "id": "d4345282-580f-420b-a9ad-4ca789140231",
        "name": "早上9点问候",
        "new_delivery": {
            "mode": "announce",
            "channel": "dingtalk-connector",
            "to": "manager7367"
        }
    }
]

def update_cron_tasks():
    # 备份原文件
    with open(cron_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建备份
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已创建备份: {backup_file}")
    
    # 更新任务
    updated_count = 0
    for job in data.get("jobs", []):
        for task in tasks_to_update:
            if job.get("id") == task["id"]:
                print(f"更新任务: {job.get('name')} ({job.get('id')})")
                
                # 更新delivery配置
                job["delivery"] = task["new_delivery"]
                
                # 重置错误状态
                if "state" in job:
                    job["state"]["lastStatus"] = "pending"
                    job["state"]["lastRunStatus"] = "pending"
                    job["state"]["lastError"] = None
                    job["state"]["consecutiveErrors"] = 0
                
                updated_count += 1
                break
    
    # 保存更新后的文件
    with open(cron_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated_count} 个任务到钉钉通道")
    print("更新后的配置:")
    for task in tasks_to_update:
        print(f"  - {task['name']}: 钉钉 -> manager7367")
    
    return updated_count

if __name__ == "__main__":
    if not os.path.exists(cron_file):
        print(f"错误: 找不到cron配置文件 {cron_file}")
        exit(1)
    
    try:
        updated = update_cron_tasks()
        if updated == len(tasks_to_update):
            print("\n🎉 所有任务更新成功！")
        else:
            print(f"\n⚠️  只更新了 {updated}/{len(tasks_to_update)} 个任务")
    except Exception as e:
        print(f"错误: {e}")
        exit(1)