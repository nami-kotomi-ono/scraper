from fastapi import FastAPI
from app.api.items import router as items_router
import logging

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

# ルーターの登録
app.include_router(items_router, prefix="/api/v1", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Mercari Scraper API is running"} 