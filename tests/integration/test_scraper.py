import pytest
from app.services.scraper import scrape_items
from app.config.settings import Settings

@pytest.mark.asyncio
async def test_scrape_items_single_page():
    """1ページのスクレイピングテスト"""
    print("test_scrape_items_single_page")
    settings = Settings()
    keyword = "iPhone"  # 必ず結果が返ってくるキーワード
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    print(items)
    # 結果の検証
    assert len(items) > 0
    for item in items:
        assert "name" in item
        assert "price" in item
        assert item["name"] != ""
        assert item["price"] != ""
        # 価格が数値文字列であることを確認
        assert item["price"].replace(",", "").isdigit()
    print("test_scrape_items_single_page_success")

@pytest.mark.asyncio
async def test_scrape_items_multiple_pages():
    """複数ページのスクレイピングテスト"""
    print("test_scrape_items_multiple_pages")
    settings = Settings()
    keyword = "iPhone"  # 必ず結果が返ってくるキーワード
    
    # 1ページ目の情報を取得
    max_pages = 1
    first_page_items = await scrape_items(keyword, max_pages, settings)
    first_page_count = len(first_page_items)

    # 2ページ目まで取得
    max_pages = 2
    items = await scrape_items(keyword, max_pages, settings)
    print(items)
    
    # 結果の検証
    assert len(items) > first_page_count
    for item in items:
        assert "name" in item
        assert "price" in item
        assert item["name"] != ""
        assert item["price"] != ""
        # 価格が数値文字列であることを確認
        assert item["price"].replace(",", "").isdigit()

    print("test_scrape_items_multiple_pages_success")

@pytest.mark.asyncio
async def test_scrape_items_invalid_keyword():
    """無効なキーワードのテスト"""
    settings = Settings()
    keyword = "存在しない商品名123456789"  # 存在しないキーワード
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) == 0
    
    print(f"\n✅ test_scrape_items_invalid_keyword")

@pytest.mark.asyncio
async def test_scrape_items_timeout():
    """タイムアウトのテスト"""
    settings = Settings()
    settings.page_load_timeout = 1  # 1ミリ秒に設定してタイムアウトを強制的に発生させる
    keyword = "iPhone"
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) == 0
    
    print(f"test_scrape_items_timeout")
