"""反向 PF-ODE 采样（论文 §5.4 / Eq. 5.4）。

PF-ODE:
    du/dτ = -σ(τ) · σ̇(τ) · s_θ(u, τ)

时间积分：EDM 的 Heun 二阶（Karras et al. 2022, Algorithm 1）。
"""

from __future__ import annotations
from typing import Callable

import torch


class HeunSampler:
    """EDM Heun 二阶反向 PF-ODE 采样器。

    Args:
        score_net: 训练好的 score 网络（baseline 或 BV-aware）
        schedule: noise schedule（提供 σ(τ), σ̇(τ)）
        n_steps: 采样步数（EDM 默认 18）

    Attributes:
        device: torch.device — 推断设备
    """

    def __init__(
        self,
        score_net: torch.nn.Module,
        schedule,  # NoiseSchedule duck-typed; see schedules/
        n_steps: int = 18,
        device: str | torch.device = "cuda",
    ) -> None:
        self.score_net = score_net
        self.schedule = schedule
        self.n_steps = n_steps
        self.device = torch.device(device)

    @torch.no_grad()
    def sample(
        self,
        shape: tuple[int, ...],
        guidance_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None = None,
    ) -> torch.Tensor:
        """从纯噪声开始采样到 τ → 0 的样本。

        Args:
            shape: 样本张量的形状（含 batch 维），如 (B, C, N_x)
            guidance_fn: 可选的 guidance 函数 g(u, τ) -> 修正项；
                         传入 None 时退化为无引导 PF-ODE

        Returns:
            shape (B, C, N_x) 的样本
        """
        raise NotImplementedError("Will be implemented in Week 5.")
