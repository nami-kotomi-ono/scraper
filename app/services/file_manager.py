from pathlib import Path
from datetime import datetime, timedelta
import csv
from .price_analysis import format_price_analysis

def setup_results_dir():
    """結果を保存するディレクトリをセットアップする関数"""
    root_dir = Path(__file__).parent.parent.parent
    results_dir = root_dir / "results"
    results_dir.mkdir(exist_ok=True)
    return results_dir

def cleanup_files(keyword: str):
    """指定されたキーワードに関連するファイルをクリーンアップ"""
    results_dir = setup_results_dir()
    now = datetime.now()
    
    # 同じキーワードのファイルを検索
    keyword_files = list(results_dir.glob(f"{keyword}*.csv"))
    
    # 古いファイルを検索（1時間以上経過）
    old_files = [
        file for file in results_dir.glob("*.csv")
        if datetime.fromtimestamp(file.stat().st_mtime) < now - timedelta(hours=1)
    ]
    
    # 削除対象のファイルを結合（重複を除く）
    files_to_delete = set(keyword_files + old_files)
    
    # ファイルを削除
    for file in files_to_delete:
        try:
            file.unlink()
            print(f"ファイルを削除しました: {file}")
        except Exception as e:
            print(f"ファイル削除エラー: {e}")

def save_to_file(data, keyword, page_number=None, is_first_page=False, is_last_page=False, all_items=None, analysis=None):
    """データをCSVファイルに保存する関数"""
    if not data:
        print("⚠️ 保存するデータがありません")
        return
        
    # 結果ディレクトリのセットアップ
    results_dir = setup_results_dir()
    
    filename = f"{keyword}.csv"
    filepath = results_dir / filename
    
    # ファイルの書き込みモードを決定（初回は新規作成、それ以外は追記）
    mode = 'w' if is_first_page else 'a'
    
    with open(filepath, mode, encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        if is_first_page:
            # ヘッダー情報を追加（初回のみ）
            writer.writerow(['検索キーワード', keyword])
            writer.writerow(['取得開始日時', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])  # 空行
            writer.writerow(['商品名', '価格'])
        
        # 商品情報を書き込み
        for item in data:
            writer.writerow([item['name'], item['price']])
        
        # 最後のページの場合、全商品の価格分析を追加
        if is_last_page and analysis:
            # 分析結果をCSVに追記
            analysis_rows = format_price_analysis(analysis)
            for row in analysis_rows:
                writer.writerow(row)
                
    if is_first_page:
        print(f"結果ファイルを作成しました: {filepath}")
    print(f"ページ {page_number if page_number else '1'} の商品情報を保存しました（{len(data)}件）")

