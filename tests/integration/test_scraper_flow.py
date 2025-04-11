import pytest
import os
from pathlib import Path
from app.services.scraper import scrape_items
from app.services.file_manager import save_to_file, setup_results_dir
from app.config.settings import Settings

@pytest.fixture
def test_keyword():
    """テスト用のキーワードを提供するフィクスチャ"""
    return "iphone"

@pytest.fixture
def cleanup_test_files(test_keyword):
    """テスト後にファイルを削除するフィクスチャ"""
    yield
    # テストファイルの削除
    results_dir = setup_results_dir()
    test_file = results_dir / f"{test_keyword}.csv"
    if test_file.exists():
        test_file.unlink()

@pytest.mark.asyncio
async def test_scrape_and_save_single_page(test_keyword, cleanup_test_files):
    """スクレイピングとCSV保存の連携テスト（1ページ）"""
    print("test_scrape_and_save_single_page")
    settings = Settings()
    max_pages = 1
    
    # スクレイピング実行
    items = await scrape_items(test_keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"
    
    # CSV保存
    save_to_file(
        data=items,
        keyword=test_keyword,
        page_number=1,
        is_first_page=True,
        is_last_page=True
    )
    
    # ファイルの存在確認
    results_dir = setup_results_dir()
    test_file = results_dir / f"{test_keyword}.csv"
    assert test_file.exists()
    
    # ファイル内容の確認
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert test_keyword in content
        for item in items:
            assert item["name"] in content
            assert item["price"] in content
    
    print(f"取得商品数: {len(items)}件")
    print("test_scrape_and_save_single_page_success")

@pytest.mark.asyncio
async def test_scrape_and_save_multiple_pages(test_keyword, cleanup_test_files):
    """スクレイピングとCSV保存の連携テスト（複数ページ）"""
    print("test_scrape_and_save_multiple_pages")
    settings = Settings()
    max_pages = 2

    # スクレイピング実行
    items = await scrape_items(test_keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"

    # ファイルの存在確認
    results_dir = setup_results_dir()
    test_file = results_dir / f"{test_keyword}.csv"
    assert test_file.exists()

    # ファイル内容の確認
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert test_keyword in content
        # 商品名と価格の行数を確認（ヘッダー行を除く）
        lines = content.split('\n')
        item_lines = [line for line in lines if ',' in line and not line.startswith('検索キーワード') and not line.startswith('取得開始日時') and not line.startswith('商品名')]
        assert len(item_lines) > 0, "商品情報が保存されていません"
        assert len(item_lines) == len(items), f"保存された商品数が一致しません: 期待={len(items)}, 実際={len(item_lines)}"

@pytest.mark.asyncio
async def test_scrape_and_save_with_analysis(test_keyword, cleanup_test_files):
    """スクレイピング、分析、CSV保存の連携テスト"""
    print("test_scrape_and_save_with_analysis")
    settings = Settings()
    max_pages = 1
    
    # スクレイピング実行
    items = await scrape_items(test_keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"
    
    # 分析結果の作成
    from app.services.price_analysis import analyze_prices
    analysis = analyze_prices(items)
    
    # CSV保存（分析結果を含む）
    save_to_file(
        data=items,
        keyword=test_keyword,
        page_number=1,
        is_first_page=True,
        is_last_page=True,
        analysis=analysis
    )
    
    # ファイルの存在確認
    results_dir = setup_results_dir()
    test_file = results_dir / f"{test_keyword}.csv"
    assert test_file.exists()
    
    # ファイル内容の確認
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert test_keyword in content
        assert "=== 価格分析 ===" in content
        assert "=== 全商品の価格情報 ===" in content
        assert f"¥{analysis.lowest['price']}" in content
        assert f"¥{analysis.highest['price']}" in content
        assert f"¥{int(analysis.average):,}" in content
        assert f"¥{int(analysis.median):,}" in content
        assert f"{analysis.total}件" in content
    
    print(f"取得商品数: {len(items)}件")
    print("test_scrape_and_save_with_analysis_success")

@pytest.mark.asyncio
async def test_csv_file_deletion(test_keyword):
    """CSVファイルの削除処理のテスト"""
    print("test_csv_file_deletion")
    settings = Settings()
    max_pages = 1

    # スクレイピング実行
    items = await scrape_items(test_keyword, max_pages, settings)
    assert len(items) > 0, "商品が見つかりませんでした"

    # ファイルの存在確認
    results_dir = setup_results_dir()
    test_file = results_dir / f"{test_keyword}.csv"
    assert test_file.exists()

    # ファイルの削除
    if test_file.exists():
        test_file.unlink()
    assert not test_file.exists(), "ファイルが削除されていません"

    print("test_csv_file_deletion_success")
