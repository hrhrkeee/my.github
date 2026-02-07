"""CLIP検索エンジンのCLIインターフェース。

コマンドラインから画像・動画の登録と検索を行う。

使い方:
    # 画像を登録
    python -m clip-search-engine.cli register --image path/to/image.jpg

    # 動画を登録
    python -m clip-search-engine.cli register --video path/to/video.mp4

    # ディレクトリ内の全メディアを一括登録
    python -m clip-search-engine.cli register --dir path/to/media/

    # テキストで検索
    python -m clip-search-engine.cli search --text "猫が寝ている"

    # 画像で検索
    python -m clip-search-engine.cli search --image path/to/query.jpg

    # 動画で検索
    python -m clip-search-engine.cli search --video path/to/query.mp4

    # DB情報を表示
    python -m clip-search-engine.cli info

    # DBをクリア
    python -m clip-search-engine.cli clear
"""

import argparse
import logging
import sys

from search_engine import SearchEngine


def setup_logging(verbose: bool = False) -> None:
    """ロギングを設定する。"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def print_results(results: list[dict], query_desc: str) -> None:
    """検索結果を見やすく表示する。"""
    print(f"\n{'='*60}")
    print(f"  検索クエリ: {query_desc}")
    print(f"  ヒット件数: {len(results)}")
    print(f"{'='*60}")

    if not results:
        print("  結果なし")
        return

    for r in results:
        meta = r["metadata"]
        score = r["score"]
        rank = r["rank"]
        media_type = "🖼️ 画像" if meta["type"] == "image" else "🎬 動画"
        print(f"\n  [{rank}] {media_type}  スコア: {score:.4f}")
        print(f"      パス: {meta['path']}")
        print(f"      ファイル名: {meta['filename']}")
        if meta["type"] == "video":
            print(f"      抽出フレーム数: {meta.get('num_frames', 'N/A')}")

    print(f"\n{'='*60}")


def cmd_register(args: argparse.Namespace) -> None:
    """登録コマンドを実行する。"""
    engine = SearchEngine(db_dir=args.db_dir, device=args.device)

    if args.image:
        for img_path in args.image:
            try:
                idx = engine.register_image(img_path)
                print(f"✅ 画像を登録しました: {img_path} (ID: {idx})")
            except Exception as e:
                print(f"❌ 画像登録失敗: {img_path} - {e}", file=sys.stderr)

    if args.video:
        for vid_path in args.video:
            try:
                idx = engine.register_video(
                    vid_path, frame_interval=args.frame_interval
                )
                print(f"✅ 動画を登録しました: {vid_path} (ID: {idx})")
            except Exception as e:
                print(f"❌ 動画登録失敗: {vid_path} - {e}", file=sys.stderr)

    if args.dir:
        for dir_path in args.dir:
            try:
                indices = engine.register_directory(
                    dir_path,
                    recursive=not args.no_recursive,
                    frame_interval=args.frame_interval,
                )
                print(f"✅ ディレクトリを登録しました: {dir_path} ({len(indices)}件)")
            except Exception as e:
                print(f"❌ ディレクトリ登録失敗: {dir_path} - {e}", file=sys.stderr)


def cmd_search(args: argparse.Namespace) -> None:
    """検索コマンドを実行する。"""
    engine = SearchEngine(db_dir=args.db_dir, device=args.device)

    if args.text:
        results = engine.search_by_text(args.text, top_k=args.top_k)
        print_results(results, f"テキスト: 「{args.text}」")

    elif args.image:
        results = engine.search_by_image(args.image, top_k=args.top_k)
        print_results(results, f"画像: {args.image}")

    elif args.video:
        results = engine.search_by_video(
            args.video,
            top_k=args.top_k,
            frame_interval=args.frame_interval,
        )
        print_results(results, f"動画: {args.video}")

    else:
        print("検索クエリを指定してください（--text, --image, --video のいずれか）")
        sys.exit(1)


def cmd_info(args: argparse.Namespace) -> None:
    """DB情報を表示する。"""
    engine = SearchEngine(db_dir=args.db_dir, device=args.device)
    stats = engine.get_stats()

    print("\n📊 ベクトルDB情報")
    print(f"  保存先: {engine.db.db_dir}")
    print(f"  登録数: {stats['total']}件")
    print(f"    画像: {stats['images']}件")
    print(f"    動画: {stats['videos']}件")

    if args.list_all:
        entries = engine.db.list_entries()
        print("\n  --- 登録一覧 ---")
        for entry in entries:
            meta = entry["metadata"]
            media_type = "画像" if meta["type"] == "image" else "動画"
            print(f"  [{entry['index']}] {media_type}: {meta['filename']}")


def cmd_clear(args: argparse.Namespace) -> None:
    """DBをクリアする。"""
    engine = SearchEngine(db_dir=args.db_dir, device=args.device)
    count = engine.db.count()

    if not args.yes:
        answer = input(f"DBの全データ({count}件)を削除しますか？ [y/N]: ")
        if answer.lower() != "y":
            print("キャンセルしました。")
            return

    engine.db.clear()
    print(f"✅ DBをクリアしました（{count}件削除）")


def main() -> None:
    """メインエントリーポイント。"""
    parser = argparse.ArgumentParser(
        description="CLIP Japanese v2 画像・動画検索エンジン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--db-dir",
        type=str,
        default=None,
        help="ベクトルDBの保存先ディレクトリ（デフォルト: clip-search-engine/db/）",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="推論デバイス（cuda/cpu）。省略時は自動検出。",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="詳細ログを表示する",
    )

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # register コマンド
    reg_parser = subparsers.add_parser("register", help="画像・動画をDBに登録する")
    reg_parser.add_argument(
        "--image", nargs="+", help="登録する画像ファイルのパス（複数可）"
    )
    reg_parser.add_argument(
        "--video", nargs="+", help="登録する動画ファイルのパス（複数可）"
    )
    reg_parser.add_argument(
        "--dir", nargs="+", help="登録するディレクトリのパス（複数可）"
    )
    reg_parser.add_argument(
        "--frame-interval",
        type=float,
        default=10.0,
        help="動画のフレーム抽出間隔（秒）。デフォルト: 10",
    )
    reg_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="ディレクトリを再帰的に探索しない",
    )

    # search コマンド
    search_parser = subparsers.add_parser("search", help="類似メディアを検索する")
    search_parser.add_argument("--text", type=str, help="テキストで検索")
    search_parser.add_argument("--image", type=str, help="画像で検索")
    search_parser.add_argument("--video", type=str, help="動画で検索")
    search_parser.add_argument(
        "--top-k", type=int, default=5, help="返す結果の最大数。デフォルト: 5"
    )
    search_parser.add_argument(
        "--frame-interval",
        type=float,
        default=10.0,
        help="動画クエリのフレーム抽出間隔（秒）。デフォルト: 10",
    )

    # info コマンド
    info_parser = subparsers.add_parser("info", help="DB情報を表示する")
    info_parser.add_argument(
        "--list-all", action="store_true", help="全エントリを一覧表示する"
    )

    # clear コマンド
    clear_parser = subparsers.add_parser("clear", help="DBの全データを削除する")
    clear_parser.add_argument(
        "-y", "--yes", action="store_true", help="確認なしで削除する"
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    command_map = {
        "register": cmd_register,
        "search": cmd_search,
        "info": cmd_info,
        "clear": cmd_clear,
    }

    command_map[args.command](args)


if __name__ == "__main__":
    main()
