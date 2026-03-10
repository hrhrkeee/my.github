# Tests

テストは責務別に整理します。

- `unit/`: ローカルロジック
- `integration/`: モジュール結合
- `e2e/`: 利用者視点のシナリオ
- `contract/`: 外部境界の互換性
- `regression/`: 既知不具合の再発防止
- `fixtures/`: 共有データ
- `helpers/`: 共通支援
- `golden/`: golden / snapshot 系の比較対象

## ルール
- 実装変更と同一 change set で追加・更新・削除を行う
- obsolete test を残さない
- fixture / helper / golden の増殖を抑制する
