import asyncio
from app.api.items import search_items, SearchRequest

async def test_search():
    # テスト用のリクエストを作成
    request = SearchRequest(keyword="測量用プリズム")
    
    # 検索を実行
    response = await search_items(request)
    
    # レスポンスを表示
    print("\n=== CSVファイルのURL ===")
    print(response["csv_url"])
    
    print("\n=== 価格分析結果 ===")
    analysis = response["analysis"]
    print(f"最低価格: ¥{analysis['lowest_price']['price']} - {analysis['lowest_price']['name']}")
    print(f"最高価格: ¥{analysis['highest_price']['price']} - {analysis['highest_price']['name']}")
    print(f"平均価格: ¥{analysis['average_price']:,}")
    print(f"中央値: ¥{analysis['median_price']:,}")
    print(f"取得商品数: {analysis['total_items']}件")

if __name__ == "__main__":
    asyncio.run(test_search()) 