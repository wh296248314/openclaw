#!/bin/bash
# 设置Issue #32400监控

echo "🛠️ 设置OpenClaw Issue #32400监控系统"
echo "======================================"

# 1. 创建监控目录
MONITOR_DIR="/home/admin/openclaw/workspace/monitoring"
mkdir -p "$MONITOR_DIR"

# 2. 复制监控脚本
cp /home/admin/openclaw/workspace/check-issue-32400.sh "$MONITOR_DIR/"
cp /home/admin/openclaw/workspace/monitor-issue-32400.sh "$MONITOR_DIR/"

echo "✅ 监控脚本已复制到: $MONITOR_DIR"

# 3. 设置cron任务（每天检查一次）
CRON_JOB="0 9 * * * /bin/bash $MONITOR_DIR/check-issue-32400.sh >> $MONITOR_DIR/issue-check.log 2>&1"

# 检查是否已存在cron任务
if crontab -l 2>/dev/null | grep -q "check-issue-32400.sh"; then
    echo "📅 Cron任务已存在"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "📅 已添加cron任务: 每天09:00检查issue状态"
fi

# 4. 创建状态文件
cat > "$MONITOR_DIR/issue-status.md" << 'EOF'
# OpenClaw Issue #32400 监控状态

## 问题描述
**标题**: [Bug]: Control UI hangs when WebSocket disconnects during long streaming responses  
**链接**: https://github.com/openclaw/openclaw/issues/32400  
**创建时间**: 2026-03-03  
**最后检查**: $(date '+%Y-%m-%d %H:%M:%S')

## 问题症状
- Control UI在WebSocket断开时卡住
- 需要刷新浏览器才能恢复
- 影响用户体验和工作效率

## 临时解决方案
1. ✅ 网关自动重启 (systemd Restart=always)
2. ✅ 插件冲突清理 (飞书插件重新安装)
3. ✅ 系统监控配置

## 监控命令
```bash
# 手动检查issue状态
bash /home/admin/openclaw/workspace/check-issue-32400.sh

# 查看监控日志
tail -f /home/admin/openclaw/workspace/monitoring/issue-check.log
```

## 升级提醒
当issue状态变为"closed"时，建议：
1. 检查OpenClaw新版本
2. 运行: `npm update -g openclaw`
3. 测试Control UI是否修复
EOF

echo "📝 状态文档已创建: $MONITOR_DIR/issue-status.md"

# 5. 显示设置完成
echo ""
echo "🎯 监控系统设置完成!"
echo ""
echo "可用命令:"
echo "1. 检查issue状态: bash $MONITOR_DIR/check-issue-32400.sh"
echo "2. 实时监控: bash $MONITOR_DIR/monitor-issue-32400.sh"
echo "3. 查看日志: tail -f $MONITOR_DIR/issue-check.log"
echo ""
echo "📅 Cron任务: 每天09:00自动检查"
echo "📊 状态文档: $MONITOR_DIR/issue-status.md"
echo ""
echo "💡 建议: 定期运行检查命令，关注issue状态变化"