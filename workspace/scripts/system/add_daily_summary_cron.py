#!/usr/bin/env python3
"""
添加每日总结cron任务
"""

import json
import uuid
import os
from datetime import datetime
import sys

def main():
    cron_file = os.path.expanduser("~/.openclaw/cron/jobs.json")
    
    # 备份原文件
    backup_file = f"{cron_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if os.path.exists(cron_file):
        with open(cron_file, 'r', encoding='utf-8') as f:
            original_data = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(original_data)
        print(f"✅ 已备份原cron文件: {backup_file}")
    
    # 读取现有数据
    with open(cron_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查是否已存在每日总结任务
    for job in data.get("jobs", []):
        if "每日总结" in job.get("name", ""):
            print("⚠️  每日总结任务已存在，跳过创建")
            return
    
    # 创建新任务
    new_task = {
        "id": str(uuid.uuid4()),
        "agentId": "main",
        "name": "每日总结 - 21:00",
        "enabled": True,
        "createdAtMs": int(datetime.now().timestamp() * 1000),
        "updatedAtMs": int(datetime.now().timestamp() * 1000),
        "schedule": {
            "kind": "cron",
            "expr": "0 21 * * *",
            "tz": "Asia/Shanghai"
        },
        "sessionTarget": "isolated",
        "wakeMode": "next-heartbeat",
        "payload": {
            "kind": "agentTurn",
            "message": "📊 **每日总结时间**\n\n现在是21:00，开始生成今日工作总结报告。\n\n请执行以下命令生成总结：\n```bash\ncd /home/admin/openclaw/workspace && python3 scripts/system/daily_summary.py\n```\n\n总结报告将保存到：\n- `memory/summary_YYYY-MM-DD.json` (JSON格式)\n- `memory/summary_YYYY-MM-DD.txt` (文本格式)\n\n记得查看今日完成的任务和明日计划建议！"
        },
        "state": {
            "nextRunAtMs": int(datetime.now().replace(hour=21, minute=0, second=0, microsecond=0).timestamp() * 1000),
            "lastRunAtMs": 0,
            "lastStatus": "pending",
            "lastDurationMs": 0
        }
    }
    
    # 添加到jobs数组
    data["jobs"].append(new_task)
    
    # 保存文件
    with open(cron_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ 每日总结cron任务已添加到文件")
    print(f"📅 任务ID: {new_task['id']}")
    print(f"⏰ 执行时间: 每天21:00 (Asia/Shanghai)")
    print(f"📁 总结脚本: /home/admin/openclaw/workspace/scripts/system/daily_summary.py")
    
    # 验证添加
    print("\n🔍 验证添加结果:")
    with open(cron_file, 'r', encoding='utf-8') as f:
        updated_data = json.load(f)
    
    daily_summary_jobs = [j for j in updated_data["jobs"] if "每日总结" in j.get("name", "")]
    print(f"   找到 {len(daily_summary_jobs)} 个每日总结任务")
    for job in daily_summary_jobs:
        print(f"   • {job['name']} (ID: {job['id']})")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 添加cron任务失败: {e}")
        sys.exit(1)