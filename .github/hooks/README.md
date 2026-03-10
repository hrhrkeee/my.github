# Hooks

このディレクトリには、Copilot CLI / agent execution 向けのフック設定例を置いています。

- `copilot-cli-policy.json`
  - セッション開始、プロンプト投入、ツール実行前後、セッション終了時のフック設定。
- `scripts/`
  - フックから呼び出す Bash スクリプト。

## 想定している役割
- protected branch 直作業の警告
- push 系コマンドの抑止
- docs / tests / diagrams の更新漏れの警告
- セッション方針表示
- 実行後サマリ表示

## 注意
- 実際の hook 入力形式や実行環境に応じて、必要ならスクリプトを調整してください。
- 監査ログを残す場合は `.github/hooks/logs/` を `.gitignore` に追加してください。
