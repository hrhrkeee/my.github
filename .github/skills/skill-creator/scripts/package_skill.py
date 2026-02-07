#!/usr/bin/env python3
"""
スキルパッケージングスクリプト
スキルをバリデーションした上で .skill ファイル（zip形式）にパッケージングする。

使い方:
    python package_skill.py <path-to-skill-directory> [output-directory]

例:
    python package_skill.py .github/skills/my-skill
    python package_skill.py .github/skills/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path

# quick_validate からバリデーション関数をインポート
sys.path.insert(0, str(Path(__file__).parent))
from quick_validate import validate_skill


def package_skill(skill_path: str, output_dir: str | None = None) -> Path | None:
    """
    スキルフォルダを .skill ファイルにパッケージングする。

    Args:
        skill_path: スキルフォルダのパス
        output_dir: 出力先ディレクトリ（省略時はカレントディレクトリ）

    Returns:
        作成された .skill ファイルのパス。エラー時はNone
    """
    skill_dir = Path(skill_path).resolve()

    # スキルフォルダの存在確認
    if not skill_dir.exists():
        print(f"Error: スキルフォルダが見つかりません: {skill_dir}")
        return None

    if not skill_dir.is_dir():
        print(f"Error: パスがディレクトリではありません: {skill_dir}")
        return None

    # SKILL.md の存在確認
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md が見つかりません: {skill_dir}")
        return None

    # バリデーション実行
    print("バリデーション中...")
    valid, messages = validate_skill(str(skill_dir))
    for msg in messages:
        print(f"  {msg}")

    if not valid:
        print("\nバリデーションに失敗しました。エラーを修正してから再実行してください。")
        return None

    # 出力先の決定
    if output_dir:
        out_path = Path(output_dir).resolve()
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path = Path.cwd()

    skill_name = skill_dir.name
    skill_file = out_path / f"{skill_name}.skill"

    # パッケージング
    print(f"\nパッケージング中: {skill_file}")

    # 除外するファイル名・ディレクトリ名
    exclude_names = {
        "__pycache__",
        ".git",
        ".DS_Store",
        "Thumbs.db",
    }
    # 除外する拡張子
    exclude_extensions = {".pyc", ".pyo"}

    try:
        with zipfile.ZipFile(skill_file, "w", zipfile.ZIP_DEFLATED) as zf:
            file_count = 0
            for file_path in sorted(skill_dir.rglob("*")):
                if file_path.is_file():
                    # 除外チェック: ファイル名・親ディレクトリ名で判定
                    skip = False
                    if file_path.name in exclude_names:
                        skip = True
                    elif file_path.suffix in exclude_extensions:
                        skip = True
                    else:
                        for parent in file_path.relative_to(skill_dir).parents:
                            if parent.name in exclude_names:
                                skip = True
                                break
                    if skip:
                        continue

                    # zip内の相対パス（skill-name/ をルートにする）
                    arcname = str(
                        Path(skill_name) / file_path.relative_to(skill_dir)
                    ).replace("\\", "/")
                    zf.write(file_path, arcname)
                    file_count += 1
                    print(f"  + {arcname}")

        print(f"\n完了: {skill_file} ({file_count} files)")
        return skill_file

    except Exception as e:
        print(f"Error: パッケージングに失敗: {e}")
        # 失敗時に中途半端なファイルが残っていたら削除
        if skill_file.exists():
            skill_file.unlink()
        return None


def main() -> None:
    if len(sys.argv) < 2:
        print("使い方: package_skill.py <path-to-skill> [output-directory]")
        print()
        print("例:")
        print("  package_skill.py .github/skills/my-skill")
        print("  package_skill.py .github/skills/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
