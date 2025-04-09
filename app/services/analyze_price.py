from typing import List, Dict, Any
from app.models.price_analysis import PriceAnalysis

def analyze_prices(items: List[Dict[str, Any]]) -> PriceAnalysis:
    """商品リストから価格分析を行う関数"""
    return PriceAnalysis.from_items(items)

def format_price_analysis(analysis: PriceAnalysis) -> List[List[str]]:
    """価格分析結果を表示用にフォーマットする関数"""
    if not analysis:
        return []
        
    result = []
    result.append([])  
    result.append(['=== 全商品の価格情報 ==='])
    result.append(['最低金額商品', f"¥{analysis.lowest['price']}"])
    result.append(['商品名', analysis.lowest['name']])
    result.append(['最高金額商品', f"¥{analysis.highest['price']}"])
    result.append(['商品名', analysis.highest['name']])
    result.append(['平均価格', f"¥{int(analysis.average):,}"])
    result.append(['中央値', f"¥{int(analysis.median):,}"])
    result.append(['取得商品数', f"{analysis.total}件"])
    
    return result
