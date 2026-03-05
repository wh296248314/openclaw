#!/bin/bash
# 快速检查Issue #32400状态

echo "🔍 检查OpenClaw Issue #32400状态..."
echo "问题: Control UI hangs when WebSocket disconnects during long streaming responses"
echo "链接: https://github.com/openclaw/openclaw/issues/32400"
echo ""

# 获取issue信息
response=$(curl -s -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/openclaw/openclaw/issues/32400" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "❌ 无法连接到GitHub API"
    exit 1
fi

# 解析信息
title=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('title', 'N/A'))")
state=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('state', 'N/A'))")
updated_at=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('updated_at', 'N/A'))")
comments=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('comments', 0))")
created_at=$(echo "$response" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('created_at', 'N/A'))")

# 显示状态
echo "📋 Issue信息:"
echo "   标题: $title"
echo "   状态: $( [ "$state" = "open" ] && echo "🟢 开放中" || echo "🔴 已关闭" ) ($state)"
echo "   创建时间: ${created_at:0:10}"
echo "   最后更新: ${updated_at:0:10}"
echo "   评论数量: $comments"
echo ""

# 状态解读
if [ "$state" = "open" ]; then
    echo "📢 状态解读:"
    echo "   • 问题仍在开放状态，等待修复"
    echo "   • 开发团队已知晓此问题"
    echo "   • 建议定期检查更新"
    echo ""
    echo "💡 建议操作:"
    echo "   1. 在GitHub页面点击'Subscribe'按钮订阅更新"
    echo "   2. 关注OpenClaw新版本发布"
    echo "   3. 使用我们配置的自动重启作为临时解决方案"
else
    echo "🎉 好消息!"
    echo "   • Issue已关闭，问题可能已修复"
    echo "   • 建议升级到最新版OpenClaw"
    echo ""
    echo "🚀 建议操作:"
    echo "   1. 运行: openclaw --version 检查当前版本"
    echo "   2. 运行: npm update -g openclaw 升级"
    echo "   3. 测试Control UI是否还卡住"
fi

echo ""
echo "📊 详细页面: https://github.com/openclaw/openclaw/issues/32400"