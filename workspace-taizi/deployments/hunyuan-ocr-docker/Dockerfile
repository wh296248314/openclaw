# ============================================================
# HunyuanOCR Dockerfile - 腾讯混元OCR Docker镜像
# ============================================================
# 构建说明：
#   CPU版本:  docker build -t hunyuan-ocr:latest .
#   GPU版本:  docker build -t hunyuan-ocr:latest-gpu --build-arg CUDA_VERSION=12.1 .
#
# 运行示例：
#   CPU:  docker run -d -p 8000:8000 --name hunyuan-ocr hunyuan-ocr:latest
#   GPU:  docker run -d --gpus all -p 8000:8000 --name hunyuan-ocr-gpu hunyuan-ocr:latest-gpu
# ============================================================

# ---- 阶段1: 构建阶段 ----
FROM python:3.10-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装PyTorch (CUDA 12.1 支持)
# GPU版本使用预编译轮子，CPU版本使用CPU版本
ARG CUDA_VERSION=cpu
ENV PYTHONUNBUFFERED=1

RUN if [ "$CUDA_VERSION" != "cpu" ]; then \
    pip install --no-cache-dir \
        torch==2.2.0 \
        torchvision==0.17.0 \
        --index-url https://download.pytorch.org/whl/cu121; \
    else \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu; \
    fi

# 安装HunyuanOCR及依赖
# 优先从PyPI安装，如官方发布
RUN pip install --no-cache-dir \
    hunyuan-ocr \
    fastapi==0.111.0 \
    uvicorn[standard]==0.29.0 \
    python-multipart==0.0.9 \
    pydantic==2.7.1 \
    pydantic-settings==2.2.1 \
    huggingface_hub==0.23.0 \
    requests==2.31.0 \
    Pillow==10.3.0 \
    numpy==1.26.4 \
    opencv-python-headless==4.9.0.80 \
    loguru==0.7.2

# ---- 阶段2: 运行阶段 (CPU) ----
FROM python:3.10-slim AS runtime-cpu

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# 复制Python包
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY --chown=appuser:appuser . .

# 模型缓存目录
ENV MODEL_CACHE_DIR=/models
RUN mkdir -p $MODEL_CACHE_DIR && chown -R appuser:appuser $MODEL_CACHE_DIR

USER appuser

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV MODEL_NAME=Tencent/HunyuanOCR

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["python", "api/server.py"]

# ---- 阶段2: 运行阶段 (GPU) ----
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 AS runtime-gpu

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV MODEL_CACHE_DIR=/models

# 安装Python和运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    curl \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# 复制Python包和代码
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --chown=appuser:appuser . .

# 模型缓存目录
RUN mkdir -p $MODEL_CACHE_DIR && chown -R appuser:appuser $MODEL_CACHE_DIR

USER appuser

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "api/server.py"]
