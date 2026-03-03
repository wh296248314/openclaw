#!/bin/bash

# 测试Cron时间表脚本
# 模拟每日三次提交的时间检查

echo "=== Obsidian Git 自动提交时间表测试 ==="
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查当前时间是否接近预定时间
CURRENT_HOUR=$(date '+%H')
CURRENT_MINUTE=$(date '+%M')

echo "预定提交时间:"
echo "1. 中午12:00 🕛"
echo "2. 晚上19:00 🌙"
echo "3. 晚上23:00 🌜"
echo ""

# 计算距离下次提交的时间
CURRENT_HOUR_NUM=$(echo $CURRENT_HOUR | sed 's/^0//')
CURRENT_MINUTE_NUM=$(echo $CURRENT_MINUTE | sed 's/^0//')

if [ "$CURRENT_HOUR_NUM" -lt 12 ]; then
    NEXT_TIME="12:00"
    HOURS_REMAINING=$((12 - CURRENT_HOUR_NUM))
    MINUTES_REMAINING=$((60 - CURRENT_MINUTE_NUM))
    echo "下次提交: 中午12:00 (约${HOURS_REMAINING}小时${MINUTES_REMAINING}分钟后)"
elif [ "$CURRENT_HOUR_NUM" -lt 19 ]; then
    NEXT_TIME="19:00"
    HOURS_REMAINING=$((19 - CURRENT_HOUR_NUM))
    MINUTES_REMAINING=$((60 - CURRENT_MINUTE_NUM))
    echo "下次提交: 晚上19:00 (约${HOURS_REMAINING}小时${MINUTES_REMAINING}分钟后)"
elif [ "$CURRENT_HOUR_NUM" -lt 23 ]; then
    NEXT_TIME="23:00"
    HOURS_REMAINING=$((23 - CURRENT_HOUR_NUM))
    MINUTES_REMAINING=$((60 - CURRENT_MINUTE_NUM))
    echo "下次提交: 晚上23:00 (约${HOURS_REMAINING}小时${MINUTES_REMAINING}分钟后)"
else
    NEXT_TIME="明天12:00"
    echo "下次提交: 明天中午12:00"
fi

echo ""
echo "要手动运行提交脚本，请执行: ./auto-commit.sh"
echo "要查看提交日志，请查看: commit-log.md"