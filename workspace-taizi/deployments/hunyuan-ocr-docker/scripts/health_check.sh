#!/bin/bash
# ============================================================
# health_check.sh - HunyuanOCR 健康检查脚本
# ============================================================
set -e

HOST=${1:-"localhost"}
PORT=${2:-"8000"}
TIMEOUT=5

echo "=========================================="
echo "  HunyuanOCR 健康检查"
echo "  目标: $HOST:$PORT"
echo "=========================================="

# 检查端口
if ! nc -z -w$TIMEOUT $HOST $PORT 2>/dev/null; then
    echo "❌ 端口 $PORT 未开放"
    exit 1
fi

# 检查健康端点
HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "http://$HOST:$PORT/health" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 健康检查通过 (HTTP $HTTP_CODE)"

    # 获取详细信息
    RESPONSE=$(curl -sf --max-time $TIMEOUT "http://$HOST:$PORT/health" 2>/dev/null)
    echo ""
    echo "服务详情:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 0
elif [ "$HTTP_CODE" = "503" ]; then
    echo "⚠️  服务响应，但模型未加载 (HTTP 503)"
    echo "   可能原因: 首次启动正在下载模型，请稍候..."
    exit 1
else
    echo "❌ 健康检查失败 (HTTP $HTTP_CODE)"
    exit 1
fi
