from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

async def setup_browser():
    """ブラウザのセットアップを行う関数"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        user_agent=os.getenv('USER_AGENT'),
        viewport={'width': 1920, 'height': 1080},
        locale='ja-JP',
        timezone_id='Asia/Tokyo'
    )
    
    # クッキーを設定
    await context.add_cookies([
        {
            'name': os.getenv('COOKIE_NAME'),
            'value': os.getenv('COOKIE_VALUE'),
            'domain': os.getenv('COOKIE_DOMAIN'),
            'path': os.getenv('COOKIE_PATH')
        }
    ])
    
    return playwright, browser, context

async def scroll_page(page):
    """ページをスクロールして商品を読み込む関数"""

    # 1/8までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight/8)")
    await page.wait_for_timeout(2000)

    # 1/4までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight/4)")
    await page.wait_for_timeout(2000)

    # 3/8までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight*3/8)")
    await page.wait_for_timeout(2000)

    # 半分までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
    await page.wait_for_timeout(2000)

    # 5/8までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight*5/8)")
    await page.wait_for_timeout(2000)

    # 3/4までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight*3/4)")
    await page.wait_for_timeout(2000)

    # 7/8までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight*7/8)")
    await page.wait_for_timeout(2000)

    # 最後までスクロール
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(2000)
