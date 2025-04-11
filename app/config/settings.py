from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

class Settings(BaseSettings):
    # アプリケーション設定
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    # CORS設定
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    cors_credentials: bool = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    cors_methods: List[str] = os.getenv("CORS_METHODS", "GET,POST").split(",")
    cors_headers: List[str] = os.getenv("CORS_HEADERS", "*").split(",")

    # メルカリの設定
    search_url_template: str = "https://jp.mercari.com/search?keyword={keyword}"
    item_cell_selector: str = "li[data-testid='item-cell']"
    item_name_selector: str = "span[data-testid='thumbnail-item-name']"
    item_price_selector: str = "span[class*='number__']"
    next_button_selector: str = "div[data-testid='pagination-next-button']"
    
    # ブラウザの設定
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # 結果を保存するディレクトリ
    results_dir: str = "results"

    # ブラウザの設定
    viewport: dict = {'width': 1920, 'height': 1080}
    locale: str = 'ja-JP'
    timezone_id: str = 'Asia/Tokyo'

    # クッキー設定
    cookie_name: str = os.getenv("COOKIE_NAME", "mercari_accept_cookie")
    cookie_value: str = os.getenv("COOKIE_VALUE", "1")
    cookie_domain: str = os.getenv("COOKIE_DOMAIN", ".mercari.com")
    cookie_path: str = os.getenv("COOKIE_PATH", "/")

    # ページ読み込みの設定
    page_load_timeout: int = 30000
    min_wait_time: int = 3000
    max_wait_time: int = 7000

    # スクロールの設定
    scroll_points: list[float] = [1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8, 1]
    wait_time_between_scrolls: int = 2000

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "case_sensitive": True
    }

def get_settings() -> Settings:
    return Settings() 