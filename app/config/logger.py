import logging
import sys
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """ロガーのセットアップを行う関数
    
    Args:
        name (str): ロガー名（通常は__name__を使用）
        
    Returns:
        logging.Logger: 設定済みのロガー
    """
    # 既存のロガーを取得
    logger = logging.getLogger(name)
    
    # ロガーが既に設定されている場合は、そのまま返す
    if logger.handlers:
        return logger
        
    # ロガーのレベルを設定
    logger.setLevel(logging.INFO)


    logger.propagate = False
    
    # ログのフォーマットを設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 標準出力へのハンドラ
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイルへのハンドラ
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger 
