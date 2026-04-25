"""Denoising score matching loss（论文 §3.1）。

L_DSM = E_{τ, u_0, ε} || D_θ(u_0 + σ(τ)·ε, τ) - u_0 ||^2

等价于 score matching 因 Vincent (2011) 等价定理。
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def dsm_loss(
    denoiser_out: torch.Tensor,
    u0: torch.Tensor,
    weight: torch.Tensor | None = None,
) -> torch.Tensor:
    """计算 denoising score matching loss。

    Args:
        denoiser_out: D_θ(u_τ, τ), shape (B, C, N_x)
        u0:           ground-truth 干净样本, shape (B, C, N_x)
        weight:       可选的 per-sample 权重, shape (B,)；用于 EDM weighting c_skip 等

    Returns:
        scalar tensor (mean MSE)
    """
    se = F.mse_loss(denoiser_out, u0, reduction="none")  # (B, C, N_x)
    if weight is not None:
        # 把 (B,) 广播到 (B, C, N_x)
        se = se * weight.view(-1, 1, 1)
    return se.mean()
