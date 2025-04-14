class ScraperError(Exception):
    """スクレイピング関連の基本エラー"""
    pass

class DataValidationError(ScraperError):
    """データ検証エラー"""
    pass
