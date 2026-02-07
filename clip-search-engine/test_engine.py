"""CLIP検索エンジンの動作確認テストスクリプト。

各モジュールのインポートと基本的な動作を確認する。
テスト用に擬似画像を生成して登録・検索の一連のフローを検証する。
"""

import os
import sys
import tempfile

# パスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import Image


def test_video_processor() -> None:
    """動画プロセッサーのインポートテスト。"""
    import video_processor  # noqa: F401

    # インポートできることを確認（関数の存在チェック）
    assert hasattr(video_processor, "extract_frames")
    assert hasattr(video_processor, "extract_frames_by_count")
    assert hasattr(video_processor, "get_video_info")

    print("✅ video_processor: インポート成功")


def test_vector_db() -> None:
    """ベクトルDBの基本動作テスト。"""
    from vector_db import VectorDB

    # 一時ディレクトリでテスト
    with tempfile.TemporaryDirectory() as tmp_dir:
        db = VectorDB(db_dir=tmp_dir, dim=768)
        assert db.count() == 0, "初期状態でDB件数が0であること"

        # ダミーベクトルを追加
        dummy_vec = np.random.randn(768).astype(np.float32)
        dummy_vec = dummy_vec / np.linalg.norm(dummy_vec)
        meta = {"type": "image", "path": "/tmp/test.jpg", "filename": "test.jpg"}

        idx = db.add(dummy_vec, meta)
        assert idx == 0, "最初のインデックスが0であること"
        assert db.count() == 1, "追加後の件数が1であること"

        # 検索テスト
        results = db.search(dummy_vec, top_k=1)
        assert len(results) == 1, "検索結果が1件であること"
        assert results[0]["score"] > 0.99, "同一ベクトルのスコアが1に近いこと"
        assert results[0]["metadata"]["filename"] == "test.jpg"

        # 保存・ロードテスト
        db.save()
        db2 = VectorDB(db_dir=tmp_dir, dim=768)
        assert db2.count() == 1, "ロード後の件数が1であること"

        # クリアテスト
        db.clear()
        assert db.count() == 0, "クリア後の件数が0であること"

    print("✅ vector_db: 全テスト通過")


def test_clip_model() -> None:
    """CLIPモデルの基本動作テスト。"""
    from clip_model import CLIPJapaneseModel

    model = CLIPJapaneseModel()
    dim = model.embedding_dim
    print(f"  embedding_dim={dim}, device={model.device}")

    # 擬似画像を生成してエンコード
    dummy_image = Image.fromarray(
        np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    )
    image_vec = model.encode_image(dummy_image)
    assert image_vec.shape == (1, dim), f"画像ベクトルの形状が正しいこと: {image_vec.shape}"
    assert np.allclose(np.linalg.norm(image_vec), 1.0, atol=1e-5), "L2正規化済みであること"

    # テキストをエンコード
    text_vec = model.encode_text("これはテストです")
    assert text_vec.shape == (1, dim), f"テキストベクトルの形状が正しいこと: {text_vec.shape}"
    assert np.allclose(np.linalg.norm(text_vec), 1.0, atol=1e-5), "L2正規化済みであること"

    # 複数画像のバッチエンコード
    images = [dummy_image, dummy_image]
    batch_vec = model.encode_images(images)
    assert batch_vec.shape == (2, dim), f"バッチベクトルの形状が正しいこと: {batch_vec.shape}"

    print("✅ clip_model: 全テスト通過")


def test_search_engine() -> None:
    """検索エンジンのE2Eテスト。"""
    from search_engine import SearchEngine

    with tempfile.TemporaryDirectory() as tmp_dir:
        engine = SearchEngine(db_dir=tmp_dir)

        # テスト用画像を生成して保存
        test_images_dir = os.path.join(tmp_dir, "images")
        os.makedirs(test_images_dir)

        for i in range(3):
            img = Image.fromarray(
                np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            )
            img.save(os.path.join(test_images_dir, f"test_{i}.jpg"))

        # 画像を登録
        for i in range(3):
            path = os.path.join(test_images_dir, f"test_{i}.jpg")
            engine.register_image(path)

        # DB統計を確認
        stats = engine.get_stats()
        assert stats["total"] == 3, f"登録数が3であること: {stats['total']}"
        assert stats["images"] == 3, f"画像数が3であること: {stats['images']}"

        # テキスト検索テスト
        results = engine.search_by_text("赤い花", top_k=2)
        assert len(results) == 2, f"検索結果が2件であること: {len(results)}"

        # 画像検索テスト
        query_path = os.path.join(test_images_dir, "test_0.jpg")
        results = engine.search_by_image(query_path, top_k=3)
        assert len(results) == 3, f"検索結果が3件であること: {len(results)}"

        # ディレクトリ一括登録テスト
        new_dir = os.path.join(tmp_dir, "new_images")
        os.makedirs(new_dir)
        for i in range(2):
            img = Image.fromarray(
                np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            )
            img.save(os.path.join(new_dir, f"new_{i}.png"))

        indices = engine.register_directory(new_dir)
        assert len(indices) == 2, f"一括登録が2件であること: {len(indices)}"
        assert engine.get_stats()["total"] == 5, "合計5件であること"

    print("✅ search_engine: 全テスト通過")


if __name__ == "__main__":
    print("=" * 50)
    print("  CLIP検索エンジン 動作確認テスト")
    print("=" * 50)

    # ベクトルDB（CLIPモデル不要）
    print("\n--- ベクトルDBテスト ---")
    test_vector_db()

    # 動画プロセッサー（インポートのみ）
    print("\n--- 動画プロセッサーテスト ---")
    test_video_processor()

    # CLIPモデル（モデルダウンロードが必要）
    print("\n--- CLIPモデルテスト ---")
    test_clip_model()

    # 検索エンジンE2E
    print("\n--- 検索エンジンE2Eテスト ---")
    test_search_engine()

    print("\n" + "=" * 50)
    print("  全テスト通過 🎉")
    print("=" * 50)
