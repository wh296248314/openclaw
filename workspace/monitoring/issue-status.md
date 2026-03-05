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
