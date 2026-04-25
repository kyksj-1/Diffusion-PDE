"""Godunov-form PDE residual guidance（论文 §5.4 / Eq. 5.4 后半）。

DiffusionPDE 用中心差分计算 PDE residual ||L(D_θ)||^2 — 但中心差分在 shock
附近没有定义。我们改用 Godunov 通量的有限体积差分，自动 entropy-consistent。
"""

from __future__ import annotations
from typing import Callable

import torch


def godunov_guidance(
    u: torch.Tensor,
    flux_fn: Callable[[torch.Tensor], torch.Tensor],
    dx: float,
    dt: float,
) -> torch.Tensor:
    """计算 Godunov-form PDE residual 作为 guidance gradient。

    L_PDE^Godunov(u) = || ∂_t u + (F^G_{i+1/2} - F^G_{i-1/2}) / dx ||^2

    其中 F^G 是 Godunov 数值通量（Riemann 解）。

    Args:
        u:       shape (B, C, N_t, N_x) — 时空格点解
        flux_fn: 通量函数 f(u)
        dx, dt:  网格步长

    Returns:
        shape (B, C, N_t, N_x) — guidance gradient ∇_u L_PDE^Godunov
    """
    raise NotImplementedError("Will be implemented in Week 5.")
