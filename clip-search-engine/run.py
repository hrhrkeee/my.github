"""CLIP検索エンジンの実行スクリプト。

使い方:
    uv run python clip-search-engine/run.py register --image path/to/image.jpg
    uv run python clip-search-engine/run.py search --text "猫が寝ている"
    uv run python clip-search-engine/run.py info --list-all
    uv run python clip-search-engine/run.py clear -y
"""

import os
import sys

# 自身のディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import main

if __name__ == "__main__":
    main()
