# GitHub Copilot 戦略テンプレート

このテンプレートは、GitHub Copilot を以下の方針で運用するための骨格です。

- `copilot-instructions.md` は薄く保つ
- 詳細ルールは path-specific instructions に分割する
- 再利用可能な問題解決手順は Skills に蓄積する
- 役割特化は custom agents に分離する
- 実行時の強制事項は Hooks で担保する
- 仕様・設計・運用・既知回帰は `docs/` に正本として残す
- 実行環境は `project/environment/environment.yaml` を正本とする
- Git はブランチ・コミットまで自動化対象、push は明示指示がない限り禁止する

## 使い方

1. このテンプレート一式を既存リポジトリのルートへ展開する
2. `project/environment/environment.yaml` を実プロジェクトに合わせて更新する
3. `.github/copilot-instructions.md` の汎用ルールを維持しつつ、必要な規約を `.github/instructions/` に追加する
4. `.github/skills/` のテンプレートを実プロジェクトに合わせて具体化する
5. `.github/agents/` を IDE / CLI から読み込み、必要に応じて agent 選択または subagent 運用を行う
6. `.github/hooks/copilot-cli-policy.json` と `.github/hooks/scripts/` をベースに、禁止操作・品質ゲート・監査ルールを調整する

## 同梱物の要点

- `.github/copilot-instructions.md`
  - 全体ルール。100 行以内。
- `.github/instructions/*.instructions.md`
  - docs / tests / diagrams / architecture / env / git 向けの詳細ルール。
- `.github/agents/*.agent.md`
  - 実装、仕様維持、テスト、図、Git 運用の各専門エージェント。
- `.github/skills/*/SKILL.md`
  - 要件整理、設計パターン選定、仕様同期、テスト保守、回帰防止、環境検出、Git 運用、Draw.io 編集。
- `.github/prompts/*.prompt.md`
  - 実行用テンプレート。環境差や preview 状態を踏まえた補助導線。
- `.github/hooks/copilot-cli-policy.json`
  - CLI / エージェント向けのフック設定例。
- `docs/`
  - 仕様、ADR、アーキテクチャ、運用、回帰知見の正本。
- `project/environment/`
  - 実行環境定義の正本。

## 前提

- Git は利用可能である
- push は明示指示がない限り行わない
- Draw.io の正本形式は `.drawio`、配布兼編集向けは `.drawio.svg` を想定する
- Copilot 機能の対応状況は IDE / CLI / GitHub.com に差があるため、このテンプレートは「最低限 instructions だけでも成立する」構成を優先している
