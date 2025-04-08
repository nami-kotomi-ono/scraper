import asyncio
from scraper import scrape_items

def main():
    """メイン関数"""
    keyword = input("検索キーワードを入力: ")
    asyncio.run(scrape_items(keyword))

if __name__ == "__main__":
    main() 