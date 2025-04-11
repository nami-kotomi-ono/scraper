import os
import sys

# プロジェクトのルートディレクトリをPythonのパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root) 