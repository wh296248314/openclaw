# 每日总结机制说明

## 🎯 功能概述
每日总结机制是一个自动化系统，每天21:00自动生成当天的工作总结报告。

## 📁 文件结构

### 核心脚本
```
scripts/system/daily_summary.py          # 主总结脚本
scripts/system/add_daily_summary_cron.py # Cron任务添加脚本
```

### 输出文件
```
memory/summary_YYYY-MM-DD.json          # JSON格式总结数据
memory/summary_YYYY-MM-DD.txt           # 可读文本总结报告
logs/system/daily_summary.log           # 运行日志
```

### Cron配置
- 位置：`~/.openclaw/cron/jobs.json`
- 任务名称：`每日总结 - 21:00`
- 执行时间：每天21:00 (Asia/Shanghai)

## 🔧 工作机制

### 1. 数据收集
- 读取当天的记忆文件 (`memory/YYYY-MM-DD.md`)
- 分析监控卫士任务数据 (`data/guardian_tasks.json`)
- 提取任务状态和进度信息

### 2. 总结生成
- **已完成任务**：标记为✅的项目
- **进行中任务**：标记为🔄的项目  
- **发现问题**：标记为⚠️的项目
- **监控指标**：监控卫士任务统计
- **明日计划**：基于当前状态的建议

### 3. 输出格式
#### 文本报告 (`summary_YYYY-MM-DD.txt`)
```
============================================================
📊 每日工作总结 - 2026-03-04
============================================================

✅ 今日完成的任务:
  1. 任务1描述
  2. 任务2描述

🔄 进行中的任务:
  1. 任务1描述

⚠️ 发现的问题:
  1. 问题1描述

📈 监控指标:
  • Running Tasks: 5
  • Completed Today: 3

🎯 明日计划建议:
  1. 继续完成进行中的任务
  2. 处理发现的问题
  3. 检查监控卫士任务状态
  4. 更新工作空间文档

============================================================
生成时间: 2026-03-04T21:00:00.000000
============================================================
```

#### JSON数据 (`summary_YYYY-MM-DD.json`)
```json
{
  "date": "2026-03-04",
  "generated_at": "2026-03-04T21:00:00.000000",
  "tasks_completed": ["任务1", "任务2"],
  "tasks_in_progress": ["任务3"],
  "issues_found": ["问题1"],
  "next_day_plan": ["建议1", "建议2"],
  "metrics": {
    "guardian_running_tasks": 5,
    "guardian_completed_today": 3
  }
}
```

## 🚀 使用方法

### 手动执行
```bash
cd /home/admin/openclaw/workspace
python3 scripts/system/daily_summary.py
```

### 自动执行
- 系统会在每天21:00自动执行
- 通过OpenClaw cron系统调度
- 结果自动保存到memory目录

### 查看历史总结
```bash
# 查看今日总结
cat memory/summary_$(date +%Y-%m-%d).txt

# 查看所有总结文件
ls -la memory/summary_*.txt
```

## ⚙️ 配置选项

### 修改执行时间
编辑cron任务表达式：
- 当前：`0 21 * * *` (每天21:00)
- 修改为：`0 22 * * *` (每天22:00)

### 自定义总结内容
编辑`scripts/system/daily_summary.py`：
- 修改`generate_summary_report()`函数调整输出格式
- 修改`generate_daily_summary()`函数调整数据收集逻辑

## 🔍 故障排除

### 问题：总结未生成
1. 检查cron任务状态：
   ```bash
   grep "每日总结" ~/.openclaw/cron/jobs.json
   ```
2. 检查日志：
   ```bash
   tail -f logs/system/daily_summary.log
   ```
3. 手动测试：
   ```bash
   python3 scripts/system/daily_summary.py
   ```

### 问题：数据不准确
1. 确保记忆文件格式正确
2. 检查监控卫士数据文件
3. 验证脚本解析逻辑

## 📈 扩展功能

### 计划中的改进
1. **邮件通知**：将总结发送到邮箱
2. **钉钉推送**：推送到钉钉工作群
3. **数据可视化**：生成图表报告
4. **周度汇总**：自动生成周度报告

### 集成建议
- 与监控卫士深度集成
- 与工作空间管理工具结合
- 支持自定义模板

---
*最后更新：2026-03-04 每日总结机制测试完成*