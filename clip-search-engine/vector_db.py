"""FAISSを使ったベクトルデータベース管理モジュール。

FAISS IndexFlatIPを使用して、コサイン類似度ベースの近傍検索を行う。
メタデータ（ファイルパス、種別など）はJSON形式で別途保存する。
"""

import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any

import faiss
import numpy as np

logger = logging.getLogger(__name__)

# デフォルトのDBディレクトリ
DEFAULT_DB_DIR = Path(__file__).parent / "db"


class VectorDB:
    """FAISSベースのベクトルデータベース。

    正規化済みベクトルを格納し、内積（=コサイン類似度）で検索する。

    Attributes:
        db_dir: データベースファイルの保存先ディレクトリ。
        index: FAISSインデックス。
        metadata: 各ベクトルに紐づくメタデータのリスト。
        dim: ベクトルの次元数。
    """

    def __init__(self, db_dir: str | Path | None = None, dim: int = 256) -> None:
        """ベクトルDBを初期化する。

        Args:
            db_dir: データベースの保存先ディレクトリ。Noneの場合はデフォルトパス。
            dim: ベクトルの次元数。
        """
        self.db_dir = Path(db_dir) if db_dir else DEFAULT_DB_DIR
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.dim = dim

        self._index_path = self.db_dir / "faiss.index"
        self._metadata_path = self.db_dir / "metadata.json"

        # 既存のDBがあればロード、なければ新規作成
        if self._index_path.exists() and self._metadata_path.exists():
            self._load()
        else:
            # 内積ベースのインデックス（正規化済みベクトルならコサイン類似度と同等）
            self.index = faiss.IndexFlatIP(dim)
            self.metadata: list[dict[str, Any]] = []
            logger.info("新しいベクトルDBを作成しました (dim=%d)", dim)

    def add(self, vector: np.ndarray, meta: dict[str, Any]) -> int:
        """ベクトルとメタデータをDBに追加する。

        Args:
            vector: 正規化済みの特徴量ベクトル (1, dim) または (dim,)。
            meta: このベクトルに紐づくメタデータ。

        Returns:
            追加されたベクトルのインデックスID。
        """
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        vector = vector.astype(np.float32)
        idx = self.index.ntotal
        self.index.add(vector)
        self.metadata.append(meta)

        logger.debug("ベクトル追加: idx=%d, meta=%s", idx, meta)
        return idx

    def add_batch(
        self, vectors: np.ndarray, metas: list[dict[str, Any]]
    ) -> list[int]:
        """複数のベクトルとメタデータをまとめてDBに追加する。

        Args:
            vectors: 正規化済みの特徴量ベクトル (N, dim)。
            metas: 各ベクトルに紐づくメタデータのリスト。

        Returns:
            追加されたベクトルのインデックスIDリスト。
        """
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        vectors = vectors.astype(np.float32)
        start_idx = self.index.ntotal
        self.index.add(vectors)
        self.metadata.extend(metas)

        indices = list(range(start_idx, start_idx + len(metas)))
        logger.debug("バッチ追加: %d件", len(metas))
        return indices

    def search(
        self, query_vector: np.ndarray, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """クエリベクトルに類似するベクトルを検索する。

        Args:
            query_vector: 検索クエリの特徴量ベクトル (1, dim) または (dim,)。
            top_k: 返す結果の最大数。

        Returns:
            類似度スコアとメタデータを含む辞書のリスト。
            各辞書は {"score": float, "metadata": dict} の形式。
        """
        if self.index.ntotal == 0:
            logger.warning("DBが空です。先にデータを登録してください。")
            return []

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        query_vector = query_vector.astype(np.float32)

        # top_kがDB内のベクトル数より大きい場合は調整
        actual_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vector, actual_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append(
                {
                    "score": float(score),
                    "rank": len(results) + 1,
                    "metadata": self.metadata[idx],
                }
            )

        return results

    def save(self) -> None:
        """データベースをディスクに保存する。

        FAISSはUnicodeパス（日本語等）でファイルI/Oに失敗することがあるため、
        一時ディレクトリを介して保存する。
        """
        # 一時ディレクトリでFAISSファイルを作成し、後で移動する
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_index_path = Path(tmp_dir) / "faiss.index"
            faiss.write_index(self.index, str(tmp_index_path))
            # 一時ファイルを目的のパスにコピー
            shutil.copy2(tmp_index_path, self._index_path)

        # メタデータはJSON（Python標準ライブラリ）なのでUnicodeパスでも問題なし
        with open(self._metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

        logger.info(
            "DBを保存しました: %s (件数: %d)", self.db_dir, self.index.ntotal
        )

    def _load(self) -> None:
        """ディスクからデータベースをロードする。

        FAISSはUnicodeパス（日本語等）でファイルI/Oに失敗することがあるため、
        一時ディレクトリを介して読み込む。
        """
        # 一時ディレクトリにコピーしてFAISSで読み込む
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_index_path = Path(tmp_dir) / "faiss.index"
            shutil.copy2(self._index_path, tmp_index_path)
            self.index = faiss.read_index(str(tmp_index_path))

        with open(self._metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        logger.info(
            "DBをロードしました: %s (件数: %d)", self.db_dir, self.index.ntotal
        )

    def count(self) -> int:
        """DBに登録されているベクトルの数を返す。"""
        return self.index.ntotal

    def clear(self) -> None:
        """DBの全データを削除する。"""
        self.index = faiss.IndexFlatIP(self.dim)
        self.metadata = []
        # ファイルも削除
        if self._index_path.exists():
            self._index_path.unlink()
        if self._metadata_path.exists():
            self._metadata_path.unlink()
        logger.info("DBをクリアしました")

    def list_entries(self) -> list[dict[str, Any]]:
        """DBに登録されている全エントリのメタデータを返す。"""
        return [
            {"index": i, "metadata": meta}
            for i, meta in enumerate(self.metadata)
        ]
