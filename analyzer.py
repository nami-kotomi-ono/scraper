def analyze_prices(items):
    """商品の価格分析を行う関数"""
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
    
    return {
        'lowest': {
            'name': lowest_item['name'],
            'price': lowest_item['price']
        },
        'highest': {
            'name': highest_item['name'],
            'price': highest_item['price']
        },
        'average': average_price,
        'median': median_price,
        'total': len(items)
    }

def format_price_analysis(analysis):
    """価格分析結果を表示用にフォーマットする関数"""
    if not analysis:
        return []
        
    result = []
    result.append([])  
    result.append(['=== 全商品の価格情報 ==='])
    result.append(['最低金額商品', f"¥{analysis['lowest']['price']}"])
    result.append(['商品名', analysis['lowest']['name']])
    result.append(['最高金額商品', f"¥{analysis['highest']['price']}"])
    result.append(['商品名', analysis['highest']['name']])
    result.append(['平均価格', f"¥{int(analysis['average']):,}"])
    result.append(['中央値', f"¥{int(analysis['median']):,}"])
    result.append(['取得商品数', f"{analysis['total']}件"])
    
    return result
