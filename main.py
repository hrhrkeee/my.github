"""
メインエントリーポイント
乱数データを生成し、簡単なニューラルネットワークで5エポック学習して結果を確認する。
"""

import logging
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class SimpleNet(nn.Module):
    """シンプルな3層全結合ネットワーク"""

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)


def generate_random_data(
    n_samples: int = 1000,
    input_dim: int = 10,
    seed: int = 42,
) -> tuple[torch.Tensor, torch.Tensor]:
    """乱数で回帰用データセットを生成する。

    Args:
        n_samples: サンプル数
        input_dim: 入力次元数
        seed: 乱数シード

    Returns:
        (入力テンソル, ターゲットテンソル) のタプル
    """
    torch.manual_seed(seed)
    np.random.seed(seed)

    # 入力特徴量: 標準正規分布
    x = torch.randn(n_samples, input_dim)

    # ターゲット: 線形結合 + ノイズ（学習可能な関係を持たせる）
    true_weights = torch.randn(input_dim, 1)
    noise = torch.randn(n_samples, 1) * 0.1
    y = x @ true_weights + noise

    logger.info("データ生成完了: x=%s, y=%s", x.shape, y.shape)
    return x, y


def train(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    n_epochs: int = 5,
) -> list[float]:
    """モデルを学習する。

    Args:
        model: 学習対象のモデル
        dataloader: 学習データローダー
        criterion: 損失関数
        optimizer: オプティマイザ
        device: 使用デバイス
        n_epochs: エポック数

    Returns:
        各エポックの平均損失のリスト
    """
    model.train()
    epoch_losses: list[float] = []

    for epoch in range(n_epochs):
        running_loss = 0.0
        n_batches = 0

        for x_batch, y_batch in dataloader:
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)

            optimizer.zero_grad()
            output = model(x_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            n_batches += 1

        avg_loss = running_loss / n_batches
        epoch_losses.append(avg_loss)
        logger.info("Epoch [%d/%d] - Loss: %.6f", epoch + 1, n_epochs, avg_loss)

    return epoch_losses


def evaluate(
    model: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
    device: torch.device,
) -> dict[str, float]:
    """モデルの予測精度を評価する。

    Args:
        model: 評価対象のモデル
        x: 入力テンソル
        y: ターゲットテンソル
        device: 使用デバイス

    Returns:
        評価指標の辞書（MSE, MAE, R2）
    """
    model.eval()
    with torch.no_grad():
        x = x.to(device)
        y = y.to(device)
        pred = model(x)

        mse = nn.functional.mse_loss(pred, y).item()
        mae = nn.functional.l1_loss(pred, y).item()

        # R2スコア
        ss_res = ((y - pred) ** 2).sum().item()
        ss_tot = ((y - y.mean()) ** 2).sum().item()
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return {"mse": mse, "mae": mae, "r2": r2}


def save_results(
    epoch_losses: list[float],
    metrics: dict[str, float],
    output_dir: Path,
) -> None:
    """学習結果をファイルに保存する。

    Args:
        epoch_losses: 各エポックの損失リスト
        metrics: 評価指標の辞書
        output_dir: 出力ディレクトリ
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 損失の推移をプロット
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, len(epoch_losses) + 1), epoch_losses, marker="o")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss (MSE)")
    ax.set_title("Training Loss")
    ax.grid(True)
    fig.savefig(output_dir / "training_loss.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("損失グラフを保存: %s", output_dir / "training_loss.png")

    # 評価結果をテキストで保存
    result_path = output_dir / "results.txt"
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("=== 学習結果 ===\n\n")
        f.write("--- エポックごとの損失 ---\n")
        for i, loss in enumerate(epoch_losses, 1):
            f.write(f"  Epoch {i}: {loss:.6f}\n")
        f.write(f"\n--- 評価指標 ---\n")
        f.write(f"  MSE: {metrics['mse']:.6f}\n")
        f.write(f"  MAE: {metrics['mae']:.6f}\n")
        f.write(f"  R2:  {metrics['r2']:.6f}\n")
    logger.info("結果を保存: %s", result_path)


def main() -> None:
    """メイン処理"""
    # ハイパーパラメータ
    n_samples = 1000
    input_dim = 10
    hidden_dim = 64
    output_dim = 1
    batch_size = 64
    n_epochs = 5
    learning_rate = 1e-3
    seed = 42

    # デバイスの選択
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("使用デバイス: %s", device)

    # 再現性の確保
    torch.manual_seed(seed)

    # データ生成
    x, y = generate_random_data(n_samples=n_samples, input_dim=input_dim, seed=seed)
    dataset = TensorDataset(x, y)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # モデル・損失関数・オプティマイザの定義
    model = SimpleNet(input_dim, hidden_dim, output_dim).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    logger.info("モデル構造:\n%s", model)
    total_params = sum(p.numel() for p in model.parameters())
    logger.info("総パラメータ数: %d", total_params)

    # 学習
    logger.info("学習開始 (epochs=%d, batch_size=%d, lr=%s)", n_epochs, batch_size, learning_rate)
    epoch_losses = train(model, dataloader, criterion, optimizer, device, n_epochs)

    # 評価
    metrics = evaluate(model, x, y, device)
    logger.info("評価結果 - MSE: %.6f, MAE: %.6f, R2: %.6f", metrics["mse"], metrics["mae"], metrics["r2"])

    # 結果の保存
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = Path("output") / f"{timestamp}_random_regression"
    save_results(epoch_losses, metrics, output_dir)

    logger.info("完了: 出力先 → %s", output_dir)


if __name__ == "__main__":
    main()
