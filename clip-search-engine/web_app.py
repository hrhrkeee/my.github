"""Gradio Webアプリ版 CLIP日本語画像・動画検索エンジン。

ブラウザベースのUIで画像・動画の登録と検索を行う。
"""

import logging
from pathlib import Path
from typing import Any

import gradio as gr
import numpy as np
from PIL import Image

from search_engine import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS, SearchEngine
from video_processor import extract_frames_by_count

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# デフォルトパス
DEFAULT_DB_DIR = Path(__file__).parent / "db"
DEFAULT_CACHE_DIR = Path(__file__).parent / "model"


class WebSearchEngine:
    """Webアプリ用の検索エンジンラッパー。

    Gradioとの連携を容易にするためのメソッドを提供する。
    """

    def __init__(self) -> None:
        """検索エンジンを初期化する。"""
        self.engine: SearchEngine | None = None
        self._initialized = False

    def initialize(
        self,
        db_dir: str | None = None,
        cache_dir: str | None = None,
    ) -> str:
        """エンジンを初期化する。

        Args:
            db_dir: ベクトルDBの保存先ディレクトリ。
            cache_dir: モデルキャッシュの保存先ディレクトリ。

        Returns:
            初期化結果のメッセージ。
        """
        try:
            db_path = Path(db_dir) if db_dir else DEFAULT_DB_DIR
            cache_path = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR

            self.engine = SearchEngine(db_dir=db_path, cache_dir=cache_path)
            self._initialized = True

            stats = self.engine.get_stats()
            return (
                f"✅ 初期化完了\n"
                f"  DB: {db_path}\n"
                f"  モデルキャッシュ: {cache_path}\n"
                f"  登録数: {stats['total']}件 (画像: {stats['images']}, 動画: {stats['videos']})"
            )
        except Exception as e:
            logger.exception("初期化エラー")
            return f"❌ 初期化エラー: {e}"

    def is_ready(self) -> bool:
        """エンジンが初期化済みかどうか。"""
        return self._initialized and self.engine is not None

    def get_stats(self) -> str:
        """DB統計を取得する。"""
        if not self.is_ready():
            return "⚠️ エンジンが初期化されていません。先に「初期化」タブで初期化してください。"

        stats = self.engine.get_stats()
        entries = self.engine.db.list_entries()

        # 最新10件のエントリを表示
        recent = entries[-10:] if len(entries) > 10 else entries
        recent_list = "\n".join(
            f"  [{e['index']}] {e['metadata']['type']}: {e['metadata']['filename']}"
            for e in reversed(recent)
        )

        return (
            f"📊 DB統計\n"
            f"  合計: {stats['total']}件\n"
            f"  画像: {stats['images']}件\n"
            f"  動画: {stats['videos']}件\n\n"
            f"📋 最新の登録（最大10件）:\n{recent_list if recent_list else '  (なし)'}"
        )

    def register_directory(
        self,
        dir_path: str,
        recursive: bool = True,
        frame_interval: float = 10.0,
        progress: gr.Progress = gr.Progress(),
    ) -> str:
        """ディレクトリ内の画像・動画を一括登録する。

        Args:
            dir_path: 登録対象ディレクトリのパス。
            recursive: サブディレクトリを再帰的に処理するか。
            frame_interval: 動画のフレーム抽出間隔（秒）。
            progress: Gradioプログレスバー。

        Returns:
            登録結果のメッセージ。
        """
        if not self.is_ready():
            return "⚠️ エンジンが初期化されていません。先に「初期化」タブで初期化してください。"

        if not dir_path or not Path(dir_path).exists():
            return f"❌ ディレクトリが見つかりません: {dir_path}"

        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            return f"❌ ディレクトリではありません: {dir_path}"

        try:
            # ファイル数をカウント
            if recursive:
                files = list(dir_path.rglob("*"))
            else:
                files = list(dir_path.iterdir())

            image_files = [
                f for f in files if f.suffix.lower() in IMAGE_EXTENSIONS
            ]
            video_files = [
                f for f in files if f.suffix.lower() in VIDEO_EXTENSIONS
            ]

            total = len(image_files) + len(video_files)
            if total == 0:
                return f"⚠️ 対象ファイルが見つかりません: {dir_path}"

            progress(0, desc="登録準備中...")

            # 登録実行
            registered = 0
            errors = []

            # 画像を登録
            for i, img_path in enumerate(image_files):
                progress(
                    (i + 1) / total,
                    desc=f"画像を登録中 ({i + 1}/{len(image_files)})",
                )
                try:
                    self.engine.register_image(img_path)
                    registered += 1
                except Exception as e:
                    errors.append(f"{img_path.name}: {e}")
                    logger.error("画像登録失敗: %s - %s", img_path, e)

            # 動画を登録
            for i, vid_path in enumerate(video_files):
                progress(
                    (len(image_files) + i + 1) / total,
                    desc=f"動画を登録中 ({i + 1}/{len(video_files)})",
                )
                try:
                    self.engine.register_video(vid_path, frame_interval=frame_interval)
                    registered += 1
                except Exception as e:
                    errors.append(f"{vid_path.name}: {e}")
                    logger.error("動画登録失敗: %s - %s", vid_path, e)

            result = (
                f"✅ 登録完了\n"
                f"  対象: {dir_path}\n"
                f"  登録: {registered}/{total}件\n"
            )

            if errors:
                result += f"\n⚠️ エラー ({len(errors)}件):\n"
                for err in errors[:5]:  # 最初の5件のみ表示
                    result += f"  - {err}\n"
                if len(errors) > 5:
                    result += f"  ... 他 {len(errors) - 5}件"

            return result

        except Exception as e:
            logger.exception("ディレクトリ登録エラー")
            return f"❌ 登録エラー: {e}"

    def search_by_text(
        self, query: str, top_k: int = 10
    ) -> tuple[str, list[tuple[str, str]]]:
        """テキストで検索する。

        Args:
            query: 検索テキスト。
            top_k: 返す結果の数。

        Returns:
            (結果メッセージ, ギャラリー用画像リスト)のタプル。
        """
        if not self.is_ready():
            return (
                "⚠️ エンジンが初期化されていません。先に「初期化」タブで初期化してください。",
                [],
            )

        if not query or not query.strip():
            return "⚠️ 検索テキストを入力してください。", []

        try:
            results = self.engine.search_by_text(query.strip(), top_k=top_k)
            return self._format_results(f"テキスト「{query}」", results)
        except Exception as e:
            logger.exception("テキスト検索エラー")
            return f"❌ 検索エラー: {e}", []

    def search_by_image(
        self, image: np.ndarray | Image.Image | str | None, top_k: int = 10
    ) -> tuple[str, list[tuple[str, str]]]:
        """画像で検索する。

        Args:
            image: クエリ画像。
            top_k: 返す結果の数。

        Returns:
            (結果メッセージ, ギャラリー用画像リスト)のタプル。
        """
        if not self.is_ready():
            return (
                "⚠️ エンジンが初期化されていません。先に「初期化」タブで初期化してください。",
                [],
            )

        if image is None:
            return "⚠️ 検索画像をアップロードしてください。", []

        try:
            # 画像をPILに変換
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image).convert("RGB")
            elif isinstance(image, str):
                pil_image = Image.open(image).convert("RGB")
            else:
                pil_image = image.convert("RGB")

            # 画像をエンコードして検索
            query_vector = self.engine.model.encode_image(pil_image)
            results = self.engine.db.search(query_vector, top_k=top_k)

            return self._format_results("アップロード画像", results)
        except Exception as e:
            logger.exception("画像検索エラー")
            return f"❌ 検索エラー: {e}", []

    def _format_results(
        self, query_desc: str, results: list[dict[str, Any]]
    ) -> tuple[str, list[tuple[Image.Image | str, str]]]:
        """検索結果をフォーマットする。

        Args:
            query_desc: クエリの説明。
            results: 検索結果リスト。

        Returns:
            (結果メッセージ, ギャラリー用画像リスト)のタプル。
            画像はPILオブジェクトとして返す（Gradioのパス制限を回避するため）。
        """
        if not results:
            return f"🔍 {query_desc} の検索結果: 0件", []

        msg_lines = [f"🔍 {query_desc} の検索結果: {len(results)}件\n"]
        gallery_items = []

        for r in results:
            meta = r["metadata"]
            score = r["score"]
            rank = r["rank"]
            path = meta.get("path", "")
            filename = meta.get("filename", "不明")
            media_type = "画像" if meta.get("type") == "image" else "動画"

            msg_lines.append(
                f"[{rank}] {media_type}: {filename} (スコア: {score:.4f})"
            )

            # ギャラリー用の画像を準備（PIL Imageとして読み込む）
            if Path(path).exists():
                try:
                    if meta.get("type") == "image":
                        # 画像をPILで読み込んでサムネイル化
                        img = Image.open(path).convert("RGB")
                        img.thumbnail((512, 512))  # サムネイルサイズに縮小
                        gallery_items.append((img, f"[{rank}] {filename}\n{score:.4f}"))
                    elif meta.get("type") == "video":
                        # 動画の場合は先頭フレームを抽出
                        frames = extract_frames_by_count(path, num_frames=1)
                        if frames:
                            frame = frames[0]
                            frame.thumbnail((512, 512))
                            gallery_items.append(
                                (frame, f"[{rank}] 🎬 {filename}\n{score:.4f}")
                            )
                except Exception as e:
                    logger.warning("サムネイル生成失敗: %s - %s", path, e)

        return "\n".join(msg_lines), gallery_items

    def clear_db(self) -> str:
        """DBをクリアする。"""
        if not self.is_ready():
            return "⚠️ エンジンが初期化されていません。"

        try:
            self.engine.db.clear()
            return "✅ DBをクリアしました。登録数: 0件"
        except Exception as e:
            logger.exception("DBクリアエラー")
            return f"❌ クリアエラー: {e}"


