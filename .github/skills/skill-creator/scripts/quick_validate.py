#!/usr/bin/env python3
"""
スキルバリデーションスクリプト
SKILL.mdの構造とフロントマターを検証する。

使い方:
    python quick_validate.py <path-to-skill-directory>

例:
    python quick_validate.py .github/skills/my-skill
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def validate_skill(skill_path: str) -> tuple[bool, str]:
    """
    スキルディレクトリの基本的なバリデーションを行う。

    Args:
        skill_path: スキルディレクトリのパス

    Returns:
        (成功/失敗, メッセージ)のタプル
    """
    skill_path = Path(skill_path)

    # SKILL.mdの存在確認
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md が見つかりません"

    content = skill_md.read_text(encoding="utf-8")

    # フロントマターの存在確認
    if not content.startswith("---"):
        return False, "YAMLフロントマターがありません（先頭に --- が必要）"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "フロントマターの形式が不正です"

    frontmatter_text = match.group(1)

    # YAMLのパース
    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "フロントマターはYAML辞書形式である必要があります"
        except yaml.YAMLError as e:
            return False, f"YAMLパースエラー: {e}"
    else:
        # yamlモジュールがない場合は簡易チェック
        frontmatter = {}
        for line in frontmatter_text.strip().split("\n"):
            if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                key = line.split(":")[0].strip()
                frontmatter[key] = True

    # 許可されたプロパティの確認
    allowed = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    unexpected = set(frontmatter.keys()) - allowed
    if unexpected:
        return False, f"予期しないフロントマターキー: {', '.join(sorted(unexpected))}"

    # 必須フィールドの確認
    if "name" not in frontmatter:
        return False, "必須フィールド 'name' がありません"
    if "description" not in frontmatter:
        return False, "必須フィールド 'description' がありません"

    # nameの形式チェック
    name = str(frontmatter.get("name", "")).strip()
    if not name:
        return False, "name が空です"
    if len(name) > 64:
        return False, f"name が64文字を超えています（{len(name)}文字）"
    if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", name):
        return False, "name は小文字・数字・ハイフンのみで構成してください"

    # descriptionのチェック
    desc = str(frontmatter.get("description", "")).strip()
    if not desc:
        return False, "description が空です"
    if len(desc) > 1024:
        return False, f"description が1024文字を超えています（{len(desc)}文字）"

    # 本文の存在確認
    body = content[match.end():].strip()
    if not body:
        return False, "SKILL.md の本文が空です"

    return True, "バリデーション成功"


def main() -> None:
    if len(sys.argv) < 2:
        print("使い方: quick_validate.py <path-to-skill>")
        sys.exit(1)

    skill_path = sys.argv[1]
    valid, message = validate_skill(skill_path)

    if valid:
        print(f"OK: {message}")
        sys.exit(0)
    else:
        print(f"NG: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
