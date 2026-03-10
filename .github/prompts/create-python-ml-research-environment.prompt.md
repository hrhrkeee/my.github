---
name: create-python-ml-research-environment
description: Python機械学習研究プロジェクト向けに、証拠優先で environment.yaml と関連文書を作成・更新する
argument-hint: "追加要件、既知の制約、優先事項、既存構成との差分があれば入力してください"
agent: agent
---
あなたは、このリポジトリの **Python 機械学習研究プロジェクト向け実行環境テンプレート** を整備する担当です。

この prompt は、単なる説明文ではなく、**そのまま実行する作業指示**です。ユーザーが追加情報を与えた場合はそれを優先し、与えていない場合はリポジトリ内の証拠を優先して判断してください。証拠が不足する場合は、推測で断定せず、未確定事項として分離してください。

## ゴール

以下を作成または更新してください。

### 正本
- `project/environment/environment.yaml`

### 補助文書
- `project/environment/detected-environment.md`
- `project/environment/command-matrix.md`
- `project/environment/compatibility-matrix.md`

必要に応じて、以下も更新または提案してください。
- `.gitignore`
- `docs/specs/` 配下の環境仕様書
- `docs/runbooks/` 配下のセットアップ手順
- `tests/` または既存の `test/` 配下の軽量サニティテスト
- `.github/skills/` への Skill 化候補

## 作業原則

### 1. まずリポジトリの証拠を確認する
次の順で証拠を調べてください。

1. `project/environment/environment.yaml`
2. `pyproject.toml`
3. `uv.lock`
4. `README*`, `docs/`, `docs/specs/`, `docs/runbooks/`
5. `Dockerfile*`, `docker-compose*`, `compose.yaml`, `docker/`
6. `.github/workflows/`
7. `main.py`, `src/`, `util/`, `tests/`, `test/`
8. `notebooks/`
9. `requirements*.txt`, `environment*.yml`, `.python-version`, `.tool-versions`

証拠がない事項は断定しないでください。推測が必要な内容は `detected-environment.md` に分離し、`environment.yaml` には根拠のある内容だけを書いてください。

### 2. 不明点は先に質問する
作業を始める前に、足りない情報がある場合は細かな点でも質問してください。特に以下は優先して確認してください。

- 想定 OS: macOS / Linux / Windows / WSL / 混在
- 計算資源: CPU only / CUDA / ROCm / Apple Silicon MPS
- Python の最小・推奨バージョン
- 学習・推論・評価・デプロイ準備のどこまでを対象にするか
- Docker の用途: 開発 / 検証 / デプロイ
- Notebook の役割: 探索専用か、正式資産へ昇格するか
- CI の有無
- データ、重み、生成物の管理方針
- デプロイ対象の有無

ただし、リポジトリの証拠が十分で、未回答でも限定的に進められる場合は、**仮定を明示したうえで** 作業を進めてください。

### 3. このプロジェクトの既定候補
ユーザーから別指定がない限り、以下を既定候補として扱ってください。ただし、証拠が優先です。

- 言語: Python 3.11+
- パッケージマネージャー: `uv`
- ローカル仮想環境: `.venv/` を使用するが、リポジトリには含めない
- 主要ライブラリ候補: PyTorch, Transformers, scikit-learn, pandas, numpy, matplotlib
- Notebook: Jupyter Notebook
- コンテナ: Docker
- エントリーポイント候補: `main.py`

## 必須ルール

### Python 環境・依存管理
- 依存追加は原則 `uv add <package>` を使う
- 開発依存は `uv add --dev <package>` を使う
- 環境再構築は `uv sync` を使う
- `uv pip install` は、明確な理由がある場合を除き標準手段にしない
- `.venv/` は Git 管理対象にしない
- `pyproject.toml` と lock file を再現性の正本として扱う

### コーディング規約
- Python コードは PEP 8 を前提とする
- コメントと docstring は日本語
- 変数名・関数名・クラス名は英語
- Notebook ファイル名は日本語可、先頭に番号を付ける
- 例: `01_基盤モデルを試す.ipynb`

### ディレクトリ構成方針
既存構成を優先してください。既存構成がない場合のみ、以下を既定候補として扱ってください。

- `main.py`: エントリーポイント候補
- `pyproject.toml`: プロジェクト設定・依存関係
- `.env`: 環境変数
- `src/`: モデル定義、学習、推論、前処理、後処理
- `data/`: データセット
- `notebooks/`: 実験・探索用 Notebook
- `util/`: 汎用ユーティリティ
- `model_weights/`: 学習済み重み
- `output/`: 実行結果
- `temp/`: 一時ファイル・一時スクリプト
- `docker/`: Dockerfile, compose, 補助スクリプト
- `tests/` または既存の `test/`: pytest ベースのテスト
- `.github/`: Copilot instructions, prompts, skills, hooks

既存リポジトリに `tests/` がある場合は `tests/` を優先し、`test/` を新設しないでください。

