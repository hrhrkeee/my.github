"""動画からフレームを抽出するモジュール。

PyAV（av）ライブラリを使用し、動画ファイルからフレームをシークベースで
高速に抽出する。等間隔サンプリングと秒単位の間隔サンプリングの両方に対応。
"""

import logging
from pathlib import Path

import av
from PIL import Image

logger = logging.getLogger(__name__)

# デフォルトのフレーム抽出間隔（秒）
DEFAULT_FRAME_INTERVAL = 10.0

# デフォルトの抽出フレーム数（等間隔サンプリング時）
DEFAULT_NUM_FRAMES = 5


def extract_frames(
    video_path: str | Path,
    interval_sec: float = DEFAULT_FRAME_INTERVAL,
) -> list[Image.Image]:
    """動画から一定間隔でフレームを抽出する。

    動画の総時間を interval_sec で割って等間隔のタイムスタンプを算出し、
    各タイムスタンプにシークしてフレームを取得する。

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

    try:
        container = av.open(str(video_path))
        stream = container.streams.video[0]

        # 動画の総時間を取得
        duration_sec = _get_duration_sec(stream, container)
        if duration_sec <= 0:
            logger.warning("動画の時間を取得できません: %s", video_path)
            container.close()
            return []

        # 抽出するフレーム数を計算
        num_frames = max(1, int(duration_sec / interval_sec) + 1)

        logger.info(
            "動画情報: %s (duration=%.1fs, interval=%.1fs, num_frames=%d)",
            video_path.name,
            duration_sec,
            interval_sec,
            num_frames,
        )

        frames = _extract_frames_at_positions(
            container, stream, num_frames, duration_sec
        )
        container.close()

    except Exception as e:
        raise RuntimeError(f"動画の処理に失敗しました: {video_path} - {e}") from e

    if not frames:
        logger.warning("フレームが抽出できませんでした: %s", video_path)

    logger.info("抽出フレーム数: %d (interval=%.1fs)", len(frames), interval_sec)
    return frames


def extract_frames_by_count(
    video_path: str | Path,
    num_frames: int = DEFAULT_NUM_FRAMES,
) -> list[Image.Image]:
    """動画から指定フレーム数を等間隔で抽出する（シーク使用で高速化）。

    Args:
        video_path: 動画ファイルのパス。
        num_frames: 抽出するフレーム数。デフォルトは5。

    Returns:
        抽出された各フレームのPIL Imageリスト。

    Raises:
        FileNotFoundError: 動画ファイルが見つからない場合。
        RuntimeError: 動画の読み込みに失敗した場合。
    """
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

    try:
        container = av.open(str(video_path))
        stream = container.streams.video[0]

        duration_sec = _get_duration_sec(stream, container)
        if duration_sec <= 0:
            logger.warning("動画の時間を取得できません: %s", video_path)
            container.close()
            return []

        logger.info(
            "動画情報: %s (duration=%.1fs, num_frames=%d)",
            video_path.name,
            duration_sec,
            num_frames,
        )

        frames = _extract_frames_at_positions(
            container, stream, num_frames, duration_sec
        )
        container.close()

    except Exception as e:
        raise RuntimeError(f"動画の処理に失敗しました: {video_path} - {e}") from e

    if not frames:
        logger.warning("フレームが抽出できませんでした: %s", video_path)

    logger.info("抽出フレーム数: %d", len(frames))
    return frames


def get_video_info(video_path: str | Path) -> dict:
    """動画のメタ情報を取得する。

    Args:
        video_path: 動画ファイルのパス。

    Returns:
        fps, total_frames, duration_sec, width, height を含む辞書。

    Raises:
        RuntimeError: 動画を開けない場合。
    """
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

    try:
        container = av.open(str(video_path))
        stream = container.streams.video[0]

        fps = float(stream.average_rate) if stream.average_rate else 0.0
        total_frames = stream.frames or 0
        width = stream.codec_context.width
        height = stream.codec_context.height
        duration_sec = _get_duration_sec(stream, container)

        container.close()
    except Exception as e:
        raise RuntimeError(f"動画を開けませんでした: {video_path} - {e}") from e

    return {
        "fps": fps,
        "total_frames": total_frames,
        "duration_sec": duration_sec,
        "width": width,
        "height": height,
    }


def _get_duration_sec(stream: av.video.stream.VideoStream, container: av.container.InputContainer) -> float:
    """動画ストリームの総時間（秒）を取得する。"""
    # stream.duration と time_base から算出
    if stream.duration and stream.time_base:
        return float(stream.duration * stream.time_base)

    # コンテナレベルの duration（マイクロ秒単位）
    if container.duration:
        return container.duration / 1_000_000

    # フレーム数とFPSから推定
    if stream.frames and stream.average_rate:
        return stream.frames / float(stream.average_rate)

    return 0.0


def _extract_frames_at_positions(
    container: av.container.InputContainer,
    stream: av.video.stream.VideoStream,
    num_frames: int,
    duration_sec: float,
) -> list[Image.Image]:
    """等間隔で計算した位置にシークしてフレームを抽出する。"""
    frames: list[Image.Image] = []
    time_base = stream.time_base

    # 等間隔でサンプリングする時間位置（秒）を計算
    if num_frames == 1:
        sample_times = [0.0]
    else:
        sample_times = [
            i * duration_sec / num_frames for i in range(num_frames)
        ]

    for target_sec in sample_times:
        try:
            # 秒数をPTSに変換してシーク
            target_pts = int(target_sec / time_base) if time_base else 0
            container.seek(target_pts, stream=stream)

            # シーク後の最初のフレームを取得
            for frame in container.decode(video=0):
                img = frame.to_ndarray(format="rgb24")
                frames.append(Image.fromarray(img))
                break
        except Exception as e:
            logger.debug(
                "フレーム抽出失敗 (time=%.1fs): %s", target_sec, e
            )

    return frames
