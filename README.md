# メルカリ商品スクレイピングツール

メルカリの商品情報を自動で収集し、価格分析を行うスクレイピングツールです。

## 機能

- メルカリでのキーワード検索による商品情報の収集
- 商品名と価格の取得
- 価格分析（最低価格、最高価格、平均価格、中央値）
- CSVファイルへの保存
- ページネーション対応（全ページの商品情報を取得）

## インストール方法

1. リポジトリをクローン
```bash
git clone [リポジトリURL]
cd [リポジトリ名]
```

2. 仮想環境の作成
```bash
`python3 -m venv venv`
```

3. 仮想環境を有効化
```bash
`source venv/bin/activate` 
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

## 使い方（コマンドから動作確認する場合）

1. scraper/app/test_api.pyのkeywordに検索キーワードを入力

2. プログラムを実行
```bash
python3 -m app.test_api
```
3. 結果は `results` ディレクトリにCSVファイルとして保存されます

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

🎯 目的
検索キーワードを受け取り、メルカリの商品情報と価格をスクレイピングしてCSVに書き出し、フロントにCSVファイル、分析結果、ステータスコードを返すFastAPIのAPIを構築する。

🧩 使用ライブラリ
- FastAPI：APIサーバー構築
- Playwright：メルカリページのスクレイピング

## 入力
HTTPメソッド：POST  # GETからPOSTに修正

エンドポイント：/api/v1/search  # /scrapeから修正

リクエストボディ：
```json
{
    "keyword": "iPhone"
}
```

## 出力
レスポンス：
```json
{
    "csv_url": "/api/v1/download/iPhone.csv",
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
    }
}
```
```

CSVの内容：
- 商品名（Title）
- 価格（Price）

分析結果内容：
- 最低価格
- 最高価格
- 平均価格
- 中央値
- 取得商品数