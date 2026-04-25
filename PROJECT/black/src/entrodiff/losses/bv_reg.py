"""BV (total variation) 正则（论文 §5.3 / λ_BV · TV(D_θ)）。

TV(u) = Σ_i |u(x_{i+1}) - u(x_i)|

控制去噪网络输出的全变差，保证 û ∈ BV → 落入 Kruzhkov 熵解的 L^1-紧致框架。
对应 Theorem 3 的关键一步。
"""

from __future__ import annotations

import torch


def tv_loss(u: torch.Tensor) -> torch.Tensor:
    """计算 total variation 损失（沿空间维度的一阶差分 L1 范数）。

    Args:
        u: shape (B, C, N_x) 或 (B, N_t, C, N_x)

    Returns:
        scalar tensor — TV 平均值
    """
    if u.dim() == 3:
        # (B, C, N_x)
        diff = u[..., 1:] - u[..., :-1]
    elif u.dim() == 4:
        # (B, N_t, C, N_x) — 只算空间方向
        diff = u[..., 1:] - u[..., :-1]
    else:
        raise ValueError(f"Unexpected tensor shape {tuple(u.shape)}; expected 3D or 4D.")
    return diff.abs().mean()
