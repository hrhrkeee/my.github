"""CLIP Japanese v2 モデルのラッパーモジュール。

line-corporation/clip-japanese-base-v2 を使用して、
画像・テキストの特徴量ベクトルを抽出する。
"""

import logging

import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)

# モデルのHugging Faceパス
HF_MODEL_PATH = "line-corporation/clip-japanese-base-v2"


class CLIPJapaneseModel:
    """CLIP Japanese v2 モデルを管理するクラス。

    画像とテキストの特徴量ベクトルを抽出する機能を提供する。

    Attributes:
        device: 推論に使用するデバイス（cuda/cpu）
        model: CLIPモデル本体
        tokenizer: テキストトークナイザー
        processor: 画像プロセッサー
    """

    def __init__(self, device: str | None = None) -> None:
        """モデルを初期化する。

        Args:
            device: 使用するデバイス。Noneの場合は自動検出する。
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        logger.info("CLIPモデルをロード中: %s (device=%s)", HF_MODEL_PATH, self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            HF_MODEL_PATH, trust_remote_code=True
        )
        self.processor = AutoImageProcessor.from_pretrained(
            HF_MODEL_PATH, trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            HF_MODEL_PATH, trust_remote_code=True
        ).to(self.device)
        self.model.eval()

        # 埋め込み次元を動的に取得（ダミー画像でforward）
        self._embedding_dim = self._detect_embedding_dim()

        logger.info(
            "CLIPモデルのロード完了 (embedding_dim=%d)", self._embedding_dim
        )

    @torch.no_grad()
    def encode_image(self, image: Image.Image) -> np.ndarray:
        """画像を特徴量ベクトルに変換する。

        Args:
            image: PIL Image オブジェクト。

        Returns:
            正規化された特徴量ベクトル (1, dim) の numpy 配列。
        """
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        features = self.model.get_image_features(**inputs)
        # L2正規化
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().astype(np.float32)

    @torch.no_grad()
    def encode_images(self, images: list[Image.Image]) -> np.ndarray:
        """複数の画像を一括で特徴量ベクトルに変換する。

        Args:
            images: PIL Image オブジェクトのリスト。

        Returns:
            正規化された特徴量ベクトル (N, dim) の numpy 配列。
        """
        inputs = self.processor(images, return_tensors="pt").to(self.device)
        features = self.model.get_image_features(**inputs)
        # L2正規化
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().astype(np.float32)

    @torch.no_grad()
    def encode_text(self, text: str) -> np.ndarray:
        """テキストを特徴量ベクトルに変換する。

        Args:
            text: 入力テキスト文字列。

        Returns:
            正規化された特徴量ベクトル (1, dim) の numpy 配列。
        """
        inputs = self.tokenizer([text]).to(self.device)
        features = self.model.get_text_features(**inputs)
        # L2正規化
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().astype(np.float32)

    @torch.no_grad()
    def encode_texts(self, texts: list[str]) -> np.ndarray:
        """複数のテキストを一括で特徴量ベクトルに変換する。

        Args:
            texts: テキスト文字列のリスト。

        Returns:
            正規化された特徴量ベクトル (N, dim) の numpy 配列。
        """
        inputs = self.tokenizer(texts).to(self.device)
        features = self.model.get_text_features(**inputs)
        # L2正規化
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().astype(np.float32)

    @torch.no_grad()
    def _detect_embedding_dim(self) -> int:
        """ダミー画像を使って埋め込み次元を自動検出する。"""
        dummy = Image.new("RGB", (224, 224), color=(128, 128, 128))
        inputs = self.processor(dummy, return_tensors="pt").to(self.device)
        features = self.model.get_image_features(**inputs)
        return features.shape[-1]

    @property
    def embedding_dim(self) -> int:
        """特徴量ベクトルの次元数を返す。"""
        return self._embedding_dim