### 出力フォルダ規約
既定候補は以下です。既存仕様があればそちらを優先してください。

- `output/YYYYMMDD-HHMMSS_[task-name]/`

### Notebook 規約
- 日本語ファイル名可
- 実行順番号を先頭につける
- 最初にサニティチェックや最小実行を置く
- 擬似データによる軽量検証を推奨する
- モデル別・テーマ別のサブフォルダを許容する
- Notebook は探索資産として扱い、正式パイプラインへ昇格する場合は `src/` へ移植する方針を優先する

### 既定コマンド候補
実際には証拠で確定してください。

- 環境構築: `uv sync`
- テスト: `uv run pytest tests/` または既存の `uv run pytest test/`
- リント: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- 実行: `uv run python main.py`

### Git 運用
- 編集開始前に新規ブランチを切る
- 論理的なまとまりでコミットする
- コミットメッセージは差分内容に忠実にする
- push はしない
- 必要に応じて最近のコミット履歴と変更傾向を参照する

## 作成するファイルの期待内容

### `project/environment/environment.yaml`
このファイルは正本です。最低限、以下の構造を含めてください。

```yaml
project_name:
default_branch:
runtime:
  language: python
  version:
  notebook:
  container:
package_managers:
  primary: uv
  lock_file:
commands:
  bootstrap:
  run:
  test:
  lint:
  format:
  typecheck:
paths:
  entrypoints:
  source_roots:
  test_roots:
  notebook_roots:
  data_roots:
  artifact_roots:
  temp_roots:
  docker_roots:
artifacts:
  outputs:
  model_weights:
  checkpoints:
ignore:
  gitignore:
ci:
  workflows:
platform:
  os:
  accelerators:
  docker:
libraries:
  training:
  inference:
  data:
  visualization:
quality:
  test_framework:
  linter:
  formatter:
  coverage:
deployment:
  target:
  packaging:
notes:
```

未確定値は空欄または `TBD` にしてください。証拠のない断定は禁止です。

### `project/environment/detected-environment.md`
以下を簡潔に記述してください。
- 参照した根拠ファイル
- そこから何を推定したか
- 未確定事項
- ユーザーへ確認すべき点
- 採用しなかった代替解釈

### `project/environment/command-matrix.md`
表形式で、少なくとも以下を整理してください。
- 目的
- コマンド
- 前提条件
- 成功条件
- 失敗時の確認ポイント

対象には少なくとも以下を含めてください。
- bootstrap
- test
- lint
- format
- notebook 起動
- training 実行
- inference 実行
- docker build
- docker run

### `project/environment/compatibility-matrix.md`
少なくとも以下を整理してください。
- OS ごとの差異
- CPU / CUDA / ROCm / Apple Silicon の差異
- Docker 利用可否と制約
- Notebook 運用上の注意
- Python バージョン互換性
- 主要ライブラリの互換性懸念

## ドキュメント同期ルール
以下に該当する場合は、環境ファイルだけで終わらせず、関連ドキュメントも更新してください。

- 開発手順が変わる
- 依存管理ルールが変わる
- テストや lint の実行方法が変わる
- Docker の役割が変わる
- Notebook 運用ルールが変わる
- 出力物や重みの管理方針が変わる

既存の仕様書が見つかればそこを更新し、見つからなければ新規作成候補を提案してください。

## テストとサニティチェック
必要に応じて、以下を提案または追加してください。

- import レベルのサニティチェック
- CPU で完結する最小テスト
- 擬似データを使った前処理・学習・推論の軽量確認
- Notebook 実行前の最小確認手順

重い GPU 前提の検証よりも、まず軽量で再現しやすい経路を優先してください。

## 知見蓄積ルール
再利用価値の高い知見を見つけた場合は、次の順で扱ってください。

1. まず `docs/runbooks/` または `docs/regressions/` へ正本として残すべきかを判断する
2. 他の場面でも再利用性が高い場合のみ `.github/skills/<skill-name>/SKILL.md` への昇格を提案する
3. Skill 名は小文字ハイフン区切りにする

提案形式は次でよいです。

```text
知見候補: <title>
- 問題:
- 解決:
- 再利用性:
- 正本候補: docs/runbooks または docs/regressions
- Skill 化候補: .github/skills/<skill-name>/
```

## 最終出力の形式
最終回答では、少なくとも以下を明示してください。

1. 確認した根拠ファイル
2. 置いた仮定
3. 作成・更新したファイル一覧
4. `environment.yaml` の要点
5. 未確定事項
6. 次にユーザーへ確認すべき質問
7. 必要なら Skill 化候補

## 禁止事項
- 証拠なしに CUDA や特定 GPU を前提化しない
- `uv pip install` を標準手段として採用しない
- `.venv/` や重みファイルをリポジトリ管理対象にしない
- Notebook を正式プロダクションコードの唯一の実装場所にしない
- 既存構成を無視して新規ディレクトリを乱立させない
- `environment.yaml` に根拠のない断定を書き込まない
