"""Kruzhkov 熵正则（论文 §5.3 / R_ent）。

R_ent(u) = E_k [ max{0, ∂_t |u - k| + ∂_x ( sgn(u - k) (f(u) - f(k)) )} ]

其中 f 是目标 PDE 的通量函数，k 取遍常数（实现时用 Monte Carlo 采样）。
此正则惩罚 "Kruzhkov 熵不等式被违反" 的程度，使训练后的 D_θ 偏向产出物理熵解。
"""

from __future__ import annotations
from typing import Callable

import torch


def kruzhkov_entropy_loss(
    u: torch.Tensor,
    flux_fn: Callable[[torch.Tensor], torch.Tensor],
    dx: float,
    dt: float,
    n_k_samples: int = 16,
) -> torch.Tensor:
    """计算 Kruzhkov 熵正则。

    Args:
        u:          shape (B, N_t, N_x) — 完整时空格点解
        flux_fn:    通量函数 f: R -> R（向量化）
        dx, dt:     空间 / 时间步长
        n_k_samples: 蒙特卡洛采样常数 k 的个数

    Returns:
        scalar tensor — 平均违反量

    Notes:
        实现要点:
        - 用中心差分近似 ∂_t |u-k| 与 ∂_x (sgn(u-k)·(f(u)-f(k)))
        - max{0, ·} 用 ReLU
        - k 从 [u.min(), u.max()] 上均匀采样 n_k_samples 个值
    """
    raise NotImplementedError("Will be implemented in Week 6.")
