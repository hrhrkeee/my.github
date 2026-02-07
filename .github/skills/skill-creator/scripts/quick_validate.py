#!/usr/bin/env python3
"""
スキルバリデーションスクリプト
SKILL.md の構造・フロントマター・ディレクトリ整合性を検証する。

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
    yaml = None  # type: ignore[assignment]


# Agent Skills 仕様で許可されたフロントマターキー
ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def validate_skill(skill_path: str) -> tuple[bool, list[str]]:
    """
    スキルディレクトリの包括的なバリデーションを行う。

    Args:
        skill_path: スキルディレクトリのパス

    Returns:
        (成功/失敗, メッセージリスト)のタプル
    """
    skill_dir = Path(skill_path)
    errors: list[str] = []
    warnings: list[str] = []

    # 1. SKILL.md の存在確認
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md が見つかりません"]

    content = skill_md.read_text(encoding="utf-8")

    # 2. フロントマターの存在確認
    if not content.startswith("---"):
        return False, ["YAMLフロントマターがありません（先頭に --- が必要）"]

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, ["フロントマターの形式が不正です"]

    frontmatter_text = match.group(1)

    # 3. YAMLのパース
    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, ["フロントマターはYAML辞書形式である必要があります"]
        except yaml.YAMLError as e:
            return False, [f"YAMLパースエラー: {e}"]
    else:
        # yamlモジュールがない場合は簡易チェック
        warnings.append("PyYAMLがインストールされていません。簡易チェックのみ行います")
        frontmatter: dict = {}  # type: ignore[no-redef]
        for line in frontmatter_text.strip().split("\n"):
            if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                key = line.split(":")[0].strip()
                value = ":".join(line.split(":")[1:]).strip()
                frontmatter[key] = value

    # 4. 許可されたプロパティの確認
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(
            f"予期しないフロントマターキー: {', '.join(sorted(unexpected))}。"
            f"許可されたキー: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 5. 必須フィールドの確認
    if "name" not in frontmatter:
        errors.append("必須フィールド 'name' がありません")
    if "description" not in frontmatter:
        errors.append("必須フィールド 'description' がありません")

    # 6. nameの詳細チェック
    name = str(frontmatter.get("name", "")).strip()
    if name:
        if len(name) > 64:
            errors.append(f"name が64文字を超えています（{len(name)}文字）")

        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", name):
            errors.append("name は小文字・数字・ハイフンのみ、先頭末尾はハイフン不可")

        if "--" in name:
            errors.append("name に連続ハイフンは使用できません")

        # ディレクトリ名との一致チェック
        dir_name = skill_dir.name
        if name != dir_name:
            errors.append(
                f"name '{name}' がディレクトリ名 '{dir_name}' と一致しません"
            )
    elif "name" in frontmatter:
        errors.append("name が空です")

    # 7. descriptionのチェック
    desc = str(frontmatter.get("description", "")).strip()
    if "description" in frontmatter:
        if not desc:
            errors.append("description が空です")
        elif len(desc) > 1024:
            errors.append(f"description が1024文字を超えています（{len(desc)}文字）")

        # TODO マーカーの警告
        if "[TODO" in desc:
            warnings.append("description に未完了の TODO があります")

    # 8. compatibilityのチェック
    compat = frontmatter.get("compatibility")
    if compat is not None:
        compat_str = str(compat).strip()
        if len(compat_str) > 500:
            errors.append(
                f"compatibility が500文字を超えています（{len(compat_str)}文字）"
            )

    # 9. 本文の存在確認
    body = content[match.end() :].strip()
    if not body:
        errors.append("SKILL.md の本文が空です")
    elif len(body.split("\n")) > 500:
        warnings.append(
            f"SKILL.md の本文が500行を超えています（{len(body.split(chr(10)))}行）。"
            "参照ファイルへの分割を推奨します"
        )

    # 10. 本文内の TODO チェック
    if body and "[TODO" in body:
        warnings.append("本文に未完了の TODO があります")

    # 結果の整理
    messages = []
    for w in warnings:
        messages.append(f"WARNING: {w}")
    for e in errors:
        messages.append(f"ERROR: {e}")

    if not errors:
        messages.insert(0, "OK: バリデーション成功")

    return len(errors) == 0, messages


def main() -> None:
    if len(sys.argv) < 2:
        print("使い方: quick_validate.py <path-to-skill>")
        print()
        print("例:")
        print("  quick_validate.py .github/skills/my-skill")
        sys.exit(1)

    skill_path = sys.argv[1]
    valid, messages = validate_skill(skill_path)

    for msg in messages:
        print(msg)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
