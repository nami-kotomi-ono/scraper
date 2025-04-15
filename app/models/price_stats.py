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
        valid_items = []
        valid_prices = []
        
        for item in items:
            try:
                # 価格が数値とカンマのみで構成されているか確認
                price_without_comma = item['price'].replace(',', '').strip()
                if not price_without_comma.isdigit():
                    continue  # 数値とカンマ以外の文字が含まれている場合はスキップ
                    
                # カンマを除去して数値に変換
                price = int(price_without_comma)
                valid_items.append(item)
                valid_prices.append(price)
            except (ValueError, AttributeError):
                continue  # 不正な価格形式はスキップ
                
        if not valid_prices:
            return None
            
        # 価格でソート
        sorted_items = sorted(zip(valid_prices, valid_items), key=lambda x: x[0])
        sorted_prices = [x[0] for x in sorted_items]
        sorted_items = [x[1] for x in sorted_items]
        
        lowest_item = sorted_items[0]
        highest_item = sorted_items[-1]
        average_price = sum(sorted_prices) / len(sorted_prices)
        
        # 中央値の計算
        n = len(sorted_prices)
        if n % 2 == 0:
            median_price = (sorted_prices[n//2 - 1] + sorted_prices[n//2]) / 2
        else:
            median_price = sorted_prices[n//2]
        
        return cls(
            lowest={
                'name': lowest_item['name'],
                'price': f"¥{lowest_item['price']}"
            },
            highest={
                'name': highest_item['name'],
                'price': f"¥{highest_item['price']}"
            },
            average=average_price,
            median=median_price,
            total=len(sorted_items)
        ) 
