"""
HunyuanOCR FastAPI 推理服务
腾讯混元OCR Docker部署 - API服务层
"""
import os
import io
import time
import logging
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from PIL import Image
import numpy as np
import cv2

from loguru import logger

# ---- 配置 ----
class Settings(BaseSettings):
    model_name: str = Field(default="Tencent/HunyuanOCR", env="MODEL_NAME")
    model_cache_dir: str = Field(default="/models", env="MODEL_CACHE_DIR")
    device: str = Field(default="cuda", env="DEVICE")
    port: int = Field(default=8000, env="PORT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# ---- 日志配置 ----
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level,
)

# ---- 全局模型变量 ----
ocr_pipeline = None
model_loaded = False

# ---- 启动 & 关闭 ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ocr_pipeline, model_loaded
    logger.info(f"🚀 启动 HunyuanOCR 服务...")
    logger.info(f"   模型: {settings.model_name}")
    logger.info(f"   设备: {settings.device}")
    logger.info(f"   模型缓存: {settings.model_cache_dir}")

    try:
        # 设置 HuggingFace 镜像 (国内加速)
        os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
        os.environ.setdefault("HF_HOME", settings.model_cache_dir)

        logger.info("📥 正在加载 HunyuanOCR 模型 (首次可能需要几分钟)...")

        # 动态导入，实际部署时可改为具体导入
        try:
            from hunyuan_ocr import HunyuanOCR
            ocr_pipeline = HunyuanOCR()
            logger.info("✅ HunyuanOCR 模型加载成功 (hunyuan_ocr 包)")
        except ImportError:
            # fallback: 使用 transformers 通用加载方式
            logger.info("hunyuan_ocr 未安装，尝试 transformers 方式加载...")
            from transformers import pipeline
            ocr_pipeline = pipeline(
                "ocr",
                model=settings.model_name,
                device=settings.device,
                cache_dir=settings.model_cache_dir,
            )
            logger.info("✅ HunyuanOCR 模型加载成功 (transformers)")

        model_loaded = True
        logger.info("✅ 服务就绪，监听端口 {}".format(settings.port))

    except Exception as e:
        logger.error(f"❌ 模型加载失败: {e}")
        logger.error("⚠️  服务将以有限功能模式启动 (健康检查 /health 可用)")
        model_loaded = False

    yield

    logger.info("🛑 关闭 HunyuanOCR 服务...")

# ---- FastAPI 应用 ----
app = FastAPI(
    title="HunyuanOCR API",
    description="腾讯混元OCR Docker部署 - REST API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- 请求/响应模型 ----
class OCRResult(BaseModel):
    text: str
    confidence: float
    bounding_box: Optional[dict] = None

class OCRResponse(BaseModel):
    success: bool
    request_id: str
    elapsed_ms: float
    image_size: Optional[dict] = None
    results: List[OCRResult]

# ---- 路由 ----

@app.get("/")
async def root():
    return {
        "service": "HunyuanOCR",
        "version": "1.0.0",
        "status": "running" if model_loaded else "model_not_loaded",
        "model": settings.model_name,
        "device": settings.device,
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "device": settings.device,
    }

@app.post("/ocr", response_model=OCRResponse)
async def ocr_image(file: UploadFile = File(...)):
    """OCR识别 - 单张图片"""
    import uuid
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    if not model_loaded or ocr_pipeline is None:
        raise HTTPException(status_code=503, detail="模型未加载，服务暂不可用")

    # 读取图片
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"图片读取失败: {e}")

    image_size = {"width": image.width, "height": image.height}

    try:
        # 调用OCR
        ocr_results = ocr_pipeline(image)

        results = []
        if isinstance(ocr_results, list):
            for item in ocr_results:
                if isinstance(item, dict):
                    results.append(OCRResult(
                        text=item.get("text", ""),
                        confidence=float(item.get("score", item.get("confidence", 1.0))),
                        bounding_box=item.get("bbox"),
                    ))
                else:
                    results.append(OCRResult(text=str(item), confidence=1.0))
        elif isinstance(ocr_results, dict):
            for line in ocr_results.get("text", ocr_results.get("lines", [])):
                results.append(OCRResult(
                    text=line.get("text", ""),
                    confidence=float(line.get("score", 1.0)),
                    bounding_box=line.get("bbox"),
                ))

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] OCR完成: {len(results)} 个文本区域, 耗时 {elapsed_ms:.1f}ms")

        return OCRResponse(
            success=True,
            request_id=request_id,
            elapsed_ms=round(elapsed_ms, 2),
            image_size=image_size,
            results=results,
        )

    except Exception as e:
        logger.error(f"[{request_id}] OCR处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"OCR处理失败: {e}")

@app.post("/ocr/batch")
async def ocr_batch(files: List[UploadFile] = File(...)):
    """批量OCR识别"""
    import uuid
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    if not model_loaded or ocr_pipeline is None:
        raise HTTPException(status_code=503, detail="模型未加载")

    results = []
    for i, file in enumerate(files):
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            ocr_result = ocr_pipeline(image)
            results.append({"index": i, "filename": file.filename, "data": ocr_result})
        except Exception as e:
            results.append({"index": i, "filename": file.filename, "error": str(e)})

    elapsed_ms = (time.time() - start_time) * 1000
    return {
        "success": True,
        "request_id": request_id,
        "elapsed_ms": round(elapsed_ms, 2),
        "total": len(files),
        "results": results,
    }

@app.post("/ocr/url")
async def ocr_from_url(text: str = Form(...)):
    """从URL获取图片进行OCR"""
    import uuid
    import requests as req
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    if not model_loaded or ocr_pipeline is None:
        raise HTTPException(status_code=503, detail="模型未加载")

    try:
        response = req.get(text, timeout=15)
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        ocr_results = ocr_pipeline(image)
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": True,
            "request_id": request_id,
            "elapsed_ms": round(elapsed_ms, 2),
            "results": ocr_results,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"URL图片获取失败: {e}")

# ---- 启动 (直接运行) ----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port, log_level="info")
