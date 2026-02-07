# CLIP Japanese v2 画像・動画検索エンジン

[line-corporation/clip-japanese-base-v2](https://huggingface.co/line-corporation/clip-japanese-base-v2) を使用して、画像・動画をベクトル化し、FAISS ベクトルDBに保存・検索するシステムです。

## 特徴

- **画像のベクトル化**: CLIP Japanese v2 で画像を256次元の特徴量ベクトルに変換
- **動画のベクトル化**: 10秒おきにフレームを抽出し、各フレームの特徴量を平均化して1つのベクトルに集約
- **マルチモーダル検索**: テキスト・画像・動画のいずれかをクエリとして類似メディアを検索
- **ローカルベクトルDB**: FAISS を使用したローカル保存・高速検索

## セットアップ

```bash
# プロジェクトルートで依存パッケージをインストール
uv add "transformers[torch]>=4.57.6,<5.0.0" sentencepiece pillow faiss-cpu av timm tqdm protobuf
```

## 使い方

### 画像を登録

```bash
uv run python clip-search-engine/run.py register --image path/to/image.jpg
```

### 動画を登録

```bash
uv run python clip-search-engine/run.py register --video path/to/video.mp4
```

### ディレクトリ内の全メディアを一括登録

```bash
uv run python clip-search-engine/run.py register --dir path/to/media/
```

### テキストで検索

```bash
uv run python clip-search-engine/run.py search --text "猫が寝ている"
```

### 画像で検索

```bash
uv run python clip-search-engine/run.py search --image path/to/query.jpg
```

### 動画で検索

```bash
uv run python clip-search-engine/run.py search --video path/to/query.mp4
```

### DB情報を表示

```bash
uv run python clip-search-engine/run.py info --list-all
```

### DBをクリア

```bash
uv run python clip-search-engine/run.py clear -y
```

### テスト実行

```bash
uv run python clip-search-engine/test_engine.py
```

## オプション

| オプション | 説明 |
|---|---|
| `--db-dir PATH` | ベクトルDBの保存先ディレクトリ（デフォルト: `clip-search-engine/db/`） |
| `--cache-dir PATH` | CLIPモデルキャッシュの保存先（デフォルト: `clip-search-engine/model/`） |
| `--device cuda\|cpu` | 推論デバイス（省略時は自動検出） |
| `-v, --verbose` | 詳細ログを表示 |
| `--frame-interval SEC` | 動画のフレーム抽出間隔（秒）。デフォルト: 10 |
| `--top-k N` | 検索結果の最大数。デフォルト: 5 |

## アーキテクチャ

```
clip-search-engine/
├── __init__.py          # パッケージ初期化
├── __main__.py          # CLIエントリーポイント
├── cli.py               # CLIインターフェース
├── clip_model.py        # CLIP Japanese v2 モデルラッパー
├── search_engine.py     # 登録・検索エンジン本体
├── vector_db.py         # FAISSベクトルDB管理
├── video_processor.py   # 動画フレーム抽出
├── README.md            # このファイル
├── db/                  # ベクトルDB保存先（自動生成）
└── model/               # モデルキャッシュ（自動生成）
```

## Webアプリ

ブラウザベースのGUIでも利用できます。

### 起動方法

```bash
# 基本起動（http://127.0.0.1:7860）
uv run python clip-search-engine/web_app.py

# 起動時に自動初期化
uv run python clip-search-engine/web_app.py --auto-init

# ホスト・ポート指定
uv run python clip-search-engine/web_app.py --host 0.0.0.0 --port 8080

# 公開URLを生成（Gradio Share機能）
uv run python clip-search-engine/web_app.py --share
```

### Webアプリの機能

- **初期化タブ**: エンジンの初期化（DB・モデルキャッシュパスの設定）
- **登録タブ**: ディレクトリ内の画像・動画を一括登録
- **検索タブ**: テキストまたは画像で類似メディアを検索（結果はギャラリー表示）
- **管理タブ**: DB統計表示・DBクリア

## 動画のベクトル化方法

1. PyAV (av) で動画を開き、シークベースで高速フレーム抽出
2. 10秒おき（設定変更可能）にフレームを抽出
3. 各フレームを CLIP で特徴量ベクトルに変換
4. 全フレームの特徴量を平均化して1つの256次元ベクトルに集約
5. L2正規化して保存

これにより、動画の特徴量ベクトルと画像1枚の特徴量ベクトルが同じ256次元空間に統一されます。
