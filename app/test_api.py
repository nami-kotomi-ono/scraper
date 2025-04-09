import asyncio
from .api.items import search_items
from pydantic import BaseModel
from pathlib import Path

async def test_search():
    """APIエンドポイントのテスト実行"""
    # テストリクエストの作成
    class TestRequest(BaseModel):
        keyword: str
    
    # キーワードの入力を受け付ける
    keyword = input("検索キーワードを入力してください: ")
    request = TestRequest(keyword=keyword)
    
    try:
        # APIエンドポイントの実行
        await search_items(request)
        
        # 結果ファイルのパスを構築（プロジェクトルートの results ディレクトリ）
        root_dir = Path(__file__).parent.parent
        file_path = root_dir / "results" / f"{keyword}.csv"
        
        if file_path.exists():
            print(f"\n✅ CSVファイルが正常に保存されました: {file_path}")
        else:
            print(f"\n❌ CSVファイルが見つかりません: {file_path}")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    asyncio.run(test_search()) 