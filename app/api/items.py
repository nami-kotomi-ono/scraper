from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.scraper import scrape_items, setup_results_dir
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    keyword: str

@router.post("/search")
async def search_items(request: SearchRequest):
    """メルカリで商品を検索し、CSVファイルを返すエンドポイント"""
    try:
        # スクレイピングを実行
        await scrape_items(request.keyword)
        
        # 保存されたCSVファイルのパスを取得
        results_dir = setup_results_dir()
        file_path = results_dir / f"{request.keyword}.csv"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            path=str(file_path),
            media_type="text/csv",
            filename=f"{request.keyword}.csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 