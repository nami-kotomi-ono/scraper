import pytest
from app.services.price_analysis import analyze_prices, format_price_analysis, format_price_analysis_to_json

def test_analyze_prices():
    """価格分析の基本テスト"""
    items = [
        {"name": "商品1", "price": "1,000"},
        {"name": "商品2", "price": "2,000"},
        {"name": "商品3", "price": "3,000"}
    ]
    result = analyze_prices(items)
    assert result.lowest["price"] == "1,000"
    assert result.highest["price"] == "3,000"
    assert result.average == 2000
    assert result.median == 2000
    assert result.total == 3

def test_analyze_prices_empty_list():
    """空のリストでの価格分析テスト"""
    result = analyze_prices([])
    assert result is None

def test_analyze_prices_single_item():
    """商品が1つの場合の価格分析テスト"""
    items = [{"name": "商品1", "price": "1,000"}]
    result = analyze_prices(items)
    assert result.lowest["price"] == "1,000"
    assert result.highest["price"] == "1,000"
    assert result.average == 1000
    assert result.median == 1000
    assert result.total == 1

def test_analyze_prices_even_number():
    """商品数が偶数の場合の価格分析テスト"""
    items = [
        {"name": "商品1", "price": "1,000"},
        {"name": "商品2", "price": "2,000"},
        {"name": "商品3", "price": "3,000"},
        {"name": "商品4", "price": "4,000"}
    ]
    result = analyze_prices(items)
    assert result.median == 2500  # (2000 + 3000) / 2

def test_format_price_analysis():
    """価格分析結果のCSVフォーマットテスト"""
    analysis = analyze_prices([
        {"name": "商品1", "price": "1,000"},
        {"name": "商品2", "price": "2,000"}
    ])
    result = format_price_analysis(analysis)
    assert len(result) > 0
    assert "=== 価格分析 ===" in result[0]
    assert "最低金額商品" in result[2]
    assert "最高金額商品" in result[4]

def test_format_price_analysis_to_json():
    """価格分析結果のJSONフォーマットテスト"""
    analysis = analyze_prices([
        {"name": "商品1", "price": "1,000"},
        {"name": "商品2", "price": "2,000"}
    ])
    result = format_price_analysis_to_json(analysis)
    assert "lowest_price" in result
    assert "highest_price" in result
    assert "average_price" in result
    assert "median_price" in result
    assert "total_items" in result 