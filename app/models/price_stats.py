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
        valid_prices = []
        valid_items = []
        
        for item in items:
            try:
                # 価格が数値とカンマのみで構成されているか確認
                price_without_comma = item['price'].replace(',', '')
                if not price_without_comma.isdigit():
                    continue  # 数値とカンマ以外の文字が含まれている場合はスキップ
                    
                # カンマを除去して数値に変換
                price = int(price_without_comma)
                valid_prices.append(price)
                valid_items.append(item)
            except (ValueError, AttributeError):
                continue  # 不正な価格形式はスキップ
                
        if not valid_prices:
            return None
            
        prices = valid_prices
        items = valid_items
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