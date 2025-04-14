from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.items import router as items_router
from app.config.settings import get_settings
import logging

# 設定を取得
settings = get_settings()

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Mercari Scraper API",
    description="メルカリの商品をスクレイピングするAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# ルーターの登録
app.include_router(items_router, prefix="/api/v1", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Mercari Scraper API is running"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # リクエストパスからAPIエンドポイントを判定
    path = request.url.path
    
    if path.startswith("/api/v1/search"):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "analysis": None,
                "error": exc.detail,
                "filename": None
            }
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail
            }
        )