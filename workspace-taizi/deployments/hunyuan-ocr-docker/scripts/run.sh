#!/bin/bash
# ============================================================
# run.sh - HunyuanOCR 本机运行脚本
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  HunyuanOCR 本机启动"
echo "=========================================="

# 参数解析
MODE=${1:-"cpu"}  # cpu / gpu / auto

# 自动检测GPU
if [ "$MODE" = "auto" ]; then
    if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
        MODE="gpu"
        echo "🟢 检测到 NVIDIA GPU，自动使用 GPU 模式"
    else
        MODE="cpu"
        echo "⚪ 未检测到 GPU，使用 CPU 模式"
    fi
fi

# 启动
if [ "$MODE" = "gpu" ]; then
    echo "🚀 启动 GPU 版本..."
    docker-compose -f "$PROJECT_DIR/docker-compose.gpu.yml" up -d
    echo ""
    echo "✅ GPU 容器已启动"
    echo "   API: http://localhost:8000"
    echo "   健康检查: curl http://localhost:8000/health"
else
    echo "🚀 启动 CPU 版本..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d
    echo ""
    echo "✅ CPU 容器已启动"
    echo "   API: http://localhost:8000"
    echo "   健康检查: curl http://localhost:8000/health"
fi

# 等待就绪
echo ""
echo "⏳ 等待服务就绪 (首次启动需下载模型，约1-5分钟)..."
for i in {1..30}; do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo ""
        echo "🎉 服务已就绪！"
        echo ""
        echo "测试OCR接口:"
        echo '  curl -X POST http://localhost:8000/ocr \\'
        echo '    -F "file=@your_image.png"'
        echo ""
        echo "停止服务:"
        echo "  docker-compose -f $PROJECT_DIR/docker-compose.yml down"
        exit 0
    fi
    echo -n "."
    sleep 5
done

echo ""
echo "⚠️  服务启动可能需要更长时间，首次运行请检查日志:"
echo "  docker logs hunyuan-ocr-cpu"
echo "  docker logs hunyuan-ocr-gpu"
