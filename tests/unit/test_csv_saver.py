from datetime import datetime
import pytest
import os
import csv
from pathlib import Path
from app.services.file_manager import save_to_file, setup_results_dir
from app.services.price_analysis import PriceAnalysis

@pytest.fixture
def test_data():
    """テスト用のデータを提供するフィクスチャ"""
    return [
        {"name": "iPhone 13", "price": "100,000"},
        {"name": "iPhone 12", "price": "80,000"}
    ]

@pytest.fixture
def test_keyword():
    """テスト用のキーワードを提供するフィクスチャ"""
    return "iphone"

@pytest.fixture
def create_file_name():
    """ファイル名を作成する"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.csv"
    return filename


def test_setup_results_dir():
    """結果ディレクトリのセットアップテスト"""
    print("test_setup_results_dir")
    results_dir = setup_results_dir()
    
    # ディレクトリが存在することを確認
    assert results_dir.exists()
    assert results_dir.is_dir()
    
    print("test_setup_results_dir_success")

def test_save_to_file_first_page(test_data, test_keyword, create_file_name):
    """初回ページの保存テスト"""
    print("test_save_to_file_first_page")
    filename = create_file_name
    save_to_file(
        data=test_data,
        keyword=test_keyword,
        filename=filename,
        is_first_page=True,
        is_last_page=False,
        analysis=None
    )
    
    # ファイルの存在確認
    results_dir = setup_results_dir()
    test_file = results_dir / filename
    assert test_file.exists()
    
    # ファイル内容の確認
    with open(test_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # ヘッダー行の確認
        assert rows[0] == ['検索キーワード', test_keyword]
        assert rows[2] == []  # 空行
        assert rows[3] == ['商品名', '価格']
        
        # データ行の確認
        assert rows[4] == ['iPhone 13', '100,000']
        assert rows[5] == ['iPhone 12', '80,000']
    
    print("test_save_to_file_first_page_success")

def test_save_to_file_append_page(test_data, test_keyword, create_file_name):
    """追加ページの保存テスト"""
    print("test_save_to_file_append_page")
    filename = create_file_name
    # 初回ページの保存
    save_to_file(
        data=test_data,
        keyword=test_keyword,
        filename=filename,
        is_first_page=True,
        is_last_page=False,
        analysis=None
    )
    
    # 追加ページの保存
    additional_data = [
        {"name": "iPhone 11", "price": "60,000"},
        {"name": "iPhone X", "price": "40,000"}
    ]
    save_to_file(
        data=additional_data,
        keyword=test_keyword,
        filename=filename,
        is_first_page=False,
        is_last_page=False,
        analysis=None
    )
    
    # ファイル内容の確認
    results_dir = setup_results_dir()
    test_file = results_dir / filename
    with open(test_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # 全データ行の確認
        assert rows[4] == ['iPhone 13', '100,000']
        assert rows[5] == ['iPhone 12', '80,000']
        assert rows[6] == ['iPhone 11', '60,000']
        assert rows[7] == ['iPhone X', '40,000']
    
    print("test_save_to_file_append_page_success")

def test_save_to_file_with_analysis(test_data, test_keyword, create_file_name):
    """分析結果を含む保存テスト"""
    print("test_save_to_file_with_analysis")
    filename = create_file_name
    # 分析結果の作成
    analysis = PriceAnalysis(
        lowest={"name": "iPhone X", "price": "40,000"},
        highest={"name": "iPhone 13", "price": "100,000"},
        average=70000.0,
        median=70000.0,
        total=4
    )
    
    # データの保存
    save_to_file(
        data=test_data,
        keyword=test_keyword,
        filename=filename,
        is_first_page=True,
        is_last_page=True,
        analysis=analysis
    )
    
    # ファイル内容の確認
    results_dir = setup_results_dir()
    test_file = results_dir / filename
    with open(test_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # 分析結果の確認
        assert rows[-8] == ['=== 全商品の価格情報 ===']
        assert rows[-7] == ['最低金額商品', '¥40,000']
        assert rows[-6] == ['商品名', 'iPhone X']
        assert rows[-5] == ['最高金額商品', '¥100,000']
        assert rows[-4] == ['商品名', 'iPhone 13']
        assert rows[-3] == ['平均価格', '¥70,000']
        assert rows[-2] == ['中央値', '¥70,000']
        assert rows[-1] == ['取得商品数', '4件']
    
    print("test_save_to_file_with_analysis_success") 