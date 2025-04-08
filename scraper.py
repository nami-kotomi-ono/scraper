import random
import os
from browser import setup_browser, scroll_page
from utils import save_to_file
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

async def scrape_items(keyword):
    """商品をスクレイピングする関数"""
    all_results = []  # 全ページの商品情報用
    
    playwright, browser, context = await setup_browser()
    page = await context.new_page()
    
    try:
        # 検索URLにアクセス
        search_url = os.getenv('SEARCH_URL_TEMPLATE').format(keyword=keyword)
        await page.goto(search_url)
        
        # ランダムな時間待機（ボット対策）
        await page.wait_for_timeout(random.randint(2000, 5000))
        await scroll_page(page)
                
        # 商品一覧取得
        selector = os.getenv('ITEM_CELL_SELECTOR')
        items = await page.query_selector_all(selector)
        page_number = 1
        
        while True:
            if not items:
                print("商品が見つかりませんでした")
                break
                            
            # 商品情報を取得
            page_results = []
            for index, item in enumerate(items):
                try:
                    # 商品名を取得
                    name_element = await item.query_selector(os.getenv('ITEM_NAME_SELECTOR'))
                    name = await name_element.inner_text() if name_element else None
                    
                    # 価格を取得
                    price_element = await item.query_selector(os.getenv('ITEM_PRICE_SELECTOR'))
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
            next_button = await page.query_selector(os.getenv('NEXT_BUTTON_SELECTOR'))
            
            # ページごとの結果を保存
            save_to_file(page_results, keyword, page_number, 
                        is_first_page=(page_number == 1),
                        is_last_page=(not next_button),
                        all_items=all_results if not next_button else None)
            
            if not next_button:
                print("\nこれ以上ページがありません")
                break
                
            print("\n⏭️ 次ページに遷移します...")
            await next_button.click()
            
            try:
                await page.wait_for_selector(os.getenv('ITEM_CELL_SELECTOR'), timeout=10000)
                await scroll_page(page)
            except Exception as e:
                print(f"⚠️ ページ読み込み待機中にエラーが発生: {e}")
            
            # 商品を取得
            items = await page.query_selector_all(selector)
            page_number += 1
            
    finally:
        await browser.close()
        await playwright.stop()
        
    return all_results 