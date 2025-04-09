import pytest
from unittest.mock import AsyncMock, patch
from app.services.scraper import scrape_items, setup_browser, scroll_page
from app.config.settings import Settings

@pytest.mark.asyncio
async def test_setup_browser():
    """ブラウザセットアップのテスト"""
    print("test_setup_browser")
    
    playwright, browser, context = await setup_browser()
    assert playwright is not None
    assert browser is not None
    assert context is not None
    
    # クリーンアップ
    await browser.close()
    await playwright.stop()
    
    print("test_setup_browser_success")

@pytest.mark.asyncio
async def test_scroll_page():
    """ページスクロールのテスト"""
    print("test_scroll_page")
    
    # モックの設定
    mock_page = AsyncMock()
    settings = Settings()
    
    await scroll_page(mock_page)
    assert mock_page.evaluate.call_count == len(settings.scroll_points)
    assert mock_page.wait_for_timeout.call_count == len(settings.scroll_points)
    
    print("test_scroll_page_success")

@pytest.mark.asyncio
async def test_scrape_items_error_handling():
    """エラーハンドリングのテスト"""
    print("test_scrape_items_error_handling")
    settings = Settings()
    keyword = "iPhone"
    max_pages = 1
    
    with patch('app.services.scraper.setup_browser') as mock_setup:
        # モックの設定（エラーを発生させる）
        mock_setup.side_effect = Exception("Connection error")
        
        # 例外がキャッチされ、空のリストが返されることを期待
        items = await scrape_items(keyword, max_pages, settings)
        assert len(items) == 0
        
    print("test_scrape_items_error_handling_success")

@pytest.mark.asyncio
async def test_scrape_items_basic():
    """基本的なスクレイピング機能のテスト"""
    print("test_scrape_items_basic")
    settings = Settings()
    keyword = "iPhone"
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"
    for item in items:
        assert "name" in item, "商品名が取得できていません"
        assert "price" in item, "価格が取得できていません"
        assert item["name"] != "", "商品名が空です"
        assert item["price"] != "", "価格が空です"
        # 価格が数値文字列であることを確認
        assert item["price"].replace(",", "").isdigit(), "価格が数値ではありません"
    
    print("test_scrape_items_basic_success")

@pytest.mark.asyncio
async def test_scrape_items_empty_results():
    """商品が見つからない場合のテスト"""
    print("test_scrape_items_empty_results")
    settings = Settings()
    keyword = "存在しない商品1234567890"  # 存在しないキーワード
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) == 0, "存在しない商品が取得されました"
    
    print("test_scrape_items_empty_results_success")

@pytest.mark.asyncio
async def test_scrape_items_multiple_pages():
    """複数ページのスクレイピングテスト"""
    print("test_scrape_items_multiple_pages")
    settings = Settings()
    keyword = "iPhone"
    max_pages = 2

    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"
    for item in items:
        assert "name" in item, "商品名が取得できていません"
        assert "price" in item, "価格が取得できていません"
        assert item["name"] != "", "商品名が空です"
        assert item["price"] != "", "価格が空です"
        # 価格が数値文字列であることを確認
        assert item["price"].replace(",", "").isdigit(), "価格が数値ではありません"
    
    print("test_scrape_items_multiple_pages_success")

@pytest.mark.asyncio
async def test_scrape_items_multiple_keywords():
    """複数キーワードのスクレイピングテスト"""
    print("test_scrape_items_multiple_keywords")
    settings = Settings()
    keywords = "iPhone 販売中 スマートフォン本体"
    max_pages = 1

    items = await scrape_items(keywords, max_pages, settings)
    assert len(items) > 0, f"キーワード '{keywords}' で商品が見つかりませんでした"

    for item in items:
        assert "name" in item, "商品名が取得できていません"
        assert "price" in item, "価格が取得できていません"
        assert item["name"] != "", "商品名が空です"
        assert item["price"] != "", "価格が空です"
        # 価格が数値文字列であることを確認
        assert item["price"].replace(",", "").isdigit(), "価格が数値ではありません"
        
    print("test_scrape_items_multiple_keywords_success")

@pytest.mark.asyncio
async def test_scrape_items_timeout():
    """タイムアウトのテスト"""
    print("test_scrape_items_timeout")
    settings = Settings()
    # タイムアウトを1ミリ秒に設定
    settings.page_load_timeout = 1
    settings.min_wait_time = 1
    settings.max_wait_time = 1
    
    keyword = "iPhone"
    max_pages = 1
    
    items = await scrape_items(keyword, max_pages, settings)
    assert len(items) == 0, "タイムアウトが発生しませんでした"
    
    print("test_scrape_items_timeout_success") 