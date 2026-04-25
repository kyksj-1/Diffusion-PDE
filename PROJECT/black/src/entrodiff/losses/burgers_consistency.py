"""Score-Burgers 一致性正则（论文 §5.3 / Eq. 5.3 第四项）。

基于 Score Shocks 的等式 (★):
    ∂_τ s + 2 s · ∇_x s = Δ_x s

直接惩罚 s_θ 偏离这条 PDE 的程度，作为软约束注入训练损失。
"""

from __future__ import annotations

import torch


def burgers_consistency_loss(
    s: torch.Tensor,
    s_dtau: torch.Tensor,
    s_dx: torch.Tensor,
    s_dxx: torch.Tensor,
) -> torch.Tensor:
    """计算 score-Burgers 一致性损失。

    Args:
        s:      shape (B, C, N_x) — score 值
        s_dtau: shape (B, C, N_x) — ∂_τ s（自动微分得到）
        s_dx:   shape (B, C, N_x) — ∂_x s（自动微分 / 有限差分）
        s_dxx:  shape (B, C, N_x) — Δ_x s

    Returns:
        scalar tensor — || ∂_τ s + 2 s ∂_x s - Δ_x s ||^2 的平均
    """
    residual = s_dtau + 2.0 * s * s_dx - s_dxx
    return (residual**2).mean()
