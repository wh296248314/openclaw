#!/bin/bash
# 部署专家学习任务 - 定时执行技能搜索

WORKDIR="/home/pixiu/.openclaw/workspace/experts/deployment-xiaopi"
LOGFILE="$WORKDIR/learning/learning.log"
CLAWHUB="/home/pixiu/.npm-global/bin/clawhub"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOGFILE
}

# 获取今天是周几 (0=周日, 6=周六)
WEEKDAY=$(date +%w)
DAY_OF_MONTH=$(date +%d)

log "=== 开始学习任务 ==="

# P0领域 - 每周六执行
if [ "$WEEKDAY" = "6" ]; then
    log "执行P0领域搜索 (运维自动化, 监控系统)"
    
    # 搜索运维自动化
    $CLAWHUB search automation --limit 10 >> $LOGFILE 2>&1
    $CLAWHUB search monitoring --limit 10 >> $LOGFILE 2>&1
    
    log "P0领域搜索完成"
fi

# P1领域 - 隔周六执行 (第2、4周)
if [ "$WEEKDAY" = "6" ] && [ $(($(date +%-U) % 2)) -eq 0 ]; then
    log "执行P1领域搜索 (安全合规)"
    
    $CLAWHUB search security --limit 10 >> $LOGFILE 2>&1
    
    log "P1领域搜索完成"
fi

# P2领域 - 每月最后一天
if [ "$DAY_OF_MONTH" = "$(date -d "+1 month -1 day" +%d)" ]; then
    log "执行P2领域搜索 + 汇总报告"
    
    $CLAWHUB search kubernetes --limit 10 >> $LOGFILE 2>&1
    $CLAWHUB search docker --limit 10 >> $LOGFILE 2>&1
    
    log "P2领域搜索完成，生成汇总报告"
fi

log "=== 学习任务结束 ==="
