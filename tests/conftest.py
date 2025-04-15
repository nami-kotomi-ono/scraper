import os
import sys
import pytest
from app.services.file_manager import cleanup_files

# プロジェクトのルートディレクトリをPythonのパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def cleanup_test_files():
    """すべてのテストの後にファイルを削除するフィクスチャ"""
    yield
    cleanup_files() 