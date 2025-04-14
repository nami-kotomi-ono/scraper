from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
from app.config.settings import get_settings
from app.services.scraper_service import scrape_and_analyze
from app.models.exceptions import ScraperError, DataValidationError
from typing import Optional, Dict, Any

router = APIRouter()
settings = get_settings()

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
            return JSONResponse(
                status_code=400,
                content={
                    "analysis": None,
                    "error": "キーワードが指定されていません",
                    "filename": None
                }
            )
            
        result = await scrape_and_analyze(request.keyword)
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except DataValidationError as e:
        return JSONResponse(
            status_code=400,
            content={
                "analysis": None,
                "error": str(e),
                "filename": None
            }
        )
    except ScraperError as e:
        return JSONResponse(
            status_code=500,
            content={
                "analysis": None,
                "error": str(e),
                "filename": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "analysis": None,
                "error": f"予期せぬエラーが発生しました: {str(e)}",
                "filename": None
            }
        )

@router.get("/download/{filename}")
async def download_csv(filename: str):
    """CSVファイルをダウンロードするエンドポイント"""
    try:
        file_path = Path(settings.results_dir) / filename
        
        if not file_path.exists():
            return JSONResponse(
                status_code=404,
                content={
                    "error": f"ファイルが見つかりません: {filename}"
                }
            )
            
        return FileResponse(
            path=str(file_path),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"ファイルのダウンロード中にエラーが発生しました: {str(e)}"
            }
        ) 