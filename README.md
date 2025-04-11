# メルカリ商品スクレイピングツール

メルカリの商品情報を自動で収集し、価格分析を行うスクレイピングツールです。

## 機能

- メルカリでのキーワード検索による商品情報の収集
- 商品名と価格の取得
- 価格分析（最低価格、最高価格、平均価格、中央値）
- CSVファイルへの保存
- ページネーション対応（全ページの商品情報を取得）

## 使用ライブラリ

- FastAPI：APIサーバー構築
- Playwright：メルカリページのスクレイピング

## インストール方法

1. リポジトリをクローン
```bash
git clone [リポジトリURL]
cd [リポジトリ名]
```

2. 仮想環境の作成
```bash
python3 -m venv venv
```

3. 仮想環境を有効化
```bash
source venv/bin/activate
```

4. 依存パッケージのインストール
```bash
pip3 install -r requirements.txt
```

5. Playwrightのインストール
```bash
playwright install
```

※仮想環境を抜ける
```bash
deactivate
```

## APIサーバーの起動
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API仕様

### 商品検索
- 入力
* HTTPメソッド：POST 

* エンドポイント：/api/v1/search  

* リクエストボディ：
```json
{
    "keyword": "iPhone"
}
```

- 出力
* レスポンス：
```json
{
    "analysis": {
        "lowest_price": {
            "price": "1000",
            "name": "商品名"
        },
        "highest_price": {
            "price": "100000",
            "name": "商品名"
        },
        "average_price": 50000,
        "median_price": 45000,
        "total_items": 100
    },
    "error": null
}
```
- エラー時は `analysis` が `null` になり、`error` にエラーメッセージが設定されます。

### CSVファイルダウンロード
- 入力
* HTTPメソッド：GET 
* エンドポイント: `/api/v1/download/{keyword}.csv`

- 出力
* レスポンスヘッダー:
```json
{
    "Content-Type": "text/csv",
    "Content-Disposition": "attachment; filename*=UTF-8''{keyword}.csv",
    "Access-Control-Expose-Headers": "Content-Disposition"
}
```
* レスポンスボディ: CSVファイル

## テスト実行方法

### すべてのテストを実行
```bash
pytest
```

### 特定のテストを実行
```bash
# 統合テストのみ実行
pytest tests/integration/

# ユニットテストのみ実行
pytest tests/unit/

# 特定のテストファイルを実行
pytest tests/integration/test_scraper_flow.py

# 特定のテスト関数を実行
pytest tests/unit/test_scraper.py::test_scrape_items_multiple_keywords
```

### テストカバレッジの確認
```bash
pytest --cov=app
```

## カスタマイズ方法

`app/config/settings.py`で以下の設定を変更できます：
- ブラウザ設定（ユーザーエージェントなど）
- クッキー設定
- セレクタ設定（商品一覧、商品名、価格、次ページボタンなど）
- 検索URL

## 注意事項

- メルカリの利用規約に従って使用してください
- 過度なアクセスは避けてください
- 取得したデータの利用は自己責任でお願いします
- 本ツールは教育目的で公開しています
