#!/bin/bash
# ============================================================
# build.sh - HunyuanOCR 本机镜像构建脚本
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  HunyuanOCR 本机镜像构建"
echo "=========================================="

# 参数解析
GPU_MODE=${1:-"cpu"}
TAG=${2:-"hunyuan-ocr:latest"}

# 构建参数
if [ "$GPU_MODE" = "gpu" ]; then
    echo "🔧 构建 GPU 版本 (CUDA 12.1)..."
    DOCKERFILE_TARGET="--target runtime-gpu"
    BUILD_ARGS="--build-arg CUDA_VERSION=12.1"
    TAG="${TAG}-gpu"
else
    echo "🔧 构建 CPU 版本..."
    DOCKERFILE_TARGET="--target runtime-cpu"
    BUILD_ARGS="--build-arg CUDA_VERSION=cpu"
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装或未运行"
    exit 1
fi

# 构建
echo "📦 开始构建镜像: $TAG"
docker build \
    $DOCKERFILE_TARGET \
    $BUILD_ARGS \
    -t "$TAG" \
    -f "$PROJECT_DIR/Dockerfile" \
    "$PROJECT_DIR"

echo ""
echo "✅ 镜像构建完成: $TAG"
echo ""
echo "下一步运行:"
if [ "$GPU_MODE" = "gpu" ]; then
    echo "  docker-compose -f $PROJECT_DIR/docker-compose.gpu.yml up -d"
else
    echo "  docker-compose -f $PROJECT_DIR/docker-compose.yml up -d"
fi
