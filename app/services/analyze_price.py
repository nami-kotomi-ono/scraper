from typing import List, Dict, Any
from app.models.price_analysis import PriceAnalysis

def analyze_prices(items: List[Dict[str, Any]]) -> PriceAnalysis:
    """商品リストから価格分析を行う関数"""
    return PriceAnalysis.from_items(items)

def format_price_analysis(analysis: PriceAnalysis) -> List[List[str]]:
    """価格分析結果をCSV追記用にフォーマットする関数"""
    result = []
    result.append(['=== 価格分析 ==='])
    
    if not analysis:
        result.append(['分析対象の商品がありません'])
        return result
        
    result.append(['=== 全商品の価格情報 ==='])
    result.append(['最低金額商品', f"¥{analysis.lowest['price']}"])
    result.append(['商品名', analysis.lowest['name']])
    result.append(['最高金額商品', f"¥{analysis.highest['price']}"])
    result.append(['商品名', analysis.highest['name']])
    result.append(['平均価格', f"¥{int(analysis.average):,}"])
    result.append(['中央値', f"¥{int(analysis.median):,}"])
    result.append(['取得商品数', f"{analysis.total}件"])
    
    return result

def format_price_analysis_to_json(analysis: PriceAnalysis) -> dict:
    """価格分析結果をJSON形式に変換する関数"""
    if not analysis:
        return {
            "error": "分析対象の商品がありません"
        }
        
    return {
        "lowest_price": {
            "price": analysis.lowest['price'],
            "name": analysis.lowest['name']
        },
        "highest_price": {
            "price": analysis.highest['price'],
            "name": analysis.highest['name']
        },
        "average_price": int(analysis.average),
        "median_price": int(analysis.median),
        "total_items": analysis.total
    }
