#!/usr/bin/env python3
"""
スキル初期化スクリプト
新しいスキルのテンプレートディレクトリを作成する。

使い方:
    python init_skill.py <skill-name> --path <output-directory>

例:
    python init_skill.py my-new-skill --path .github/skills
    python init_skill.py debugging-cuda --path .github/skills
"""

import re
import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: >
  [TODO: このスキルが何をするか、いつ使うべきかを具体的に記述する。
  ユーザーがどのような依頼をした場合にこのスキルが発火すべきかを含める。
  三人称で書く。最大1024文字。]
---

# {skill_title}

[TODO: スキルの概要を1-2文で記述する]

## 構成の選択

[TODO: スキルの目的に最適な構成パターンを選択する:

**1. ワークフロー型**（順次処理に最適）
- 明確なステップバイステップ手順がある場合
- 例: ## 概要 → ## ワークフロー → ## Step 1 → ## Step 2...

**2. タスク型**（ツールコレクションに最適）
- 異なる操作・機能を提供する場合
- 例: ## 概要 → ## Quick Start → ## タスク1 → ## タスク2...

**3. ガイドライン型**（標準・仕様に最適）
- ブランドガイドラインやコーディング標準など
- 例: ## 概要 → ## ガイドライン → ## 仕様 → ## 使い方...

パターンは必要に応じて組み合わせられる。
このセクションは完成後に削除すること。]

## [TODO: 最初のセクション名を入れる]

[TODO: コンテンツを追加する。スクリプト・テンプレート・参照への
リンクを必要に応じて含める]

## リソース

### scripts/
実行可能なコード。自動化や繰り返し処理に使用する。
[TODO: 不要であれば削除]

### references/
参照ドキュメント。詳細な情報が必要な場合にAIが読み込む。
[TODO: 不要であれば削除]
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3
\"\"\"
{skill_name} のサンプルスクリプト

このファイルはスクリプトの配置例。
実際のスクリプトに置き換えるか、不要であれば削除する。
\"\"\"

import sys


def main() -> None:
    \"\"\"メイン処理\"\"\"
    print(f"Running {skill_name} script...")
    print("引数:", sys.argv[1:])


if __name__ == "__main__":
    main()
"""

EXAMPLE_REFERENCE = """# {skill_title} リファレンス

このファイルは参照ドキュメントの配置例。
実際のリファレンスに置き換えるか、不要であれば削除する。

## 目次
- セクション1
- セクション2

## セクション1

[TODO: 詳細情報を記述する]

## セクション2

[TODO: 詳細情報を記述する]
"""


def title_case(name: str) -> str:
    """ハイフン区切りの名前をタイトルケースに変換する"""
    return " ".join(word.capitalize() for word in name.split("-"))


def validate_skill_name(name: str) -> tuple[bool, str]:
    """
    スキル名のバリデーションを行う。

    Args:
        name: スキル名

    Returns:
        (成功/失敗, メッセージ)のタプル
    """
    if not name:
        return False, "スキル名が空です"

    if len(name) > 64:
        return False, f"スキル名が64文字を超えています（{len(name)}文字）"

    if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", name):
        return False, "スキル名は小文字・数字・ハイフンのみで構成してください"

    if "--" in name:
        return False, "連続するハイフンは使用できません"

    return True, "OK"


def init_skill(skill_name: str, path: str) -> Path | None:
    """
    新しいスキルディレクトリをテンプレートから作成する。

    Args:
        skill_name: スキル名（小文字、ハイフン区切り）
        path: スキルディレクトリを作成する親ディレクトリ

    Returns:
        作成されたスキルディレクトリのパス。エラー時はNone
    """
    # スキル名のバリデーション
    valid, message = validate_skill_name(skill_name)
    if not valid:
        print(f"Error: {message}")
        return None

    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: ディレクトリが既に存在します: {skill_dir}")
        return None

    # スキルディレクトリを作成
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created: {skill_dir}")
    except Exception as e:
        print(f"Error: ディレクトリの作成に失敗: {e}")
        return None

    # SKILL.mdを作成
    skill_title = title_case(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
    )
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    print("Created: SKILL.md")

    # scripts/ ディレクトリの作成
    try:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / "example.py"
        example_script.write_text(
            EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8"
        )
        print("Created: scripts/example.py")
    except Exception as e:
        print(f"Warning: scripts/ の作成に失敗: {e}")

    # references/ ディレクトリの作成
    try:
        references_dir = skill_dir / "references"
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / "reference.md"
        example_reference.write_text(
            EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding="utf-8"
        )
        print("Created: references/reference.md")
    except Exception as e:
        print(f"Warning: references/ の作成に失敗: {e}")

    print(f"\nスキル '{skill_name}' を {skill_dir} に作成しました。")
    print("\n次のステップ:")
    print("1. SKILL.md の TODO を埋める（description は特に重要）")
    print("2. 不要なサンプルファイルは削除する")
    print("3. quick_validate.py でバリデーションする")

    return skill_dir


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("使い方: init_skill.py <skill-name> --path <path>")
        print()
        print("スキル名の要件:")
        print("  - 小文字、数字、ハイフンのみ")
        print("  - ハイフンで開始・終了しない")
        print("  - 連続ハイフン不可")
        print("  - 最大64文字")
        print("  - ディレクトリ名と一致させる")
        print()
        print("例:")
        print("  init_skill.py debugging-cuda --path .github/skills")
        print("  init_skill.py optimizing-dataloader --path .github/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
