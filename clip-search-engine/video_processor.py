"""動画からフレームを抽出するモジュール。

動画ファイルから一定間隔（デフォルト10秒おき）でフレームを取得し、
PIL Image として返す。
"""

import logging
from pathlib import Path

import cv2
from PIL import Image

logger = logging.getLogger(__name__)

# デフォルトのフレーム抽出間隔（秒）
DEFAULT_FRAME_INTERVAL = 10.0


def extract_frames(
    video_path: str | Path,
    interval_sec: float = DEFAULT_FRAME_INTERVAL,
) -> list[Image.Image]:
    """動画から一定間隔でフレームを抽出する。

    Args:
        video_path: 動画ファイルのパス。
        interval_sec: フレームを抽出する間隔（秒）。デフォルトは10秒。

    Returns:
        抽出された各フレームのPIL Imageリスト。

    Raises:
        FileNotFoundError: 動画ファイルが見つからない場合。
        RuntimeError: 動画の読み込みに失敗した場合。
    """
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"動画を開けませんでした: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    logger.info(
        "動画情報: %s (fps=%.1f, total_frames=%d, duration=%.1fs)",
        video_path.name,
        fps,
        total_frames,
        duration,
    )

    # 抽出するフレーム番号を計算
    frame_interval = int(fps * interval_sec)
    if frame_interval < 1:
        frame_interval = 1

    frames: list[Image.Image] = []
    frame_idx = 0

    # 最初のフレーム（0秒目）は必ず取得
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            # BGRからRGBに変換してPIL Imageに変換
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            frames.append(pil_image)
            logger.debug(
                "フレーム抽出: idx=%d, time=%.1fs", frame_idx, frame_idx / fps
            )

        frame_idx += 1

    cap.release()

    # フレームが1枚も取れなかった場合のフォールバック
    if not frames:
        logger.warning("フレームが抽出できませんでした: %s", video_path)

    logger.info("抽出フレーム数: %d (interval=%.1fs)", len(frames), interval_sec)
    return frames


def get_video_info(video_path: str | Path) -> dict:
    """動画のメタ情報を取得する。

    Args:
        video_path: 動画ファイルのパス。

    Returns:
        fps, total_frames, duration_sec, width, height を含む辞書。
    """
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"動画を開けませんでした: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_sec = total_frames / fps if fps > 0 else 0

    cap.release()

    return {
        "fps": fps,
        "total_frames": total_frames,
        "duration_sec": duration_sec,
        "width": width,
        "height": height,
    }
