# my.github

新規リポジトリに `.github` フォルダのテンプレートを追加するためのテンプレートリポジトリ。
GitHub Copilot のカスタマイズ機能（カスタムインストラクション、プロンプトファイル、カスタムエージェント、エージェントスキル）を活用するためのファイル構成が含まれている。

同梱されている例は Python + 機械学習プロジェクト向けに記述されているが、構造自体は言語やフレームワークを問わず利用できる。

## 使い方

1. このリポジトリの `.github/` フォルダをプロジェクトのルートにコピーする
2. 各ファイル内の HTML コメント（`<!-- ... -->`）を読み、自分のプロジェクトに合わせて内容を書き換える
3. 不要なファイルやフォルダは削除する

## ディレクトリ構成

```
.github/
├── copilot-instructions.md                      # 常時適用のカスタムインストラクション
├── instructions/
│   ├── python.instructions.md                   # Python ファイル向けインストラクション
│   └── notebook.instructions.md                 # Jupyter Notebook 向けインストラクション
├── prompts/
│   └── review-code.prompt.md                    # ML コードレビュー用プロンプト
├── agents/
│   └── beast-mode.agent.md                      # 自律型高性能エージェント
└── skills/
    └── skill-creator/
        ├── SKILL.md                             # スキル作成支援スキル
        └── scripts/
            ├── init_skill.py                    # スキル初期化スクリプト
            └── quick_validate.py                # スキルバリデーションスクリプト
```

## 各ファイルの役割

### copilot-instructions.md -- 常時適用のインストラクション

リポジトリ全体に自動適用されるカスタムインストラクション。プロジェクト概要、技術スタック、コーディング規約、ディレクトリ構成などを記載する。

- 適用タイミング: すべての Copilot Chat リクエストに自動付加
- 対応環境: VS Code / Visual Studio / GitHub.com
- ファイル内の HTML コメントに記載方法の詳細あり

### instructions/*.instructions.md -- パス固有のインストラクション

`applyTo` で指定した glob パターンにマッチするファイルに対してのみ適用されるインストラクション。言語やフレームワークごとに分けて定義する。

- 適用タイミング: `applyTo` パターンに一致するファイルの編集時に自動適用
- 同梱例:
  - `python.instructions.md` -- Python スクリプト向け（型ヒント、import 順序、uv 使用規約など）
  - `notebook.instructions.md` -- Jupyter Notebook 向け（命名規則、セル構成、サニティチェックなど）

### prompts/*.prompt.md -- プロンプトファイル

チャットで `/コマンド名` として呼び出せる再利用可能なプロンプト。よくあるタスクのワークフローを定義する。

- 適用タイミング: ユーザーが `/` コマンドで明示的に呼び出した時のみ
- 同梱例: `/review-code` -- ML コードの品質・再現性・パフォーマンスを観点としたレビュー

### agents/*.agent.md -- カスタムエージェント

AI に特定のペルソナ（役割）を持たせる定義ファイル。使用可能なツールや振る舞いをカスタマイズできる。

- 適用タイミング: エージェントピッカーで選択した時
- 同梱例: `beast-mode` -- 問題が完全に解決するまで自律的に作業を続行するエージェント

### skills/*/SKILL.md -- エージェントスキル

オンデマンドで読み込まれる専門的な能力パッケージ。スクリプトやドキュメントなどのリソースを含められる。Agent Skills 標準（agentskills.io）に準拠。

- 適用タイミング: タスクに関連すると判断された場合に自動的に読み込み
- 同梱例: `skill-creator` -- 新しいスキルの作成・バリデーションを支援するスキル
- Anthropic のベストプラクティス（簡潔さ、段階的開示、自由度の調整）に従って構成

## カスタマイズの指針

### プロジェクトに合わせて変更すべき箇所

- `copilot-instructions.md`: プロジェクト概要、技術スタック、ディレクトリ構成、ビルドコマンド
- `instructions/`: `applyTo` のパターンと言語固有のルール
- `prompts/`: プロジェクトで頻繁に行うタスクに合わせたプロンプト
- `agents/`: チームのワークフローに合わせたエージェント定義
- `skills/`: プロジェクト固有の自動化やドメイン知識

### ファイルの追加例

- `instructions/test.instructions.md` -- テストコード向けインストラクション（`applyTo: "test/**"`）
- `prompts/generate-test.prompt.md` -- テスト自動生成プロンプト
- `agents/planner.agent.md` -- 設計・計画に特化したエージェント
- `skills/deploy/SKILL.md` -- デプロイメント手順のスキル

## 参考リンク

- [VS Code: AI カスタマイズ概要](https://code.visualstudio.com/docs/copilot/customization/overview)
- [VS Code: カスタムインストラクション](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code: プロンプトファイル](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [VS Code: カスタムエージェント](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code: エージェントスキル](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills 標準](https://agentskills.io/)
- [Anthropic Agent Skills リポジトリ](https://github.com/anthropics/skills)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
