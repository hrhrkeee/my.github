#!/usr/bin/env python3
"""
スキル初期化スクリプト
新しいスキルのテンプレートディレクトリを作成する。

使い方:
    python init_skill.py <skill-name> --path <output-directory>

例:
    python init_skill.py my-new-skill --path .github/skills
    python init_skill.py data-analyzer --path .github/skills
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: >
  [TODO: このスキルが何をするか、いつ使うべきかを具体的に記述する。
  ユーザーがどのような依頼をした場合にこのスキルが発火すべきかを含める。]
---

# {skill_title}

[TODO: スキルの概要を1-2文で記述する]

## 手順

[TODO: スキルの使い方・手順を記述する]

## ガイドライン

[TODO: スキル使用時のガイドラインを記述する]
"""


def title_case(name: str) -> str:
    """ハイフン区切りの名前をタイトルケースに変換する"""
    return " ".join(word.capitalize() for word in name.split("-"))


def init_skill(skill_name: str, path: str) -> Path | None:
    """
    新しいスキルディレクトリをテンプレートから作成する。

    Args:
        skill_name: スキル名（小文字、ハイフン区切り）
        path: スキルディレクトリを作成する親ディレクトリ

    Returns:
        作成されたスキルディレクトリのパス。エラー時はNone
    """
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
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / ".gitkeep").touch()
    print("Created: scripts/")

    # references/ ディレクトリの作成
    references_dir = skill_dir / "references"
    references_dir.mkdir(exist_ok=True)
    (references_dir / ".gitkeep").touch()
    print("Created: references/")

    print(f"\nスキル '{skill_name}' を {skill_dir} に作成しました。")
    print("\n次のステップ:")
    print("1. SKILL.md の TODO を埋める（description は特に重要）")
    print("2. 不要なディレクトリは削除する")
    print("3. quick_validate.py でバリデーションする")

    return skill_dir


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("使い方: init_skill.py <skill-name> --path <path>")
        print()
        print("スキル名の要件:")
        print("  - 小文字、数字、ハイフンのみ")
        print("  - 最大64文字")
        print()
        print("例:")
        print("  init_skill.py my-new-skill --path .github/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
