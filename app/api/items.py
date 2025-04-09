from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from app.services.scraper import scrape_items, setup_results_dir
from app.services.price_analysis import analyze_prices, format_price_analysis_to_json
from pydantic import BaseModel
import json
from app.services.csv_saver import save_to_file

router = APIRouter()

class SearchRequest(BaseModel):
    keyword: str

class SearchResponse(BaseModel):
    csv_url: str
    analysis: dict

@router.post("/search", response_model=SearchResponse)
async def search_items(request: SearchRequest):
    """メルカリで商品を検索し、CSVファイルと分析結果を返すエンドポイント"""
    try:
        # スクレイピングを実行
        all_items = await scrape_items(request.keyword)
        
        # 価格分析を実行
        analysis = analyze_prices(all_items)
        analysis_json = format_price_analysis_to_json(analysis)
        
        # 分析結果をCSVに追記
        save_to_file(
            data=all_items,
            keyword=request.keyword,
            is_last_page=True,
            analysis=analysis
        )
            
        return {
            "csv_url": f"/api/v1/download/{request.keyword}.csv",
            "analysis": analysis_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_csv(filename: str):
    """CSVファイルをダウンロードするエンドポイント"""
    results_dir = setup_results_dir()
    file_path = results_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(
        path=str(file_path),
        media_type="text/csv",
        filename=filename
    ) 