"""画像・動画の登録と検索を行う検索エンジン。

CLIPモデルとFAISSベクトルDBを統合し、画像・動画・テキストによる
類似メディア検索を提供する。
"""

import logging
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from tqdm import tqdm

from clip_model import CLIPJapaneseModel
from vector_db import VectorDB
from video_processor import extract_frames

logger = logging.getLogger(__name__)

# 対応する画像・動画の拡張子
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"}


class SearchEngine:
    """CLIP Japanese v2 ベースのメディア検索エンジン。

    画像・動画をベクトル化してDBに登録し、
    画像・動画・テキストをクエリとして類似メディアを検索する。

    Attributes:
        model: CLIPモデルラッパー。
        db: FAISSベクトルDB。
    """

    def __init__(
        self,
        db_dir: str | Path | None = None,
        device: str | None = None,
        cache_dir: str | Path | None = None,
    ) -> None:
        """検索エンジンを初期化する。

        Args:
            db_dir: ベクトルDBの保存先。Noneの場合はデフォルトパス。
            device: CLIP推論に使用するデバイス。
            cache_dir: CLIPモデルキャッシュの保存先。Noneの場合はデフォルトパス。
        """
        self.model = CLIPJapaneseModel(device=device, cache_dir=cache_dir)
        self.db = VectorDB(db_dir=db_dir, dim=self.model.embedding_dim)

    def register_image(self, image_path: str | Path) -> int:
        """画像をDBに登録する。

        Args:
            image_path: 画像ファイルのパス。

        Returns:
            登録されたインデックスID。
        """
        image_path = Path(image_path).resolve()
        if not image_path.exists():
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")

        logger.info("画像を登録中: %s", image_path.name)

        image = Image.open(image_path).convert("RGB")
        vector = self.model.encode_image(image)

        meta = {
            "type": "image",
            "path": str(image_path),
            "filename": image_path.name,
        }

        idx = self.db.add(vector.squeeze(0), meta)
        self.db.save()

        logger.info("画像を登録しました: %s (idx=%d)", image_path.name, idx)
        return idx

    def register_video(
        self,
        video_path: str | Path,
        frame_interval: float = 10.0,
    ) -> int:
        """動画をDBに登録する。

        動画内のフレームを指定間隔で抽出し、各フレームの特徴量ベクトルを
        平均化して1つのベクトルとして登録する。

        Args:
            video_path: 動画ファイルのパス。
            frame_interval: フレーム抽出間隔（秒）。

        Returns:
            登録されたインデックスID。
        """
        video_path = Path(video_path).resolve()
        if not video_path.exists():
            raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

        logger.info("動画を登録中: %s (interval=%.1fs)", video_path.name, frame_interval)

        # フレームを抽出
        frames = extract_frames(video_path, interval_sec=frame_interval)
        if not frames:
            raise RuntimeError(f"動画からフレームを抽出できませんでした: {video_path}")

        # 各フレームの特徴量を取得
        # メモリ効率のためバッチ処理（大量フレームの場合は分割）
        batch_size = 16
        all_features = []
        for i in range(0, len(frames), batch_size):
            batch_frames = frames[i : i + batch_size]
            features = self.model.encode_images(batch_frames)
            all_features.append(features)

        # 全フレームの特徴量を結合して平均化
        all_features_np = np.concatenate(all_features, axis=0)  # (N, dim)
        avg_vector = np.mean(all_features_np, axis=0, keepdims=True)  # (1, dim)

        # L2正規化（平均化後に再正規化）
        avg_vector = avg_vector / np.linalg.norm(avg_vector, axis=-1, keepdims=True)

        meta = {
            "type": "video",
            "path": str(video_path),
            "filename": video_path.name,
            "num_frames": len(frames),
            "frame_interval_sec": frame_interval,
        }

        idx = self.db.add(avg_vector.squeeze(0), meta)
        self.db.save()

        logger.info(
            "動画を登録しました: %s (idx=%d, frames=%d)",
            video_path.name,
            idx,
            len(frames),
        )
        return idx

    def register_directory(
        self,
        dir_path: str | Path,
        recursive: bool = True,
        frame_interval: float = 10.0,
    ) -> list[int]:
        """ディレクトリ内の画像・動画を一括登録する。

        Args:
            dir_path: 対象ディレクトリのパス。
            recursive: サブディレクトリも再帰的に処理するか。
            frame_interval: 動画のフレーム抽出間隔（秒）。

        Returns:
            登録されたインデックスIDのリスト。
        """
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"ディレクトリが見つかりません: {dir_path}")

        # ファイルを収集
        if recursive:
            files = list(dir_path.rglob("*"))
        else:
            files = list(dir_path.iterdir())

        # 画像と動画に分類
        image_files = sorted(
            f for f in files if f.suffix.lower() in IMAGE_EXTENSIONS
        )
        video_files = sorted(
            f for f in files if f.suffix.lower() in VIDEO_EXTENSIONS
        )

        logger.info(
            "ディレクトリ登録: %s (画像: %d件, 動画: %d件)",
            dir_path,
            len(image_files),
            len(video_files),
        )

        indices: list[int] = []

        # 画像を登録
        for img_path in tqdm(image_files, desc="画像を登録中", disable=not image_files):
            try:
                idx = self.register_image(img_path)
                indices.append(idx)
            except Exception as e:
                logger.error("画像登録失敗: %s - %s", img_path, e)

        # 動画を登録
        for vid_path in tqdm(video_files, desc="動画を登録中", disable=not video_files):
            try:
                idx = self.register_video(vid_path, frame_interval=frame_interval)
                indices.append(idx)
            except Exception as e:
                logger.error("動画登録失敗: %s - %s", vid_path, e)

        logger.info("ディレクトリ登録完了: %d件登録", len(indices))
        return indices

    def search_by_image(
        self, image_path: str | Path, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """画像をクエリとして類似メディアを検索する。

        Args:
            image_path: クエリ画像のパス。
            top_k: 返す結果の最大数。

        Returns:
            検索結果のリスト。
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")

        logger.info("画像で検索中: %s", image_path.name)

        image = Image.open(image_path).convert("RGB")
        query_vector = self.model.encode_image(image)
        results = self.db.search(query_vector, top_k=top_k)

        return results

    def search_by_video(
        self,
        video_path: str | Path,
        top_k: int = 5,
        frame_interval: float = 10.0,
    ) -> list[dict[str, Any]]:
        """動画をクエリとして類似メディアを検索する。

        Args:
            video_path: クエリ動画のパス。
            top_k: 返す結果の最大数。
            frame_interval: フレーム抽出間隔（秒）。

        Returns:
            検索結果のリスト。
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

        logger.info("動画で検索中: %s", video_path.name)

        # フレームを抽出して平均ベクトルを作成
        frames = extract_frames(video_path, interval_sec=frame_interval)
        if not frames:
            raise RuntimeError(f"動画からフレームを抽出できませんでした: {video_path}")

        batch_size = 16
        all_features = []
        for i in range(0, len(frames), batch_size):
            batch_frames = frames[i : i + batch_size]
            features = self.model.encode_images(batch_frames)
            all_features.append(features)

        all_features_np = np.concatenate(all_features, axis=0)
        avg_vector = np.mean(all_features_np, axis=0, keepdims=True)
        avg_vector = avg_vector / np.linalg.norm(avg_vector, axis=-1, keepdims=True)

        results = self.db.search(avg_vector, top_k=top_k)

        return results

    def search_by_text(
        self, text: str, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """テキストをクエリとして類似メディアを検索する。

        Args:
            text: 検索テキスト（日本語対応）。
            top_k: 返す結果の最大数。

        Returns:
            検索結果のリスト。
        """
        logger.info("テキストで検索中: '%s'", text)

        query_vector = self.model.encode_text(text)
        results = self.db.search(query_vector, top_k=top_k)

        return results

    def get_stats(self) -> dict[str, Any]:
        """DBの統計情報を返す。"""
        entries = self.db.list_entries()
        image_count = sum(1 for e in entries if e["metadata"]["type"] == "image")
        video_count = sum(1 for e in entries if e["metadata"]["type"] == "video")

        return {
            "total": self.db.count(),
            "images": image_count,
            "videos": video_count,
        }
