class Settings:
    # メルカリの設定
    search_url_template: str = "https://jp.mercari.com/search?keyword={keyword}"
    item_cell_selector: str = "li[data-testid='item-cell']"
    item_name_selector: str = "span[data-testid='thumbnail-item-name']"
    item_price_selector: str = "span[class*='number__']"
    next_button_selector: str = "div[data-testid='pagination-next-button']"
    
    # ブラウザの設定
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # クッキー設定
    cookie_name: str = "mercari_accept_cookie"
    cookie_value: str = "1"
    cookie_domain: str = ".mercari.com"
    cookie_path: str = "/"

def get_settings() -> Settings:
    return Settings() 