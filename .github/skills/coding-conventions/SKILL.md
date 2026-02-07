---
name: coding-conventions
description: >
  Pythonプロジェクトのコーディング規約。
  PEP 8準拠の命名規則、型ヒント、docstring、コメントスタイルを定義する。
---

# Coding Conventions

Pythonプロジェクトのコーディング規約。

## 基本原則

- **PEP 8準拠** - Pythonの標準スタイルガイドに従う
- **可読性優先** - 他人が読んでも理解できるコードを書く
- **一貫性重視** - プロジェクト全体で統一されたスタイルを維持する

## 言語使用

### コメント・docstring

- **日本語**で記載する
- Pythonスクリプト、ノートブック内のコメント全て
- docstringも日本語で説明を記載

### コード

- 変数名・関数名・クラス名は**英語**
- ファイル名は英語（ノートブックのみ例外で日本語可）
- フォルダ名は英語

## 命名規則（PEP 8準拠）

### 変数・関数

```python
# snake_case を使用
user_name = "Alice"
total_count = 0

def calculate_average(values: list[float]) -> float:
    """平均値を計算する。"""
    return sum(values) / len(values)
```

### クラス

```python
# PascalCase を使用
class DataLoader:
    """データローダークラス。"""
    pass

class ImageProcessor:
    """画像処理クラス。"""
    pass
```

### 定数

```python
# UPPER_SNAKE_CASE を使用
MAX_BATCH_SIZE = 128
DEFAULT_LEARNING_RATE = 0.001
```

### プライベート変数・メソッド

```python
# アンダースコアプレフィックス
class Model:
    def __init__(self):
        self._hidden_state = None  # プライベート変数
    
    def _internal_process(self):
        """内部処理（プライベートメソッド）。"""
        pass
```

## インデント

- **スペース4つ**を使用（タブ不可）
- 継続行は適切にインデント

```python
# 良い例
def long_function_name(
    parameter_one: str,
    parameter_two: int,
    parameter_three: bool = False,
) -> dict:
    """長い関数定義の例。"""
    return {}

# 良い例
result = some_function(
    argument_one,
    argument_two,
    keyword_arg=value,
)
```

## 型ヒント

積極的に使用する:

```python
from pathlib import Path

def load_data(file_path: Path, max_rows: int = 1000) -> list[dict]:
    """データファイルを読み込む。
    
    Args:
        file_path: 読み込むファイルのパス。
        max_rows: 最大読み込み行数。
    
    Returns:
        読み込んだデータのリスト。
    """
    data: list[dict] = []
    # ...
    return data

# Python 3.10+ の型ヒント構文を推奨
def process(items: list[str] | None = None) -> dict[str, int]:
    """アイテムを処理する。"""
    if items is None:
        items = []
    return {item: len(item) for item in items}
```

### 型ヒントのガイドライン

- 関数の引数・戻り値には必ず型ヒントを付ける
- 複雑な型は `typing` モジュールを使用（`List`, `Dict`, `Optional` など）
- Python 3.10+ では組み込み型 `list`, `dict` と `|` を優先
- 変数への型ヒントは必要に応じて付ける

## Docstring（Googleスタイル）

```python
def train_model(
    model: nn.Module,
    data_loader: DataLoader,
    epochs: int = 10,
    learning_rate: float = 0.001,
) -> dict[str, float]:
    """モデルを訓練する。
    
    Args:
        model: 訓練対象のPyTorchモデル。
        data_loader: 訓練データを提供するDataLoader。
        epochs: 訓練エポック数。デフォルトは10。
        learning_rate: 学習率。デフォルトは0.001。
    
    Returns:
        訓練結果の辞書。'loss'と'accuracy'キーを含む。
    
    Raises:
        ValueError: data_loaderが空の場合。
        RuntimeError: GPU利用時にCUDAが利用不可の場合。
    
    Examples:
        >>> model = MyModel()
        >>> loader = DataLoader(dataset, batch_size=32)
        >>> results = train_model(model, loader, epochs=5)
        >>> print(results['accuracy'])
        0.95
    
    Note:
        GPUが利用可能な場合は自動的にGPUで訓練する。
    """
    pass
```

### Docstringのセクション

必須:
- 1行目: 簡潔な説明（1行で完結）
- `Args`: 引数の説明
- `Returns`: 戻り値の説明

任意（必要に応じて追加）:
- `Raises`: 発生しうる例外
- `Examples`: 使用例
- `Note`, `Warning`, `Todo`: 補足情報

## コメント

```python
# 良いコメント: なぜそうするかを説明
# GPU メモリ不足を避けるため、バッチサイズを動的に調整
batch_size = adjust_batch_size(available_memory)

# 悪いコメント: コードを読めばわかることを繰り返す
# batch_size に adjust_batch_size の結果を代入
batch_size = adjust_batch_size(available_memory)

# ブロックコメントは適切にインデント
def complex_function():
    """複雑な処理を行う関数。"""
    # ステップ1: データの前処理
    # 欠損値を補完し、正規化を適用する
    data = preprocess(raw_data)
    
    # ステップ2: 特徴量エンジニアリング
    features = extract_features(data)
    
    return features
```

### コメントのガイドライン

- **Why（なぜ）** を説明する。What（何を）はコードが既に語っている
- 複雑なロジックには必ずコメントを付ける
- TODO コメントは `# TODO: ` で始める
- 行末コメントは最小限に（2スペース空ける）

## インポート

```python
# 標準ライブラリ → サードパーティ → ローカル の順
import os
import sys
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel

from myproject.utils import load_config
from myproject.models import MyModel
```

### インポートのガイドライン

- 各グループ間は1行空ける
- グループ内はアルファベット順
- `from X import *` は使わない
- 相対インポートより絶対インポートを優先

## その他のベストプラクティス

### 行の長さ

- **79文字**を目標（PEP 8標準）
- docstringやコメントは72文字
- 長い行は適切に分割

### 空行

- トップレベルの関数・クラス定義の間は2行
- メソッド定義の間は1行
- 関数内の論理的なセクション間は1行

### 命名の禁止事項

```python
# 避けるべき名前
l = 1  # 小文字のL（数字の1と紛らわしい）
O = 0  # 大文字のO（数字の0と紛らわしい）
I = 1  # 大文字のI（小文字のlと紛らわしい）
```

### ノートブック固有の規約

- ファイル名: 日本語可、番号プレフィックス必須
  - 例: `01_基盤モデルを試す.ipynb`
- セル内コード: 上記規約に準拠
- マークダウンセル: 日本語で説明を記載
- 長いコードブロックは適切にセル分割
