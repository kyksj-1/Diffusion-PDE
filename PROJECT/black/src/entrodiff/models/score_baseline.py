"""标准 EDM-style score network（论文 §5 baseline）。

参数化:
    s_θ(u, τ) = (D_θ(u, τ) - u) / σ(τ)^2

其中 D_θ 是 EDM 的去噪网络（Karras et al. 2022）。本模块作为 path A
论文的 baseline，**不是 novelty**——novelty 在 score_bvaware.py。
"""

from __future__ import annotations

import torch
from torch import nn


class EDMDenoiser(nn.Module):
    """EDM 去噪网络 D_θ。

    Args:
        in_channels: 输入物理通道数（标量守恒律 = 1; Euler = 3）
        hidden_dim: 隐藏维数
        n_layers: U-Net depth
    """

    def __init__(self, in_channels: int = 1, hidden_dim: int = 128, n_layers: int = 4) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        # TODO[Week 5] · 实现 1D U-Net + sinusoidal time embedding

    def forward(self, u: torch.Tensor, tau: torch.Tensor) -> torch.Tensor:
        """前向：返回去噪后的 u_0 估计。

        Args:
            u: shape (B, C, N_x)
            tau: shape (B,) — 扩散时间

        Returns:
            shape (B, C, N_x) — D_θ(u, τ)
        """
        raise NotImplementedError("Will be implemented in Week 5.")


class BaselineScoreNet(nn.Module):
    """Baseline score: s_θ(u, τ) = (D_θ(u, τ) - u) / σ(τ)^2。"""

    def __init__(self, denoiser: EDMDenoiser) -> None:
        super().__init__()
        self.denoiser = denoiser

    def forward(self, u: torch.Tensor, tau: torch.Tensor, sigma_tau: torch.Tensor) -> torch.Tensor:
        """Args:
            u, tau: 同 EDMDenoiser
            sigma_tau: shape (B,) — σ(τ)
        Returns:
            shape (B, C, N_x) — score 估计
        """
        d = self.denoiser(u, tau)
        # 广播 sigma_tau 到 (B, 1, 1)
        sig2 = sigma_tau.view(-1, 1, 1) ** 2
        return (d - u) / sig2
