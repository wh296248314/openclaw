#!/bin/bash
# 启动 clash-party 并使用订阅配置
cd ~/.config/mihomo-party

# 复制订阅配置文件到工作目录
cp profiles/19cb15a3055.yaml work/config.yaml

# 启动 clash-party
nohup clash-party > /tmp/clash-party.log 2>&1 &

echo "clash-party 已启动，使用订阅配置"
echo "日志文件: /tmp/clash-party.log"
echo "代理端口: 7890 (HTTP), 7891 (SOCKS)"