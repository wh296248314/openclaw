# HunyuanOCR Docker 部署方案
# 腾讯混元OCR - 基于官方标准部署方式
# ⚠️ 注意：由于网络限制，以下内容基于腾讯官方公开资料 + OCR 部署最佳实践
#       如需精确官方配置，请通过国内网络访问 github.com/Tencent/HunyuanOCR

## 📦 部署架构

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                  │
│  (Build & Push Docker Image → Deploy to Local Host)     │
└─────────────────┬───────────────────────────────────────┘
                  │ push / manual trigger
                  ▼
┌─────────────────────────────────────────────────────────┐
│              Docker Registry (GHCR/DockerHub)            │
│                 hunyuan-ocr:latest                       │
└─────────────────┬───────────────────────────────────────┘
                  │ docker pull
                  ▼
┌─────────────────────────────────────────────────────────┐
│              Local Host (Docker Engine)                  │
│            hunyuan-ocr container                        │
│    ┌──────────────────────────────────────────┐        │
│    │  FastAPI server (port 8000)               │        │
│    │  HunyuanOCR inference engine               │        │
│    │  CUDA GPU support (optional)              │        │
│    └──────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## 🔧 前置条件

- Docker Engine >= 20.10
- (可选) NVIDIA GPU + nvidia-docker2 运行时
- GitHub account + repository
- (国内构建) Docker Hub / 阿里云镜像仓库

## 📁 交付文件清单

```
hunyuan-ocr-docker/
├── Dockerfile                          # Docker镜像构建
├── docker-compose.yml                  # 容器编排配置
├── docker-compose.gpu.yml              # GPU版本编排配置
├── .env.example                        # 环境变量示例
├── scripts/
│   ├── build.sh                        # 本机构建脚本
│   ├── run.sh                          # 本机运行脚本
│   └── health_check.sh                 # 健康检查脚本
├── api/
│   └── server.py                       # FastAPI 推理服务
├── .github/
│   └── workflows/
│       └── ci.yml                      # GitHub Actions CI/CD流水线
└── README.md                           # 部署说明文档
```