# グローバルなエンジンインスタンス
web_engine = WebSearchEngine()


def create_app() -> gr.Blocks:
    """Gradioアプリを作成する。

    Returns:
        Gradio Blocksインスタンス。
    """
    with gr.Blocks(
        title="CLIP日本語 画像・動画検索エンジン",
    ) as app:
        gr.Markdown(
            """
            # 🖼️ CLIP日本語 画像・動画検索エンジン

            `line-corporation/clip-japanese-base-v2` を使った類似画像・動画検索

            **使い方:**
            1. 「初期化」タブでエンジンを初期化
            2. 「登録」タブでディレクトリ内の画像・動画を登録
            3. 「検索」タブでテキストまたは画像で検索
            """
        )

        with gr.Tabs():
            # === 初期化タブ ===
            with gr.Tab("🔧 初期化"):
                gr.Markdown("### エンジンの初期化")
                with gr.Row():
                    db_dir_input = gr.Textbox(
                        label="DBディレクトリ",
                        placeholder="空欄の場合はデフォルト",
                        value="",
                    )
                    cache_dir_input = gr.Textbox(
                        label="モデルキャッシュディレクトリ",
                        placeholder="空欄の場合はデフォルト",
                        value="",
                    )
                init_btn = gr.Button("初期化", variant="primary")
                init_output = gr.Textbox(label="結果", lines=5, interactive=False)

                init_btn.click(
                    fn=web_engine.initialize,
                    inputs=[db_dir_input, cache_dir_input],
                    outputs=[init_output],
                )

            # === 登録タブ ===
            with gr.Tab("📁 登録"):
                gr.Markdown("### ディレクトリ一括登録")
                dir_input = gr.Textbox(
                    label="登録するディレクトリのパス",
                    placeholder=r"例: D:\写真\旅行2024",
                )
                with gr.Row():
                    recursive_check = gr.Checkbox(
                        label="サブディレクトリも含める", value=True
                    )
                    frame_interval = gr.Slider(
                        minimum=1.0,
                        maximum=60.0,
                        value=10.0,
                        step=1.0,
                        label="動画フレーム抽出間隔（秒）",
                    )
                register_btn = gr.Button("登録開始", variant="primary")
                register_output = gr.Textbox(label="結果", lines=10, interactive=False)

                register_btn.click(
                    fn=web_engine.register_directory,
                    inputs=[dir_input, recursive_check, frame_interval],
                    outputs=[register_output],
                )

            # === 検索タブ ===
            with gr.Tab("🔍 検索"):
                gr.Markdown("### テキストまたは画像で検索")

                with gr.Row():
                    # 左側: 検索入力
                    with gr.Column(scale=1):
                        search_mode = gr.Radio(
                            choices=["テキスト検索", "画像検索"],
                            value="テキスト検索",
                            label="検索モード",
                        )
                        text_input = gr.Textbox(
                            label="検索テキスト",
                            placeholder="例: 猫が寝ている",
                            visible=True,
                        )
                        image_input = gr.Image(
                            label="検索画像",
                            type="pil",
                            visible=False,
                        )
                        top_k_slider = gr.Slider(
                            minimum=1,
                            maximum=50,
                            value=10,
                            step=1,
                            label="検索件数",
                        )
                        search_btn = gr.Button("検索", variant="primary")

                    # 右側: 検索結果
                    with gr.Column(scale=2):
                        search_output = gr.Textbox(
                            label="検索結果",
                            lines=10,
                            interactive=False,
                        )
                        gallery_output = gr.Gallery(
                            label="検索結果プレビュー",
                            columns=4,
                            height="auto",
                            object_fit="contain",
                        )

                # 検索モード切り替え
                def toggle_search_mode(mode: str):
                    return (
                        gr.update(visible=mode == "テキスト検索"),
                        gr.update(visible=mode == "画像検索"),
                    )

                search_mode.change(
                    fn=toggle_search_mode,
                    inputs=[search_mode],
                    outputs=[text_input, image_input],
                )

                # 検索実行
                def do_search(mode: str, text: str, image, top_k: int):
                    if mode == "テキスト検索":
                        return web_engine.search_by_text(text, top_k)
                    else:
                        return web_engine.search_by_image(image, top_k)

                search_btn.click(
                    fn=do_search,
                    inputs=[search_mode, text_input, image_input, top_k_slider],
                    outputs=[search_output, gallery_output],
                )

            # === 管理タブ ===
            with gr.Tab("⚙️ 管理"):
                gr.Markdown("### DB管理")
                stats_btn = gr.Button("統計を表示")
                stats_output = gr.Textbox(label="DB統計", lines=15, interactive=False)
                stats_btn.click(
                    fn=web_engine.get_stats,
                    outputs=[stats_output],
                )

                gr.Markdown("### DBクリア")
                gr.Markdown("⚠️ **注意**: DBをクリアすると全ての登録データが削除されます。")
                clear_btn = gr.Button("DBをクリア", variant="stop")
                clear_output = gr.Textbox(label="結果", lines=2, interactive=False)
                clear_btn.click(
                    fn=web_engine.clear_db,
                    outputs=[clear_output],
                )

        gr.Markdown(
            """
            ---
            **技術スタック**: CLIP Japanese v2 (`line-corporation/clip-japanese-base-v2`) + FAISS
            """
        )

    return app


def main() -> None:
    """Webアプリを起動する。"""
    import argparse

    parser = argparse.ArgumentParser(description="CLIP日本語検索エンジン Webアプリ")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="ホストアドレス"
    )
    parser.add_argument("--port", type=int, default=7860, help="ポート番号")
    parser.add_argument("--share", action="store_true", help="公開URLを生成")
    parser.add_argument(
        "--auto-init", action="store_true", help="起動時に自動初期化"
    )
    args = parser.parse_args()

    # 自動初期化オプション
    if args.auto_init:
        logger.info("エンジンを自動初期化中...")
        result = web_engine.initialize()
        logger.info(result)

    app = create_app()
    app.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
    )


if __name__ == "__main__":
    main()
