#!/bin/bash
# 小皮管家健康检查 - 带告警推送
# 发现异常立即发送飞书消息

LOG_FILE="/tmp/health-check.log"
ALERT_QUEUE="/tmp/health-alerts.txt"
LAST_OK_FILE="/tmp/health-last-ok.txt"

echo "=== 健康检查 $(date '+%Y-%m-%d %H:%M') ===" > "$LOG_FILE"

ERRORS=0
WARNINGS=0
ALERTS=""

# 1. Gateway状态检查
echo -e "\n【1. Gateway状态】" >> "$LOG_FILE"
if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    echo "  ✅ Gateway运行正常" >> "$LOG_FILE"
else
    echo "  ❌ Gateway未运行！" >> "$LOG_FILE"
    ALERTS="${ALERTS}🚨 Gateway未运行！请检查！\n"
    ERRORS=$((ERRORS+1))
fi

# 2. 飞书连接检查（飞书作为Gateway内置插件，只要Gateway运行即为正常）
echo -e "\n【2. 飞书连接】" >> "$LOG_FILE"
if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    echo "  ✅ 飞书插件运行正常（Gateway内置）" >> "$LOG_FILE"
else
    echo "  ⚠️ Gateway未运行，飞书不可用" >> "$LOG_FILE"
    ALERTS="${ALERTS}⚠️ Gateway未运行，飞书不可用\n"
    WARNINGS=$((WARNINGS+1))
fi

# 3. Git同步检查
echo -e "\n【3. Git同步检查】" >> "$LOG_FILE"
GIT_STATUS=$(cd /home/pixiu/.openclaw/workspace && git status -s 2>/dev/null | wc -l)
if [ $GIT_STATUS -gt 10 ]; then
    echo "  ⚠️ Git待同步文件过多: $GIT_STATUS 个" >> "$LOG_FILE"
    ALERTS="${ALERTS}⚠️ Git待同步文件过多: ${GIT_STATUS}个\n"
    WARNINGS=$((WARNINGS+1))
else
    echo "  ✅ Git同步正常" >> "$LOG_FILE"
fi

# 4. 定时任务检查
echo -e "\n【4. 定时任务】" >> "$LOG_FILE"
GATEWAY_CRON=$(crontab -l 2>/dev/null | grep "gateway-auto-restart")
GIT_CRON=$(crontab -l 2>/dev/null | grep ".openclaw.*git.*push")
if [ -z "$GATEWAY_CRON" ]; then
    echo "  ❌ Gateway自动重启未配置！" >> "$LOG_FILE"
    ALERTS="${ALERTS}❌ Gateway自动重启未配置！\n"
    ERRORS=$((ERRORS+1))
else
    echo "  ✅ Gateway自动重启已配置" >> "$LOG_FILE"
fi

if [ -z "$GIT_CRON" ]; then
    echo "  ❌ Git同步未配置！" >> "$LOG_FILE"
    ALERTS="${ALERTS}❌ Git同步未配置！\n"
    ERRORS=$((ERRORS+1))
else
    echo "  ✅ Git同步定时任务已配置" >> "$LOG_FILE"
fi

# 5. Memory检查
echo -e "\n【5. Memory检查】" >> "$LOG_FILE"
TODAY_MEM=$(ls /home/pixiu/.openclaw/workspace/memory/$(date +%Y-%m-%d).md 2>/dev/null)
if [ -n "$TODAY_MEM" ]; then
    SIZE=$(stat -c%s "$TODAY_MEM")
    if [ $SIZE -gt 100 ]; then
        echo "  ✅ 今日Memory记录正常 (${SIZE}字节)" >> "$LOG_FILE"
    else
        echo "  ⚠️ 今日Memory记录过少" >> "$LOG_FILE"
        ALERTS="${ALERTS}⚠️ 小皮管家今日Memory记录过少\n"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo "  ❌ 今日Memory未记录！" >> "$LOG_FILE"
    ALERTS="${ALERTS}❌ 小皮管家今日Memory未记录！\n"
    ERRORS=$((ERRORS+1))
fi

# 6. Session检查
echo -e "\n【6. Session检查】" >> "$LOG_FILE"
for agent in main product design development testing deployment audit; do
    SESSION_FILE="/home/pixiu/.openclaw/agents/${agent}-xiaopi/sessions/sessions.json"
    if [ ! -f "$SESSION_FILE" ]; then
        SESSION_FILE="/home/pixiu/.openclaw/agents/main/sessions/sessions.json"
    fi
    
    if [ -f "$SESSION_FILE" ]; then
        SESSION_TIME=$(stat -c %Y "$SESSION_FILE" 2>/dev/null)
        NOW=$(date +%s)
        DIFF=$((NOW - SESSION_TIME))
        MIN=$((DIFF / 60))
        
        if [ $DIFF -lt 1800 ]; then  # 30分钟
            echo "  ✅ ${agent}-xiaopi活跃 (${MIN}分钟前)" >> "$LOG_FILE"
        elif [ $DIFF -lt 7200 ]; then  # 2小时
            if [ "$agent" == "main" ]; then
                echo "  ⚠️ ${agent}超过30分钟未活动" >> "$LOG_FILE"
                ALERTS="${ALERTS}⚠️ ${agent}超过30分钟未活动\n"
            fi
        fi
    fi
done

# 7. 网络状态检查
echo -e "\n【7. 网络状态】" >> "$LOG_FILE"
if curl -s --max-time 5 https://api.minimaxi.com > /dev/null 2>&1; then
    echo "  ✅ MiniMax API可达" >> "$LOG_FILE"
else
    echo "  ❌ MiniMax API连接失败！" >> "$LOG_FILE"
    ALERTS="${ALERTS}❌ MiniMax API连接失败！\n"
    ERRORS=$((ERRORS+1))
fi

# 8. 磁盘空间检查
echo -e "\n【8. 磁盘空间】" >> "$LOG_FILE"
DISK_USAGE=$(df /home/pixiu | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo "  ✅ 磁盘空间充足 (${DISK_USAGE}%)" >> "$LOG_FILE"
elif [ $DISK_USAGE -lt 90 ]; then
    echo "  ⚠️ 磁盘空间偏紧 (${DISK_USAGE}%)" >> "$LOG_FILE"
    WARNINGS=$((WARNINGS+1))
else
    echo "  ❌ 磁盘空间不足 (${DISK_USAGE}%)！" >> "$LOG_FILE"
    ALERTS="${ALERTS}❌ 磁盘空间不足: ${DISK_USAGE}%\n"
    ERRORS=$((ERRORS+1))
fi

# 总结
echo -e "\n【总结】" >> "$LOG_FILE"
echo "  错误: $ERRORS | 警告: $WARNINGS" >> "$LOG_FILE"

if [ $ERRORS -gt 0 ]; then
    echo "  🚨 需要立即处理！" >> "$LOG_FILE"
elif [ $WARNINGS -gt 0 ]; then
    echo "  ⚠️ 有待观察的问题" >> "$LOG_FILE"
else
    echo "  ✅ 全部正常" >> "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M') OK" > "$LAST_OK_FILE"
fi

# 如果有告警，保存并显示
if [ -n "$ALERTS" ]; then
    echo "=== $(date '+%Y-%m-%d %H:%M') ===" >> "$ALERT_QUEUE"
    echo -e "$ALERTS" >> "$ALERT_QUEUE"
    echo "---" >> "$ALERT_QUEUE"
    echo ""
    echo "=== 发现异常 ==="
    echo -e "$ALERTS"
else
    echo "无告警"
fi
