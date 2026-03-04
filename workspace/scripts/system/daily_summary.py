#!/usr/bin/env python3
"""
每日总结脚本
自动生成当天的工作总结报告
"""

import os
import json
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/admin/openclaw/workspace/logs/system/daily_summary.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DailySummary")

def generate_daily_summary():
    """生成每日总结"""
    workspace_path = "/home/admin/openclaw/workspace"
    memory_dir = os.path.join(workspace_path, "memory")
    
    # 获取今天的日期
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    
    summary = {
        "date": today_str,
        "generated_at": datetime.now().isoformat(),
        "tasks_completed": [],
        "tasks_in_progress": [],
        "issues_found": [],
        "next_day_plan": [],
        "metrics": {}
    }
    
    # 读取今天的记忆文件
    today_memory_file = os.path.join(memory_dir, f"{today_str}.md")
    if os.path.exists(today_memory_file):
        try:
            with open(today_memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取任务信息（简单解析）
            lines = content.split('\n')
            for line in lines:
                if "✅" in line or "完成" in line:
                    summary["tasks_completed"].append(line.strip())
                elif "🔄" in line or "进行中" in line:
                    summary["tasks_in_progress"].append(line.strip())
                elif "⚠️" in line or "问题" in line:
                    summary["issues_found"].append(line.strip())
                    
        except Exception as e:
            logger.error(f"读取今日记忆文件失败: {e}")
    
    # 检查监控卫士任务
    guardian_file = os.path.join(workspace_path, "data", "guardian_tasks.json")
    if os.path.exists(guardian_file):
        try:
            with open(guardian_file, 'r', encoding='utf-8') as f:
                guardian_data = json.load(f)
            
            # 统计任务
            running_tasks = 0
            completed_today = 0
            
            for task_id, task in guardian_data.items():
                if task.get("status") == "running":
                    running_tasks += 1
                elif task.get("status") == "completed":
                    # 检查是否是今天完成的
                    if "completed" in task:
                        completed_time = datetime.fromisoformat(task["completed"])
                        if completed_time.date() == today.date():
                            completed_today += 1
            
            summary["metrics"]["guardian_running_tasks"] = running_tasks
            summary["metrics"]["guardian_completed_today"] = completed_today
            
        except Exception as e:
            logger.error(f"读取监控卫士数据失败: {e}")
    
    # 生成总结报告
    report = generate_summary_report(summary)
    
    # 保存总结
    summary_file = os.path.join(memory_dir, f"summary_{today_str}.json")
    try:
        os.makedirs(os.path.dirname(summary_file), exist_ok=True)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"每日总结已保存: {summary_file}")
    except Exception as e:
        logger.error(f"保存总结文件失败: {e}")
    
    return report

def generate_summary_report(summary):
    """生成可读的总结报告"""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append(f"📊 每日工作总结 - {summary['date']}")
    report_lines.append("=" * 60)
    
    # 已完成任务
    if summary["tasks_completed"]:
        report_lines.append("\n✅ 今日完成的任务:")
        for i, task in enumerate(summary["tasks_completed"][:10], 1):
            report_lines.append(f"  {i}. {task}")
    else:
        report_lines.append("\n📝 今日没有记录完成的任务")
    
    # 进行中任务
    if summary["tasks_in_progress"]:
        report_lines.append("\n🔄 进行中的任务:")
        for i, task in enumerate(summary["tasks_in_progress"][:5], 1):
            report_lines.append(f"  {i}. {task}")
    
    # 发现的问题
    if summary["issues_found"]:
        report_lines.append("\n⚠️ 发现的问题:")
        for i, issue in enumerate(summary["issues_found"][:5], 1):
            report_lines.append(f"  {i}. {issue}")
    
    # 监控指标
    if summary["metrics"]:
        report_lines.append("\n📈 监控指标:")
        for key, value in summary["metrics"].items():
            if "guardian" in key:
                display_key = key.replace("guardian_", "").replace("_", " ").title()
                report_lines.append(f"  • {display_key}: {value}")
    
    # 明日计划建议
    report_lines.append("\n🎯 明日计划建议:")
    if summary["tasks_in_progress"]:
        report_lines.append("  1. 继续完成进行中的任务")
    if summary["issues_found"]:
        report_lines.append("  2. 处理发现的问题")
    report_lines.append("  3. 检查监控卫士任务状态")
    report_lines.append("  4. 更新工作空间文档")
    
    report_lines.append("\n" + "=" * 60)
    report_lines.append(f"生成时间: {summary['generated_at']}")
    report_lines.append("=" * 60)
    
    return "\n".join(report_lines)

def main():
    """主函数"""
    logger.info("开始生成每日总结...")
    
    try:
        report = generate_daily_summary()
        print(report)
        logger.info("每日总结生成完成")
        
        # 保存文本报告
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = f"/home/admin/openclaw/workspace/memory/summary_{today}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"总结报告已保存: {report_file}")
        
    except Exception as e:
        logger.error(f"生成每日总结失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())