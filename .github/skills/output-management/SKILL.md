---
name: output-management
description: >
  プロジェクトの output/ フォルダ管理規約。
  タイムスタンプ付きサブフォルダによる実行結果の整理と追跡方法を定義する。
---

# Output Management

プロジェクトの実行結果を整理・追跡するための output/ フォルダ管理規約。

## 基本原則

1. **output/ 直下にファイルを直接出力しない**
2. **実行ごとにタイムスタンプ付きサブフォルダを作成**
3. **タスク名を明示して後から追跡可能にする**

## フォルダ命名規則

```
output/YYYYMMDD-HHMMSS_[task名]/
```

### 構成要素

- `YYYYMMDD`: 実行日（年月日）
- `HHMMSS`: 実行時刻（時分秒）
- `task名`: 実行タスクの簡潔な説明（英語、スネークケース）

### 例

```
output/20260207-143025_finetune_bert/
output/20260208-091530_data_preprocessing/
output/20260208-152045_inference_test/
output/20260209-103012_hyperparameter_search/
```

## サブフォルダ構造

各実行フォルダの中は自由に構成できるが、以下を推奨:

```
output/20260207-143025_finetune_bert/
├── args.yaml              # 実行時のハイパーパラメータ・設定
├── model/                 # 保存されたモデルチェックポイント
│   ├── checkpoint_epoch_10.pt
│   └── best_model.pt
├── logs/                  # ログファイル
│   ├── train.log
│   └── tensorboard/
├── results.csv            # 実験結果の数値データ
├── plots/                 # 可視化
│   ├── loss_curve.png
│   └── confusion_matrix.png
└── README.md              # 実行内容のメモ（任意）
```

## 実装パターン

### Python での実装例

```python
from datetime import datetime
from pathlib import Path

def create_output_dir(task_name: str, base_dir: Path = Path("output")) -> Path:
    """タイムスタンプ付き出力ディレクトリを作成する。
    
    Args:
        task_name: タスク名（英語、スネークケース推奨）。
        base_dir: 出力のベースディレクトリ。デフォルトは "output"。
    
    Returns:
        作成された出力ディレクトリのパス。
    
    Examples:
        >>> output_dir = create_output_dir("finetune_bert")
        >>> print(output_dir)
        output/20260207-143025_finetune_bert
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = base_dir / f"{timestamp}_{task_name}"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

# 使用例
if __name__ == "__main__":
    # 実行開始時にディレクトリ作成
    output_dir = create_output_dir("train_model")
    
    # ログ保存
    log_file = output_dir / "train.log"
    
    # モデル保存
    model_dir = output_dir / "model"
    model_dir.mkdir(exist_ok=True)
    
    # 結果保存
    results_file = output_dir / "results.csv"
```

### ノートブックでの使用例

```python
# セル1: 出力ディレクトリ準備
from datetime import datetime
from pathlib import Path

task_name = "data_exploration"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
output_dir = Path("output") / f"{timestamp}_{task_name}"
output_dir.mkdir(parents=True, exist_ok=True)

print(f"出力先: {output_dir}")

# セル2以降: 結果を保存
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(data)
fig.savefig(output_dir / "plot.png")
plt.close()

# データフレーム保存
df.to_csv(output_dir / "processed_data.csv", index=False)
```

## タスク名のガイドライン

### 推奨される命名

- **動詞 + 名詞**: `train_model`, `evaluate_performance`, `preprocess_data`
- **明確な目的**: 何をしたか一目でわかる
- **スネークケース**: 単語を `_` で区切る

### 例

```
✅ 良い例:
- finetune_bert
- inference_test
- data_preprocessing
- hyperparameter_search
- model_comparison
- ablation_study

❌ 避ける例:
- test (あいまい)
- exp1, exp2 (番号だけでは内容不明)
- temp (一時的なものは temp/ フォルダへ)
- my_experiment (所有者情報は不要)
```

## 設定ファイルの保存

実験の再現性のため、実行時の設定を保存する:

```python
import yaml

def save_config(output_dir: Path, config: dict) -> None:
    """設定をYAMLで保存する。
    
    Args:
        output_dir: 出力ディレクトリ。
        config: 保存する設定の辞書。
    """
    config_file = output_dir / "args.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

# 使用例
config = {
    "model": "bert-base-uncased",
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 10,
    "seed": 42,
}

output_dir = create_output_dir("finetune_bert")
save_config(output_dir, config)
```

## 古い出力の管理

### 定期的なクリーンアップ

output/ フォルダが肥大化した場合:

1. **必要なもの**: 重要な実験結果は別の場所（例: `results/` や `experiments/`）に移動
2. **一時的なもの**: 削除
3. **参考用**: 圧縮して保存

```python
# 30日以上前の出力を自動削除（例）
from datetime import datetime, timedelta
from pathlib import Path

def cleanup_old_outputs(days: int = 30, base_dir: Path = Path("output")):
    """古い出力ディレクトリを削除する。
    
    Args:
        days: 保持する日数。
        base_dir: 出力のベースディレクトリ。
    """
    cutoff = datetime.now() - timedelta(days=days)
    
    for item in base_dir.iterdir():
        if not item.is_dir():
            continue
        
        # YYYYMMDD-HHMMSS 形式のタイムスタンプを解析
        try:
            timestamp_str = item.name.split("_")[0]
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
            
            if timestamp < cutoff:
                print(f"削除: {item}")
                # shutil.rmtree(item)  # 実際に削除する場合はコメント解除
        except (ValueError, IndexError):
            # タイムスタンプ形式でない場合はスキップ
            continue
```

## まとめ

- **一貫性**: 全ての実行で同じ規約を使用
- **追跡性**: タイムスタンプとタスク名で実行を特定可能
- **整理**: 出力は個別のフォルダに隔離
- **再現性**: 設定ファイルを保存して実験を再現可能にする
