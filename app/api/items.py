from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from app.services.scraper import scrape_items, setup_results_dir
from app.services.price_analysis import analyze_prices, format_price_analysis_to_json
from pydantic import BaseModel
import json
from app.services.file_manager import save_to_file, cleanup_files
from urllib.parse import quote, unquote
from datetime import datetime, timedelta
from pathlib import Path
from app.config.settings import Settings, get_settings

router = APIRouter()
settings = get_settings()

class SearchRequest(BaseModel):
    keyword: str

class SearchResponse(BaseModel):
    analysis: dict | None = None
    error: str | None = None

@router.post("/search", response_model=SearchResponse)
async def search_items(request: SearchRequest):
    """メルカリで商品を検索し、分析結果を返すエンドポイント"""
    try:
        # 既存のファイルをクリーンアップ
        cleanup_files(request.keyword)
        
        # スクレイピングを実行
        all_items = await scrape_items(request.keyword)
        
        if not all_items:
            return {
                "analysis": None,
                "error": "商品が見つかりませんでした"
            }
        
        # 価格分析を実行
        analysis = analyze_prices(all_items)
        if not analysis:
            return {
                "analysis": None,
                "error": "価格分析に失敗しました"
            }
            
        analysis_json = format_price_analysis_to_json(analysis)
        
        # 分析結果をCSVに追記
        save_to_file(
            data=all_items,
            keyword=request.keyword,
            is_last_page=True,
            analysis=analysis
        )
            
        return {
            "analysis": analysis_json,
            "error": None
        }
    except Exception as e:
        return {
            "analysis": None,
            "error": str(e)
        }

@router.get("/download/{filename}")
async def download_csv(filename: str):
    """CSVファイルをダウンロードするエンドポイント"""
    try:
        # .csv拡張子を追加
        if not filename.endswith('.csv'):
            filename += '.csv'
        file_path = Path(settings.results_dir) / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"ファイルが見つかりません: {filename}"
            )
        # ファイル名をURLエンコード
        encoded_filename = quote(filename)
            
        return FileResponse(
            path=str(file_path),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"ファイルのダウンロード中にエラーが発生しました: {str(e)}"
        ) 