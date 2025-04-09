import random
from pathlib import Path
from playwright.async_api import async_playwright
from .save import save_to_file
from app.config.settings import get_settings
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
settings = get_settings()

def setup_results_dir() -> Path:
    """結果を保存するディレクトリをセットアップする"""
    results_dir = Path(settings.results_dir)
    results_dir.mkdir(exist_ok=True)
    return results_dir

async def setup_browser():
    """ブラウザのセットアップを行う関数"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    
    context = await browser.new_context(
        user_agent=settings.user_agent,
        viewport=settings.viewport,
        locale=settings.locale,
        timezone_id=settings.timezone_id
    )
    
    cookies = [
        {
            'name': settings.cookie_name,
            'value': settings.cookie_value,
            'domain': settings.cookie_domain,
            'path': settings.cookie_path
        }
    ]
    await context.add_cookies(cookies)
    
    return playwright, browser, context

async def scroll_page(page):
    """ページをスクロールして商品を読み込む関数"""
    scroll_points = settings.scroll_points
    for point in scroll_points:
        await page.evaluate(f"window.scrollTo(0, document.body.scrollHeight*{point})")
        await page.wait_for_timeout(settings.wait_time_between_scrolls)

async def scrape_items(keyword):
    """商品をスクレイピングする関数"""
    all_results = []  # 全ページの商品情報用
    
    playwright, browser, context = await setup_browser()
    page = await context.new_page()
    
    try:
        search_url = settings.search_url_template.format(keyword=keyword)
        await page.goto(search_url)
        page_number = 1
        
        while True:
            await page.wait_for_timeout(random.randint(settings.min_wait_time, settings.max_wait_time))
            await page.wait_for_selector(settings.item_cell_selector, timeout=settings.page_load_timeout)
            await scroll_page(page)
            items = await page.query_selector_all(settings.item_cell_selector)

            if not items:
                print("商品が見つかりませんでした")
                break
                            
            # 商品情報を取得
            page_results = []
            for index, item in enumerate(items):
                try:
                    # 商品名を取得
                    name_element = await item.query_selector(settings.item_name_selector)
                    name = await name_element.inner_text() if name_element else None
                    
                    # 価格を取得
                    price_element = await item.query_selector(settings.item_price_selector)
                    price = await price_element.inner_text() if price_element else None
                    
                    if name and price:
                        item_data = {
                            'name': name.strip(),
                            'price': price.strip()
                        }
                        page_results.append(item_data)
                        all_results.append(item_data)
                    else:
                        print(f"⚠️ 商品{index + 1}: 商品情報の取得に失敗")
                        
                except Exception as e:
                    print(f"⚠️ 商品{index + 1}: 処理中にエラーが発生: {e}")
            
            # 次ページボタンを探す
            next_button = await page.query_selector(settings.next_button_selector)
            
            # ページごとの結果を保存
            save_to_file(
                data=page_results,
                keyword=keyword,
                page_number=page_number,
                is_first_page=(page_number == 1),
                is_last_page=False,  # 分析結果の追記はitems.pyで行うためFalse
                all_items=None  # 分析結果の追記はitems.pyで行うためNone
            )
            
            if not next_button:
                print("\nこれ以上ページがありません")
                break
                
            print("\n⏭️ 次ページに遷移します...")
            await next_button.click()
            page_number += 1
            
    finally:
        await browser.close()
        await playwright.stop()
        
    return all_results 