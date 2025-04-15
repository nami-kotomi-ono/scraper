from typing import Dict, List, Optional
from app.services.scraper import scrape_items
from app.services.price_analysis import analyze_prices, format_price_analysis_to_json
from app.services.file_manager import save_to_file, cleanup_files
from app.models.exceptions import ScraperError, DataValidationError
from datetime import datetime

async def scrape_and_analyze(keyword: str) -> Dict:
    """スクレイピングと分析を実行するサービス関数
    
    Args:
        keyword (str): 検索キーワード
        
    Returns:
        Dict: 分析結果を含む辞書
        
    Raises:
        ScraperError: スクレイピング処理中のエラー
        DataValidationError: データ検証エラー
    """
    try:
        # タイムスタンプ付きのファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.csv"
        
        # 既存のファイルをクリーンアップ（古いファイルの削除）
        cleanup_files()
        
        # スクレイピングを実行
        all_items = await scrape_items(keyword, filename)
        
        if not all_items:
            raise DataValidationError("商品が見つかりませんでした")
        
        # 価格分析を実行
        analysis = analyze_prices(all_items)
        if not analysis:
            raise DataValidationError("価格分析に失敗しました")
            
        # 分析結果をJSON形式に変換
        analysis_json = format_price_analysis_to_json(analysis)
        
        # 分析結果をCSVに追記
        save_to_file(
            data=all_items,
            keyword=keyword,
            filename=filename,
            is_first_page=False,
            is_last_page=True,
            analysis=analysis
        )
            
        return {
            "analysis": analysis_json,
            "error": None,
            "filename": filename
        }
        
    except Exception as e:
        if isinstance(e, (ScraperError, DataValidationError)):
            raise
        raise ScraperError(f"スクレイピング処理中にエラーが発生しました: {str(e)}")
