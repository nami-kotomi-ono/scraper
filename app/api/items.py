from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
import re
from app.config.settings import get_settings
from app.config.logger import setup_logger
from app.services.scraper_service import scrape_and_analyze
from app.models.exceptions import ScraperError, DataValidationError
from typing import Optional, Dict, Any

router = APIRouter()
settings = get_settings()
logger = setup_logger(__name__)

class SearchRequest(BaseModel):
    keyword: str

class SearchResponse(BaseModel):
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    filename: Optional[str] = None

@router.post("/search", response_model=SearchResponse)
async def search_items(request: SearchRequest):
    """メルカリで商品を検索し、分析結果を返すエンドポイント"""
    try:
        if not request.keyword:
            raise HTTPException(status_code=400, detail="キーワードがありません")
            
        result = await scrape_and_analyze(request.keyword)
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except DataValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except ScraperError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予期せぬエラーが発生しました: {str(e)}")

@router.get("/download/{filename}")
async def download_csv(filename: str):
    """CSVファイルをダウンロードするエンドポイント"""
    try:
        # ファイル名の検証
        if not re.match(r'^[\w\-\.]+\.csv$', filename):
            raise HTTPException(
                status_code=400,
                detail="無効なファイル名です"
            )
            
        file_path = Path(settings.results_dir) / filename
        
        # ファイルの存在確認
        if not file_path.exists():
            logger.error(f"ファイルが見つかりません: {filename}")
            raise HTTPException(
                status_code=404,
                detail=f"ファイルが見つかりません: {filename}"
            )
            
        # ファイルサイズの確認（10MB制限）
        if file_path.stat().st_size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="ファイルサイズが大きすぎます"
            )
            
        return FileResponse(
            path=str(file_path),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ファイルのダウンロード中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"ファイルのダウンロード中にエラーが発生しました: {str(e)}"
        ) 
