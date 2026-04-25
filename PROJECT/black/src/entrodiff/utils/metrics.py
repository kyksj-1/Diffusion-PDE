"""评估指标（论文 §7 / Theorem 3 收敛率验证）。

- ``wasserstein_1``  : 用 POT 库的 sinkhorn / EMD 估计
- ``l1_error``       : ||û - u^*||_{L^1}
- ``shock_location_error`` : 比较 û 与 u^* 中 shock 位置的差
"""

from __future__ import annotations

import numpy as np
import torch


def wasserstein_1(samples_a: np.ndarray, samples_b: np.ndarray) -> float:
    """计算两个经验分布之间的 W_1 距离。

    Args:
        samples_a: shape (N, d) — 样本集 A（如 EntroDiff 生成）
        samples_b: shape (M, d) — 样本集 B（如 WENO5 ground truth）

    Returns:
        W_1(P_A, P_B) 的估计值

    Notes:
        使用 POT (python-optimal-transport) 的 emd 求解器。
        对大批量样本使用 sinkhorn 更快但有近似误差。
    """
    raise NotImplementedError("Will be implemented in Week 7 with POT.emd_1d.")


def l1_error(u_hat: torch.Tensor, u_star: torch.Tensor) -> torch.Tensor:
    """L^1 误差（per-sample mean）。"""
    return (u_hat - u_star).abs().mean()


def shock_location_error(
    u_hat: np.ndarray,
    u_star: np.ndarray,
    threshold: float = 0.5,
) -> float:
    """估计 û 与 u^* 中 shock 位置的差异。

    Args:
        u_hat:     shape (N_t, N_x)
        u_star:    shape (N_t, N_x)
        threshold: 用于检测 shock 的相对值（u 在 shock 两侧的均值）

    Returns:
        shock 位置误差（按格点单位）
    """
    raise NotImplementedError("Will be implemented in Week 7.")
