class Settings:
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
    cookie_name: str = "mercari_accept_cookie"
    cookie_value: str = "1"
    cookie_domain: str = ".mercari.com"
    cookie_path: str = "/"

    # ページ読み込みの設定
    page_load_timeout: int = 30000
    min_wait_time: int = 3000
    max_wait_time: int = 7000

    # スクロールの設定
    scroll_points: list[float] = [1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8, 1]
    wait_time_between_scrolls: int = 2000


def get_settings() -> Settings:
    return Settings() 