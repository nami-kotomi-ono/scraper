from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class PriceAnalysis:
    lowest: Dict[str, Any]
    highest: Dict[str, Any]
    average: float
    median: float
    total: int

    @classmethod
    def from_items(cls, items: List[Dict[str, Any]]) -> 'PriceAnalysis':
        """商品リストから価格分析を行う"""
        if not items:
            return None
            
        # 価格を数値に変換してリスト化
        prices = [int(item['price'].replace(',', '')) for item in items]
        prices.sort()  # 中央値計算のためにソート
        
        lowest_item = items[prices.index(min(prices))]
        highest_item = items[prices.index(max(prices))]
        average_price = sum(prices) / len(prices)
        
        # 中央値の計算
        n = len(prices)
        if n % 2 == 0:
            median_price = (prices[n//2 - 1] + prices[n//2]) / 2
        else:
            median_price = prices[n//2]
        
        return cls(
            lowest={
                'name': lowest_item['name'],
                'price': lowest_item['price']
            },
            highest={
                'name': highest_item['name'],
                'price': highest_item['price']
            },
            average=average_price,
            median=median_price,
            total=len(items)
        ) 